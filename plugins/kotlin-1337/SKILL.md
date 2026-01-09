---
name: kotlin-1337
description: "Elite Kotlin development patterns. Use when: writing Kotlin for backend (Ktor, Spring Boot), Android, Multiplatform. Covers coroutines, structured concurrency, Flow, scope functions, null safety, Java interop, testing (Kotest, MockK), benchmarking (kotlinx-benchmark)."
---

# Elite Kotlin Development

Production-grade patterns for idiomatic, performant, testable Kotlin.

## Philosophy

1. **Structured concurrency** — coroutines form hierarchies; cancellation propagates ([Roman Elizarov, KotlinConf 2018](https://www.youtube.com/watch?v=Mj5P47F6nJg))
2. **Null safety is earned** — platform types break guarantees; annotate Java code ([Kotlin docs](https://kotlinlang.org/docs/java-interop.html))
3. **Explicit over magic** — prefer Ktor's explicitness for understanding, Spring's magic for velocity
4. **Value classes for domain** — type safety without allocation overhead ([Kotlin 1.5+](https://kotlinlang.org/docs/inline-classes.html))
5. **Functions compose** — extension functions + scope functions = fluent APIs
6. **Test coroutines deterministically** — use `runTest` with `TestDispatcher`, not real time

## Decision Frameworks

### Coroutine Scope Selection

```
Who owns the lifecycle?
├── UI/ViewModel → viewModelScope (Android) or custom CoroutineScope
├── Service/Request → coroutineScope { } (structured)
├── Background work → supervisorScope { } (failure isolation)
├── Fire-and-forget → NEVER GlobalScope (breaks structured concurrency)
└── Test → runTest { }
```

**Why structured concurrency matters:** "Stop launching in GlobalScope, tie every coroutine to a real scope or lifecycle, keep `runBlocking` in `main()` or tests only."

**Source:** [ProAndroidDev: Inside Kotlin Coroutines (2025)](https://proandroiddev.com/inside-kotlin-coroutines-state-machines-continuations-and-structured-concurrency-b8d3d4e48e62)

### Flow Type Selection

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

**Source:** [Android Developers: StateFlow and SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)

### Backend Framework Selection

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

**Insight:** "If you don't have much backend experience, Spring Boot is recommended since it's 'a very very mature ecosystem with a lot of batteries included.'"

**Sources:** [JetBrains: Strategic Partnership with Spring (2025)](https://blog.jetbrains.com/kotlin/2025/05/strategic-partnership-with-spring/), [JetBrains: Kotlin Backend KotlinConf 2025](https://blog.jetbrains.com/kotlin/2025/08/kotlin-on-the-backend-what-s-new-from-kotlinconf-2025/)

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

**Source:** [Kotlin Docs: Scope Functions](https://kotlinlang.org/docs/scope-functions.html)

## Production Gotchas

### GlobalScope Is Almost Always Wrong

- **Trap**: `GlobalScope.launch { }` for background work
- **Impact**: No cancellation, no failure propagation, resource leaks
- **Fix**: Use structured concurrency — tie to a lifecycle

```kotlin
// Wrong: orphan coroutine
GlobalScope.launch { sendAnalytics() }

// Correct: tied to lifecycle
class MyService(private val scope: CoroutineScope) {
    fun send() = scope.launch { sendAnalytics() }
}
```

### CancellationException Must Propagate

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

**Best practice:** Add `@Nullable`/`@NotNull` annotations to Java code. Configure compiler to treat JSR-305 as errors.

**Source:** [kt.academy: Kotlin Java Interop Traps](https://kt.academy/article/ak-java-interop-4)

### Value Class Boxing

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

**Source:** [Carrion.dev: Zero-Cost Abstractions in Kotlin](https://carrion.dev/en/posts/kotlin-inline-functions-value-classes/)

### Dispatcher.Main Without Context

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

### StateFlow Equality Conflation

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

## Idiomatic Patterns

### Sealed Classes for State

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
    data object Loading : Result<Nothing>()
}

// Exhaustive when — compiler enforces all cases
when (result) {
    is Result.Success -> showData(result.data)
    is Result.Error -> showError(result.exception)
    Result.Loading -> showLoading()
}
```

### Value Classes for Domain Types

```kotlin
@JvmInline
value class UserId(val value: Long)

@JvmInline
value class OrderId(val value: Long)

// Compile-time type safety, runtime Long
fun processOrder(userId: UserId, orderId: OrderId) { }

// processOrder(orderId, userId) // Won't compile!
```

### Extension Functions for Fluent APIs

```kotlin
// Add functionality without inheritance
fun String.toSlug(): String =
    lowercase()
        .replace(Regex("[^a-z0-9]+"), "-")
        .trim('-')

"Hello World!".toSlug() // "hello-world"
```

### Inline Functions for Performance

```kotlin
// Use for small, frequently-called higher-order functions
inline fun <T> measureTimeMillis(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    return result to (System.currentTimeMillis() - start)
}

// Enables reified type parameters
inline fun <reified T> parseJson(json: String): T =
    objectMapper.readValue(json, T::class.java)
```

## Testing Patterns

### Coroutine Testing with runTest

```kotlin
@Test
fun `loads data correctly`() = runTest {
    val repo = MyRepository(
        ioDispatcher = StandardTestDispatcher(testScheduler)
    )

    val result = repo.loadData()

    assertThat(result).isEqualTo(expected)
}
```

### MockK for Mocking

```kotlin
@Test
fun `handles errors`() = runTest {
    val api = mockk<Api>()
    coEvery { api.fetch() } throws IOException()

    val repo = Repository(api)
    val result = repo.load()

    assertThat(result).isInstanceOf(Result.Error::class)
    coVerify { api.fetch() }
}
```

### Kotest Spec Styles

```kotlin
class UserServiceTest : FunSpec({
    val service = UserService()

    test("creates user with valid email") {
        val user = service.create("test@example.com")
        user.email shouldBe "test@example.com"
    }

    test("rejects invalid email") {
        shouldThrow<ValidationException> {
            service.create("invalid")
        }
    }
})
```

## Benchmarking with kotlinx-benchmark

```kotlin
@State(Scope.Benchmark)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
open class StringBenchmark {

    @Param("10", "100", "1000")
    var size: Int = 0

    private lateinit var data: List<String>

    @Setup
    fun setup() {
        data = (1..size).map { "item$it" }
    }

    @Benchmark
    fun joinWithPlus(): String {
        var result = ""
        data.forEach { result += it }
        return result
    }

    @Benchmark
    fun joinWithStringBuilder(): String {
        return buildString { data.forEach { append(it) } }
    }
}
```

**Setup:** Requires `allopen` plugin for JMH compatibility (classes must be non-final).

**Source:** [GitHub: kotlinx-benchmark](https://github.com/Kotlin/kotlinx-benchmark)

## Specialized References

Load reference based on context:

| Detected | Load |
|----------|------|
| Coroutines, structured concurrency, dispatchers | [coroutines.md](references/coroutines.md) |
| Flow, StateFlow, SharedFlow, channels | [flow.md](references/flow.md) |
| Ktor, Spring Boot, backend patterns | [backend.md](references/backend.md) |
| Multiplatform, expect/actual, KMP | [multiplatform.md](references/multiplatform.md) |
| Testing, Kotest, MockK | [testing.md](references/testing.md) |

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| `GlobalScope.launch` | Structured `coroutineScope` | No cancellation, leaks |
| Catch all exceptions | Rethrow `CancellationException` | Breaks structured concurrency |
| `runBlocking` in production | `suspend` functions | Blocks thread |
| Trust platform types | Explicit `?` at boundaries | Runtime NPE |
| Nest scope functions | Flatten or extract | Unreadable |
| `!!` everywhere | Safe calls, elvis, early return | NPE waiting to happen |
| Data class for value wrapper | `@JvmInline value class` | Allocation overhead |
| Mutable shared state | Flow/StateFlow | Race conditions |

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
