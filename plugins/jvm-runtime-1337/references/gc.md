# Garbage Collector Deep Dive

GC selection, tuning, and troubleshooting patterns.

## GC Evolution Timeline

| JDK | Default GC | Major Changes |
|-----|------------|---------------|
| 8 | Parallel | — |
| 9 | G1 | G1 becomes default |
| 11 | G1 | ZGC experimental |
| 14 | G1 | CMS removed |
| 15 | G1 | ZGC production-ready |
| 17 | G1 | — |
| 21 | G1 | ZGC generational mode |
| 23 | G1 | ZGC generational default |

## G1GC (Garbage-First)

### How It Works

G1 divides the heap into regions (1-32MB each) and collects the "garbage-first" — regions with most garbage.

**Phases:**
1. Young collection (STW) — Evacuate young regions
2. Concurrent marking — Find live objects
3. Mixed collection (STW) — Collect young + old regions

### When to Use

- Heap 4-32GB
- Pause time more important than throughput
- General-purpose workloads

### Key Tuning Options

```bash
# Target pause time (default 200ms)
-XX:MaxGCPauseMillis=100

# Heap region size (auto-selected if not set)
-XX:G1HeapRegionSize=16m

# Concurrent threads (default: ~1/4 of CPUs)
-XX:ConcGCThreads=4

# Initiating heap occupancy (when to start marking)
-XX:InitiatingHeapOccupancyPercent=45
```

### Common G1 Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Long pauses | Too many mixed collections | Increase `-XX:G1HeapWastePercent` |
| Full GC | Allocation faster than collection | More heap, or tune IHOP |
| Humongous allocations | Objects > 50% region size | Larger regions or smaller objects |

## ZGC (Z Garbage Collector)

### How It Works

ZGC uses colored pointers and load barriers to collect concurrently. Most work happens while application runs.

**Key innovation:** Colored pointers encode GC metadata in unused pointer bits, enabling concurrent relocation.

### When to Use

- Large heaps (tens to hundreds of GB)
- Latency-critical applications
- Can tolerate slightly lower throughput

### ZGC Modes (JDK 21+)

| Mode | Flag | Description |
|------|------|-------------|
| Generational (default JDK 23+) | `-XX:+UseZGC` | Separates young/old generations |
| Non-generational (legacy) | `-XX:+UseZGC -XX:-ZGenerational` | Single-generation |

**Generational ZGC** provides better throughput while maintaining low pause times.

### Key Tuning Options

```bash
# Enable ZGC
-XX:+UseZGC

# Heap size (ZGC scales to TB)
-Xmx64g

# Concurrent threads (auto-tuned, rarely needs adjustment)
-XX:ConcGCThreads=4

# Soft max heap (GC tries to stay below this)
-XX:SoftMaxHeapSize=48g
```

### ZGC Characteristics

| Metric | Typical Value |
|--------|---------------|
| Pause time | <1ms (often <200µs) |
| Throughput overhead | 5-15% vs Parallel |
| Memory overhead | ~3% for colored pointers |

**Source:** [Gunnar Morling: Lower Java Tail Latencies with ZGC](https://www.morling.dev/blog/lower-java-tail-latencies-with-zgc/)

## Shenandoah

### How It Works

Shenandoah performs concurrent compaction using Brooks forwarding pointers. Every object has a forwarding pointer that either points to itself or the new location.

### When to Use

- Need low latency on older JDKs (8+)
- Large heaps
- Red Hat-based distributions (bundled)

### Shenandoah vs ZGC

| Aspect | Shenandoah | ZGC |
|--------|------------|-----|
| Pause target | <10ms | <1ms |
| JDK support | 8+ (via backport) | 11+ (experimental), 15+ (production) |
| Memory overhead | Brooks pointers | Colored pointers |
| Throughput | Slightly better | Slightly worse |

### Key Tuning Options

```bash
# Enable Shenandoah
-XX:+UseShenandoahGC

# Heuristics mode
-XX:ShenandoahGCHeuristics=adaptive

# Uncommit unused memory
-XX:ShenandoahUncommitDelay=1000
```

## Parallel GC

### When to Use

- Batch processing
- Throughput > latency
- Predictable memory allocation patterns

```bash
# Enable Parallel GC
-XX:+UseParallelGC

# Number of GC threads
-XX:ParallelGCThreads=8
```

## GC Logging

### Unified Logging (JDK 9+)

```bash
# Basic GC logging
-Xlog:gc:file=gc.log

# Detailed with timestamps
-Xlog:gc*:file=gc.log:time,uptime,tags

# Specific components
-Xlog:gc+heap=debug:file=gc.log

# Rotating logs
-Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=10m
```

### Analyzing GC Logs

| Tool | Type | Notes |
|------|------|-------|
| GCViewer | OSS GUI | Classic, supports all GCs |
| GCEasy | Online | Upload and analyze |
| gceasy.io | Online | Same as GCEasy |
| JDK Mission Control | GUI | Built into JDK |

### Key Metrics to Monitor

| Metric | Healthy Range | Red Flag |
|--------|---------------|----------|
| Pause time | < target | Consistently over target |
| Allocation rate | Stable | Sudden spikes |
| Promotion rate | Low | High (premature tenuring) |
| Full GC frequency | Rare | Frequent |
| Heap after GC | < 50% | > 70% (memory pressure) |

## Tuning Workflow

1. **Establish baseline** — Measure current GC behavior
2. **Set goals** — Latency target? Throughput target?
3. **Choose collector** — Based on heap size and goals
4. **Tune incrementally** — One change at a time
5. **Measure impact** — Compare before/after
6. **Monitor in production** — Continuous observation

### Common Tuning Mistakes

| Mistake | Why It's Wrong |
|---------|----------------|
| Setting `-Xms` = `-Xmx` always | Wastes memory for small workloads |
| Over-tuning G1 regions | G1 auto-tunes well |
| Disabling compressed oops | 32GB+ heaps need this, but costs memory |
| Ignoring allocation rate | GC frequency tracks allocation |
| Tuning without measuring | Guessing rarely works |

## Memory Sizing

### Rule of Thumb

- **Working set** × 2-3 = minimum heap
- **Production heap** should allow GC overhead < 5%

### Container Memory Budget

For a container with 4GB limit:

| Component | Size |
|-----------|------|
| Heap (`-Xmx`) | 3GB (75%) |
| Metaspace | 256MB |
| Thread stacks | 200MB (200 threads × 1MB) |
| CodeCache | 128MB |
| Direct buffers | 256MB |
| Overhead | 160MB |

## Debugging GC Issues

### Full GC Too Frequent

1. Check promotion rate — young objects dying in old gen
2. Check metaspace — may need `-XX:MaxMetaspaceSize`
3. Check explicit `System.gc()` — use `-XX:+DisableExplicitGC`

### Long GC Pauses

1. Enable GC logging with timing
2. Check heap size vs live data
3. Consider ZGC or Shenandoah

### OOM Despite Available Heap

1. Check metaspace: `-XX:MaxMetaspaceSize`
2. Check direct memory: `-XX:MaxDirectMemorySize`
3. Native memory leak: use `-XX:NativeMemoryTracking=summary`
