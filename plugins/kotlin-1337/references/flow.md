# Kotlin Flow Deep Dive

Cold flows, hot flows, StateFlow, SharedFlow, and channels.

## Cold vs Hot Flows

### Cold Flows

Cold flows execute per collector. Each collector gets its own stream:

```kotlin
val coldFlow = flow {
    println("Flow started")
    emit(1)
    emit(2)
}

coldFlow.collect { } // Prints "Flow started"
coldFlow.collect { } // Prints "Flow started" again
```

**Characteristics:**
- Lazy — nothing runs until collected
- Per-collector execution
- No state between collections
- Examples: database queries, API calls, file reads

### Hot Flows

Hot flows exist independently of collectors. Multiple collectors share the same stream:

```kotlin
val stateFlow = MutableStateFlow(0)

// Collectors share the same state
launch { stateFlow.collect { println("A: $it") } }
launch { stateFlow.collect { println("B: $it") } }

stateFlow.value = 1 // Both A and B print
```

**Characteristics:**
- Active regardless of collectors
- State persists
- Multiple collectors share emissions
- Examples: UI state, configuration, events

## StateFlow

### Purpose

StateFlow is a state-holder flow that always has a current value:

```kotlin
private val _uiState = MutableStateFlow(UiState.Loading)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()

fun loadData() {
    _uiState.value = UiState.Loading
    viewModelScope.launch {
        val data = repository.fetch()
        _uiState.value = UiState.Success(data)
    }
}
```

### Key Properties

| Property | Behavior |
|----------|----------|
| Initial value | Required |
| Current value | Always accessible via `.value` |
| Replay | 1 (latest value to new collectors) |
| Equality | Conflates equal values (won't re-emit) |

### StateFlow Gotcha: Equality Conflation

```kotlin
val state = MutableStateFlow("error")

state.value = "error" // First emit
state.value = "error" // Ignored! Same value

// Fix: wrap in unique container or use SharedFlow for events
data class Event<T>(val value: T, val id: UUID = UUID.randomUUID())
```

### Converting Flow to StateFlow

```kotlin
val stateFlow = flow.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5000),
    initialValue = emptyList()
)
```

**SharingStarted options:**
- `Eagerly` — Start immediately, never stop
- `Lazily` — Start on first collector, never stop
- `WhileSubscribed(timeout)` — Start on first collector, stop after timeout with no collectors

## SharedFlow

### Purpose

SharedFlow is for events that may have zero, one, or multiple collectors:

```kotlin
private val _events = MutableSharedFlow<Event>()
val events: SharedFlow<Event> = _events.asSharedFlow()

fun sendEvent(event: Event) {
    viewModelScope.launch {
        _events.emit(event) // Suspends if buffer full
    }
}
```

### Configuration

```kotlin
val sharedFlow = MutableSharedFlow<Event>(
    replay = 0,           // How many past values to replay
    extraBufferCapacity = 64, // Buffer for slow collectors
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
```

| Parameter | Purpose |
|-----------|---------|
| `replay` | Events buffered for new collectors |
| `extraBufferCapacity` | Buffer beyond replay |
| `onBufferOverflow` | `SUSPEND`, `DROP_OLDEST`, `DROP_LATEST` |

### SharedFlow vs StateFlow

| Aspect | StateFlow | SharedFlow |
|--------|-----------|------------|
| Initial value | Required | Not required |
| Current value | `.value` | No |
| Default replay | 1 | 0 |
| Conflation | Yes (by equality) | No |
| Use case | State | Events |

### Converting Flow to SharedFlow

```kotlin
val sharedFlow = flow.shareIn(
    scope = viewModelScope,
    started = SharingStarted.Eagerly,
    replay = 1
)
```

## Channels

### When to Use Channels

Channels are for **point-to-point** communication:

```kotlin
val channel = Channel<Int>(capacity = Channel.BUFFERED)

// Producer
launch {
    channel.send(1)
    channel.send(2)
    channel.close()
}

// Consumer
launch {
    for (item in channel) {
        process(item)
    }
}
```

### Channel vs Flow

| Aspect | Channel | Flow |
|--------|---------|------|
| Consumption | Single consumer | Multiple collectors |
| Backpressure | Suspends sender | Operator-based |
| State | Mutable | Immutable |
| Use case | Work queues | Data streams |

### Channel Types

| Type | Behavior |
|------|----------|
| `RENDEZVOUS` (0) | Sender waits for receiver |
| `BUFFERED` (64) | Default buffered |
| `CONFLATED` | Keeps only latest |
| `UNLIMITED` | No limit (OOM risk) |

## Flow Operators

### Transformation

```kotlin
flow
    .map { it * 2 }           // Transform each
    .filter { it > 10 }       // Filter
    .take(5)                  // Limit count
    .distinctUntilChanged()   // Remove consecutive duplicates
```

### Combination

```kotlin
// Combine latest values
combine(flow1, flow2) { a, b -> a + b }

// Zip pairs
flow1.zip(flow2) { a, b -> Pair(a, b) }

// Flatten
flowOfFlows.flatMapConcat { it }  // Sequential
flowOfFlows.flatMapMerge { it }   // Concurrent
flowOfFlows.flatMapLatest { it }  // Cancel previous
```

### Error Handling

```kotlin
flow
    .catch { e -> emit(fallbackValue) }  // Handle upstream errors
    .onCompletion { e -> cleanup() }     // Always runs
    .retry(3) { e -> e is IOException }  // Retry on condition
```

### Context

```kotlin
flow
    .flowOn(Dispatchers.IO)  // Upstream runs on IO
    .collect { }             // Collection on original
```

## Patterns

### Search with Debounce

```kotlin
searchQuery
    .debounce(300)                    // Wait for typing pause
    .filter { it.length >= 2 }        // Minimum length
    .distinctUntilChanged()           // Skip duplicates
    .flatMapLatest { query ->         // Cancel previous search
        repository.search(query)
            .catch { emit(emptyList()) }
    }
    .collect { results -> show(results) }
```

### Periodic Polling

```kotlin
fun poll(interval: Long): Flow<Data> = flow {
    while (true) {
        emit(api.fetch())
        delay(interval)
    }
}.flowOn(Dispatchers.IO)
```

### Combine Multiple Sources

```kotlin
val combined = combine(
    userFlow,
    settingsFlow,
    connectionFlow
) { user, settings, connection ->
    UiState(user, settings, connection)
}
```

### Cold Flow from Callback

```kotlin
fun observeLocation(): Flow<Location> = callbackFlow {
    val callback = object : LocationCallback() {
        override fun onLocationUpdate(location: Location) {
            trySend(location)
        }
    }

    locationManager.register(callback)

    awaitClose {
        locationManager.unregister(callback)
    }
}
```

## Testing Flows

### Turbine Library

```kotlin
@Test
fun `emits loading then success`() = runTest {
    viewModel.state.test {
        assertEquals(UiState.Loading, awaitItem())
        assertEquals(UiState.Success(data), awaitItem())
        cancelAndIgnoreRemainingEvents()
    }
}
```

### Testing StateFlow

```kotlin
@Test
fun `updates state`() = runTest {
    val viewModel = MyViewModel()

    viewModel.loadData()

    assertEquals(UiState.Success(expected), viewModel.state.value)
}
```

### Testing with Fakes

```kotlin
class FakeRepository : Repository {
    private val _dataFlow = MutableSharedFlow<Data>()

    override fun observe(): Flow<Data> = _dataFlow

    suspend fun emit(data: Data) = _dataFlow.emit(data)
}

@Test
fun `handles data updates`() = runTest {
    val fakeRepo = FakeRepository()
    val viewModel = MyViewModel(fakeRepo)

    fakeRepo.emit(testData)

    assertEquals(testData, viewModel.data.value)
}
```
