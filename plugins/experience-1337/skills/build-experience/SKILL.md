---
name: build-experience
description: Svelte-first frontend experience engineering. Use when building interactive experiences: animations, 3D/WebGL, scrollytelling, data visualization, or any visual/interactive work. Covers GSAP, Threlte 8, D3, Layer Cake, PixiJS, Melt UI, typography, and design patterns. Triggers on (1) animation/motion design, (2) 3D/WebGL work, (3) scroll-driven storytelling, (4) data visualization, (5) headless UI, (6) graphics/sprites.
---

# Experience Engineering

Svelte-first patterns for interactive frontend experiences. Uses bun, not npm.

**Before visual implementation:** Aesthetic direction should be established. If unclear, invoke the **artist** agent to conduct discovery. The designer and architect need direction to work from.

Claims cite sources inline [Author Year] or in the Sources section.

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
| GSAP | ~23KB core | Timelines, scroll, SVG | Free but prohibits Webflow competitors [GSAP License 2025] |
| Lenis | ~3KB | Smooth scroll | Production standard (not Locomotive) |

**What Claude doesn't know:**
- Lenis + ScrollTrigger is the Awwwards stack [Darkroom Engineering, Lusion SOTD]
- GSAP Standard License prohibits "Competitive Products" — tools for visual animation building [GSAP 2025]
- CSS `animation-timeline: scroll()` landed in Safari 26 [WebKit 2025]
- View Transitions API became Baseline Oct 2025 [web.dev 2025]
- `linear()` timing function enables CSS springs [Comeau 2024]

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
- Locomotive Scroll breaks `position: sticky` [GitHub Issues #282, #30, #401]
- `scroll-snap-type: mandatory` dangerous with tall content
- Passive listeners are non-negotiable
- NYT Snow Fall team "toned down" flashy transitions for reader focus [OpenNews 2012]

See `references/scrollytelling.md` for Sticky+Steps pattern, CSS scroll-driven examples, and award-winning implementations.

## Typography

Use `clamp()` for fluid scaling (never pure `vw` — fails WCAG 1.4.4 [WCAG 2.1]).

See `references/typography.md` for fluid type patterns, system font stacks, and variable fonts.

## Color Systems

**OKLCH over HSL:** Perceptually uniform, predictable contrast, P3 support [CSS Color Level 4 spec].

**Dark mode:** Deep grays (not pure black), off-white text, desaturated colors.

See `references/color-systems.md` for OKLCH syntax, dark mode patterns, and accessible palettes.

## "Designed" vs "AI-Generated"

| AI Tell | Fix |
|---------|-----|
| Sterile, hollow | Add personality, point of view |
| Symmetric everything | Intentional asymmetry, tension |
| Generic gradients | Context-specific color choices |
| Mathematically equal spacing | Optical adjustments |
| No micro-polish | Hover states, 300-500ms transitions |
| Linear timing | Cubic-bezier curves |

**The gap:** Technically correct but emotionally hollow. Visual equality ≠ mathematical equality.

## Design System Tooling

| Approach | Use When | Trade-off |
|----------|----------|-----------|
| Tailwind | Rapid development, utility-first | HTML verbosity |
| vanilla-extract | TypeScript-first, build-time CSS | Setup complexity |
| Panda CSS | Tailwind-like + CSS-in-JS patterns | Newer, smaller ecosystem |
| CSS Modules | Simple scoping, no runtime | Less dynamic |

See `references/design-systems.md` for design tokens (primitives → semantic → component slots) and production patterns.

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
| Age decline | 0.8%/year task slowdown ages 25-60 [Nielsen 2013] |
| Tailored UIs | +30% improvement for older adults [NNg research] |
| Cultural color | White = death in China; red = luck |

**What Claude gets wrong:**
- 7±2 everywhere (it's recall, not recognition)
- F-pattern as natural (it's a failure mode)
- 300ms for everything (different elements need different durations)
- Western color meanings as universal

See `references/cognitive-design.md` for full research.

## Microcopy & Interaction

**Microcopy test:** Can you remove a word without losing meaning? Remove it. ("copy" not "click to copy")

**Focus states:** Use `:focus-visible` (not `:focus`), add `opacity: 0` transitions (not `display: none`).

**Positioning:** Absolute elements need containing blocks; test min AND max content lengths.

## Pre-Ship Checklist

**Animation:** GSAP cleanup on unmount, SSR guards, `prefers-reduced-motion`, mobile test (iOS), passive listeners.

**Design:** Optical adjustments, personality, audience (age/culture).

**Interaction:** Minimal microcopy, visible focus states, edge-case content lengths.

## Aesthetic Discovery (Non-Conformist by Design)

Categorical aesthetic agents converge output. Instead: help users discover and articulate their own visual voice.

### The Collaboration Model

| Role | Who | What |
|------|-----|------|
| Creative direction | Human | Spark, synthesis, "I want it to feel like X meets Y" |
| Articulation support | artist agent | Help explore/express intent, show references, ask questions |
| Evidence | labcoat agent | "For that audience, research shows..." |
| Structure | front-end-architect agent | "That interaction needs this component pattern" |
| Execution | expert-* agents | "Here's how to build that in Svelte/GSAP/etc" |

### Discovering Your Aesthetic

The skill doesn't prescribe style. It helps users crystallize their own influences through a structured interview process (see `assets/aesthetic-interview.md`):

1. **Influences** - Surface what has moved you (films, games, art, spaces)
2. **Qualities** - Extract underlying patterns (density, temperature, precision, energy)
3. **Context** - Ground in the specific project and constraints
4. **Synthesis** - Build vocabulary and reference shorthand
5. **Crystallization** - Optionally persist as personal skill using plugin-dev/extension-builder

**Example influences** (demonstration, not prescription):
- Film: Blade Runner, Kubrick's geometric dread, Villeneuve's restrained atmosphere
- Anime: Ghibli warmth → Death Note tension → Ghost in the Shell density
- Games: BOTW's invitation vs Elden Ring's hostility (same openness, different emotional register)
- Web: The Boat (SBS), Wix space exploration

### Agents

Four collaborative agents - each with values-based construction and references to internalize:

| Agent | Role |
|-------|------|
| **artist** | Facilitate aesthetic discovery through dialogue - surfaces influences, builds vocabulary |
| **experience-designer** | Implement aesthetic vision - typography, color, spacing, visual craft |
| **experience-architect** | Technical architecture - components, state, animation structure, performance |
| **experience-labcoat** | Experience science - UX research, behavioral evidence, validation |

The artist + human discover direction. The designer implements it. The architect structures it. The labcoat validates it.

## References

Technical knowledge domains - agents internalize relevant references before working.

**Fundamentals:**

| Reference | Content |
|-----------|---------|
| `references/html.md` | Semantic structure, accessibility, ARIA, document architecture |
| `references/css.md` | Modern CSS, layout, custom properties, container queries, layers |
| `references/javascript.md` | Language patterns, async, performance, Web APIs |

**Svelte Ecosystem:**

| Reference | Content |
|-----------|---------|
| `references/svelte-patterns.md` | Svelte 5 runes, SvelteKit, Threlte 8 |

**Visual Implementation:**

| Reference | Content |
|-----------|---------|
| `references/typography.md` | Fluid type, variable fonts, type scales |
| `references/color-systems.md` | OKLCH, accessible palettes, dark mode |
| `references/design-systems.md` | Tokens, Tailwind, CSS-in-JS decisions |

**Motion & Animation:**

| Reference | Content |
|-----------|---------|
| `references/motion-design.md` | GSAP, CSS animations, timing functions |
| `references/scrollytelling.md` | ScrollTrigger, Scrollama, Lenis patterns |

**Graphics & 3D:**

| Reference | Content |
|-----------|---------|
| `references/3d-experiences.md` | Three.js, Threlte 8, WebGL performance |
| `references/graphics-primitives.md` | SVG, Canvas, sprites, PixiJS |
| `references/data-visualization.md` | D3, Layer Cake, uPlot, high-performance viz |

**Components & UI:**

| Reference | Content |
|-----------|---------|
| `references/component-patterns.md` | Compound, composition patterns |
| `references/headless-ui.md` | Melt UI, Bits UI, shadcn-svelte |

**Cognitive & Sources:**

| Reference | Content |
|-----------|---------|
| `references/cognitive-design.md` | Attention, load, timing, audience targeting |
| `references/sources.md` | Full citations for all claims |

**Assets:**

| Asset | Content |
|-------|---------|
| `assets/aesthetic-interview.md` | Interview template for aesthetic discovery process |
