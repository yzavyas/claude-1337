# Native Applications

Desktop and mobile apps. Best-in-class choices.

## Framework Decision

```
Need mobile (iOS/Android)?
├── YES → Dioxus (only option with true mobile)
└── NO → Desktop only?
    ├── Web skills + native feel → Tauri
    ├── Quick tool/utility → egui
    └── Embedded/HMI → Slint
```

## Tauri 2.0

**Best for**: Desktop apps with web frontend. Smallest binaries (3-6MB).

```
┌─────────────────────────────┐
│     Web Frontend (JS/TS)    │
├─────────────────────────────┤
│    Native WebView (WRY)     │
├─────────────────────────────┤
│      Rust Backend           │
└─────────────────────────────┘
```

**IPC Pattern**:
```rust
#[tauri::command]
async fn process_data(data: String) -> Result<String, String> {
    Ok(format!("Processed: {}", data))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![process_data])
        .run(tauri::generate_context!())
        .unwrap();
}
```

**v2.0 changes**: New IPC protocol (5-10x faster), mobile support, granular permissions.

**Packaging**: Built-in .dmg, .msi, .deb, .AppImage, APK, iOS.

## Dioxus Native

**Best for**: Cross-platform from one codebase (web + desktop + mobile).

```rust
fn App() -> Element {
    rsx! {
        div { "Works on web, desktop, iOS, Android" }
    }
}
```

**CLI**:
```bash
dx serve --platform desktop
dx serve --platform ios
dx bundle --platform android  # Produces APK
```

**Renderer options**:
- WebView (default): Mature, smallest size
- Blitz (WGPU): Native rendering, beta

## egui

**Best for**: Quick tools, game dev editors, utilities.

**Philosophy**: Immediate mode - rebuild UI every frame.

```rust
impl eframe::App for MyApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            if ui.button("Click").clicked() {
                self.count += 1;
            }
            ui.label(format!("Count: {}", self.count));
        });
    }
}
```

**5-minute setup**. No state management boilerplate. Perfect with Bevy (`bevy_egui`).

**Trade-offs**: No native look (intentional), poor accessibility.

## Slint

**Best for**: Embedded HMI, resource-constrained devices.

**Production proof**: SK Signet EV chargers, QNX deployments.

**Specs**: <300KB RAM, runs on Cortex-M to x86.

Uses declarative `.slint` DSL files.

## NOT Recommended

| Framework | Why Not |
|-----------|---------|
| iced | Viable but Tauri more mature |
| Druid | Archived |
| Yew | Use Leptos/Dioxus instead |

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Tauri v2 not backward compatible | Don't mix v1/v2 APIs |
| Tauri println!() invisible | Use IPC for frontend logging |
| egui no CJK fonts | Load custom font |
| Dioxus mobile CSS animations only | No native animations yet |
| Large Tauri payloads >1MB | Use raw bytes API |
