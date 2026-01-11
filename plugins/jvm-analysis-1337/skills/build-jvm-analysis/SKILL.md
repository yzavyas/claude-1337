---
name: build-jvm-analysis
description: "JVM runtime analysis. Use when: profiling JVM performance, tuning GC, debugging memory leaks, finding dead code with production data. Not for general Java development or syntax questions."
---

# JVM Analysis

Patterns for analyzing, optimizing, and debugging JVM applications — both static and runtime.

## Philosophy

1. **Measure before tuning** — profile first, optimize based on evidence
2. **Static + runtime complement** — static finds structural issues, runtime finds behavioral issues
3. **Production-safe tooling** — low overhead profilers that won't crash or slow production
4. **Understand tool limitations** — safepoint bias, entry point coverage, what tools can't see
5. **Right tool for the job** — no single tool does everything

---

## Static Analysis

### Dead Code Detection

```
Finding unused code?
├── Have production traffic → Runtime analysis (Scavenger)
├── Need static-only analysis →
│   ├── Simple → ProGuard -printusage
│   └── Custom analysis → SootUp or ProGuard Core
└── Just bug patterns → SpotBugs, Error Prone
```

| Tool | Type | What It Does | When to Use |
|------|------|--------------|-------------|
| Scavenger | Runtime | Tracks actual usage in production | Have production data |
| ProGuard -printusage | Static | Lists unreachable from entry points | Know your entry points |
| SootUp | Library | Call graphs, data flow analysis | Building custom analysis |
| ProGuard Core | Library | Bytecode analysis primitives | Building custom tools |
| Dead Code Agent | Runtime | Tracks class loading | Quick prototype |

**Key insight:** No turnkey "run this, get dead code" CLI exists. You either:
- Deploy runtime agents (needs production) — Scavenger
- Configure static analysis (needs entry points) — ProGuard
- Build custom tooling (needs engineering) — SootUp

### SootUp for Code Analysis

SootUp provides call graph construction and analysis primitives. Useful for:
- Building reachability analysis (find what's called from entry points)
- Data flow analysis (track how values propagate)
- Dependency mapping (what calls what)

*(Karakaya et al., TACAS 2024)*

**Gotcha:** SootUp is a library, not a tool. You build analysis on top of it.

### Bug Detection (Not Dead Code)

| Tool | Focus | Integration |
|------|-------|-------------|
| SpotBugs | Bug patterns (400+) | Gradle/Maven, CI |
| Error Prone | Compile-time checks | javac plugin |
| NullAway | Null safety | Error Prone plugin |

---

## Runtime Analysis

### Profiler Selection

```
Need production profiling?
├── YES → CPU or memory?
│   ├── CPU → Need flame graphs?
│   │   ├── YES → async-profiler
│   │   └── NO → JFR (built-in, zero config)
│   └── Memory → JFR (allocation profiling)
└── NO (development only) → VisualVM or IntelliJ Profiler
```

| Profiler | Overhead | Safepoint-Free | Output | Tradeoff | Best For |
|----------|----------|----------------|--------|----------|----------|
| async-profiler | ~2% CPU | Yes | Flame graphs, JFR | Requires native agent attachment | Production CPU/allocation |
| JFR + JMC | ~1-2% | Partial (improved Java 16+) | Binary events | Less granular CPU data | Continuous monitoring |
| VisualVM | 5-10% | No | Various | Safepoint bias distorts results | Development only |
| IntelliJ Profiler | ~2% | Yes (uses async-profiler) | Flame graphs | IDE dependency | IDE-integrated |

*(InfoQ 2025)*

**Why safepoint-free matters:** JVM can only safely inspect threads at safepoints. JVMTI-based profilers (VisualVM, hprof) miss code between safepoints, skewing flame graphs toward safepoint-heavy code. async-profiler uses `AsyncGetCallTrace` to sample anytime (Wakart 2016).

### Garbage Collector Selection

```
Heap size?
├── < 4 GB → G1 (default since JDK 9)
│   WHY: ZGC/Shenandoah overhead not justified; G1's region-based collection efficient at this scale
├── 4-32 GB → Latency-sensitive?
│   ├── YES → ZGC or Shenandoah
│   │   WHY: Concurrent marking/compaction keeps pauses <10ms regardless of heap size
│   └── NO → G1
│       WHY: G1's mixed collections handle this range well; simpler tuning
└── > 32 GB → ZGC (generational, JDK 21+)
    WHY: ZGC's concurrent compaction scales linearly; G1 pauses grow with heap
```

| Collector | Pause Target | Heap Size | Tradeoff | JDK | Best For |
|-----------|--------------|-----------|----------|-----|----------|
| G1GC | 200ms (tunable) | Any | Pauses scale with heap | 9+ default | General workloads |
| ZGC | <1ms | Large (100GB+) | ~15% throughput cost vs G1 | 15+ prod, 21+ gen | Latency-critical |
| Shenandoah | <10ms | Large | Higher CPU for barriers | 12+ (Red Hat) | Low-latency, older JDKs |
| Parallel | Max throughput | Medium | Stop-the-world only | All | Batch processing |

**Why the thresholds:**
- **<4GB**: G1's region-based approach (2048 regions default) works well. ZGC's colored pointers and load barriers add overhead not justified at small scale (Oracle GC Tuning Guide).
- **4-32GB**: The "compressed OOPs" boundary. Above 32GB, object pointers expand from 4 to 8 bytes, increasing memory footprint ~20%. ZGC handles this better (Shipilev 2019).
- **>32GB**: G1's pause times grow with live set size during mixed collections. ZGC's concurrent compaction maintains <1ms regardless (ZGC wiki, Oracle).

**Key insight:** ZGC generational (JDK 21+) closes the throughput gap — concurrent minor collections reduce allocation pressure (JEP 439).

*(Oracle GC Tuning Guide, Shipilev JVM Anatomy Quarks, JEP 439)*

### Heap Dump Analysis

```
OOM or suspected leak?
├── Capture dump → -XX:+HeapDumpOnOutOfMemoryError
├── Analyze → Eclipse MAT or HeapHero
│   ├── Run "Leak Suspects" report
│   ├── Check retained heap (not just shallow)
│   └── Path to GC Roots (exclude weak refs)
└── Fix → Collections holding references, static fields, caches without eviction
```

### Thread Dump Analysis

```
Application hanging or slow?
├── Capture → jstack -l <pid> (or jcmd <pid> Thread.print)
├── Take 3-5 dumps seconds apart
├── Analyze:
│   ├── BLOCKED threads → lock contention
│   ├── WAITING on same monitor → bottleneck
│   └── Same stack across dumps → stuck thread
└── Tools: FastThread.io, TDA, or manual grep
```

## Production Gotchas

### Safepoint Bias

- **Trap**: Traditional profilers (VisualVM, hprof) only sample at safepoints
- **Impact**: Misleading flame graphs — hot spots skewed to safepoint-heavy code
- **Detection**: Compare async-profiler output vs traditional profiler
- **Fix**: Use async-profiler or JFR (Java 16+ with JEP 376)

**Why it happens:** JVM can only safely inspect thread state at safepoints — points where all threads are known to be in a consistent state. JVMTI's `GetStackTrace` requires this. Safepoints occur at method returns, loop back-edges, and allocation. Tight loops without allocations may run millions of cycles between safepoints, becoming invisible (Wakart 2015).

*(Wakart 2015, async-profiler docs)*

### DebugNonSafepoints Flag

- **Trap**: Even async-profiler needs `-XX:+DebugNonSafepoints` for accurate frame resolution
- **Impact**: Inlined methods may not appear in profiles
- **Fix**: Start JVM with flag, or attach agent early

```bash
# At JVM start (recommended)
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -agentpath:/path/to/libasyncProfiler.so ...

# Late attach works but misses already-compiled methods
```

### Container Memory Limits (OOMKilled)

- **Trap**: JVM uses more memory than `-Xmx` (native memory, metaspace, stacks, codecache)
- **Impact**: Kubernetes kills pod with OOMKilled even when heap looks fine
- **Detection**: `kubectl describe pod` shows OOMKilled; native memory tracking shows usage
- **Fix**: Budget 25-30% of container memory for non-heap

```bash
# Good: percentage-based, container-aware
java -XX:MaxRAMPercentage=75.0 -XX:+UseContainerSupport ...

# Budget breakdown for 2GB container:
# Heap: ~1.5GB (75%)
# Metaspace: ~100MB (default MaxMetaspaceSize unbounded, set explicitly)
# Thread stacks: ~100MB (100 threads × 1MB default Linux stack)
# CodeCache: ~50MB (240MB reserved, typically uses ~50MB)
# Native/JNI: ~150MB buffer (JDBC drivers, compression libs, etc.)
```

**Why 25-30%:** Empirical guidance from production incidents. Exact overhead depends on workload — NMT (Native Memory Tracking) gives precise breakdown for your app (Schatzl, Oracle GC team). Spring Boot apps with web frameworks often need closer to 30%; minimal services can use 20% (Datadog 2024).

*(JEP 345, Datadog JVM Container Best Practices)*

### Heap Dump Performance Impact

- **Trap**: Heap dumps pause the JVM during capture
- **Impact**: Pause duration depends on heap size and live objects — observed 1-3 seconds per GB in production (SAP Memory Analyzer docs, Eclipse MAT wiki)
- **Fix**: Use continuous profiling (JFR) for allocation tracking; reserve dumps for post-mortem or during maintenance windows

**Why the pause:** Full GC + heap traversal + I/O. The JVM must walk all live objects to write the dump. Parallel GC can speed traversal but I/O often dominates (Eclipse MAT FAQ).

### JMH Microbenchmark Pitfalls

- **Trap**: Dead code elimination, constant folding, insufficient warmup
- **Impact**: Benchmarks show 10x faster than production
- **Detection**: Results too good to be true; `-XX:+PrintCompilation` shows unexpected inlining
- **Fix**: Use `Blackhole.consume()`, `@State` objects, sufficient warmup

```java
// Wrong: JIT may eliminate this
@Benchmark
public void bad() {
    compute(); // No side effects, may be removed
}

// Correct: Blackhole prevents DCE
@Benchmark
public void good(Blackhole bh) {
    bh.consume(compute());
}
```

## Tool Selection by Scenario

| Scenario | Primary Tool | Alternative |
|----------|--------------|-------------|
| Production CPU profile | async-profiler | JFR |
| Allocation hotspots | JFR | async-profiler `--alloc` |
| Memory leak | Heap dump + MAT | HeapHero |
| Deadlock | jstack -l | JMC thread analysis |
| GC issues | GC logs + GCViewer | JFR |
| Container sizing | NMT + metrics | VisualVM (dev) |
| Microbenchmarks | JMH | (no alternative) |

## Quick Reference

### Profiling Commands

```bash
# async-profiler CPU flame graph
./profiler.sh -d 30 -f flamegraph.html <pid>

# JFR recording (no overhead until dump)
jcmd <pid> JFR.start duration=60s filename=recording.jfr

# Heap dump
jcmd <pid> GC.heap_dump /path/to/dump.hprof

# Thread dump
jcmd <pid> Thread.print > threads.txt

# Native memory tracking
java -XX:NativeMemoryTracking=summary ...
jcmd <pid> VM.native_memory summary
```

### GC Flags

```bash
# G1 (default, balanced)
-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# ZGC (ultra-low latency, JDK 21+ generational default)
-XX:+UseZGC

# Shenandoah (low-latency, older JDKs)
-XX:+UseShenandoahGC

# Diagnostics
-Xlog:gc*:file=gc.log:time,tags
```

### Container Flags

```bash
# Production container setup
-XX:+UseContainerSupport \
-XX:MaxRAMPercentage=75.0 \
-XX:+HeapDumpOnOutOfMemoryError \
-XX:HeapDumpPath=/dumps/ \
-XX:+ExitOnOutOfMemoryError
```

## Specialized References

Load reference based on context:

| Detected | Load |
|----------|------|
| Profiling, flame graphs, sampling | [profiling.md](references/profiling.md) |
| GC tuning, pause times, heap sizing | [gc.md](references/gc.md) |
| Memory leaks, thread dumps, OOM | [debugging.md](references/debugging.md) |
| Kubernetes, containers, cgroups | [containers.md](references/containers.md) |

## Obsolete Patterns

| Obsolete | Replacement | Why |
|----------|-------------|-----|
| `-XX:+PrintGCDetails` | `-Xlog:gc*` | Unified logging (JDK 9+) |
| VisualVM for production | async-profiler / JFR | Safepoint bias, overhead |
| Manual `-Xmx` in containers | `MaxRAMPercentage` | Container-aware |
| `jmap -heap` | `jcmd GC.heap_info` | jcmd preferred |
| hprof | JFR | hprof removed JDK 9+ |
| CMS | G1 or ZGC | CMS removed JDK 14 |

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| Profile with default VisualVM in prod | Use async-profiler or JFR | Safepoint bias, overhead |
| Set `-Xmx` = container limit | Leave 25-30% for non-heap | OOMKilled by cgroup |
| Trust microbenchmarks naively | Use JMH properly | JIT optimizations mislead |
| Tune GC without measuring | Profile first, tune second | Premature optimization |
| Use `-XX:+PrintGCDetails` (JDK 9+) | Use unified logging `-Xlog:gc*` | Old flags deprecated |
| Ignore safepoint bias | Check `-XX:+DebugNonSafepoints` | Hidden hot spots |
