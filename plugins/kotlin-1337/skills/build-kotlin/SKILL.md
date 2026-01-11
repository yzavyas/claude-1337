---
name: build-kotlin
description: "Elite Kotlin development patterns. Use when: writing Kotlin for backend (Ktor, Spring Boot), Android, Multiplatform. Covers coroutines, structured concurrency, Flow, scope functions, null safety, Java interop, testing (Kotest, MockK), benchmarking (kotlinx-benchmark)."
---

# Elite Kotlin Development

Production-grade patterns for idiomatic, performant, testable Kotlin.

## Philosophy

1. **Structured concurrency** — coroutines form hierarchies; cancellation propagates (Elizarov, KotlinConf 2018)
2. **Null safety is earned** — platform types break guarantees; annotate Java code (Kotlin docs)
3. **Explicit over magic** — prefer Ktor's explicitness for understanding, Spring's magic for velocity
4. **Value classes for domain** — type safety without allocation overhead (Kotlin 1.5+)
5. **Functions compose** — extension functions + scope functions = fluent APIs
6. **Test coroutines deterministically** — use `runTest` with `TestDispatcher`, not real time

## Decision Frameworks

### Coroutine Scope Selection

```
Who owns the lifecycle?
├── UI/ViewModel → viewModelScope (Android) or custom CoroutineScope
├── Service/Request → coroutineScope { } (structured)
├── Background work → supervisorScope { } (failure isolation)
├── Fire-and-forget → See "GlobalScope Decision Framework" below
└── Test → runTest { }
```

**Why structured concurrency matters:** "Stop launching in GlobalScope, tie every coroutine to a real scope or lifecycle, keep `runBlocking` in `main()` or tests only." (ProAndroidDev 2025)

### Flow Type Selection

**Confidence:** High — official Android/Kotlin guidance.

```
What are you modeling?
├── State (always has current value) → StateFlow
│   └── UI state, configuration, connection status
├── Events (happen once, may have no collectors) → SharedFlow
│   └── Navigation events, errors, user actions
├── Cold data stream (computes per collector) → Flow
│   └── Database queries, API responses, file reads
└── Producer-consumer (one-to-one) → Channel
    └── Work queues, actor patterns
```

| Type | Hot/Cold | Has Current Value | Replay | Use Case |
|------|----------|-------------------|--------|----------|
| `Flow` | Cold | No | N/A | Data streams |
| `StateFlow` | Hot | Yes (always) | 1 (latest) | UI state |
| `SharedFlow` | Hot | Configurable | Configurable | Events |
| `Channel` | Hot | No | No | Producer-consumer |

**What Claude often misses:** StateFlow conflation — won't emit duplicate values. Use SharedFlow for events that may repeat. See "StateFlow Equality Conflation" gotcha. (Android docs)

### Backend Framework Selection

**Confidence:** High — JetBrains official guidance as of 2025.

```
Project requirements?
├── Lightweight, explicit, KMP-compatible → Ktor
├── Enterprise, batteries-included → Spring Boot
├── Team experience?
│   ├── Kotlin-first team → Ktor
│   └── Java/Spring background → Spring Boot
└── Startup time critical → Ktor
```

| Aspect | Ktor | Spring Boot |
|--------|------|-------------|
| Philosophy | Explicit, minimal | Convention over configuration |
| Learning curve | Steeper (must wire everything) | Gentler (auto-configuration) |
| Startup time | Fast (~1s) | Slower (~3-5s) |
| Ecosystem | Growing | Massive |
| Coroutine-native | Yes | Needs `suspend` bridges |
| KMP support | Yes (shared networking) | No |

**What to recommend:** For backend newcomers or enterprise contexts, Spring Boot. For Kotlin-first teams wanting explicit control, Ktor. JetBrains has a strategic partnership with Spring, so both are first-class options. (JetBrains 2025)

### Scope Function Selection

```
What do you need?
├── Configure object and return it → apply { }
├── Null-safe transformation → ?.let { }
├── Compute something → run { } or with(obj) { }
├── Side effect in chain → also { }
└── Non-null scope → with(obj) { }
```

| Function | Context | Returns | Best For |
|----------|---------|---------|----------|
| `apply` | `this` | Context object | Object configuration |
| `also` | `it` | Context object | Side effects in chains |
| `let` | `it` | Lambda result | Null checks, transforms |
| `run` | `this` | Lambda result | Computing with object |
| `with` | `this` | Lambda result | Grouping calls (non-null) |

(Source: Kotlin docs)

### GlobalScope Decision Framework

**Confidence:** High — Roman Elizarov (coroutines lead) consistently advocates this position.

```
Is GlobalScope appropriate here?
├── Does the work outlive any owning component? → Maybe GlobalScope
│   └── Example: Startup cache warm-up that must complete regardless of UI
├── Is there truly no owner that should manage lifecycle? → Maybe GlobalScope
│   └── Example: JVM shutdown hooks, application-level singletons
├── Do you need cancellation or failure tracking? → NO, use structured scope
├── Is this test or prototyping code? → Acceptable, but prefer runBlocking/runTest
└── Default: If in doubt, find an owner — there almost always is one
```

**When GlobalScope is defensible:**
- Application-scoped work with no logical owner (rare in well-structured code)
- Work that must survive any individual component's cancellation
- Low-stakes fire-and-forget (analytics, non-critical logging) — though injecting a scope is still cleaner

**When GlobalScope is wrong (most cases):**
- Request-scoped work — will leak on request cancellation
- UI-triggered work — will continue after view destruction
- Anything where you'd want to cancel on shutdown

(Sources: Elizarov, KotlinConf 2018; ProAndroidDev 2025)

## Production Gotchas

### CancellationException Must Propagate

**Confidence:** High — documented behavior, common source of bugs.

- **Trap**: Catching all exceptions swallows cancellation
- **Impact**: Coroutine won't cancel, structured concurrency breaks
- **Fix**: Rethrow `CancellationException` or use `runCatching`

```kotlin
// Wrong: swallows cancellation
try {
    doWork()
} catch (e: Exception) {
    log(e)
}

// Correct: rethrow cancellation
try {
    doWork()
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    log(e)
}

// Better: use runCatching (handles it)
runCatching { doWork() }
    .onFailure { if (it !is CancellationException) log(it) }
```

### Platform Types Break Null Safety

**Confidence:** High — well-documented, frequently encountered.

- **Trap**: Java methods return platform types (`String!`)
- **Impact**: Runtime NPE in "null-safe" Kotlin code
- **Detection**: `String!` notation in IDE
- **Fix**: Explicitly declare nullability at boundary

```kotlin
// Java method: String getName() — no annotation
// Kotlin sees: String! (platform type)

// Dangerous: compiler trusts you
val name: String = javaObj.name // NPE if null!

// Safe: explicit nullable
val name: String? = javaObj.name
```

**Best practice:** Add `@Nullable`/`@NotNull` annotations to Java code. Configure compiler to treat JSR-305 as errors. (kt.academy)

### Value Class Boxing

**Confidence:** High — bytecode-verifiable behavior.

- **Trap**: Value classes box when used with generics, interfaces, or as nullable
- **Impact**: Allocation overhead negates performance benefit
- **Detection**: Decompile bytecode, profile allocations

```kotlin
@JvmInline
value class UserId(val id: Long)

fun direct(id: UserId) {}        // No boxing
fun nullable(id: UserId?) {}     // Boxing!
fun generic(id: T) {}            // Boxing!
fun asInterface(id: Comparable<UserId>) {} // Boxing!
```

**When to still use value classes despite boxing:** Type safety benefit > allocation cost in non-hot paths. Profile before optimizing. (carrion.dev)

### Dispatcher.Main Without Context

**Confidence:** High — common mistake in cross-platform code.

- **Trap**: Using `Dispatchers.Main` in library/backend code
- **Impact**: Crashes on non-Android or missing Main dispatcher
- **Fix**: Inject dispatchers, default to `Dispatchers.Default`

```kotlin
// Wrong: hardcoded
class MyRepo {
    suspend fun load() = withContext(Dispatchers.IO) { ... }
}

// Correct: injectable
class MyRepo(private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) {
    suspend fun load() = withContext(ioDispatcher) { ... }
}
```

(Source: Kotlin docs)

### StateFlow Equality Conflation

**Confidence:** High — documented behavior, commonly misunderstood.

- **Trap**: StateFlow doesn't emit if value equals previous
- **Impact**: Duplicate events swallowed silently
- **Fix**: Use SharedFlow for events, or wrap in unique container

```kotlin
// Problem: same error won't re-emit
_error.value = "Network error"
_error.value = "Network error" // Ignored!

// Fix: use SharedFlow for events
private val _events = MutableSharedFlow<Event>()
```

(Source: Android docs)

## Decision Frameworks: When to Use What

### Sealed vs Enum vs Data Class

```
What are you modeling?
├── Fixed set of singleton values → enum class
├── Fixed set with varying data per variant → sealed class/interface
├── Unbounded data container → data class
└── Hierarchy needing inheritance → sealed interface (Kotlin 1.5+)
```

**What Claude often misses:** Sealed interfaces allow subclasses in other files (same module). Sealed classes require same file. Choose based on organization needs.

### Value Class vs Type Alias

```
Need runtime type distinction?
├── Yes (parameter order bugs, serialization identity) → value class
├── No (just readability) → typealias
└── Need nullable or generic usage? → value class still works, but boxes (see gotcha)
```

### Inline Function Usage

```
Should this function be inline?
├── Higher-order function with lambda param? → Likely yes (avoids lambda allocation)
├── Need reified type parameter? → Must be inline
├── Small, frequently-called? → Consider inline
├── Large function body? → NO (bloats bytecode at call sites)
└── Non-local return needed in lambda? → Must be inline
```

**What Claude gets wrong:** Inlining large functions. The bytecode duplication cost outweighs lambda allocation savings. Profile if unsure.

## Testing Decision Framework

### Test Framework Selection

| Framework | Best For | Kotlin-native |
|-----------|----------|---------------|
| Kotest | Kotlin-first teams, property testing, rich matchers | Yes |
| JUnit 5 | Mixed Java/Kotlin, existing JUnit infrastructure | No (works fine) |

### Coroutine Testing: Critical Gotchas

**Always use `runTest`** — not `runBlocking` for coroutine tests. `runTest` controls virtual time.

**Inject dispatchers** — hardcoded `Dispatchers.IO` is untestable. Pass `StandardTestDispatcher(testScheduler)` in tests.

**MockK coroutine syntax:**
- `coEvery { }` for suspend functions (not `every`)
- `coVerify { }` for verification (not `verify`)

### Benchmarking Gotcha

**kotlinx-benchmark requires `allopen` plugin** — JMH needs non-final classes. Without it, benchmarks compile but give wrong results. (kotlinx-benchmark docs)

## Specialized References

Load reference based on context:

| Detected | Load |
|----------|------|
| Coroutines, structured concurrency, dispatchers | [coroutines.md](references/coroutines.md) |
| Flow, StateFlow, SharedFlow, channels | [flow.md](references/flow.md) |
| Ktor, Spring Boot, backend patterns | [backend.md](references/backend.md) |
| Multiplatform, expect/actual, KMP | [multiplatform.md](references/multiplatform.md) |
| Testing, Kotest, MockK | [testing.md](references/testing.md) |

## Common Mistakes (Decision Guidance)

| Pattern | Default Guidance | When to Reconsider |
|---------|------------------|-------------------|
| `GlobalScope.launch` | Prefer structured scope | Application-scoped fire-and-forget (rare) |
| Catch all exceptions | Rethrow `CancellationException` | Almost never — cancellation must propagate |
| `runBlocking` | Prefer `suspend` functions | Entry points: `main()`, tests, Java interop bridges |
| Trust platform types | Explicit `?` at boundaries | Never — always assume nullable from Java |
| Nested scope functions | Flatten or extract | Acceptable if genuinely clearer (rare) |
| `!!` operator | Safe calls, elvis, early return | Private internal code with proven invariant |
| Data class for wrapper | `@JvmInline value class` | When you need `copy()`, `equals` override, or multiple fields |
| Mutable shared state | Flow/StateFlow | Atomic counters, carefully synchronized caches |

## Quick Reference

### Coroutine Builders

```kotlin
launch { }          // Fire-and-forget, returns Job
async { }           // Returns Deferred<T>, call .await()
runBlocking { }     // Blocks thread (main/tests only)
coroutineScope { }  // Suspends, structured
supervisorScope { } // Failure isolation
```

### Flow Operators

```kotlin
flow.map { }        // Transform elements
flow.filter { }     // Filter elements
flow.collect { }    // Terminal, suspends
flow.stateIn(scope) // Convert to StateFlow
flow.shareIn(scope) // Convert to SharedFlow
```

### Testing Dependencies

```kotlin
// build.gradle.kts
testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8+")
testImplementation("io.kotest:kotest-runner-junit5:5.8+")
testImplementation("io.mockk:mockk:1.13+")
```
