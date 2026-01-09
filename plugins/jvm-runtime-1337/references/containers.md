# JVM in Containers Deep Dive

Kubernetes, Docker, and cgroup-aware JVM configuration.

## The Container Memory Problem

### Why JVMs Get OOMKilled

The JVM's memory model doesn't match container limits:

| JVM Memory | Description | Controlled By |
|------------|-------------|---------------|
| Heap | Object storage | `-Xmx` |
| Metaspace | Class metadata | `-XX:MaxMetaspaceSize` |
| Thread stacks | Per-thread stack | `-Xss` × thread count |
| CodeCache | JIT compiled code | `-XX:ReservedCodeCacheSize` |
| Direct buffers | Off-heap ByteBuffers | `-XX:MaxDirectMemorySize` |
| Native/JNI | Native libraries | Uncontrolled |

**The trap:** Setting `-Xmx` = container limit causes OOMKilled because heap is only one component.

### Memory Budget Formula

```
Container Limit = Heap + Metaspace + ThreadStacks + CodeCache + DirectBuffers + Native + Buffer

Recommended:
Heap ≤ 75% of container limit
```

**Example for 4GB container:**

| Component | Size | Flag |
|-----------|------|------|
| Heap | 3GB | `-Xmx3g` or `-XX:MaxRAMPercentage=75.0` |
| Metaspace | 256MB | `-XX:MaxMetaspaceSize=256m` |
| Thread stacks | 200MB | 200 threads × 1MB |
| CodeCache | 128MB | `-XX:ReservedCodeCacheSize=128m` |
| Direct buffers | 256MB | `-XX:MaxDirectMemorySize=256m` |
| Native + buffer | 160MB | Overhead |

## Container-Aware JVM (Java 8u191+, Java 10+)

### UseContainerSupport

Since Java 8u191/10+, the JVM automatically detects container limits:

```bash
# Enabled by default in modern JVMs
-XX:+UseContainerSupport
```

This makes the JVM:
- Read cgroup memory limits instead of host memory
- Adjust default heap size accordingly
- Adjust default GC thread count

### Percentage-Based Sizing

**Preferred approach** — adapts to different container sizes:

```bash
# Use 75% of container memory for heap
-XX:MaxRAMPercentage=75.0

# Initial heap as percentage
-XX:InitialRAMPercentage=50.0

# Minimum heap as percentage (for small containers)
-XX:MinRAMPercentage=50.0
```

**Note:** `MaxRAMPercentage` works with container limits when `UseContainerSupport` is enabled.

### Legacy Flags (Avoid)

```bash
# Old approach - don't use
-XX:+UseCGroupMemoryLimitForHeap  # Deprecated, removed in Java 11
-XX:MaxRAMFraction=2              # Replaced by MaxRAMPercentage
```

## Kubernetes Configuration

### Resource Requests and Limits

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1"
  limits:
    memory: "2Gi"
    cpu: "2"
```

**Best practices:**
- **Set requests = limits for memory** → Guaranteed QoS class, prevents OOMKilled from throttling
- **CPU limits can be higher than requests** → Burstable is fine for CPU
- **Never set memory limit without request** → Scheduling won't account for memory

### QoS Classes

| Class | Condition | Eviction Priority |
|-------|-----------|-------------------|
| Guaranteed | requests = limits for all containers | Lowest (last evicted) |
| Burstable | requests < limits for any resource | Medium |
| BestEffort | No requests or limits | Highest (first evicted) |

**For production JVMs:** Use Guaranteed (requests = limits).

### JVM Flags for Kubernetes

```yaml
env:
  - name: JAVA_OPTS
    value: >-
      -XX:+UseContainerSupport
      -XX:MaxRAMPercentage=75.0
      -XX:+HeapDumpOnOutOfMemoryError
      -XX:HeapDumpPath=/heap-dumps/
      -XX:+ExitOnOutOfMemoryError
```

### Heap Dumps in Kubernetes

```yaml
# Volume for heap dumps
volumes:
  - name: heap-dumps
    emptyDir: {}

volumeMounts:
  - name: heap-dumps
    mountPath: /heap-dumps
```

**Recovery:** Use `kubectl cp` to retrieve dumps before pod terminates.

For persistent storage:
```yaml
volumes:
  - name: heap-dumps
    persistentVolumeClaim:
      claimName: heap-dump-pvc
```

## CPU Considerations

### CPU Limits and GC Threads

The JVM sets GC thread count based on available CPUs:
- With `UseContainerSupport`, it respects cgroup CPU limits
- Without it, it uses host CPU count (wrong in containers)

```bash
# The JVM auto-detects, but can override:
-XX:ParallelGCThreads=4
-XX:ConcGCThreads=2
```

### CPU Throttling Impact

With CPU limits, Kubernetes throttles via CFS (Completely Fair Scheduler):
- Throttled JVM appears to have long GC pauses
- Actually it's waiting for CPU quota

**Detection:** Check `throttled_time` in cgroup stats or use `kubectl top`.

**Mitigation:**
- Set CPU limits high enough
- Or use only CPU requests (no hard limits)

## Container Startup Optimization

### Class Data Sharing (CDS)

Pre-generate class metadata to reduce startup time:

```bash
# Generate shared archive (build time)
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -jar app.jar

# Use shared archive (runtime)
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar
```

**AppCDS (Application Class Data Sharing):**
```bash
# Step 1: Generate class list
java -XX:DumpLoadedClassList=classes.lst -jar app.jar

# Step 2: Generate archive
java -Xshare:dump -XX:SharedClassListFile=classes.lst \
     -XX:SharedArchiveFile=app.jsa -jar app.jar

# Step 3: Use in production
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar
```

### JVM Warmup

JIT compilation during startup can cause:
- Slow initial requests
- High CPU at start
- Inconsistent latency

**Mitigation:**
- **Readiness probes** — Don't route traffic until warmed up
- **AOT compilation** — GraalVM native-image (different tradeoffs)
- **Warmup requests** — Init container or startup hook

### Readiness Probe Configuration

```yaml
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 5
  failureThreshold: 3
```

## Debugging Containers

### Getting a Shell

```bash
# If container has shell
kubectl exec -it <pod> -- /bin/sh

# Java debugging tools
kubectl exec -it <pod> -- jcmd 1 help
kubectl exec -it <pod> -- jcmd 1 Thread.print
```

### Container Images Without JDK Tools

JRE images don't include `jmap`, `jstack`, etc.

**Solutions:**
1. Use JDK base image in production (recommended)
2. Use `jcmd` (included in JRE since Java 11)
3. Ephemeral debug containers (Kubernetes 1.23+)

```bash
# Ephemeral debug container
kubectl debug -it <pod> --image=eclipse-temurin:21-jdk --target=<container>
```

### Remote JMX in Kubernetes

```bash
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
-Dcom.sun.management.jmxremote.rmi.port=9010
-Dcom.sun.management.jmxremote.local.only=false
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Djava.rmi.server.hostname=localhost
```

**Port-forward and connect:**
```bash
kubectl port-forward <pod> 9010:9010
# Connect JMC to localhost:9010
```

**Security warning:** Disable auth/SSL only for debugging. Use proper auth in production.

## Common Container Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| OOMKilled | Pod terminated with exit code 137 | Reduce heap percentage, check native memory |
| Slow startup | Pod not ready for minutes | CDS, readiness probe tuning |
| High CPU at start | JIT compilation | Warmup, consider GraalVM |
| Wrong GC threads | Too many/few parallel threads | Verify `UseContainerSupport` |
| Heap dump fills disk | emptyDir full | Use PVC or external storage |
| Can't debug | No jstack/jmap | Use JDK image, ephemeral containers |

## Recommended Production Configuration

```dockerfile
FROM eclipse-temurin:21-jdk-alpine

# Set defaults that work for containers
ENV JAVA_OPTS="\
  -XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0 \
  -XX:+UseZGC \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/heap-dumps/ \
  -XX:+ExitOnOutOfMemoryError \
  -Djava.security.egd=file:/dev/./urandom"
```

```yaml
# Kubernetes deployment
containers:
  - name: app
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "2Gi"
        cpu: "2"
    livenessProbe:
      httpGet:
        path: /actuator/health/liveness
        port: 8080
      initialDelaySeconds: 60
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /actuator/health/readiness
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 5
```
