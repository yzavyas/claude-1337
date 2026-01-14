# Frontend (Browser)

Rust web apps compiled to WASM. Best-in-class choices.

## Framework

```
Need SSR/streaming?
├── YES → Leptos
└── NO → Full-stack with mobile later?
    ├── YES → Dioxus
    └── NO → Leptos (better performance)
```

**Leptos** wins for web-first. Fine-grained reactivity, best SSR.

**Dioxus** if you'll also target desktop/mobile from same codebase.

## Leptos

```rust
#[component]
fn Counter() -> impl IntoView {
    let (count, set_count) = signal(0);
    view! {
        <button on:click=move |_| set_count.update(|n| *n += 1)>
            {count}
        </button>
    }
}
```

**Islands architecture** - 50-80% WASM size reduction:
```rust
#[island]  // Only this ships as WASM
fn InteractiveWidget() -> impl IntoView { ... }
```

## Dioxus (Web)

```rust
fn Counter() -> Element {
    let mut count = use_signal(|| 0);
    rsx! {
        button { onclick: move |_| count += 1, "{count}" }
    }
}
```

## Build Stack

| Framework | Tool |
|-----------|------|
| Leptos | cargo-leptos |
| Dioxus | dx serve |
| Manual | Trunk |

## Size Optimization

```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
```

Post-process: `wasm-opt -Oz -o out.wasm in.wasm`

Analyze: `twiggy top -n 20 app.wasm`

**wee_alloc is DEAD** - memory leak, unmaintained. Use default allocator.

## JS Interop

**Minimize boundary crossings** - each call has overhead.

```rust
// Bad: many crossings
for item in items {
    js_log(&item.to_string());
}

// Good: batch
js_log(&items.join("\n"));
```

**Intern repeated strings**:
```rust
let class = wasm_bindgen::intern("my-class");
element.set_class_name(class);
```

## Async

**Cannot block** - browser event loop is your runtime.

```rust
use wasm_bindgen_futures::spawn_local;

spawn_local(async {
    let data = fetch_data().await;
    // ...
});
```

**Tokio/async-std DON'T WORK** in browser WASM.

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| `std::time::Instant` panics | Use `web_sys::Performance` |
| `getrandom` fails | Add `features = ["js"]` |
| Threads need special setup | SharedArrayBuffer + COOP/COEP headers |
| Debug builds huge | Always measure release |
| Hydration mismatch | Check HTML validity, avoid non-deterministic IDs |
