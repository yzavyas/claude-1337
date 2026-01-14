# Color Systems

Production color patterns for web experiences.

## OKLCH: The Modern Standard

OKLCH (Oklch Lightness Chroma Hue) is perceptually uniform—changes in values match how eyes perceive shifts.

### Why OKLCH Over HSL

| Problem with HSL | OKLCH Solution |
|------------------|----------------|
| Yellow appears lighter than blue at same "lightness" | Consistent perceived lightness across hues |
| Muddy gradients between certain hues | Smooth gradients without gray middle |
| Unpredictable contrast | Predictable contrast when shifting hues |
| Limited to sRGB | Supports P3 displays |

### Syntax

```css
/* OKLCH: Lightness (0-100%), Chroma (0-0.4), Hue (0-360) */
color: oklch(70% 0.15 240);

/* With fallback for older browsers */
.element {
  color: rgb(59, 130, 246);  /* Fallback */
  color: oklch(61% 0.18 250);
}

/* With alpha */
color: oklch(70% 0.15 240 / 50%);
```

### Generating Palettes

Same lightness across hues = consistent visual hierarchy:

```css
:root {
  /* All at 60% lightness, 0.2 chroma */
  --color-red: oklch(60% 0.2 25);
  --color-orange: oklch(60% 0.2 50);
  --color-yellow: oklch(60% 0.2 90);
  --color-green: oklch(60% 0.2 145);
  --color-blue: oklch(60% 0.2 250);
  --color-purple: oklch(60% 0.2 300);
}
```

### Browser Support

92%+ support in 2025. Use fallbacks for older browsers.

**Source**: [OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)

## Accessible Color Systems

### Contrast Requirements

| Level | Ratio | Use |
|-------|-------|-----|
| WCAG AA (normal text) | 4.5:1 | Minimum for body text |
| WCAG AA (large text) | 3:1 | Headings 18pt+ |
| WCAG AAA (normal text) | 7:1 | Enhanced accessibility |
| WCAG AA (UI components) | 3:1 | Buttons, inputs |

### Stripe's Methodology

Stripe used CIELAB color space for perceptual uniformity:

1. None of their default text colors (except black) met 4.5:1
2. Solution: Manipulate colors in perceptual space
3. Key insight: "Really dark yellow" isn't perceivable
4. By shifting both background and text uniformly, maintain contrast across all badge colors

**Source**: [Stripe Accessible Color Systems](https://stripe.com/blog/accessible-color-systems)

### Practical Palette Generation

```css
:root {
  /* Light mode */
  --text-primary: oklch(20% 0 0);      /* Near black */
  --text-secondary: oklch(40% 0 0);    /* Dark gray */
  --text-tertiary: oklch(55% 0 0);     /* Medium gray */
  --bg-primary: oklch(99% 0 0);        /* Near white */
  --bg-secondary: oklch(96% 0 0);      /* Light gray */
  --bg-tertiary: oklch(92% 0 0);       /* Lighter gray */
}

/* Verify contrast programmatically */
```

## Dark Mode

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Pure black (#000000) | Harsh, tiring | Use #0a0a0a or #121212 |
| Pure white text (#FFFFFF) | Halo effect | Use #E0E0E0 or lighter gray |
| Same saturation as light mode | Eye strain | Desaturate colors |
| Same line height | Text feels cramped | Increase slightly |

### Production Patterns

```css
:root {
  --surface-1: oklch(12% 0 0);   /* Darkest */
  --surface-2: oklch(16% 0 0);   /* Cards */
  --surface-3: oklch(20% 0 0);   /* Elevated */
  --surface-4: oklch(24% 0 0);   /* Highest */

  --text-primary: oklch(92% 0 0);
  --text-secondary: oklch(70% 0 0);
  --text-tertiary: oklch(50% 0 0);
}
```

### Elevation Through Lightness

Linear's approach: Create depth with lightness, not color variety.

```css
/* Surface hierarchy */
.card { background: var(--surface-2); }
.card:hover { background: var(--surface-3); }
.modal { background: var(--surface-3); }
.tooltip { background: var(--surface-4); }
```

### Desaturation Rule

Reduce chroma for dark mode to prevent eye strain:

```css
/* Light mode */
--brand: oklch(60% 0.25 250);

/* Dark mode - reduce chroma */
--brand: oklch(65% 0.18 250);
```

## Color Tokens

### Three-Layer Architecture

```
primitives → semantic aliases → component slots
```

```css
/* Layer 1: Primitives (raw values) */
:root {
  --blue-50: oklch(97% 0.02 250);
  --blue-100: oklch(93% 0.05 250);
  --blue-500: oklch(60% 0.2 250);
  --blue-900: oklch(25% 0.1 250);
}

/* Layer 2: Semantic aliases */
:root {
  --color-brand-primary: var(--blue-500);
  --color-brand-subtle: var(--blue-100);
  --color-text-primary: var(--gray-900);
  --color-text-secondary: var(--gray-600);
}

/* Layer 3: Component slots */
:root {
  --button-bg-default: var(--color-brand-primary);
  --button-bg-hover: var(--color-brand-dark);
  --button-text: var(--color-text-inverse);
}
```

Components reference slots, slots reference semantics, semantics reference primitives. Themes change layer 2, not layer 1 or 3.

## Gradients

### OKLCH Gradients

No muddy middle colors:

```css
/* HSL: muddy brown in middle */
.gradient-hsl {
  background: linear-gradient(to right, blue, yellow);
}

/* OKLCH: clean transition */
.gradient-oklch {
  background: linear-gradient(
    to right in oklch,
    oklch(60% 0.2 250),
    oklch(85% 0.2 90)
  );
}
```

### Interpolation Control

```css
.gradient {
  background: linear-gradient(
    to right in oklch longer hue,  /* Go the long way around the color wheel */
    oklch(60% 0.2 30),
    oklch(60% 0.2 60)
  );
}
```

## Brand Color Integration

### Surgical Accent (Linear's Approach)

- Monochrome foundation (grays only)
- Bold color as accent only
- Color draws attention to what matters

```css
:root {
  /* Foundation: grayscale */
  --bg: oklch(10% 0 0);
  --surface: oklch(15% 0 0);
  --text: oklch(90% 0 0);
  --text-muted: oklch(60% 0 0);
  --border: oklch(25% 0 0);

  /* Accent: used sparingly */
  --accent: oklch(70% 0.2 250);
  --accent-hover: oklch(75% 0.22 250);
}
```

### Where to Use Accent

- Primary CTA buttons
- Links
- Active/selected states
- Important indicators
- **Not** decorative elements

## P3 Wide Gamut

Modern displays support more vibrant colors.

```css
/* Check support */
@media (color-gamut: p3) {
  .vibrant {
    --brand: oklch(70% 0.3 250);  /* Higher chroma */
  }
}

/* color() function for explicit P3 */
.p3-color {
  color: rgb(0, 100, 255);  /* Fallback */
  color: color(display-p3 0 0.4 1);
}
```

## Tools

| Tool | Use |
|------|-----|
| [OKLCH Color Picker](https://oklch.com/) | Generate colors |
| [Contrast Checker](https://webaim.org/resources/contrastchecker/) | Verify accessibility |
| [Realtime Colors](https://realtimecolors.com/) | Preview palettes |
| [Huetone](https://huetone.ardov.me/) | Build accessible palettes |

## Sources

- [OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- [Stripe Accessible Color Systems](https://stripe.com/blog/accessible-color-systems)
- [MDN OKLCH](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)
- [Dark Mode Design](https://www.smashingmagazine.com/2025/04/inclusive-dark-mode-designing-accessible-dark-themes/)
