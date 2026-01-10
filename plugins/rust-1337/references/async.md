# Deep Async Patterns

Advanced async/tokio patterns beyond the basics.

## Sources

| Attribution | URL |
|-------------|-----|
| tokio preemption blog | https://tokio.rs/blog/2020-04-preemption |
| tokio shared-state tutorial | https://tokio.rs/tokio/tutorial/shared-state#holding-a-mutexguard-across-an-await |
| tokio-console | https://github.com/tokio-rs/console |
| tokio docs: cancel-safety | https://docs.rs/tokio/latest/tokio/io/trait.AsyncBufReadExt.html#cancel-safety |
| CancellationToken (tokio-util) | https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html |

## Runtime Selection

```
Need Windows support?
├── YES → tokio (only real option)
└── NO → Writing runtime-agnostic library?
    ├── YES → smol
    └── NO → High-performance network proxy?
        ├── YES (Linux 5.6+) → monoio or glommio
        └── NO → tokio (default)
```

**When async adds complexity without benefit**:
- Simple CLI tools with sequential operations
- CPU-bound processing (use threads)
- Low concurrency requirements

## Cancellation Safety Deep Dive

**What it means**: A future is cancel-safe if dropping it mid-execution doesn't leave state invalid or lose data.

**Safe vs unsafe APIs**:
| Safe | NOT Safe |
|------|----------|
| `AsyncReadExt::read` | `AsyncBufReadExt::read_line` |
| `tokio::sync::mpsc::recv` | `tokio::io::copy` (partial) |
| `tokio::time::sleep` | Custom state machines |

**CancellationToken pattern**:

```rust
use tokio_util::sync::CancellationToken;

let token = CancellationToken::new();
let cloned = token.clone();

tokio::spawn(async move {
    tokio::select! {
        _ = cloned.cancelled() => {
            // Cleanup
        }
        result = do_work() => {
            // Normal completion
        }
    }
});

// Later: trigger cancellation
token.cancel();
```

**Structured shutdown template**:

```rust
async fn shutdown(token: CancellationToken, tasks: JoinSet<()>) {
    token.cancel();

    let timeout = tokio::time::timeout(
        Duration::from_secs(30),
        async {
            while tasks.join_next().await.is_some() {}
        }
    );

    if timeout.await.is_err() {
        tracing::warn!("Shutdown timed out, forcing exit");
    }
}
```

## Shared State Patterns

| Pattern | Use When |
|---------|----------|
| `Arc<Mutex<T>>` | Low contention, need to peek |
| `mpsc` channels | Clear data flow, no shared state |
| `DashMap` | High-contention concurrent HashMap |
| `Arc<RwLock<T>>` | Many readers, few writers |

**Lock ordering discipline**:
- Always acquire locks in consistent order
- Document lock hierarchy
- Use lock-free structures when possible

**When to use `tokio::sync::Mutex` vs `std`**:
- `std::sync::Mutex`: Lock released before any `.await`
- `tokio::sync::Mutex`: Must hold lock across `.await` points

```rust
// std is fine here
async fn good(mutex: Arc<std::sync::Mutex<i32>>) {
    let val = { *mutex.lock().unwrap() }; // Dropped immediately
    do_async_work(val).await;
}

// Need tokio here
async fn needs_tokio(mutex: Arc<tokio::sync::Mutex<i32>>) {
    let mut guard = mutex.lock().await;
    *guard = fetch_value().await; // Held across await
}
```

## Backpressure & Bounded Channels

**Why unbounded channels are dangerous**:
- Memory grows without limit under load
- Producer unaware of consumer lag
- System OOMs instead of gracefully degrading

**Channel sizing heuristics**:
- Start with `buffer = 2 * num_producers`
- Measure and adjust based on latency/throughput tradeoff
- Consider `tokio::sync::Semaphore` for more control

**`poll_ready` in tower services**:

```rust
impl<S> Service<Request> for MyMiddleware<S>
where
    S: Service<Request>,
{
    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Error>> {
        // MUST call inner poll_ready for backpressure
        self.inner.poll_ready(cx)
    }
}
```

## Blocking Detection & Prevention

**tokio-console setup**:

```toml
[dependencies]
tokio = { version = "1", features = ["full", "tracing"] }
console-subscriber = "0.2"
```

```toml
# .cargo/config.toml
[build]
rustflags = ["--cfg", "tokio_unstable"]
```

**Identifying blocking code**:
- tokio-console shows tasks with high "busy" time
- Tasks not yielding for >100µs
- CPU at 100% with tasks stuck

**`spawn_blocking` patterns**:

```rust
// CPU-intensive work
let result = tokio::task::spawn_blocking(|| {
    expensive_computation()
}).await?;

// Sync I/O (avoid if possible)
let data = tokio::task::spawn_blocking(|| {
    std::fs::read_to_string("file.txt")
}).await??;
```

## Structured Concurrency

**`JoinSet` for dynamic task groups**:

```rust
use tokio::task::JoinSet;

let mut set = JoinSet::new();

for url in urls {
    set.spawn(fetch(url));
}

while let Some(result) = set.join_next().await {
    match result {
        Ok(Ok(data)) => process(data),
        Ok(Err(e)) => tracing::error!("Task error: {e}"),
        Err(e) => tracing::error!("Task panicked: {e}"),
    }
}
```

**Graceful shutdown with timeout**:

```rust
let shutdown = async {
    signal::ctrl_c().await.expect("signal handler");
};

tokio::select! {
    _ = shutdown => {
        tracing::info!("Shutting down...");
    }
    _ = server.serve() => {}
}

// Drain with timeout
tokio::time::timeout(Duration::from_secs(30), drain_connections()).await.ok();
```

**Task panic handling**:

```rust
let handle = tokio::spawn(async {
    might_panic().await
});

match handle.await {
    Ok(result) => result,
    Err(e) if e.is_panic() => {
        tracing::error!("Task panicked: {:?}", e.into_panic());
        // Decide: propagate, restart, or ignore
    }
    Err(e) => {
        tracing::error!("Task cancelled: {e}");
    }
}
```
