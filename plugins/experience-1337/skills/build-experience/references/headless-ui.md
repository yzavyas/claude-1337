# Headless UI

Unstyled, accessible component primitives for flexible UX.

## Why Headless?

| Problem | Headless Solution |
|---------|-------------------|
| Styled libraries fight your design system | Zero styling — you control every pixel |
| Accessibility is hard to implement correctly | WAI-ARIA baked in, keyboard nav handled |
| Component libraries lock you into their patterns | Primitives compose however you need |
| Bundle bloat from unused styles | Tree-shakeable, style-free |

**The core insight**: Behavior and accessibility are the hard parts. Styling is the easy part you want control over. Headless libraries invert the typical trade-off.

## Library Decision

| Library | Framework | Bundle | Accessibility | Maturity |
|---------|-----------|--------|---------------|----------|
| **Melt UI** | Svelte | ~15KB | Full WAI-ARIA | Production |
| **Bits UI** | Svelte | ~20KB | Full WAI-ARIA | Production |
| Ark UI | Svelte/others | ~25KB | Full WAI-ARIA | Newer |
| Radix | React-only | ~30KB | Industry standard | N/A |

### Decision Tree

```
Building Svelte UI?
├── Need maximum flexibility → Melt UI (primitives)
├── Want pre-composed patterns → Bits UI (built on Melt)
├── Want state machines → Ark UI (Zag.js under hood)
└── Quick prototype → shadcn-svelte (Bits + Tailwind)
```

## Melt UI

**Builder pattern** — returns stores and actions, you render everything.

```svelte
<script>
  import { createDialog } from '@melt-ui/svelte';

  const {
    elements: { trigger, overlay, content, title, close },
    states: { open }
  } = createDialog();
</script>

<button use:melt={$trigger}>Open</button>

{#if $open}
  <div use:melt={$overlay} class="fixed inset-0 bg-black/50" />
  <div use:melt={$content} class="dialog-content">
    <h2 use:melt={$title}>Dialog Title</h2>
    <p>Your content here</p>
    <button use:melt={$close}>Close</button>
  </div>
{/if}
```

**Why Melt UI:**
- Zero styling opinions
- Full keyboard navigation
- Focus management handled
- Svelte stores for state
- Tree-shakeable

**Source**: [melt-ui.com](https://melt-ui.com/)

## Bits UI

**Component pattern** — pre-composed from Melt primitives.

```svelte
<script>
  import { Dialog } from 'bits-ui';
</script>

<Dialog.Root>
  <Dialog.Trigger class="btn">Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay class="fixed inset-0 bg-black/50" />
    <Dialog.Content class="dialog-content">
      <Dialog.Title>Dialog Title</Dialog.Title>
      <Dialog.Description>Your content here</Dialog.Description>
      <Dialog.Close class="btn">Close</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**Why Bits UI:**
- Familiar component API (like Radix)
- Built on Melt (same accessibility)
- Easier migration from React/Radix
- Powers shadcn-svelte

**Source**: [bits-ui.com](https://www.bits-ui.com/)

## shadcn-svelte

**Copy-paste components** — Bits UI + Tailwind, own the code.

```bash
bunx shadcn-svelte@latest init
bunx shadcn-svelte@latest add button dialog
```

```svelte
<script>
  import * as Dialog from '$lib/components/ui/dialog';
  import { Button } from '$lib/components/ui/button';
</script>

<Dialog.Root>
  <Dialog.Trigger asChild let:builder>
    <Button builders={[builder]}>Open</Button>
  </Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Dialog Title</Dialog.Title>
    </Dialog.Header>
    <p>Content goes here</p>
  </Dialog.Content>
</Dialog.Root>
```

**Why shadcn-svelte:**
- You own the code (copy, not install)
- Tailwind styling included
- Modify anything
- Great for rapid prototyping

**Source**: [shadcn-svelte.com](https://www.shadcn-svelte.com/)

## Common Components

| Component | Melt UI | Bits UI | Notes |
|-----------|---------|---------|-------|
| Dialog/Modal | `createDialog` | `Dialog.*` | Focus trap, escape close |
| Dropdown Menu | `createDropdownMenu` | `DropdownMenu.*` | Keyboard nav, submenus |
| Select | `createSelect` | `Select.*` | Typeahead, multi-select |
| Tabs | `createTabs` | `Tabs.*` | Arrow key nav |
| Accordion | `createAccordion` | `Accordion.*` | Single/multi expand |
| Tooltip | `createTooltip` | `Tooltip.*` | Delay, positioning |
| Popover | `createPopover` | `Popover.*` | Focus management |
| Combobox | `createCombobox` | `Combobox.*` | Autocomplete |
| Slider | `createSlider` | `Slider.*` | Range, steps |
| Toggle Group | `createToggleGroup` | `ToggleGroup.*` | Single/multi |

## Headless vs Styled

| Approach | When | Trade-off |
|----------|------|-----------|
| **Headless (Melt)** | Custom design system | More work, full control |
| **Pre-composed (Bits)** | Faster start | Slightly less flexible |
| **Copy-paste (shadcn)** | Prototyping | Tailwind dependency |

## Accessibility Handled

What headless libraries give you for free:

| Feature | Manual Implementation |
|---------|----------------------|
| Focus trap in modals | Complex, error-prone |
| Keyboard navigation | Arrow keys, Home/End, typeahead |
| ARIA attributes | role, aria-expanded, aria-selected |
| Screen reader announcements | Live regions |
| Focus restoration | Return focus on close |

**The value**: You get production accessibility without implementing it yourself.

## Performance Notes

- Melt UI uses Svelte stores — reactive, minimal overhead
- No virtual DOM reconciliation
- Tree-shakeable — only import what you use
- SSR compatible (SvelteKit)

## Sources

- [Melt UI Docs](https://melt-ui.com/)
- [Bits UI Docs](https://www.bits-ui.com/)
- [shadcn-svelte Docs](https://www.shadcn-svelte.com/)
- [Ark UI Svelte](https://ark-ui.com/svelte/docs/overview/introduction)
