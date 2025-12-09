# FFI & Unsafe Rust

Foreign function interface, unsafe patterns, and soundness.

## Tool Selection

| Scenario | Tool |
|----------|------|
| Wrapping C library | bindgen + safe wrapper |
| Exposing Rust to C | cbindgen |
| C++ integration (new project) | cxx |
| Large existing C++ | autocxx |
| Multi-language (Swift + Kotlin + Python) | UniFFI |
| Python extensions | PyO3 + maturin |
| Node.js native modules | napi-rs |

**cxx vs bindgen**: Use cxx for new projects — zero unsafe in user code, type-safe at compile time. Fallback to bindgen for ~5% of cases where cxx restrictions limit.

**Production users**: cxx (Chrome, Meta), PyO3 (Hugging Face, Polars), UniFFI (Firefox mobile/desktop).

## Soundness vs Safety

**Critical distinction**:
- **Safe**: No `unsafe` keyword in API
- **Sound**: Cannot cause undefined behavior through safe API

**A safe API can be unsound**:

```rust
// SAFE but UNSOUND - public API has no unsafe, but causes UB
pub fn bad_index(slice: &[u8], idx: usize) -> u8 {
    unsafe { *slice.get_unchecked(idx) }  // Missing bounds check!
}

// SOUND - safe wrapper validates inputs
pub fn good_index(slice: &[u8], idx: usize) -> Option<u8> {
    slice.get(idx).copied()
}
```

**Your responsibility**: Unsafe blocks must uphold invariants for ALL possible safe inputs.

## Memory Ownership Rules

**Golden rules**:
1. Rust-allocated → Rust-freed
2. C-allocated → C-freed
3. Never mix allocators

**Ownership transfer**:

```rust
// Give ownership to C
let boxed = Box::new(MyStruct { ... });
let ptr = Box::into_raw(boxed);  // Rust forgets about it
ffi_take_ownership(ptr);

// Take ownership from C
let ptr = ffi_give_ownership();
let boxed = unsafe { Box::from_raw(ptr) };  // Rust owns it again
// Dropped normally
```

## CString Lifetime Trap

**The classic bug**:

```rust
// WRONG - dangling pointer!
let ptr = CString::new("text").unwrap().as_ptr();
// CString dropped immediately, ptr is dangling!
ffi_call(ptr);  // UB

// CORRECT - bind to variable
let c_string = CString::new("text").unwrap();
let ptr = c_string.as_ptr();  // Valid while c_string lives
ffi_call(ptr);
// c_string dropped here, after use
```

## Safe Transmutation

**Use zerocopy** (compile-time checked):

```rust
use zerocopy::{FromBytes, IntoBytes};

#[derive(FromBytes, IntoBytes)]
#[repr(C)]
struct Header {
    magic: u32,
    version: u16,
    flags: u16,
}

let bytes: &[u8] = ...;
let header = Header::read_from_prefix(bytes).unwrap();
```

**Use bytemuck** (Pod types):

```rust
use bytemuck::{Pod, Zeroable};

#[derive(Pod, Zeroable, Copy, Clone)]
#[repr(C)]
struct Vertex {
    position: [f32; 3],
    color: [f32; 4],
}
```

**Avoid raw `transmute`** — zerocopy/bytemuck catch mistakes at compile time.

## Miri for UB Detection

**Setup**:

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

**CI integration**:

```yaml
miri:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: rustup toolchain install nightly --component miri
    - run: cargo +nightly miri test
      env:
        MIRIFLAGS: "-Zmiri-tree-borrows"
```

**Tree Borrows flag**: More permissive than Stacked Borrows, catches different UB patterns.

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| `*const` from `&mut` can't write | Stacked/Tree Borrows rules |
| Panic crossing FFI | Use `extern "C-unwind"` |
| Rust 2024 Edition | `#[no_mangle]` requires `#[unsafe(no_mangle)]` |
| Uninitialized memory | Use `MaybeUninit<T>` |
| Aliasing violations | Review pointer provenance rules |

**`extern "C-unwind"`** (Rust 1.71+):

```rust
// If Rust code might panic and caller is C
#[no_mangle]
pub extern "C-unwind" fn might_panic() {
    // Panic will unwind through C frames safely
}
```

**Layered crate pattern**:

```
mylib-sys/     # Raw unsafe bindings (bindgen output)
  └── build.rs
mylib/         # Safe Rust wrapper
  └── src/lib.rs  # impl Drop, Result types, etc.
```
