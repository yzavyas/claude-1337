# Design Systems

Production patterns for CSS architecture and design tokens.

## Tooling Decision

| Approach | Use When | Trade-off |
|----------|----------|-----------|
| Tailwind CSS | Rapid development, utility-first | HTML verbosity, learning curve |
| vanilla-extract | TypeScript-first, type-safe tokens | Build setup, less dynamic |
| Panda CSS | Tailwind-like + CSS-in-JS | Newer ecosystem |
| CSS Modules | Simple scoping | Less powerful theming |
| Plain CSS + Custom Properties | Small projects, max control | Manual organization |

### Runtime CSS-in-JS: Avoid

styled-components, Emotion with runtime: Performance cost on every render.

**Zero-runtime alternatives**: vanilla-extract, Linaria, Panda CSS.

## Design Tokens

### Three-Layer Architecture

```
primitives → semantic aliases → component slots
```

| Layer | Contains | Example |
|-------|----------|---------|
| Primitives | Raw values | `--color-blue-500: #3b82f6` |
| Semantic | Meaningful aliases | `--color-brand-primary: var(--color-blue-500)` |
| Component | Specific uses | `--button-bg: var(--color-brand-primary)` |

### Implementation

```css
/* Layer 1: Primitives */
:root {
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  --color-gray-50: oklch(98% 0 0);
  --color-gray-100: oklch(95% 0 0);
  --color-gray-900: oklch(15% 0 0);

  --color-blue-500: oklch(60% 0.2 250);
}

/* Layer 2: Semantic */
:root {
  --color-bg: var(--color-gray-50);
  --color-surface: var(--color-gray-100);
  --color-text: var(--color-gray-900);
  --color-brand: var(--color-blue-500);

  --spacing-tight: var(--space-2);
  --spacing-normal: var(--space-4);
  --spacing-loose: var(--space-8);
}

/* Layer 3: Component */
:root {
  --card-padding: var(--spacing-normal);
  --card-bg: var(--color-surface);
  --button-padding-x: var(--spacing-normal);
  --button-padding-y: var(--spacing-tight);
}
```

### Theming

Change layer 2, components adapt automatically:

```css
[data-theme="dark"] {
  --color-bg: var(--color-gray-900);
  --color-surface: var(--color-gray-800);
  --color-text: var(--color-gray-50);
}
```

## Tailwind CSS

### Production Setup

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx,svelte}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: 'oklch(60% 0.2 250)',
          light: 'oklch(75% 0.15 250)',
          dark: 'oklch(45% 0.2 250)',
        }
      },
      fontFamily: {
        sans: ['Inter var', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'ui-monospace', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}
```

### Tailwind 4 Changes

- CSS-first configuration
- Built on Lightning CSS
- No more `tailwind.config.js` required
- Theme in `@theme` directive

```css
/* Tailwind 4 */
@import 'tailwindcss';

@theme {
  --color-brand: oklch(60% 0.2 250);
  --font-family-sans: 'Inter var', system-ui, sans-serif;
}
```

### Avoiding Verbosity

```jsx
// BAD: Long class strings everywhere
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">

// GOOD: Extract to components
<Card variant="elevated">
```

## CSS Layers

Control specificity without `!important`.

```css
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
  }
}

@layer base {
  body {
    font-family: system-ui;
    line-height: 1.5;
  }
}

@layer components {
  .card {
    padding: var(--spacing-normal);
    background: var(--color-surface);
  }
}

@layer utilities {
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
  }
}
```

Later layers override earlier layers, regardless of source order.

## Container Queries

Component-based responsive design.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container card (min-width: 400px) {
  .card {
    grid-template-columns: 1fr 2fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 1fr 3fr;
  }
}
```

### Container Query Units

```css
.card-title {
  font-size: clamp(1rem, 3cqi, 1.5rem);  /* cqi = container inline size */
}
```

## Spacing System

### 8-Point Grid

```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
}
```

### Usage Patterns

| Context | Token | Why |
|---------|-------|-----|
| Inline text spacing | `--space-1` | Subtle |
| Form input padding | `--space-2` to `--space-3` | Comfortable |
| Card padding | `--space-4` to `--space-6` | Breathable |
| Section spacing | `--space-12` to `--space-16` | Chunking |

## Shadow System

### Elevation Layers

```css
:root {
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 5%);
  --shadow-md: 0 4px 6px oklch(0% 0 0 / 7%), 0 2px 4px oklch(0% 0 0 / 5%);
  --shadow-lg: 0 10px 15px oklch(0% 0 0 / 10%), 0 4px 6px oklch(0% 0 0 / 5%);
  --shadow-xl: 0 20px 25px oklch(0% 0 0 / 10%), 0 10px 10px oklch(0% 0 0 / 4%);
}
```

### Layered Shadows

More realistic than single shadows:

```css
.card {
  box-shadow:
    0 1px 1px oklch(0% 0 0 / 4%),
    0 2px 2px oklch(0% 0 0 / 4%),
    0 4px 4px oklch(0% 0 0 / 4%),
    0 8px 8px oklch(0% 0 0 / 4%);
}
```

### Colored Shadows

```css
.brand-button {
  box-shadow: 0 4px 14px oklch(60% 0.2 250 / 40%);
}
```

## Border Radius

### System

```css
:root {
  --radius-sm: 0.25rem;  /* 4px - subtle */
  --radius-md: 0.5rem;   /* 8px - default */
  --radius-lg: 1rem;     /* 16px - prominent */
  --radius-xl: 1.5rem;   /* 24px - large cards */
  --radius-full: 9999px; /* Pills, avatars */
}
```

### Nested Radius

Inner radius should be outer radius minus padding:

```css
.card {
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.card-inner {
  /* radius-lg (1rem) - space-4 (1rem) = 0, or use smaller radius */
  border-radius: var(--radius-sm);
}
```

## Production Examples

### Linear

- Monochrome foundation
- LCH color space for themes
- Elevation through opacity
- Minimal color variety

### Vercel Geist

- Purpose-built Geist font family
- Tailwind-consumable tokens
- Coordinated type/space scales

### Stripe

- Perceptually uniform color (CIELAB)
- Custom accessibility tooling
- Three-layer token architecture

## Sources

- [Design Tokens Guide](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [CSS Cascade Layers](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_layers)
- [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)
