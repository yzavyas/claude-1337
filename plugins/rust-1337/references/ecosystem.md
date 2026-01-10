# Rust Ecosystem Guide

Crate selection, deprecations, and evaluation frameworks.

## Sources

| Attribution | URL |
|-------------|-----|
| Rust 1.80 (LazyLock) | https://blog.rust-lang.org/2024/07/25/Rust-1.80.0/ |
| Rust 1.70 (OnceLock) | https://blog.rust-lang.org/2023/06/01/Rust-1.70.0/ |
| Rust 1.75 (async fn in traits) | https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/ |
| Rust 1.85 (async closures) | https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/ |
| async-std deprecated | https://github.com/async-rs/async-std/issues/1072 |
| clap 3.0 release | https://github.com/clap-rs/clap/releases/tag/v3.0.0 |
| RUSTSEC-2021-0139 (ansi_term) | https://rustsec.org/advisories/RUSTSEC-2021-0139 |
| RUSTSEC-2022-0054 (wee_alloc) | https://rustsec.org/advisories/RUSTSEC-2022-0054 |
| wee_alloc Issue #106 | https://github.com/rustwasm/wee_alloc/issues/106 |
| Cargo reference: features | https://doc.rust-lang.org/cargo/reference/features.html#feature-unification |
| Cargo book | https://doc.rust-lang.org/cargo/commands/cargo-tree.html |
| DHAT | https://docs.rs/dhat |
| cargo-flamegraph | https://github.com/flamegraph-rs/flamegraph |
| Rust Book ch15 | https://doc.rust-lang.org/book/ch15-06-reference-cycles.html |

## What Production Tools Actually Use

Evidence over opinion:

| Tool | Dependencies | Insight |
|------|--------------|---------|
| ripgrep | lexopt, termcolor, anyhow | Migrated FROM clap in 2024 |
| fd, bat, delta | clap derive, nu-ansi-term | Feature-rich CLI pattern |
| crates.io | diesel | ORM at scale works |

BurntSushi on lexopt: "demonstrates exactly how something new can arrive on the scene and just thoroughly solve a problem minimalistically."

## Crate Selection by Category

### Error Handling

| Crate | Use When |
|-------|----------|
| thiserror | Library — callers match on variants |
| anyhow | Application — just propagate errors |
| color-eyre | CLI — colored pretty errors |
| miette | Compiler/linter — source snippets |
| snafu | Large multi-crate systems |

### Serialization

| Need | Default | High-perf |
|------|---------|-----------|
| JSON | serde_json | simd-json (3x faster, when >5% CPU) |
| Config | toml | — |
| Binary | bincode | — |
| no_std binary | postcard | — |

### Async Runtime

| Scenario | Choice |
|----------|--------|
| Default | tokio |
| Runtime-agnostic lib | smol |
| io_uring (Linux) | monoio |
| Embedded | embassy |
| **DEAD** | async-std (March 2025) |

### CLI Parsing

| Complexity | Crate | Compile |
|------------|-------|---------|
| Simple flags | lexopt | ~0.5s |
| Minimal | pico-args | ~1s |
| Full-featured | clap derive | ~5s |

### Web

| Priority | Framework |
|----------|-----------|
| Default | axum |
| Max performance | actix-web |
| Best DX | rocket |

| Need | Client |
|------|--------|
| Default | reqwest |
| Max control | hyper |
| Sync/minimal | ureq |

### Database

| Scenario | Crate |
|----------|-------|
| SQLite | rusqlite |
| Async + raw SQL | sqlx |
| Async + ORM | sea-orm |
| Sync + type DSL | diesel |

### Testing

| Need | Crate |
|------|-------|
| Test runner | nextest (3x faster) |
| Property testing | proptest |
| Snapshots | insta |
| Parameterized | rstest |
| HTTP mocking | wiremock |

### Observability

| Need | Crate |
|------|-------|
| Logging | tracing (THE standard) |
| OpenTelemetry | opentelemetry 0.27+ |
| Metrics | metrics |

### Concurrency

| Need | Use |
|------|-----|
| Default mutex | std::sync::Mutex |
| 1-byte mutex | parking_lot |
| Data parallelism | rayon |
| Concurrent HashMap | dashmap (only if bottleneck) |

## Deprecation Details

| Obsolete | Replacement | Migration |
|----------|-------------|-----------|
| `lazy_static!` | `LazyLock` | `static X: LazyLock<T> = LazyLock::new(\|\| ...)` |
| `once_cell::Lazy` | `LazyLock` | Direct replacement (Rust 1.80+) |
| `once_cell::OnceCell` | `OnceLock` | Direct replacement (Rust 1.70+) |
| `async-std` | smol/tokio | Rewrite with new runtime |
| `structopt` | clap v4 | Update derive syntax |
| `cargo-edit` | `cargo add` | Native since Cargo 1.62 |
| `ansi_term` | `nu-ansi-term` | Drop-in fork |
| `wee_alloc` | default/Talc | Memory leak in wee_alloc |

## Crate Evaluation Red Flags

**Maintenance signals**:
- Last release > 1 year without activity
- Issues/PRs ignored
- No CI badges

**Dependency concerns**:
- High transitive dep count
- Pulling in tokio for sync-only lib
- Feature flags that aren't additive

**Check features**: `cargo tree --edges features`

## MSRV Strategies

| Project Type | Recommended |
|--------------|-------------|
| Tokio ecosystem | 6-month rolling (1.70-1.71) |
| General libraries | 6-12 months behind stable |
| Enterprise | 1 year behind |

BurntSushi: "I try to target a year behind."

## When Nightly Is Needed

Rarely in 2025. Stable has:
- async fn in traits (1.75)
- GATs (1.65)
- impl Trait in traits (1.75)
- async closures `async || {}` (1.85)
- LazyLock/OnceLock (1.70-1.80)

Only need nightly for:
- `cargo-udeps`
- Miri testing
- Experimental Cranelift
- gen blocks (coming soon)
