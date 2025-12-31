[&larr; reference](../)

production-grade patterns that separate competent from exceptional rust developers

## install

```
/plugin install rust-1337@claude-1337
```

## philosophy

1. **make illegal states unrepresentable** - use types to eliminate bugs
2. **parse, don't validate** - transform unstructured data into typed structures
3. **zero-cost abstractions** - high-level code that compiles to optimal machine code
4. **explicit over implicit** - no hidden allocations, no surprise behavior
5. **design away lifetime complexity** - if fighting borrow checker, reconsider data model

## decision frameworks

### string ownership (95% rule)

| context | use | why |
|---------|-----|-----|
| struct fields | String | owned data lives with struct |
| function params | &str | accept any string via deref |
| return (from input) | &str | zero-cost slice |
| return (newly created) | String | caller needs ownership |
| conditional modification | Cow&lt;'_, str&gt; | clone-on-write |

### error handling

```
Writing a library?
├── YES → thiserror (callers match on variants)
└── NO (application) → Need pretty diagnostics?
    ├── YES → color-eyre (CLI) or miette (source snippets)
    └── NO → anyhow
```

### async vs threads

| workload | choice | rule |
|----------|--------|------|
| CPU-bound | threads / spawn_blocking | never block async workers |
| high-concurrency I/O | async | scales to millions |
| simple concurrency | threads | avoid async complexity |

**critical:** no more than 10-100µs between .await points

## production gotchas

### blocking in async

**trap:** sync operations inside async tasks starve runtime
**fix:** spawn_blocking() for CPU work; async alternatives for I/O

```rust
// wrong
async fn bad() { std::thread::sleep(Duration::from_secs(2)); }

// correct
async fn good() { tokio::task::spawn_blocking(|| heavy_computation()).await.unwrap(); }
```

### mutex across await

**trap:** std::sync::Mutex guard held across .await deadlocks
**fix:** drop guard before await, or tokio::sync::Mutex

```rust
// deadlock risk
async fn bad(mutex: Arc<std::sync::Mutex<i32>>) {
    let guard = mutex.lock().unwrap();
    some_async_op().await; // guard held!
}

// safe: explicit drop
async fn good(mutex: Arc<std::sync::Mutex<i32>>) {
    {
        let mut guard = mutex.lock().unwrap();
        *guard += 1;
    } // dropped before await
    some_async_op().await;
}
```

### cancellation safety

**trap:** futures dropped mid-operation leave invalid state
**detection:** check API docs; read is safe, read_line is NOT

## obsolete patterns

| obsolete | replacement | since |
|----------|-------------|-------|
| lazy_static! | std::sync::LazyLock | rust 1.80 |
| once_cell (most uses) | std::sync::OnceLock | rust 1.70 |
| async-std | smol (or tokio) | march 2025 |
| structopt | clap v4 derive | clap 3.0 |
| async-trait (some) | native async fn in traits | rust 1.75 |
| async closure workarounds | native async || {} closures | rust 1.85 |

## common crates

| need | crate |
|------|-------|
| errors (lib) | thiserror |
| errors (app) | anyhow |
| serialization | serde, serde_json, toml |
| CLI | clap (or lexopt for minimal) |
| async | tokio |
| http client | reqwest |
| http server | axum |
| logging | tracing |
| testing | proptest, nextest, insta |

## specialized domains

the skill routes to specific references based on project context:

| detected | loads |
|----------|-------|
| clap, lexopt, CLI binary | cli.md |
| axum, tonic, sqlx | backend.md |
| leptos, dioxus, wasm-bindgen | frontend.md |
| tauri, egui | native.md |
| #![no_std], cortex-m, embassy | embedded.md |
| pingora, rama, proxy | data-plane.md |
| bindgen, cxx, PyO3, unsafe | ffi-unsafe.md |
| proc-macro = true, syn, quote | proc-macros.md |
| reqwest, HTTP client | networking.md |
| project setup, CI | tooling.md |
| deep async patterns | async.md |

## structure

```
plugins/rust-1337/
├── SKILL.md              # core patterns, decision frameworks
└── references/           # 12 specialized domain files
    ├── cli.md
    ├── backend.md
    ├── frontend.md
    ├── native.md
    ├── embedded.md
    ├── data-plane.md
    ├── ffi-unsafe.md
    ├── proc-macros.md
    ├── networking.md
    ├── ecosystem.md
    ├── tooling.md
    └── async.md
```
