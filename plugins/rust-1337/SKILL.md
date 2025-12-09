---
name: rust-1337
description: "Elite Rust development. Use when: building Rust CLI, backend, frontend, or native apps. Covers axum, tonic, sqlx, Leptos, Dioxus, Tauri, clap, tokio. Production gotchas (blocking, cancellation, mutex), ownership decisions, crate selection. Routes to specialized domains: embedded, FFI, proc-macros, proxies/data-plane."
---

# Elite Rust Development

Production-grade patterns that separate competent from exceptional Rust developers.

## Philosophy

1. **Make illegal states unrepresentable** — use types to eliminate bugs
2. **Parse, don't validate** — transform unstructured data into typed structures
3. **Zero-cost abstractions** — high-level code that compiles to optimal machine code
4. **Explicit over implicit** — no hidden allocations, no surprise behavior
5. **Design away lifetime complexity** — if fighting the borrow checker, reconsider data model
6. **Clone consciously** — every `.clone()` is a decision about allocation
7. **Trust but verify safety** — Rust prevents data races, not deadlocks

## Decision Frameworks

### String Ownership (95% Rule)

| Context | Use | Why |
|---------|-----|-----|
| Struct fields | `String` | Owned data lives with struct |
| Function params | `&str` | Accept any string via deref |
| Return (from input) | `&str` | Zero-cost slice |
| Return (newly created) | `String` | Caller needs ownership |
| Conditional modification | `Cow<'_, str>` | Clone-on-write |

### Trait Objects vs Generics

| Factor | Generics | `dyn Trait` |
|--------|----------|-------------|
| Performance | Faster (static dispatch) | Slower (vtable) |
| Binary size | Larger | Smaller |
| Heterogeneous collections | No | Yes |

Rule: Default to generics. Use `dyn` for heterogeneous collections or plugin systems.

### Error Handling Selection

```
Writing a library?
├── YES → thiserror (callers match on variants)
└── NO (application) → Need pretty diagnostics?
    ├── YES → color-eyre (CLI) or miette (source snippets)
    └── NO → anyhow
```

### Async vs Threads

| Workload | Choice | Rule |
|----------|--------|------|
| CPU-bound | Threads / `spawn_blocking` | Never block async workers |
| High-concurrency I/O | Async | Scales to millions |
| Simple concurrency | Threads | Avoid async complexity |

**Critical: No more than 10-100µs between `.await` points.**

## Production Gotchas

### Blocking in Async

- **Trap**: Sync operations inside async tasks starve runtime
- **Detection**: `tokio-console` shows tasks not yielding
- **Fix**: `spawn_blocking()` for CPU work; async alternatives for I/O

```rust
// Wrong
async fn bad() {
    std::thread::sleep(Duration::from_secs(2)); // Blocks worker
}

// Correct
async fn good() {
    tokio::task::spawn_blocking(|| heavy_computation()).await.unwrap();
}
```

### Mutex Across Await

- **Trap**: `std::sync::Mutex` guard held across `.await` deadlocks
- **Detection**: Deadlock under load; compiles fine
- **Fix**: Drop guard before await, or `tokio::sync::Mutex`

```rust
// Deadlock risk
async fn bad(mutex: Arc<std::sync::Mutex<i32>>) {
    let guard = mutex.lock().unwrap();
    some_async_op().await; // Guard held!
}

// Safe: explicit drop
async fn good(mutex: Arc<std::sync::Mutex<i32>>) {
    {
        let mut guard = mutex.lock().unwrap();
        *guard += 1;
    } // Dropped before await
    some_async_op().await;
}
```

### Cancellation Safety

- **Trap**: Futures dropped mid-operation leave invalid state
- **Detection**: Check API docs; `read` is safe, `read_line` is NOT
- **Fix**: Don't hold invalid state across await; use `CancellationToken`

### Feature Flag Unification

- **Trap**: Cargo unifies features globally; non-additive features break
- **Detection**: `cargo tree --edges features`
- **Fix**: Features must be additive; use `default-features = false`

### Hidden Allocations

- **Trap**: `clone()`, `to_string()`, `format!()`, Vec growth
- **Detection**: DHAT, cargo-flamegraph
- **Fix**: `with_capacity()`, `SmallVec`, `Cow`, `shrink_to_fit()`

### Reference Cycles

- **Trap**: `Rc<RefCell<T>>` cycles leak memory
- **Fix**: `Weak<T>` for back-edges; consider arenas

## Obsolete Patterns

| Obsolete | Replacement | Since |
|----------|-------------|-------|
| `lazy_static!` | `std::sync::LazyLock` | Rust 1.80 |
| `once_cell` (most uses) | `std::sync::OnceLock` | Rust 1.70 |
| `async-std` | smol (or tokio) | March 2025 |
| `structopt` | clap v4 derive | clap 3.0 |
| `async-trait` (some cases) | Native async fn in traits | Rust 1.75 |
| async closure workarounds | Native `async \|\| {}` closures | Rust 1.85 |
| `ansi_term` | `nu-ansi-term` | Unmaintained |
| `wee_alloc` | Default allocator or Talc | Memory leak #106 |

Note: `async-trait` still needed for `dyn Trait` with async methods.

## Type Design Patterns

### Newtype Pattern

Compile-time type safety for IDs:

```rust
struct UserId(u64);
struct OrderId(u64);

fn process_user(id: UserId) { /* ... */ }
// process_user(OrderId(1)); // Won't compile!
```

### Builder Pattern

```rust
struct ConfigBuilder {
    required_field: Option<String>,
    optional_field: Option<i32>,
}

impl ConfigBuilder {
    fn required_field(mut self, val: String) -> Self {
        self.required_field = Some(val);
        self
    }

    fn build(self) -> Result<Config, BuilderError> {
        Ok(Config {
            required_field: self.required_field.ok_or(BuilderError::MissingField)?,
            optional_field: self.optional_field.unwrap_or_default(),
        })
    }
}
```

Use `typed-builder` crate in production.

### Typestate Pattern

Compile-time state machine enforcement:

```rust
struct Connection<State> { /* ... */ _state: PhantomData<State> }
struct Disconnected;
struct Connected;
struct Authenticated;

impl Connection<Disconnected> {
    fn connect(self) -> Connection<Connected> { /* ... */ }
}

impl Connection<Connected> {
    fn authenticate(self, creds: &str) -> Connection<Authenticated> { /* ... */ }
}

impl Connection<Authenticated> {
    fn query(&self, sql: &str) -> Result<Data, Error> { /* ... */ }
}
// Can't call query() on unauthenticated connection - won't compile
```

When to use: Required state transitions, protocol implementations.

### Enums Over Booleans

```rust
// Bad
fn validate(data: &str, strict: bool) { /* ... */ }

// Good
enum Validation { Strict, Lenient }
fn validate(data: &str, mode: Validation) { /* ... */ }
```

## Error Handling

### Library Errors — thiserror

```rust
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("invalid input: {0}")]
    InvalidInput(String),
    #[error("network error")]
    Network(#[from] std::io::Error),
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

pub type Result<T> = std::result::Result<T, Error>;
```

### Application Errors — anyhow

```rust
use anyhow::{Context, Result, bail, ensure};

fn process() -> Result<()> {
    let data = read_file()
        .with_context(|| format!("failed to read config"))?;

    ensure!(!data.is_empty(), "config file is empty");

    if invalid(&data) {
        bail!("invalid configuration format");
    }
    Ok(())
}
```

**Rules**:
- Never `.unwrap()` in library code
- Never `.expect()` without useful message

## Elite Patterns

### Defensive Slice Matching

```rust
// Anti-pattern: decoupled check
if !users.is_empty() { let user = users[0]; }

// Elite: coupled via match
match users.as_slice() {
    [] => handle_empty(),
    [single] => handle_one(single),
    [first, ..] => handle_multiple(first),
}
```

### Simplify Lifetimes Through Architecture

Insight: "Data lives forever or for duration of event loop."

- Use `Copy` IDs instead of references
- Pass references top-down each frame
- Trade-off: Lookup indirection vs lifetime elimination

### Temporary Mutability Scoping

```rust
let sorted = {
    let mut temp = get_data();
    temp.sort();
    temp  // Immutable from here
};
```

### Extension Traits

- Suffix with `Ext` (RFC 445)
- Export in prelude for glob import

## Specialized Domains

Load reference based on project context:

| Detected | Load |
|----------|------|
| `clap`, `lexopt`, CLI binary | [cli.md](references/cli.md) |
| `axum`, `tonic`, `sqlx`, API/service | [backend.md](references/backend.md) |
| `leptos`, `dioxus`, `wasm-bindgen`, browser WASM | [frontend.md](references/frontend.md) |
| `tauri`, `egui`, desktop/mobile app | [native.md](references/native.md) |
| `#![no_std]`, `cortex-m`, `embassy`, `rtic` | [embedded.md](references/embedded.md) |
| `pingora`, `rama`, `proxy`, `xds` | [data-plane.md](references/data-plane.md) |
| `bindgen`, `cbindgen`, `cxx`, `PyO3`, `unsafe` | [ffi-unsafe.md](references/ffi-unsafe.md) |
| `proc-macro = true`, `syn`, `quote` | [proc-macros.md](references/proc-macros.md) |
| `reqwest`, HTTP client, protocols | [networking.md](references/networking.md) |
| Crate selection questions | [ecosystem.md](references/ecosystem.md) |
| Project setup, CI, configs | [tooling.md](references/tooling.md) |
| Deep async patterns, tokio internals | [async.md](references/async.md) |

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| `.unwrap()` in libs | Return `Result` | Callers can't recover |
| `.clone()` to fix borrow checker | Redesign ownership | Hidden allocation, wrong model |
| `Arc<Mutex<T>>` everywhere | Channels, message passing | Deadlock risk, contention |
| `String` for everything | Newtypes, enums | Type safety |
| `pub` by default | `pub(crate)`, minimal exposure | API surface control |
| Hold mutex across `.await` | Drop before await | Deadlock |
| `lazy_static!` | `LazyLock` | Deprecated |
| Block in async | `spawn_blocking` | Starves runtime |

## Quick Reference

### Commands

```bash
cargo clippy -- -W clippy::pedantic  # Lints
cargo nextest run   # Faster tests    |  cargo deny check    # Deps
cargo tree --edges features          # Feature resolution
cargo bloat --release                # Binary size
```

### Common Crates

| Need | Crate |
|------|-------|
| Errors (lib) | thiserror |
| Errors (app) | anyhow |
| Serialization | serde, serde_json, toml |
| CLI | clap (or lexopt for minimal) |
| Async | tokio |
| HTTP | reqwest (client), axum (server) |
| Logging | tracing |
| Testing | proptest, nextest, insta |