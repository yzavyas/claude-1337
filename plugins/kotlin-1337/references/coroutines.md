# Kotlin Coroutines Deep Dive

Structured concurrency, dispatchers, and production patterns.

## How Coroutines Work

Coroutines are compiled to state machines with continuations. Each `suspend` point becomes a state transition.

**Key insight:** Coroutines are lightweight not because they use less memory, but because they don't block threads while waiting.

## Structured Concurrency Principles

### The Job Hierarchy

Every coroutine has a Job. Jobs form parent-child relationships:

```
CoroutineScope
    └── Job (parent)
        ├── Job (child 1)
        └── Job (child 2)
```

**Rules:**
1. Parent waits for all children to complete
2. Cancelling parent cancels all children
3. Child failure cancels parent (unless SupervisorJob)

### CoroutineScope vs coroutineScope

| Construct | Purpose | Blocks Thread? |
|-----------|---------|----------------|
| `CoroutineScope` | Interface for launching | No |
| `coroutineScope { }` | Structured scope | No (suspends) |
| `supervisorScope { }` | Isolated failures | No (suspends) |
| `runBlocking { }` | Bridge blocking/suspend | Yes! |

### SupervisorScope for Failure Isolation

```kotlin
supervisorScope {
    launch { task1() } // Failure here won't cancel task2
    launch { task2() }
}
```

**When to use:** Independent parallel operations where one failure shouldn't stop others.

## Dispatchers

### Built-in Dispatchers

| Dispatcher | Threads | Use For |
|------------|---------|---------|
| `Default` | CPU cores | CPU-intensive work |
| `IO` | Expandable pool | Blocking I/O |
| `Main` | Single (UI) | UI updates |
| `Unconfined` | Caller's thread | Testing, special cases |

### Dispatcher Selection

```kotlin
// CPU-bound
withContext(Dispatchers.Default) {
    heavyComputation()
}

// IO-bound (blocking)
withContext(Dispatchers.IO) {
    file.readText()
}

// Never block Dispatchers.Default
```

### Custom Dispatchers

```kotlin
// Limited parallelism
val dbDispatcher = Dispatchers.IO.limitedParallelism(4)

// Single-threaded (for non-thread-safe resources)
val singleThread = Executors.newSingleThreadExecutor()
    .asCoroutineDispatcher()
```

## Cancellation

### Cooperative Cancellation

Cancellation is cooperative — code must check for it:

```kotlin
suspend fun processItems(items: List<Item>) {
    for (item in items) {
        ensureActive() // Check cancellation
        process(item)
    }
}

// Or use yield()
suspend fun processItems(items: List<Item>) {
    for (item in items) {
        yield() // Check cancellation + yield to scheduler
        process(item)
    }
}
```

### CancellationException Handling

```kotlin
// Wrong: swallows cancellation
try {
    suspendingWork()
} catch (e: Exception) {
    log.error("Failed", e)
}

// Correct: rethrow CancellationException
try {
    suspendingWork()
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    log.error("Failed", e)
}

// Best: use specific exception types
try {
    suspendingWork()
} catch (e: IOException) {
    log.error("IO failed", e)
}
```

### NonCancellable for Cleanup

```kotlin
suspend fun saveData(data: Data) {
    try {
        uploadToServer(data)
    } finally {
        // Ensure cleanup runs even if cancelled
        withContext(NonCancellable) {
            saveToLocalCache(data)
        }
    }
}
```

## Exception Handling

### Exception Propagation

| Builder | Exception Behavior |
|---------|-------------------|
| `launch` | Propagates to parent (crashes) |
| `async` | Stored in Deferred, thrown on `.await()` |

### CoroutineExceptionHandler

```kotlin
val handler = CoroutineExceptionHandler { _, exception ->
    log.error("Uncaught exception", exception)
}

val scope = CoroutineScope(SupervisorJob() + handler)

scope.launch {
    throw RuntimeException("oops") // Caught by handler
}
```

**Important:** Handler only catches exceptions from `launch`, not `async`.

### Try-Catch in Coroutines

```kotlin
// For async, catch at await()
val deferred = async { riskyOperation() }
try {
    deferred.await()
} catch (e: Exception) {
    handleError(e)
}

// For launch, use try-catch inside
launch {
    try {
        riskyOperation()
    } catch (e: Exception) {
        handleError(e)
    }
}
```

## Context Propagation

### CoroutineContext Elements

```kotlin
val context = Dispatchers.IO +           // Dispatcher
              CoroutineName("worker") +  // Name (debugging)
              SupervisorJob() +          // Job
              handler                    // Exception handler

val scope = CoroutineScope(context)
```

### withContext for Context Switching

```kotlin
suspend fun loadData(): Data {
    return withContext(Dispatchers.IO) {
        // Now on IO dispatcher
        api.fetch()
    }
    // Back to original dispatcher
}
```

## Patterns for Production

### Retry with Exponential Backoff

```kotlin
suspend fun <T> retry(
    times: Int = 3,
    initialDelay: Long = 100,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) {
        try {
            return block()
        } catch (e: Exception) {
            if (e is CancellationException) throw e
        }
        delay(currentDelay)
        currentDelay = (currentDelay * factor).toLong()
    }
    return block() // Last attempt
}
```

### Timeout

```kotlin
val result = withTimeoutOrNull(5000) {
    slowOperation()
} ?: defaultValue
```

### Rate Limiting

```kotlin
val semaphore = Semaphore(10) // Max 10 concurrent

suspend fun rateLimitedCall() {
    semaphore.withPermit {
        api.call()
    }
}
```

### Debounce with Flow

```kotlin
searchQuery
    .debounce(300)
    .distinctUntilChanged()
    .flatMapLatest { query ->
        searchApi(query)
    }
    .collect { results ->
        showResults(results)
    }
```

## Testing Coroutines

### runTest

```kotlin
@Test
fun `test suspending function`() = runTest {
    val result = myRepository.fetchData()
    assertEquals(expected, result)
}
```

### TestDispatcher

```kotlin
@Test
fun `test with controlled time`() = runTest {
    val testDispatcher = StandardTestDispatcher(testScheduler)
    val viewModel = MyViewModel(testDispatcher)

    viewModel.startTimer()

    advanceTimeBy(1000)

    assertEquals(1, viewModel.seconds.value)
}
```

### Inject Dispatchers

```kotlin
class MyRepository(
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend fun load() = withContext(ioDispatcher) {
        // testable!
    }
}

@Test
fun test() = runTest {
    val repo = MyRepository(StandardTestDispatcher(testScheduler))
    // ...
}
```
