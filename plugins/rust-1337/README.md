# rust-1337

Rust development decisions. Picks winners, not catalogs.

## Coverage

| Domain | Topics |
|--------|--------|
| CLI | lexopt vs clap, argument parsing |
| Backend | axum, sqlx, tonic, API patterns |
| Frontend | Leptos, Dioxus, WASM |
| Native | Tauri, egui, cross-platform |
| Data-plane | Pingora, Rama, proxy patterns |
| Networking | reqwest, Tower, protocols |
| Async | tokio gotchas, cancellation, blocking |
| Embedded | no_std, HALs, RTIC |
| FFI/Unsafe | CString traps, soundness |
| Proc-macros | syn, quote, derive patterns |

## Decision Examples

- **HTTP server**: axum (not actix-web, not rocket)
- **Database**: sqlx (compile-time checked)
- **CLI (simple)**: lexopt (what ripgrep uses)
- **CLI (complex)**: clap with derive
- **Frontend**: Leptos (fine-grained reactivity)
- **Native apps**: Tauri (not Electron)

## Contents

```
rust-1337/
├── SKILL.md             # Core decisions + gotchas
└── references/          # 12 domain-specific files
    ├── cli.md
    ├── backend.md
    ├── frontend.md
    └── ...
```
