# Typography

Production typography patterns for web experiences.

## Fluid Typography

### The clamp() Approach

No breakpoints. Smooth scaling across all viewport sizes.

```css
/* Base scale */
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.15vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.2vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.35vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.3rem + 0.75vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.8rem + 1.5vw, 3.5rem);
}

/* Usage */
h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
p { font-size: var(--text-base); }
```

### Accessibility Warning

Pure `vw` units fail WCAG 1.4.4 (200% zoom test). Always use `clamp()` with rem bounds.

```css
/* BAD: Can't zoom */
h1 { font-size: 5vw; }

/* GOOD: Respects user zoom */
h1 { font-size: clamp(2rem, 5vw, 4rem); }
```

**Source**: [Fluid Type Scale Calculator](https://www.fluid-type-scale.com/)

## System Font Stacks

Zero download, instant render.

```css
/* Simple modern */
font-family: system-ui, sans-serif;

/* Comprehensive sans-serif */
font-family:
  -apple-system, BlinkMacSystemFont,
  'Segoe UI', 'Noto Sans',
  Helvetica, Arial, sans-serif,
  'Apple Color Emoji', 'Segoe UI Emoji';

/* Monospace */
font-family:
  ui-monospace, 'Cascadia Code', 'Source Code Pro',
  Menlo, Consolas, 'DejaVu Sans Mono', monospace;

/* Serif */
font-family:
  'Iowan Old Style', 'Palatino Linotype',
  'URW Palladio L', P052, serif;
```

### Modern Font Stacks Categories

| Category | Stack | Feel |
|----------|-------|------|
| Neo-Grotesque | `Inter, Roboto, 'Helvetica Neue', Arial` | Clean, modern |
| Humanist | `Seravek, 'Gill Sans Nova', Ubuntu, Calibri` | Friendly, readable |
| Geometric | `Avenir, Montserrat, 'Century Gothic'` | Precise, modern |
| Classical | `Optima, Candara, 'Noto Sans'` | Elegant |
| Transitional | `Charter, 'Bitstream Charter', 'Sitka Text'` | Book-like |

**Source**: [Modern Font Stacks](https://modernfontstacks.com/)

## Variable Fonts

Single file, multiple weights/widths.

### Benefits

- Single font file for all weights
- Animatable properties
- Smaller total download than multiple files
- No FOUT between weights

### Usage

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

/* Use any weight */
.light { font-weight: 300; }
.regular { font-weight: 400; }
.medium { font-weight: 500; }
.bold { font-weight: 700; }

/* Animate weight */
.hover-effect {
  font-weight: 400;
  transition: font-weight 200ms;
}
.hover-effect:hover {
  font-weight: 600;
}
```

### Popular Variable Fonts

| Font | Axes | Use |
|------|------|-----|
| Inter | weight | UI, interfaces |
| Geist | weight | Modern apps |
| Source Sans 3 | weight | Body text |
| Fraunces | weight, opsz | Display, editorial |
| Recursive | weight, slant, mono | Code + prose |

**Source**: [Variable Fonts Guide](https://web.dev/articles/variable-fonts)

## Type Scale

### Modular Scales

| Ratio | Name | Use |
|-------|------|-----|
| 1.125 | Major Second | Compact UI |
| 1.200 | Minor Third | Default |
| 1.250 | Major Third | Spacious |
| 1.333 | Perfect Fourth | Editorial |
| 1.414 | Augmented Fourth | Dramatic |
| 1.618 | Golden Ratio | Display |

```css
/* Minor Third (1.2) scale */
:root {
  --scale-ratio: 1.2;
  --text-base: 1rem;
  --text-sm: calc(var(--text-base) / var(--scale-ratio));
  --text-lg: calc(var(--text-base) * var(--scale-ratio));
  --text-xl: calc(var(--text-lg) * var(--scale-ratio));
  --text-2xl: calc(var(--text-xl) * var(--scale-ratio));
}
```

**Source**: [Type Scale](https://typescale.com/)

## Line Height

### Context-Based Line Height

| Context | Line Height | Why |
|---------|-------------|-----|
| Body text | 1.5-1.7 | Readability |
| Large headings | 1.1-1.2 | Tight, impactful |
| Small headings | 1.2-1.3 | Balanced |
| Captions/UI | 1.3-1.4 | Compact |
| Code | 1.4-1.5 | Scannable |

```css
h1 { line-height: 1.1; }
h2, h3 { line-height: 1.2; }
p { line-height: 1.6; }
code { line-height: 1.5; }
```

### Dark Mode Adjustment

Increase line height slightly on dark backgrounds—text feels more cramped.

```css
@media (prefers-color-scheme: dark) {
  p { line-height: 1.7; }  /* vs 1.6 in light */
}
```

## Letter Spacing

### Context-Based Tracking

| Context | Tracking | Why |
|---------|----------|-----|
| Large headings | -0.02em to -0.01em | Tighten, more impactful |
| Body text | 0 (default) | Natural |
| All caps | 0.05em to 0.1em | Improve legibility |
| Small text | 0.01em | Slight opening |

```css
h1 {
  letter-spacing: -0.02em;
  text-transform: none;
}

.all-caps {
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

## Measure (Line Length)

Optimal reading: 45-75 characters per line.

```css
p {
  max-width: 65ch;  /* character units */
}

article {
  max-width: 70ch;
  margin-inline: auto;
}
```

## Font Loading

### font-display Strategies

| Value | Behavior | Use |
|-------|----------|-----|
| `swap` | Fallback shown immediately, swap when loaded | Most cases |
| `optional` | Only use if cached, skip otherwise | Performance-critical |
| `fallback` | Brief block, then fallback, late swap | Balance |

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.woff2') format('woff2');
  font-display: swap;  /* Best default */
}
```

### Preloading Critical Fonts

```html
<link
  rel="preload"
  href="/fonts/Inter-Variable.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### Subsetting

Reduce font file size by including only needed characters.

```bash
# Using glyphhanger
glyphhanger --whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" \
  --subset="Inter.ttf" --formats=woff2
```

## Responsive Typography Tips

### Don't Just Scale Down

| Element | Mobile | Desktop |
|---------|--------|---------|
| H1 | 2rem | 3.5rem |
| Body | 1rem | 1rem (same!) |
| Line height | 1.6 | 1.5 |
| Measure | 45ch | 65ch |

Body text rarely needs to change size. Headings do.

### Mobile Readability

- Minimum 16px body text (prevents iOS zoom)
- Increase touch targets, not just text
- Consider thumb zones for interactive text

## Vercel Geist Typography

Production example from a leading design system.

### Principles

- High x-height for legibility
- Short descenders for compact line spacing
- Angular stroke terminals for distinction
- 10 weights from hairline to black

### Implementation

```css
:root {
  --font-geist-sans: 'Geist', system-ui, sans-serif;
  --font-geist-mono: 'Geist Mono', ui-monospace, monospace;
}
```

**Source**: [Vercel Geist](https://vercel.com/font)

## Sources

- [Fluid Type Scale Calculator](https://www.fluid-type-scale.com/)
- [Modern Font Stacks](https://modernfontstacks.com/)
- [Variable Fonts Guide](https://web.dev/articles/variable-fonts)
- [Type Scale](https://typescale.com/)
- [Vercel Geist Font](https://vercel.com/font)
- [The Elements of Typographic Style](https://en.wikipedia.org/wiki/The_Elements_of_Typographic_Style)
