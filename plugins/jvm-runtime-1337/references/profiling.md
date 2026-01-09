# JVM Profiling Deep Dive

Advanced profiling patterns beyond the basics.

## The Safepoint Bias Problem Explained

### What Are Safepoints?

Safepoints are points in code where the JVM can safely stop all threads to perform operations like:
- Garbage collection
- Thread stack sampling (traditional profilers)
- Deoptimization
- Biased lock revocation

The JVM inserts safepoint checks:
- At method returns
- At backward branches (loop ends)
- At allocation sites

### Why This Creates Bias

Traditional JVMTI profilers call `GetStackTrace()` which requires all threads to reach a safepoint. This means:

1. Code between safepoints is **invisible** to the profiler
2. Hot spots appear skewed toward safepoint-heavy code
3. Tight computational loops may be underrepresented

**Example:** A loop with no allocations and no calls may run thousands of iterations between safepoints, but appear "cool" in profiles.

### async-profiler's Solution

async-profiler uses two techniques:

1. **`AsyncGetCallTrace`** — HotSpot-specific API that samples without requiring safepoints
2. **`perf_events`** — Linux kernel's performance monitoring for native code

The combination produces accurate profiles of both Java and native code.

**Source:** [Jean-Philippe Bempel: Debug Non-Safepoints (2022)](https://jpbempel.github.io/2022/06/22/debug-non-safepoints.html)

### Java 16+ Improvements (JEP 376)

JEP 376 introduced thread-local handshakes, allowing profilers to sample individual threads without global safepoints. This reduced the bias significantly for JVMTI-based tools.

However, async-profiler still provides advantages:
- Flame graph output
- Native code profiling
- Lower overhead in some scenarios

## async-profiler Usage Patterns

### Basic CPU Profiling

```bash
# 30-second CPU profile with flame graph output
./profiler.sh -d 30 -f profile.html <pid>

# Output as JFR (viewable in JMC)
./profiler.sh -d 30 -o jfr -f profile.jfr <pid>

# Wall-clock time (includes sleeping/blocked)
./profiler.sh -d 30 -e wall -f profile.html <pid>
```

### Allocation Profiling

```bash
# Track heap allocations
./profiler.sh -d 30 -e alloc -f alloc.html <pid>

# With allocation size threshold (bytes)
./profiler.sh -d 30 -e alloc --alloc 512k -f alloc.html <pid>
```

### Lock Contention

```bash
# Profile lock contention
./profiler.sh -d 30 -e lock -f locks.html <pid>
```

### Attaching at JVM Start vs Runtime

| Approach | Pros | Cons |
|----------|------|------|
| `-agentpath` at start | Full coverage, `DebugNonSafepoints` from start | Requires restart |
| Runtime attach | No restart needed | Misses already-compiled methods |

**Best practice:** For production, use runtime attach. For thorough analysis, restart with `-agentpath`.

```bash
# At JVM start (full accuracy)
java -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints \
     -agentpath:/path/to/libasyncProfiler.so=start,file=profile.jfr \
     -jar app.jar

# Runtime attach (most common)
./profiler.sh start -e cpu -f profile.jfr <pid>
./profiler.sh stop <pid>
```

## JFR (Java Flight Recorder)

### When to Use JFR vs async-profiler

| Scenario | Prefer |
|----------|--------|
| Continuous monitoring | JFR |
| Deep CPU investigation | async-profiler |
| Memory allocation tracking | JFR (richer events) |
| Native code profiling | async-profiler |
| No external dependencies | JFR (built-in) |

### JFR Configuration

```bash
# Start recording
jcmd <pid> JFR.start name=myrecording settings=profile duration=5m

# Settings: default (low overhead) or profile (more detail)
# duration: auto-stop after time
# maxsize: rolling buffer size

# Dump recording
jcmd <pid> JFR.dump name=myrecording filename=dump.jfr

# Stop
jcmd <pid> JFR.stop name=myrecording
```

### Analyzing JFR Files

1. **JDK Mission Control (JMC)** — Full GUI analysis
2. **jfr CLI** — Command-line summary
3. **async-profiler** — Convert to flame graph

```bash
# CLI summary
jfr summary recording.jfr

# Print specific events
jfr print --events jdk.CPULoad recording.jfr

# Convert JFR to flame graph
./profiler.sh -f flamegraph.html jfr recording.jfr
```

### JEP 509: CPU-Time Profiling (JDK 25)

New in JDK 25 (experimental): Native CPU-time profiling in JFR on Linux. This provides async-profiler-like accuracy with JFR's integration.

**Source:** [JEP 509](https://openjdk.org/jeps/509)

## Flame Graph Interpretation

### Reading Flame Graphs

- **Width** = time spent (wider = more samples)
- **Height** = stack depth (taller = deeper call chain)
- **Color** = arbitrary (helpful for visual grouping)

### Common Patterns

| Pattern | Indicates |
|---------|-----------|
| Wide flat top | Single hot method |
| Wide plateau mid-stack | Bottleneck deeper in call chain |
| Many narrow towers | Diverse code paths |
| "GC" frames | GC activity (may indicate allocation pressure) |

### Differential Flame Graphs

Compare before/after with async-profiler:

```bash
# Generate differential flame graph
./profiler.sh -d 30 -f before.collapsed <pid>
# ... make change ...
./profiler.sh -d 30 -f after.collapsed <pid>

# Diff (requires FlameGraph tools)
difffolded.pl before.collapsed after.collapsed | flamegraph.pl > diff.svg
```

## Continuous Profiling in Production

### Why Continuous Profiling

- Catch performance regressions early
- Correlate performance with deployments
- Historical data for incident investigation

### Options

| Tool | Type | Notes |
|------|------|-------|
| Pyroscope | OSS | async-profiler based |
| Datadog Continuous Profiler | Commercial | Integrated with APM |
| AWS CodeGuru Profiler | Commercial | AWS-integrated |
| Grafana Pyroscope | OSS | Flame graphs + Grafana |

### Low-Overhead Setup

```bash
# async-profiler with low sampling rate for production
./profiler.sh -d 0 -i 10ms -e cpu -f /tmp/profile.jfr <pid>

# JFR with default (low-overhead) settings
jcmd <pid> JFR.start settings=default maxage=1h maxsize=500m
```
