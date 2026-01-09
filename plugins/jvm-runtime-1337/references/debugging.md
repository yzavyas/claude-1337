# JVM Debugging Deep Dive

Memory leaks, thread dumps, and production troubleshooting patterns.

## Heap Dump Analysis

### Capturing Heap Dumps

| Method | Command | When to Use |
|--------|---------|-------------|
| On OOM | `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/path/` | Production default |
| jcmd (preferred) | `jcmd <pid> GC.heap_dump /path/dump.hprof` | On-demand |
| jmap (legacy) | `jmap -dump:live,format=b,file=dump.hprof <pid>` | Fallback |
| Spring Actuator | `curl localhost:8080/actuator/heapdump` | Spring Boot apps |

**Important:** Heap dumps pause the JVM. Expect ~2 seconds per GB of heap.

### The `live` Option

```bash
# With live: triggers full GC first, only dumps reachable objects
jcmd <pid> GC.heap_dump -live /path/dump.hprof

# Without live: dumps everything including garbage
jcmd <pid> GC.heap_dump /path/dump.hprof
```

**Use `live`** for memory leak analysis (smaller, cleaner). **Skip `live`** when investigating specific objects that might be unreachable.

### Eclipse MAT (Memory Analyzer Tool)

**Installation:** Download from [eclipse.org/mat](https://eclipse.org/mat/)

**Key Analysis Steps:**

1. **Leak Suspects Report** — Auto-generated analysis of probable leaks
2. **Dominator Tree** — Objects sorted by retained heap
3. **Path to GC Roots** — Why an object is retained
4. **Histogram** — Object counts by class

### Understanding Shallow vs Retained Heap

| Metric | Meaning |
|--------|---------|
| Shallow heap | Memory consumed by the object itself |
| Retained heap | Memory freed if object is GC'd (includes dependencies) |

**Example:** An `ArrayList` has small shallow heap (just the array reference) but large retained heap (all elements).

### Common Leak Patterns

| Pattern | Symptom in MAT | Fix |
|---------|----------------|-----|
| Unbounded cache | HashMap with millions of entries | Add eviction policy (Caffeine, Guava) |
| Listener leak | Old listeners in event lists | Weak references or explicit removal |
| Static collection | Static field holding references | Clear on shutdown or use WeakHashMap |
| Thread-local leak | ThreadLocal values in pooled threads | Call `remove()` in finally block |
| ClassLoader leak | Classes retained after redeploy | Fix class/resource references |

### Finding the Leak Root

1. **Dominator Tree** → Sort by retained heap
2. Find unexpectedly large objects
3. **Path to GC Roots** → Exclude weak/soft/phantom references
4. Trace back to the code keeping the reference

## Thread Dump Analysis

### Capturing Thread Dumps

```bash
# jcmd (preferred)
jcmd <pid> Thread.print > threads.txt

# jstack (with lock info)
jstack -l <pid> > threads.txt

# jstack (force, when JVM is hung)
jstack -F <pid> > threads.txt

# Kill -3 (writes to stdout/stderr)
kill -3 <pid>
```

**Best practice:** Take 3-5 dumps, 5-10 seconds apart. Compare to find stuck threads.

### Thread States

| State | Meaning | Common Cause |
|-------|---------|--------------|
| RUNNABLE | Executing or ready | CPU work |
| BLOCKED | Waiting for monitor | Lock contention |
| WAITING | Waiting indefinitely | `Object.wait()`, `Lock.lock()` |
| TIMED_WAITING | Waiting with timeout | `Thread.sleep()`, `Lock.tryLock()` |

### Detecting Deadlocks

jstack automatically detects and reports deadlocks:

```
Found one Java-level deadlock:
=============================
"Thread-A":
  waiting to lock monitor 0x00007f... (object 0x00000076..., a java.lang.Object),
  which is held by "Thread-B"
"Thread-B":
  waiting to lock monitor 0x00007f... (object 0x00000076..., a java.lang.Object),
  which is held by "Thread-A"
```

### Analyzing Lock Contention

Look for multiple threads BLOCKED on the same monitor:

```
"http-nio-8080-exec-1" BLOCKED
   waiting to lock <0x000000076ab9a4e8> (a com.example.Service)

"http-nio-8080-exec-2" BLOCKED
   waiting to lock <0x000000076ab9a4e8> (a com.example.Service)

"http-nio-8080-exec-3" RUNNABLE
   locked <0x000000076ab9a4e8> (a com.example.Service)
```

**Analysis:** Thread exec-3 holds the lock. exec-1 and exec-2 are waiting. If exec-3 is slow, all others queue up.

### Finding Stuck Threads

Compare multiple dumps:
1. Take dump at T+0
2. Take dump at T+5s
3. Take dump at T+10s

Threads with **same stack trace across all dumps** are stuck.

### Thread Dump Analysis Tools

| Tool | Type | URL |
|------|------|-----|
| FastThread.io | Online | fastthread.io |
| TDA | Java GUI | github.com/irockel/tda |
| IBM TMDA | Java GUI | ibm.com/support |
| sampler (JDK tool) | CLI | Built into JDK |

## Native Memory Tracking (NMT)

### Enabling NMT

```bash
# Summary mode (lower overhead)
java -XX:NativeMemoryTracking=summary ...

# Detail mode (higher overhead)
java -XX:NativeMemoryTracking=detail ...
```

### Querying NMT

```bash
# Current memory
jcmd <pid> VM.native_memory summary

# Baseline + diff (for leak detection)
jcmd <pid> VM.native_memory baseline
# ... wait ...
jcmd <pid> VM.native_memory summary.diff
```

### NMT Output Categories

| Category | Contents |
|----------|----------|
| Java Heap | `-Xmx` allocation |
| Class | Metaspace, class metadata |
| Thread | Thread stacks |
| Code | JIT compiled code (CodeCache) |
| GC | GC data structures |
| Internal | JVM internal allocations |
| Symbol | Symbol tables |
| Native Memory Tracking | NMT overhead |

### Diagnosing Native Memory Leaks

1. Enable NMT at startup
2. Baseline after warmup: `jcmd <pid> VM.native_memory baseline`
3. Run workload
4. Diff: `jcmd <pid> VM.native_memory summary.diff`
5. Growing category indicates leak source

## OOM Error Types

| Error | Meaning | Common Fix |
|-------|---------|------------|
| `Java heap space` | Heap exhausted | Increase `-Xmx`, fix leak |
| `Metaspace` | Class metadata exhausted | Increase `-XX:MaxMetaspaceSize`, fix classloader leak |
| `Unable to create new native thread` | Thread limit reached | Reduce `-Xss`, increase ulimit |
| `Direct buffer memory` | Direct ByteBuffers exhausted | Increase `-XX:MaxDirectMemorySize`, close buffers |
| `GC overhead limit exceeded` | >98% time in GC | Memory leak or heap too small |

### Recommended OOM Flags

```bash
# Dump heap on OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/

# Kill process on OOM (for containers)
-XX:+ExitOnOutOfMemoryError

# Or run custom script
-XX:OnOutOfMemoryError="kill -9 %p"
```

## jcmd Reference

Preferred over older tools (jstack, jmap, jinfo).

```bash
# List running JVMs
jcmd -l

# All available commands for a JVM
jcmd <pid> help

# Thread dump
jcmd <pid> Thread.print

# Heap dump
jcmd <pid> GC.heap_dump /path/dump.hprof

# GC info
jcmd <pid> GC.heap_info

# JFR control
jcmd <pid> JFR.start
jcmd <pid> JFR.dump
jcmd <pid> JFR.stop

# Native memory
jcmd <pid> VM.native_memory summary

# Flags
jcmd <pid> VM.flags

# System properties
jcmd <pid> VM.system_properties
```
