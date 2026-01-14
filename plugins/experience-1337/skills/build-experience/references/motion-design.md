# Motion Design

Animation patterns for production experiences. Framework-agnostic.

## Library Landscape

| Library | Bundle | Best For | Trade-off |
|---------|--------|----------|-----------|
| Motion (Framer Motion) | ~32KB | React, declarative | Heavier but intuitive API |
| GSAP | ~23KB core | Timelines, scroll, SVG | **Free but prohibits Webflow competitors** |
| Lenis | ~3KB | Smooth scroll | **Production standard (not Locomotive)** |
| svelte-motion | Built-in | Svelte spring/tweened | Framework-specific |
| CSS Animations | 0KB | Simple, declarative | Limited control |

**What Claude doesn't know:**
- Lenis + ScrollTrigger is the Awwwards stack (Locomotive is dated)
- GSAP licensing prohibits certain commercial uses (read the license)
- View Transitions API is Baseline (Oct 2025)
- CSS `animation-timeline: scroll()` landed in Safari 26
- `linear()` timing function enables CSS springs

**Source**: [motion.dev](https://motion.dev/), [GSAP License](https://gsap.com/licensing/), [Lenis](https://lenis.studiofreight.com/)

## React: Motion (Framer Motion)

### Basic Usage

```jsx
import { motion, AnimatePresence } from 'motion/react';

function Component({ isVisible }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        />
      )}
    </AnimatePresence>
  );
}
```

### Production Gotchas

| Trap | What Happens | Fix |
|------|--------------|-----|
| Exit animations don't run | Elements unmount immediately | Wrap in `AnimatePresence` |
| Layout shift on animate | Other elements jump | Use `layout` prop |
| Hydration mismatch | Server/client differ | Use `initial={false}` |
| Heavy on mobile | Jank on old devices | Reduce complexity, use CSS |

### Spring Physics

```jsx
// Natural, responsive
<motion.div animate={{ x: 100 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }} />

// Quick, snappy
<motion.div animate={{ x: 100 }} transition={{ type: 'spring', stiffness: 500, damping: 25 }} />

// Bouncy
<motion.div animate={{ x: 100 }} transition={{ type: 'spring', stiffness: 200, damping: 10 }} />
```

**Source**: [Motion React Docs](https://motion.dev/docs/react-quick-start)

## Svelte: Built-in Motion

### spring vs tweened

| Use Case | Choice | Why |
|----------|--------|-----|
| Following cursor/input | `spring` | Natural physics response |
| Dragging elements | `spring` | Momentum feels right |
| Progress bars | `tweened` | Predictable timing |
| Counter animations | `tweened` | Controlled duration |

```svelte
<script>
  import { spring, tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';

  // Physics-based
  let position = spring({ x: 0, y: 0 }, { stiffness: 0.1, damping: 0.5 });

  // Time-based
  let progress = tweened(0, { duration: 400, easing: cubicOut });
</script>
```

### Spring Configurations

| Feel | stiffness | damping | Use |
|------|-----------|---------|-----|
| Sluggish | 0.05 | 0.5 | UI panels |
| Normal | 0.15 | 0.8 | Default |
| Snappy | 0.3 | 0.6 | Buttons |
| Bouncy | 0.2 | 0.3 | Playful |

### Svelte Transitions

```svelte
<script>
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  let visible = $state(true);
</script>

{#if visible}
  <div in:fly={{ y: 50, duration: 400, easing: cubicOut }} out:fade>
    Content
  </div>
{/if}
```

| Trap | What Happens | Fix |
|------|--------------|-----|
| Transition on mount | Nothing animates | Use `in:` or wrap in `{#if}` |
| Heavy `blur()` | Jank on mobile | Use `opacity` + `transform` only |
| Missing `easing` | Uses linear (looks wrong) | Import from `svelte/easing` |

**Source**: [Svelte Motion](https://svelte.dev/docs/svelte/svelte-motion), [Svelte Transitions](https://svelte.dev/docs/svelte/transition)

## GSAP (Both Frameworks)

### Setup & Cleanup

```javascript
// React
import { useEffect, useRef } from 'react';
import gsap from 'gsap';

function Component() {
  const ref = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(ref.current, { y: 50, opacity: 0, duration: 0.8 });
    });
    return () => ctx.revert(); // REQUIRED
  }, []);

  return <div ref={ref}>Content</div>;
}
```

```svelte
<!-- Svelte -->
<script>
  import { onMount } from 'svelte';
  import { gsap } from 'gsap';

  let element;

  onMount(() => {
    const ctx = gsap.context(() => {
      gsap.from(element, { y: 50, opacity: 0, duration: 0.8 });
    });
    return () => ctx.revert(); // REQUIRED
  });
</script>

<div bind:this={element}>Content</div>
```

### Timeline Pattern

```javascript
const tl = gsap.timeline();

tl.from('.title', { y: 50, opacity: 0, duration: 0.6 })
  .from('.subtitle', { y: 30, opacity: 0, duration: 0.4 }, '-=0.3')  // overlap
  .from('.content', { y: 20, opacity: 0, duration: 0.4 }, '-=0.2');
```

### Stagger Pattern

```javascript
gsap.from('.item', {
  y: 30,
  opacity: 0,
  duration: 0.5,
  stagger: 0.1,  // 100ms between each
  ease: 'power2.out'
});
```

### Common Easings

| Ease | Feel | Use |
|------|------|-----|
| `power2.out` | Smooth decel | Most animations |
| `power3.out` | Stronger decel | Hero reveals |
| `back.out(1.7)` | Overshoot | Buttons, cards |
| `elastic.out(1, 0.3)` | Bouncy | Playful |
| `none` | Linear | Progress, loading |

**Source**: [GSAP Docs](https://gsap.com/docs/v3/), [GSAP Ease Visualizer](https://gsap.com/docs/v3/Eases/)

## CSS Animations

### Performance Rules

**Animate only (GPU-accelerated):**
- `transform` (translate, scale, rotate)
- `opacity`

**Never animate (triggers layout):**
- `width`, `height`
- `top`, `left`, `right`, `bottom`
- `margin`, `padding`

### CSS Springs with linear()

```css
/* CSS spring approximation */
.spring {
  transition: transform 500ms linear(
    0, 0.006, 0.025, 0.057, 0.103, 0.163, 0.236, 0.319,
    0.41, 0.506, 0.604, 0.702, 0.796, 0.883, 0.962,
    1.029, 1.083, 1.123, 1.147, 1.154, 1.145, 1.121,
    1.085, 1.04, 0.99, 0.938, 0.888, 0.844, 0.807,
    0.78, 0.763, 0.757, 0.761, 0.775, 0.797, 0.825,
    0.857, 0.891, 0.924, 0.955, 0.983, 1.005, 1.023,
    1.036, 1.043, 1.045, 1.042, 1.034, 1.023, 1.008, 1
  );
}
```

**Source**: [linear() easing generator](https://linear-easing-generator.netlify.app/)

### Scroll-Driven Animations (CSS)

```css
@supports (animation-timeline: scroll()) {
  .parallax {
    animation: parallax linear both;
    animation-timeline: scroll();
  }

  @keyframes parallax {
    from { transform: translateY(0); }
    to { transform: translateY(-100px); }
  }

  .reveal {
    animation: reveal linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }

  @keyframes reveal {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
  }
}
```

**Source**: [MDN Scroll-driven Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations)

## View Transitions API

```javascript
// Basic usage (Baseline Oct 2025)
document.startViewTransition(() => {
  updateDOM();
});

// With async
document.startViewTransition(async () => {
  await fetchData();
  updateDOM();
});
```

```css
/* Customize transition */
::view-transition-old(root) {
  animation: fade-out 300ms ease-out;
}

::view-transition-new(root) {
  animation: fade-in 300ms ease-out;
}
```

**Source**: [Chrome View Transitions](https://developer.chrome.com/docs/web-platform/view-transitions)

## Easing Selection

| Context | Easing | Why |
|---------|--------|-----|
| Enter screen | `ease-out` / `power2.out` | Decelerates into view |
| Exit screen | `ease-in` | Accelerates away |
| Hover state | `ease-in-out` | Bidirectional |
| Spring/bouncy | `back.out` or spring physics | Overshoot feels alive |
| Progress/loading | `linear` | Predictable |

## Timing Guidelines

| Context | Duration | Rationale |
|---------|----------|-----------|
| Micro-feedback (hover, press) | 100-200ms | Immediate response |
| UI state changes | 200-400ms | Noticeable but not slow |
| Page transitions | 300-500ms | Allow orientation |
| Reveals/entrances | 400-800ms | Dramatic effect |
| Complex sequences | 800-1500ms | Narrative pacing |

**The 300-500ms sweet spot**: Long enough to notice, short enough not to annoy.

## Accessibility

### prefers-reduced-motion

```css
/* No-motion-first approach (better than nuclear removal) */
.animated {
  /* Default: no animation */
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: no-preference) {
  .animated {
    animation: fade-in 400ms ease-out;
  }
}
```

```javascript
// JS detection
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  gsap.from('.hero', { y: 50, opacity: 0 });
}
```

**Never completely remove**: Reduce intensity, keep essential feedback.

**Source**: [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

## Performance

### Compositor-Only Properties

Only these run on the GPU without layout:
- `transform`
- `opacity`
- `filter` (with care)

### Layout Thrashing

```javascript
// BAD: interleaved reads/writes
elements.forEach(el => {
  const height = el.offsetHeight; // read
  el.style.height = height + 10 + 'px'; // write
});

// GOOD: batch reads, then writes
const heights = elements.map(el => el.offsetHeight); // all reads
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // all writes
});
```

### will-change Usage

```css
/* Use sparingly - creates GPU layer */
.will-animate {
  will-change: transform;
}

/* Remove after animation */
.finished {
  will-change: auto;
}
```

**Warning**: Overuse causes memory issues on mobile.

## Sources

- [Motion (Framer Motion)](https://motion.dev/)
- [GSAP Docs](https://gsap.com/docs/v3/)
- [Svelte Motion](https://svelte.dev/docs/svelte/svelte-motion)
- [Web Animations Performance](https://web.dev/articles/animations-guide)
- [CSS Easing Functions](https://easings.net/)
- [Josh Comeau Animation Guide](https://www.joshwcomeau.com/animation/css-transitions/)
