# Svelte 5 Patterns

Production patterns for Svelte 5 and SvelteKit.

## Svelte 5 Runes

### The Core Runes

| Rune | Purpose | Replaces |
|------|---------|----------|
| `$state` | Reactive state | `let x = ...` (reactive) |
| `$derived` | Computed values | `$: x = ...` (reactive) |
| `$effect` | Side effects | `$: { ... }` (statement) |
| `$props` | Component props | `export let` |
| `$bindable` | Two-way binding | `export let` with bind: |

### Production Gotchas

| Trap | What Happens | Fix |
|------|--------------|-----|
| Destructuring `$state` | Loses reactivity | Access properties directly: `obj.prop` |
| `$state` in module scope | Won't update across components | Use Context or component-level `$state` |
| Missing `$effect` cleanup | Memory leaks | Return cleanup: `$effect(() => { return () => cleanup(); })` |
| Context without getter | Stale values | Use getter: `{ get value() { return state } }` |
| `$derived` for async | Doesn't work | Use `$effect` + `$state` |
| `createEventDispatcher` | Svelte 4 pattern | Use callback props |
| `$state` on element refs | Unnecessary | Use plain `let el: HTMLElement;` |

### Basic Patterns

```svelte
<script lang="ts">
  // Props
  let { name, count = 0 }: { name: string; count?: number } = $props();

  // State
  let counter = $state(0);

  // Derived
  let doubled = $derived(counter * 2);

  // Effect with cleanup
  $effect(() => {
    const interval = setInterval(() => counter++, 1000);
    return () => clearInterval(interval);  // Cleanup
  });
</script>
```

### Reactive Context

```svelte
<!-- Parent.svelte -->
<script>
  import { setContext } from 'svelte';

  let theme = $state('light');

  // Use getter for reactive context
  setContext('theme', {
    get current() { return theme; },
    toggle: () => theme = theme === 'light' ? 'dark' : 'light'
  });
</script>
```

```svelte
<!-- Child.svelte -->
<script>
  import { getContext } from 'svelte';

  const theme = getContext('theme');
</script>

<p>Theme: {theme.current}</p>  <!-- Reactive! -->
<button onclick={theme.toggle}>Toggle</button>
```

### Snippets (Replacing Slots)

```svelte
<!-- Table.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    data,
    header,
    row
  }: {
    data: T[];
    header: Snippet;
    row: Snippet<[T]>;
  } = $props();
</script>

<table>
  <thead>{@render header()}</thead>
  <tbody>
    {#each data as item}
      <tr>{@render row(item)}</tr>
    {/each}
  </tbody>
</table>
```

```svelte
<!-- Usage -->
<Table data={users}>
  {#snippet header()}
    <th>Name</th>
    <th>Email</th>
  {/snippet}

  {#snippet row(user)}
    <td>{user.name}</td>
    <td>{user.email}</td>
  {/snippet}
</Table>
```

## SvelteKit Patterns

### Load Functions

| Need | Use | Why |
|------|-----|-----|
| Data before render | `+page.ts` load | Streaming, SEO |
| Server secrets | `+page.server.ts` | Never expose to client |
| Client-only lib | `browser` check | SSR crashes otherwise |
| Shared state | Context API | Component tree scoping |

```typescript
// +page.ts
export const load = async ({ fetch }) => {
  const res = await fetch('/api/data');
  const data = await res.json();
  return { data };
};
```

```typescript
// +page.server.ts (server secrets safe)
import { PRIVATE_API_KEY } from '$env/static/private';

export const load = async () => {
  const res = await fetch('https://api.example.com', {
    headers: { Authorization: `Bearer ${PRIVATE_API_KEY}` }
  });
  return { data: await res.json() };
};
```

### SSR Guards

```svelte
<script>
  import { browser } from '$app/environment';
  let ThreeScene;

  if (browser) {
    import('./ThreeScene.svelte').then(m => ThreeScene = m.default);
  }
</script>

{#if ThreeScene}
  <svelte:component this={ThreeScene} />
{/if}
```

### Form Actions

```typescript
// +page.server.ts
export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');

    // Validate and save
    return { success: true };
  },

  subscribe: async ({ request }) => {
    // Named action
  }
};
```

```svelte
<!-- +page.svelte -->
<form method="POST">
  <input name="email" type="email" required />
  <button>Submit</button>
</form>

<!-- Named action -->
<form method="POST" action="?/subscribe">
  ...
</form>
```

## Threlte 8 (Svelte + Three.js)

### Basic Setup

```svelte
<script>
  import { Canvas } from '@threlte/core';
  import Scene from './Scene.svelte';
</script>

<Canvas>
  <Scene />
</Canvas>
```

### Scene Component

```svelte
<script>
  import { T, useTask } from '@threlte/core';

  let rotation = $state({ y: 0 });

  useTask((delta) => {
    rotation.y += delta;
  });
</script>

<T.AmbientLight intensity={0.5} />
<T.PointLight position={[10, 10, 10]} />

<T.Mesh rotation.y={rotation.y}>
  <T.BoxGeometry args={[1, 1, 1]} />
  <T.MeshStandardMaterial color="orange" />
</T.Mesh>
```

### Render Modes

| Mode | Use When |
|------|----------|
| `always` | Continuous animation |
| `on-demand` | Static with interactions |
| `manual` | Full control with `advance()` |

```svelte
<Canvas renderMode="on-demand">
  <Scene />
</Canvas>
```

### SSR Guard for Threlte

```svelte
<script>
  import { browser } from '$app/environment';
  let Scene;

  if (browser) {
    import('./Scene.svelte').then(m => Scene = m.default);
  }
</script>

{#if Scene}
  <svelte:component this={Scene} />
{/if}
```

## GSAP Integration

### Setup with Cleanup

```svelte
<script>
  import { onMount } from 'svelte';
  import { gsap } from 'gsap';

  let element;

  onMount(() => {
    const ctx = gsap.context(() => {
      gsap.from(element, {
        y: 50,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out'
      });
    });

    return () => ctx.revert();  // REQUIRED cleanup
  });
</script>

<div bind:this={element}>Content</div>
```

### Svelte Action Pattern

```typescript
// src/lib/actions/animate.ts
import { gsap } from 'gsap';

export function animate(node: HTMLElement, params: gsap.TweenVars) {
  const tween = gsap.from(node, params);

  return {
    destroy() {
      tween.kill();
    }
  };
}
```

```svelte
<script>
  import { animate } from '$lib/actions/animate';
</script>

<div use:animate={{ y: 50, opacity: 0, duration: 0.8 }}>
  Content
</div>
```

### ScrollTrigger

```svelte
<script>
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';

  let triggers = [];

  onMount(async () => {
    if (!browser) return;

    const gsap = (await import('gsap')).gsap;
    const { ScrollTrigger } = await import('gsap/ScrollTrigger');

    gsap.registerPlugin(ScrollTrigger);

    triggers.push(
      ScrollTrigger.create({
        trigger: '.section',
        start: 'top center',
        onEnter: () => console.log('entered')
      })
    );
  });

  onDestroy(() => {
    triggers.forEach(t => t.kill());
  });
</script>
```

## Transitions

### Built-in Transitions

```svelte
<script>
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  let visible = $state(true);
</script>

{#if visible}
  <div transition:fade>Fades both ways</div>
{/if}

{#if visible}
  <div in:fly={{ y: 50, duration: 400, easing: cubicOut }} out:fade>
    Flies in, fades out
  </div>
{/if}
```

### Motion (spring/tweened)

```svelte
<script>
  import { spring, tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';

  let position = spring({ x: 0, y: 0 }, { stiffness: 0.1, damping: 0.5 });
  let progress = tweened(0, { duration: 400, easing: cubicOut });
</script>

<div style="transform: translate({$position.x}px, {$position.y}px)">
  Follows spring
</div>

<div style="width: {$progress}%">Progress bar</div>
```

## Checklist

Before shipping Svelte 5 code:

- [ ] `$state` not destructured?
- [ ] Context uses getter for reactivity?
- [ ] `$effect` returns cleanup function?
- [ ] Threlte behind `browser` check?
- [ ] GSAP/ScrollTrigger cleanup on destroy?
- [ ] `renderMode="on-demand"` where possible?

## Sources

- [Svelte 5 Docs](https://svelte.dev/docs)
- [SvelteKit Docs](https://kit.svelte.dev/docs)
- [Threlte Docs](https://threlte.xyz/)
- [GSAP + Svelte](https://gsap.com/resources/Svelte/)
