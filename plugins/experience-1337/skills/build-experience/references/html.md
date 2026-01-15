# HTML Reference

Semantic structure, accessibility, and document architecture.

---

## Semantic Structure

**Use semantic elements.** Not just for accessibility - for maintainability and SEO.

| Element | Use | Not |
|---------|-----|-----|
| `<header>` | Page/section header | Generic container |
| `<nav>` | Navigation links | Any link group |
| `<main>` | Primary content (one per page) | Wrapper div |
| `<article>` | Self-contained content | Any section |
| `<section>` | Thematic grouping | Generic container |
| `<aside>` | Tangentially related | Sidebar styling |
| `<footer>` | Page/section footer | Bottom content |

**Why semantics matter:**
- Screen readers navigate by landmarks
- Search engines understand structure
- Future maintainers understand intent
- CSS hooks without class soup

---

## Document Outline

```html
<body>
  <header>
    <nav aria-label="Main">...</nav>
  </header>

  <main>
    <article>
      <header>
        <h1>Page Title</h1>
      </header>
      <section aria-labelledby="section-1">
        <h2 id="section-1">Section</h2>
      </section>
    </article>
  </main>

  <footer>...</footer>
</body>
```

**Heading hierarchy:** Never skip levels. `h1` → `h2` → `h3`, not `h1` → `h3`.

---

## Accessibility (ARIA)

### Landmarks

Screen readers use landmarks for navigation:

| Role | Element | ARIA |
|------|---------|------|
| banner | `<header>` (top-level) | `role="banner"` |
| navigation | `<nav>` | `role="navigation"` |
| main | `<main>` | `role="main"` |
| complementary | `<aside>` | `role="complementary"` |
| contentinfo | `<footer>` (top-level) | `role="contentinfo"` |

**Prefer native semantics.** Only add ARIA when HTML can't express it.

### Labels

```html
<!-- Visible label -->
<nav aria-labelledby="nav-label">
  <h2 id="nav-label">Main Navigation</h2>
</nav>

<!-- Invisible label -->
<nav aria-label="Main">...</nav>

<!-- Described by -->
<input aria-describedby="hint">
<p id="hint">Password must be 8+ characters</p>
```

### Live Regions

For dynamic content updates:

```html
<!-- Polite: announced when user is idle -->
<div aria-live="polite" aria-atomic="true">
  Status: Saved
</div>

<!-- Assertive: announced immediately (use sparingly) -->
<div aria-live="assertive">
  Error: Connection lost
</div>
```

### States and Properties

| Attribute | Use |
|-----------|-----|
| `aria-expanded` | Collapsible sections, menus |
| `aria-selected` | Tabs, listboxes |
| `aria-pressed` | Toggle buttons |
| `aria-hidden` | Hide from assistive tech (not visual) |
| `aria-disabled` | Disabled but focusable |
| `aria-busy` | Loading states |

---

## Interactive Patterns

### Buttons vs Links

| Element | Use |
|---------|-----|
| `<button>` | Actions (submit, toggle, open modal) |
| `<a href>` | Navigation (goes somewhere) |

**Never:**
- `<div onclick>` for buttons
- `<a href="#">` for actions
- `<button>` for navigation

### Focus Management

```html
<!-- Skip link -->
<a href="#main" class="skip-link">Skip to content</a>

<!-- Focus trap for modals -->
<div role="dialog" aria-modal="true">
  <!-- First and last focusable elements trap focus -->
</div>
```

**Focus order:** DOM order = tab order. Don't break this with `tabindex > 0`.

### Keyboard Support

| Pattern | Keys |
|---------|------|
| Buttons | Enter, Space |
| Links | Enter |
| Tabs | Arrow keys, Home, End |
| Menus | Arrow keys, Escape |
| Dialogs | Escape to close |

---

## Forms

### Labels

```html
<!-- Explicit association -->
<label for="email">Email</label>
<input id="email" type="email">

<!-- Implicit (wrapping) -->
<label>
  Email
  <input type="email">
</label>
```

**Every input needs a label.** No exceptions.

### Validation

```html
<input
  type="email"
  required
  aria-invalid="true"
  aria-describedby="email-error"
>
<p id="email-error" role="alert">Please enter a valid email</p>
```

### Input Types

Use correct types for mobile keyboards and validation:

| Type | Keyboard | Validation |
|------|----------|------------|
| `email` | @ key | Email format |
| `tel` | Number pad | None |
| `url` | .com key | URL format |
| `number` | Number pad | Numeric |
| `date` | Date picker | Date format |

---

## Images

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 40% in Q4">

<!-- Decorative image -->
<img src="decoration.png" alt="" role="presentation">

<!-- Complex image -->
<figure>
  <img src="diagram.png" alt="System architecture">
  <figcaption>
    Detailed description of the architecture...
  </figcaption>
</figure>
```

**Alt text guidelines:**
- Describe function, not appearance
- Be concise (125 chars guideline)
- Empty alt for decorative images
- Never "image of" or "picture of"

---

## Tables

```html
<table>
  <caption>Quarterly Sales</caption>
  <thead>
    <tr>
      <th scope="col">Quarter</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Q1</th>
      <td>$1.2M</td>
    </tr>
  </tbody>
</table>
```

**Use tables for tabular data only.** Not for layout.

---

## Performance Patterns

### Loading

```html
<!-- Lazy load below-fold images -->
<img src="photo.jpg" loading="lazy" alt="...">

<!-- Eager load above-fold (LCP) -->
<img src="hero.jpg" loading="eager" fetchpriority="high" alt="...">
```

### Preloading

```html
<!-- Critical resources -->
<link rel="preload" href="font.woff2" as="font" crossorigin>
<link rel="preload" href="hero.jpg" as="image">

<!-- Prefetch next page -->
<link rel="prefetch" href="/next-page">
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `<div>` for everything | Use semantic elements |
| Heading for styling | Use CSS, keep hierarchy |
| `tabindex="1"` | Use `tabindex="0"` or `-1` |
| Missing `alt` | Always provide (empty for decorative) |
| `<a>` without `href` | Use `<button>` for actions |
| Hiding with `display:none` | Also hides from screen readers |

---

## Sources

- WCAG 2.2 Guidelines [W3C 2023]
- ARIA Authoring Practices Guide [W3C 2024]
- HTML Living Standard [WHATWG 2025]
- WebAIM accessibility resources
