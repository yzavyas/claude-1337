# Rust Tooling & Configuration

Project setup, CI, and development workflow configurations.

## clippy.toml

```toml
msrv = "1.80"
cognitive-complexity-threshold = 25
too-many-lines-threshold = 100
too-many-arguments-threshold = 7
type-complexity-threshold = 250
avoid-breaking-exported-api = true

disallowed-methods = [
    { path = "std::env::var", reason = "Use dotenvy or config crate" },
    { path = "std::thread::sleep", reason = "Use tokio::time::sleep in async" },
]
```

## rustfmt.toml

```toml
edition = "2024"
max_width = 100
tab_spaces = 4
newline_style = "Unix"
use_small_heuristics = "Default"
reorder_imports = true
reorder_modules = true
group_imports = "StdExternalCrate"
imports_granularity = "Crate"
format_code_in_doc_comments = true
```

## Cargo.toml Lints Section

```toml
[lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"

[lints.clippy]
all = "warn"
pedantic = "warn"
# Selective allows for pedantic
needless_pass_by_value = "allow"
must_use_candidate = "allow"
module_name_repetitions = "allow"
# Extra restrictions
enum_glob_use = "deny"
unwrap_used = "warn"
expect_used = "warn"
```

**Critical**: Never use `#![deny(warnings)]` in library code—breaks forward compatibility.

## .cargo/config.toml

```toml
[build]
# rustc-wrapper = "sccache"  # Uncomment for shared cache

[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]

[alias]
t = "nextest run"
c = "clippy --all-targets --all-features -- -D warnings"
b = "build --release"
d = "doc --no-deps --open"

[net]
git-fetch-with-cli = true

[registries.crates-io]
protocol = "sparse"
```

## GitHub Actions CI

```yaml
name: CI
on: [push, pull_request]

env:
  CARGO_TERM_COLOR: always
  RUSTFLAGS: "-D warnings"

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: rustup toolchain install stable --profile minimal
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --all-features

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: rustup toolchain install stable --profile minimal
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@nextest
      - run: cargo nextest run --all-features

  clippy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: rustup toolchain install stable --profile minimal --component clippy
      - uses: Swatinem/rust-cache@v2
      - run: cargo clippy --all-targets --all-features -- -D warnings

  fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: rustup toolchain install stable --profile minimal --component rustfmt
      - run: cargo fmt --all -- --check

  msrv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: rustup toolchain install 1.75 --profile minimal
      - uses: Swatinem/rust-cache@v2
      - run: cargo +1.75 check --all-features

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: rustsec/audit-check@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## nextest.toml

```toml
[profile.default]
retries = 0
fail-fast = true

[profile.ci]
fail-fast = false
retries = 2

[profile.ci.junit]
path = "junit.xml"
```

## Release Profile Optimization

```toml
[profile.release]
opt-level = 3        # Maximum optimization
lto = "thin"         # Link-time optimization (or true for max)
codegen-units = 1    # Better optimization, slower compile
strip = "symbols"    # Remove debug symbols
panic = "abort"      # Smaller binary (no unwinding)

[profile.release-small]
inherits = "release"
opt-level = "z"      # Optimize for size
lto = true

[profile.dev.package."*"]
opt-level = 2        # Optimize deps in dev builds
```

**When to use `opt-level = "z"`**: WASM, embedded, size-critical deployments.

## Development Workflow

### bacon Setup

```toml
# bacon.toml
[jobs.default]
command = ["cargo", "check", "--all-targets", "--color", "always"]

[jobs.clippy]
command = ["cargo", "clippy", "--all-targets", "--all-features", "--color", "always"]

[jobs.test]
command = ["cargo", "nextest", "run", "--color", "always"]

[keybindings]
c = "job:clippy"
t = "job:test"
```

Run `bacon`, press `c` for clippy, `t` for tests.

### rust-analyzer Settings

```json
{
  "rust-analyzer.check.command": "clippy",
  "rust-analyzer.cargo.features": "all"
}
```

### tokio-console Setup

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full", "tracing"] }
console-subscriber = "0.2"
```

```toml
# .cargo/config.toml
[build]
rustflags = ["--cfg", "tokio_unstable"]
```

```rust
#[tokio::main]
async fn main() {
    console_subscriber::init();
    // Run `tokio-console` in another terminal
}
```

## Recommended Workflow

**Daily development**:
1. `bacon` for continuous feedback
2. rust-analyzer with clippy on save
3. `cargo nextest run` over cargo test
4. mold linker for faster iteration

**Before committing**:
1. `cargo fmt --all`
2. `cargo clippy --all-targets --all-features -- -D warnings`
3. `cargo nextest run`
4. `cargo deny check` (for libraries)

**CI essentials**:
1. Swatinem/rust-cache for caching
2. cargo-nextest with JUnit output
3. MSRV check against stated minimum
4. cargo-audit for security

**Release workflow**:
1. release-plz for automated releases
2. cargo-semver-checks for API compatibility
3. cargo-chef for Docker layer caching
