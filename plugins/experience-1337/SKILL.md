---
name: experience-1337
description: Svelte-first frontend experience engineering. Use when building interactive experiences: animations, 3D/WebGL, scrollytelling, data visualization, or any visual/interactive work. Covers GSAP, Threlte 8, D3, Layer Cake, PixiJS, Melt UI, typography, and design patterns. Triggers on (1) animation/motion design, (2) 3D/WebGL work, (3) scroll-driven storytelling, (4) data visualization, (5) headless UI, (6) graphics/sprites.
---

# Experience Engineering

Svelte-first patterns for interactive frontend experiences. Uses bun, not npm.

## How This Skill Teaches

Reasoning is woven into every pattern — not separable footnotes, but integrated explanations. You absorb the WHY by using the skill, not by reading "teaching sections."

| Property | How It's Applied |
|----------|------------------|
| **Readable** | Decision trees show the path, not just the answer |
| **Forkable** | Patterns are modular — take what works, modify what doesn't |
| **Verifiable** | Sources linked, claims traceable |
| **Observable** | "What Claude doesn't know" sections expose gap-filling |

**Success metric:** You can explain to someone else why a choice was made.

---

## Framework Decision

| Project | Use | Why |
|---------|-----|-----|
| Interactive experience | Svelte 5 + Threlte 8 | Compiler, smaller bundles, performance |
| Content site | Astro + Svelte islands | Static-first, hydrate sparingly |
| Data journalism | Svelte + Layer Cake | The Pudding's stack |
| Quick prototype | Vanilla + GSAP | No build, direct control |

**Tooling:** Always `bun`, never `npm`.

## Animation Decision Tree

```
Need animation?
├── Simple enter/exit → Svelte transition:fade, in:fly
├── State-driven values → Svelte spring(), tweened()
├── Complex timeline/sequence → GSAP timeline
├── Scroll-driven
│   ├── Simple triggers → Scrollama
│   └── Complex scrub/pin → GSAP ScrollTrigger + Lenis
├── 3D per-frame → Threlte useTask
└── 2D graphics → PixiJS ticker
```

### Motion Library Landscape

| Library | Bundle | Best For | Gotcha |
|---------|--------|----------|--------|
| Svelte transitions | 0KB | Enter/exit, simple | Built-in |
| GSAP | ~23KB core | Timelines, scroll, SVG | **Free but prohibits Webflow competitors** |
| Lenis | ~3KB | Smooth scroll | **Production standard (not Locomotive)** |

**What Claude doesn't know:**
- Lenis + ScrollTrigger is the Awwwards stack
- GSAP licensing prohibits certain commercial uses
- CSS `animation-timeline: scroll()` landed in Safari 26
- View Transitions API is Baseline (Oct 2025)
- `linear()` timing function enables CSS springs

### Performance Rules

| Do | Don't | Why |
|----|-------|-----|
| Animate `transform`, `opacity` | Animate `width`, `height`, `top` | Compositor-only = 60fps |
| Batch reads, then writes | Interleave reads/writes | Layout thrashing |
| `will-change` sparingly | `will-change: transform` everywhere | GPU memory on mobile |
| `scrub: 0.5` | `scrub: true` | Smoothness without lag |

**GSAP cleanup is mandatory** — memory leaks are common:

```svelte
<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';

  onMount(() => {
    const tl = gsap.timeline();
    // ... animations
    return () => tl.kill(); // REQUIRED
  });
</script>
```

## 3D / WebGL Decision Tree

```
Need 3D?
├── Svelte app → Threlte 8
├── Vanilla/other → Three.js direct
├── Banner/tiny → Vanilla WebGL
└── Low-code → Spline (max 1-2 per page)

Need 2D graphics?
├── < 1,000 elements → SVG + GSAP
├── 1,000-10,000 → Canvas 2D
└── 10,000+ → PixiJS (WebGL)
```

See `references/graphics-primitives.md` for SVG, Canvas, PixiJS patterns.

### Object Count Decision

| Count | Geometry | Use | Why |
|-------|----------|-----|-----|
| 1-50 | Any | Individual meshes | Simple, full control |
| 50-10,000 | Same | InstancedMesh | One draw call |
| 1,000+ | Points only | Points/Particles | GPU particles |

### Mobile Reality Check

| Platform | Issue | Fix |
|----------|-------|-----|
| iOS | Phong drops 60→15fps | Use Lambert |
| iPad | `isMobilePlatform` returns false | Feature detect, not device detect |
| Safari | No OffscreenCanvas | Fallback to main thread |
| All mobile | Context drops for inactive tabs | Handle `contextlost` event |

**Think 2015 mobile for draw call budget.**

See `references/3d-experiences.md` for full patterns.

## Scrollytelling Decision

| Tool | Use When | Gotcha |
|------|----------|--------|
| Scrollama | Step triggers, lightweight | Intersection-based, not scroll position |
| GSAP ScrollTrigger | Complex scrub/pin/snap | Must kill on destroy |
| Lenis | Smooth scroll foundation | **Combine with ScrollTrigger** |
| CSS scroll-driven | Progressive enhancement | Still limited support |

**What Claude doesn't know:**
- Locomotive Scroll breaks `position: sticky`
- `scroll-snap-type: mandatory` dangerous with tall content
- Passive listeners are non-negotiable
- NYT Snow Fall team toned down "spectacular" transitions

### Production Patterns

**Sticky + Steps (Pudding standard):**
```css
.sticky-container {
  position: relative;
  display: flex;
}
.sticky-graphic {
  position: sticky;
  top: 0;
  height: 100vh;
  flex: 1;
}
.steps {
  flex: 1;
}
.step {
  min-height: 100vh;
}
```

**CSS Scroll-driven (progressive enhancement):**
```css
@supports (animation-timeline: scroll()) {
  .element {
    animation: reveal linear both;
    animation-timeline: scroll();
    animation-range: entry 0% entry 100%;
  }
}
```

See `references/scrollytelling.md` for award-winning examples.

## Typography

### Fluid Scaling

```css
/* Modern approach - no breakpoints */
h1 { font-size: clamp(2rem, 2.4rem + 1vw, 3.2rem); }
h2 { font-size: clamp(1.5rem, 1.7rem + 0.5vw, 2.2rem); }
body { font-size: clamp(1rem, 0.9rem + 0.25vw, 1.125rem); }
```

**Accessibility**: Pure `vw` units fail WCAG 1.4.4 (200% zoom). Always use `clamp()` with rem bounds.

### System Font Stacks

```css
/* Simple modern */
font-family: system-ui, sans-serif;

/* Comprehensive */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Helvetica Neue', Arial, sans-serif;

/* Monospace */
font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro',
             Menlo, Consolas, monospace;
```

See `references/typography.md` for variable fonts and type scales.

## Color Systems

### OKLCH: The Modern Standard

```css
/* OKLCH syntax: L (lightness), C (chroma), H (hue) */
color: oklch(70% 0.15 240);

/* With fallback */
color: rgb(59, 130, 246);
color: oklch(61% 0.18 250);
```

**Why OKLCH over HSL:**
- Perceptually uniform (HSL's yellow appears lighter than blue at same "lightness")
- Predictable contrast when shifting hues
- Better gradients (no muddy middle colors)
- Supports P3 displays

### Dark Mode

| Do | Don't | Why |
|----|-------|-----|
| Deep grays (#0a0a0a, #121212) | Pure black (#000000) | Reduces eye strain |
| Off-white text (#E0E0E0) | Pure white (#FFFFFF) | Halo effect on dark |
| Desaturate colors | Keep bright saturated colors | Eye strain |
| Increase line height slightly | Same as light mode | Dark backgrounds compress |

See `references/color-systems.md` for accessible palettes.

## "Designed" vs "AI-Generated"

### AI Tells to Avoid

| Tell | Fix |
|------|-----|
| Sterile, hollow feeling | Add personality, point of view |
| Symmetric everything | Intentional asymmetry, tension |
| Generic blue-to-purple gradients | Context-specific color choices |
| Cookie-cutter layouts | Unexpected compositions |
| No micro-polish | Hover states, 300-500ms transitions |
| Mathematically equal spacing | Optical adjustments |

### What Claude Often Misses

1. **Optical adjustments** — Visual equality ≠ mathematical equality
2. **Tension and contrast** — Over-reliance on harmony
3. **Restraint** — Great design is what you leave out
4. **Personality** — Defaults to neutral, safe choices
5. **Animation timing** — Cubic-bezier curves, not linear
6. **Color temperature** — Pure hues vs intentional warm/cool

**The gap**: Technically correct but emotionally hollow. Every choice should serve a purpose.

## Design System Tooling

| Approach | Use When | Trade-off |
|----------|----------|-----------|
| Tailwind | Rapid development, utility-first | HTML verbosity |
| vanilla-extract | TypeScript-first, build-time CSS | Setup complexity |
| Panda CSS | Tailwind-like + CSS-in-JS patterns | Newer, smaller ecosystem |
| CSS Modules | Simple scoping, no runtime | Less dynamic |

### Design Tokens

Three-layer structure:
```
primitives → semantic aliases → component slots
color-blue-500 → color-brand-primary → button-background-default
```

See `references/design-systems.md` for production patterns.

## Headless UI

| Library | Use | Why |
|---------|-----|-----|
| **Melt UI** | Maximum flexibility | Builder pattern, you render |
| **Bits UI** | Faster start | Pre-composed from Melt |
| **shadcn-svelte** | Rapid prototyping | Bits + Tailwind, own the code |

**Why headless:** Behavior and accessibility are the hard parts. Styling is the easy part you want control over.

See `references/headless-ui.md` for Melt UI, Bits UI, shadcn-svelte patterns.

## Component Patterns

| Problem | Pattern | Why |
|---------|---------|-----|
| 3+ layout regions | Compound components | Flexible composition |
| Deep prop passing | Svelte context | Avoids drilling |
| Modal/overlay | Portal rendering | Clean z-index |
| Shared UI state | Local state, not global | Scoped, predictable |
| Animation sequences | State machine | Explicit phases |

See `references/component-patterns.md` for full patterns.

## Cognitive Design

### Attention & Load

| principle | application |
|-----------|-------------|
| 7±2 chunks | Applies to recall, NOT visible menus |
| F-pattern | **Failure mode** — indicates poor content |
| Serial position | First AND last positions privileged |
| Line length | 45-75 chars optimal |

### Animation Psychology

| duration | use |
|----------|-----|
| 100-200ms | Micro-interactions |
| 200-300ms | Components |
| 300-500ms | Page transitions |

**Asymmetric timing:** Enter slower than exit (300ms in, 200ms out).

### Audience Targeting

| factor | evidence |
|--------|----------|
| Age decline | 0.8%/year usability loss (NNg) |
| Tailored UIs | +30% improvement for older adults |
| Cultural color | White = death in China; red = luck |

**What Claude gets wrong:**
- 7±2 everywhere (it's recall, not recognition)
- F-pattern as natural (it's a failure mode)
- 300ms for everything (different elements need different durations)
- Western color meanings as universal

See `references/cognitive-design.md` for full research.

## Checklist

Before shipping experience work:

- [ ] GSAP/ScrollTrigger cleanup on unmount?
- [ ] 3D behind SSR guard (`browser` check / dynamic import)?
- [ ] `prefers-reduced-motion` respected?
- [ ] Mobile tested (especially iOS)?
- [ ] Passive scroll listeners?
- [ ] Optical adjustments, not just math?
- [ ] Personality in the design, not just correctness?
- [ ] Audience considered (age, expertise, culture)?
- [ ] Asymmetric animation timing (enter slower than exit)?

## Aesthetic Agents

Agents are **modes of expression**, not personas to copy. Each represents an archetypal approach to visual design.

| Agent | Essence | Use When |
|-------|---------|----------|
| **symmetrist** | Geometric precision, one-point perspective | Formal, controlled, authoritative |
| **atmospherist** | Vast scale, mood, environmental | Immersive, contemplative, cinematic |
| **whimsicalist** | Centered, pastels, handcrafted | Playful, charming, storybook |
| **shadowist** | Dark, desaturated, tension | Dramatic, premium, mysterious |
| **brutalist** | Raw, honest, confrontational | Artistic, anti-corporate, stark |
| **editorialist** | Typography-forward, white space | Content-driven, longform, magazine |

### How to Use Agents

| Approach | Example |
|----------|---------|
| **Invoke by name** | "Use the atmospherist approach for this" |
| **Blend archetypes** | "Combine shadowist palette with editorialist typography" |
| **Learn the principles** | Read the agent, apply the principles yourself |
| **Fork and modify** | Take symmetrist's grid system, add your own color theory |

**The goal isn't to invoke the agent forever** — it's to internalize the mode of expression so you can apply it independently.

See `agents/` for full definitions.

## References

| File | Content |
|------|---------|
| `references/svelte-patterns.md` | Svelte 5 runes, SvelteKit, Threlte 8 |
| `references/motion-design.md` | GSAP, CSS animations, timing functions |
| `references/scrollytelling.md` | ScrollTrigger, Scrollama, Lenis patterns |
| `references/3d-experiences.md` | Three.js, Threlte 8, WebGL performance |
| `references/graphics-primitives.md` | SVG, Canvas, sprites, PixiJS |
| `references/data-visualization.md` | D3, Layer Cake, uPlot, high-performance viz |
| `references/headless-ui.md` | Melt UI, Bits UI, shadcn-svelte |
| `references/typography.md` | Fluid type, variable fonts, type scales |
| `references/color-systems.md` | OKLCH, accessible palettes, dark mode |
| `references/design-systems.md` | Tokens, Tailwind, CSS-in-JS decisions |
| `references/component-patterns.md` | Compound, composition patterns |
| `references/cognitive-design.md` | Attention, load, timing, audience targeting |
