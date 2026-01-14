# Embedded & no_std Rust

Microcontrollers, Embassy, RTIC, and bare-metal patterns.

## Target Readiness Matrix

| Target | Status |
|--------|--------|
| ARM Cortex-M | Tier 2 stable, production ready |
| RISC-V | Tier 2 stable (Rust 1.76+ atomic load/store) |
| ESP32 RISC-V | Works with upstream Rust |
| ESP32 Xtensa | Requires esp-rs toolchain |
| AVR | Experimental, LLVM bugs, nightly only |

**Production deployments**: Google (Ti50, OpenSK), Microsoft (Pluton, Surface UEFI), Volvo, Oxide Computers.

**Safety certification**: Ferrocene (ISO 26262 ASIL D, IEC 61508 SIL 4).

## Embassy vs RTIC Decision

| Factor | Embassy | RTIC |
|--------|---------|------|
| Model | Async/await cooperative | Interrupt-driven preemptive |
| Power efficiency | Excellent (auto-sleep) | Manual |
| Hard real-time | Complex | Guaranteed WCET analysis |
| Learning curve | Familiar if know async | Steeper |
| Memory | Slightly larger | Smallest |

**Use Embassy**: Async I/O heavy applications, familiar async model, power-sensitive.

**Use RTIC**: Hard real-time signal processing, formal timing analysis needs, minimum memory.

## Essential Stack

**Tooling**:
- `probe-rs` (v0.30.0) — unified debugging/flashing
- `flip-link` — stack overflow protection
- `defmt` — efficient logging

**Core crates**:

```toml
[dependencies]
cortex-m = "0.7"
cortex-m-rt = "0.7"
embedded-hal = "1.0"  # The 1.0 release!
critical-section = "1.1"
heapless = "0.8"
```

**HALs by family**:
- STM32: `embassy-stm32`
- Nordic: `embassy-nrf`
- RP2040/RP2350: `embassy-rp`
- ESP32: `esp-hal`

## no_std Fundamentals Checklist

1. **Panic handler required**:

```rust
use panic_halt as _;  // Or panic_probe for dev
```

2. **Allocator if using `alloc`**:

```rust
#[global_allocator]
static ALLOCATOR: /* your allocator */;
```

3. **critical-section implementation**:

```toml
# Enable for your HAL
embassy-stm32 = { features = ["critical-section-single-core"] }
```

## Typestate for Peripherals

Compile-time peripheral state enforcement:

```rust
pub struct Uart<State> {
    // ...
    _state: PhantomData<State>,
}

pub struct Unconfigured;
pub struct Configured;

impl Uart<Unconfigured> {
    pub fn configure(self, baud: u32) -> Uart<Configured> {
        // Setup...
        Uart { _state: PhantomData }
    }
}

impl Uart<Configured> {
    pub fn write(&mut self, data: &[u8]) {
        // Only callable after configure
    }
}

// Compile error: unconfigured UART can't write
```

## Static Mut Alternatives

**Never use `static mut`** — undefined behavior waiting to happen.

**Use `critical_section::Mutex`**:

```rust
use critical_section::Mutex;
use core::cell::RefCell;

static COUNTER: Mutex<RefCell<u32>> = Mutex::new(RefCell::new(0));

fn increment() {
    critical_section::with(|cs| {
        *COUNTER.borrow_ref_mut(cs) += 1;
    });
}
```

**Use atomics where applicable**:

```rust
use core::sync::atomic::{AtomicU32, Ordering};

static COUNTER: AtomicU32 = AtomicU32::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::Relaxed);
}
```

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Stack overflow | Use `flip-link` (flips memory layout, HardFault instead of corruption) |
| Forgetting panic handler | Add `use panic_halt as _;` |
| critical-section not enabled | Check HAL feature flags |
| AVR integer division broken | Pin to `nightly-2024-05-01` |
| Blocking in Embassy | System hangs — tasks are cooperative |
| Memory-mapped I/O ordering | Use `read_volatile`/`write_volatile` or HAL abstractions |

**flip-link setup**:

```toml
# .cargo/config.toml
[target.thumbv7em-none-eabihf]
rustflags = ["-C", "linker=flip-link"]
```

**defmt logging**:

```rust
use defmt::info;

info!("Value: {}", value);  // Efficient, no format strings in binary
```

Run with `probe-rs run --chip STM32F401 target/...` to see output.
