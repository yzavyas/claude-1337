# CSS Reference

Modern CSS patterns for experience engineering.

---

## Layout Systems

### Grid

```css
/* Auto-fit responsive grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1rem;
}

/* Named areas for complex layouts */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
}
```

### Flexbox

```css
/* Center anything */
.center {
  display: flex;
  place-items: center;
}

/* Space between with wrap */
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
}
```

### When to Use Which

| Layout | Use |
|--------|-----|
| Grid | 2D layouts, complex arrangements |
| Flexbox | 1D alignment, distribution |
| Both | Grid for page, flex for components |

---

## Container Queries

Style based on container size, not viewport:

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

**Why container queries:**
- Components don't know their context
- Viewport queries break in sidebars
- True component encapsulation

---

## Custom Properties

### Design Tokens

```css
:root {
  /* Primitives */
  --color-blue-500: oklch(60% 0.15 250);
  --space-4: 1rem;
  --font-size-base: 1rem;

  /* Semantic */
  --color-primary: var(--color-blue-500);
  --space-component: var(--space-4);

  /* Component */
  --button-bg: var(--color-primary);
}
```

### Dynamic Values

```css
.progress {
  --progress: 0;
  background: linear-gradient(
    to right,
    var(--color-primary) calc(var(--progress) * 1%),
    transparent calc(var(--progress) * 1%)
  );
}
```

Set via JS: `element.style.setProperty('--progress', 75)`

---

## Modern Selectors

### :has() (Parent Selector)

```css
/* Style parent based on child */
.card:has(img) {
  padding: 0;
}

/* Form validation */
.field:has(input:invalid) {
  border-color: var(--color-error);
}

/* Sibling awareness */
.card:has(+ .card) {
  margin-bottom: 1rem;
}
```

### :is() and :where()

```css
/* Group selectors (specificity preserved) */
:is(h1, h2, h3):hover {
  color: var(--color-primary);
}

/* Group selectors (zero specificity) */
:where(h1, h2, h3) {
  margin-bottom: 1em;
}
```

### :focus-visible

```css
/* Keyboard focus only, not click */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none;
}
```

---

## CSS Layers

Control specificity order:

```css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; box-sizing: border-box; }
}

@layer base {
  body { font-family: system-ui; }
}

@layer components {
  .button { /* component styles */ }
}

@layer utilities {
  .hidden { display: none !important; }
}
```

**Why layers:**
- Predictable cascade
- Third-party CSS control
- No specificity wars

---

## Logical Properties

Write direction-agnostic CSS:

| Physical | Logical |
|----------|---------|
| `margin-left` | `margin-inline-start` |
| `padding-top` | `padding-block-start` |
| `width` | `inline-size` |
| `height` | `block-size` |
| `top` | `inset-block-start` |

```css
.sidebar {
  inline-size: 300px;
  padding-inline: 1rem;
  border-inline-end: 1px solid var(--border);
}
```

---

## Animation Performance

### Compositor Properties

Only animate these for 60fps:

```css
/* Good - compositor only */
.animate {
  transform: translateX(100px);
  opacity: 0.5;
}

/* Bad - triggers layout/paint */
.animate {
  left: 100px; /* layout */
  width: 200px; /* layout */
  background: red; /* paint */
}
```

### will-change

```css
/* Use sparingly - consumes GPU memory */
.will-animate {
  will-change: transform, opacity;
}

/* Remove after animation */
.animated {
  will-change: auto;
}
```

---

## Scroll Behavior

### Smooth Scroll

```css
html {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
```

### Scroll Snap

```css
.carousel {
  scroll-snap-type: x mandatory;
  overflow-x: scroll;
}

.carousel-item {
  scroll-snap-align: start;
}
```

**Caution:** `mandatory` with tall content can trap users.

### Scroll-Driven Animations (2025)

```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

---

## Dark Mode

```css
:root {
  --bg: oklch(98% 0 0);
  --text: oklch(20% 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: oklch(15% 0 0);
    --text: oklch(90% 0 0);
  }
}
```

**Dark mode tips:**
- Don't use pure black (`oklch(0% 0 0)`)
- Reduce saturation in dark mode
- Test contrast ratios both ways

---

## Responsive Patterns

### Fluid Typography

```css
/* Never pure vw (fails WCAG 1.4.4) */
h1 {
  font-size: clamp(1.5rem, 1rem + 2vw, 3rem);
}
```

### Fluid Spacing

```css
:root {
  --space-m: clamp(1rem, 0.5rem + 2vw, 2rem);
}
```

### Container-Based Sizing

```css
.container {
  --content-width: min(65ch, 100% - 2rem);
  width: var(--content-width);
  margin-inline: auto;
}
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `100vh` on mobile | Use `100dvh` or JS |
| `z-index: 9999` | Use CSS layers or stacking context |
| `!important` everywhere | Fix specificity with layers |
| `@media` for everything | Use container queries |
| Physical properties | Use logical properties |
| `px` for spacing | Use `rem` for accessibility |

---

## Sources

- CSS Working Group Drafts [W3C 2025]
- web.dev CSS guides [Google 2025]
- Every Layout [Heydon & Andy 2024]
- Modern CSS Solutions [Stephanie Eckles 2024]
