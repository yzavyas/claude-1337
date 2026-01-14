# JVM Analysis Sources

URLs for verification and further reading. Organized by topic.

---

## Tools

### Static Analysis

| Tool | URL |
|------|-----|
| Scavenger | https://github.com/naver/scavenger |
| ProGuard -printusage | https://www.guardsquare.com/manual/configuration/usage |
| SootUp | https://soot-oss.github.io/SootUp/ |
| ProGuard Core | https://github.com/Guardsquare/proguard-core |
| Dead Code Agent | https://github.com/parttimenerd/dead-code-agent |
| SpotBugs | https://spotbugs.github.io/ |
| Error Prone | https://errorprone.info/ |

### Profiling

| Tool | URL |
|------|-----|
| async-profiler | https://github.com/async-profiler/async-profiler |
| JDK Mission Control (JMC) | https://jdk.java.net/jmc/ |
| VisualVM | https://visualvm.github.io/ |

### Memory Analysis

| Tool | URL |
|------|-----|
| Eclipse MAT | https://eclipse.org/mat/ |
| HeapHero | https://heaphero.io/ |
| GCViewer | https://github.com/chewiebug/GCViewer |
| GCEasy | https://gceasy.io/ |
| FastThread.io | https://fastthread.io/ |

---

## Academic Papers

### SootUp

Karakaya et al., "SootUp: A Redesign of the Soot Static Analysis Framework"
- TACAS 2024
- https://link.springer.com/chapter/10.1007/978-3-031-57246-3_13

---

## Official Documentation

### Oracle / OpenJDK

| Topic | URL |
|-------|-----|
| GC Tuning Guide (JDK 21) | https://docs.oracle.com/en/java/javase/21/gctuning/ |
| JEP 345 (NUMA-Aware Memory) | https://openjdk.org/jeps/345 |
| JEP 376 (ZGC Concurrent Thread-Stack Processing) | https://openjdk.org/jeps/376 |
| JEP 439 (Generational ZGC) | https://openjdk.org/jeps/439 |
| JEP 509 (JFR CPU-Time Profiling) | https://openjdk.org/jeps/509 |
| ZGC Wiki | https://wiki.openjdk.org/display/zgc |

---

## Technical Blogs

### Profiling & Safepoints

| Author | Article | URL |
|--------|---------|-----|
| Nitsan Wakart | Safepoints: Meaning, Side Effects and Overheads (2015) | http://psy-lob-saw.blogspot.com/2015/12/safepoints.html |
| Jean-Philippe Bempel | Debug Non-Safepoints (2022) | https://jpbempel.github.io/2022/06/22/debug-non-safepoints.html |
| InfoQ | Open Source Java Profilers (2025) | https://www.infoq.com/articles/open-source-java-profilers/ |

### GC & Memory

| Author | Article | URL |
|--------|---------|-----|
| Aleksey Shipilev | JVM Anatomy Quarks (2019) | https://shipilev.net/jvm/anatomy-quarks/ |
| Gunnar Morling | Lower Java Tail Latencies with ZGC | https://www.morling.dev/blog/lower-java-tail-latencies-with-zgc/ |
| Datadog | JVM Container Best Practices (2024) | https://www.datadoghq.com/blog/java-memory-management/ |

---

## Notes

- Oracle GC Tuning Guide is the authoritative source for GC behavior
- Shipilev's JVM Anatomy Quarks covers low-level JVM internals with empirical data
- Wakart's blog remains the canonical reference for safepoint behavior
- async-profiler README has detailed usage and troubleshooting
