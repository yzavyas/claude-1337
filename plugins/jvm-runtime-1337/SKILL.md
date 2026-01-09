---
name: jvm-runtime-1337
description: "JVM runtime analysis and production debugging. Use when: profiling Java applications, tuning GC, analyzing heap/thread dumps, debugging memory leaks, optimizing for containers. Covers async-profiler, JFR, JMC, G1/ZGC/Shenandoah, MAT, jstack."
---

# JVM Runtime Analysis

Production-grade patterns for profiling, debugging, and tuning JVM applications.

## Philosophy

1. **Measure before tuning** — profile first, optimize based on evidence (universal principle)
2. **Production-safe tooling** — low overhead profilers that won't crash or slow production ([async-profiler](https://github.com/async-profiler/async-profiler))
3. **Understand the bias** — know what your tools can and cannot see (safepoint bias problem)
4. **Right GC for the job** — latency vs throughput tradeoffs are real ([JEP 376](https://openjdk.org/jeps/376))
5. **Containers are not VMs** — JVM memory model clashes with cgroup limits (community lessons)

## Decision Frameworks

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

| Profiler | Overhead | Safepoint-Free | Output | Best For |
|----------|----------|----------------|--------|----------|
| async-profiler | ~2% CPU | Yes | Flame graphs, JFR | Production CPU/allocation |
| JFR + JMC | ~1-2% | Partial (improved Java 16+) | Binary events | Continuous monitoring |
| VisualVM | 5-10% | No | Various | Development debugging |
| IntelliJ Profiler | ~2% | Yes (uses async-profiler) | Flame graphs | IDE-integrated |

**Source:** [InfoQ: Open Source Java Profilers (2025)](https://www.infoq.com/articles/open-source-java-profilers/)

### Garbage Collector Selection

```
Heap size?
├── < 4 GB → G1 (default since JDK 9)
├── 4-32 GB → Latency-sensitive?
│   ├── YES → ZGC or Shenandoah
│   └── NO → G1
└── > 32 GB → ZGC (generational, JDK 21+)
```

| Collector | Pause Target | Heap Size | JDK | Best For |
|-----------|--------------|-----------|-----|----------|
| G1GC | 200ms (tunable) | Any | 9+ default | General workloads |
| ZGC | <1ms | Large (100GB+) | 15+ production, 21+ generational | Latency-critical |
| Shenandoah | <10ms | Large | 12+ (Red Hat) | Low-latency, older JDKs |
| Parallel | Max throughput | Medium | All | Batch processing |

**Key insight:** ZGC generational (JDK 21+) outperforms both G1 and Shenandoah in benchmarks. It became the default ZGC mode in JDK 23.

**Sources:** [Java Code Geeks: GC Performance (2025)](https://www.javacodegeeks.com/2025/08/java-gc-performance-g1-vs-zgc-vs-shenandoah.html), [IBM Community: GC Comparison (2025)](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors)

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

**Why it happens:** JVM can only safely inspect thread state at safepoints. Code between safepoints is invisible to JVMTI-based profilers.

**Source:** [Baeldung: async-profiler Guide](https://www.baeldung.com/java-async-profiler), [GitHub Issue #47](https://github.com/async-profiler/async-profiler/issues/47)

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
# Metaspace: ~100MB
# Thread stacks: ~100MB (100 threads × 1MB default)
# CodeCache: ~50MB
# Native/JNI: ~150MB buffer
```

**Source:** Docker/Kubernetes best practices, Java 8u191+ container awareness

### Heap Dump Performance Impact

- **Trap**: Heap dumps pause the JVM (~2 seconds per GB of heap)
- **Impact**: 8GB heap = 16 second pause in production
- **Fix**: Use continuous profiling (JFR) instead of reactive dumps when possible

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
