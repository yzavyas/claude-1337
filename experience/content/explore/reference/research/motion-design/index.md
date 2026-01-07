# motion design for the web

Research synthesis: animation and motion design patterns for production web experiences.

---

## library landscape (2025)

### production-grade options

| library | bundle | best for | licensing |
|---------|--------|----------|-----------|
| **Motion** (Framer Motion) | ~32KB gzip | React apps, declarative UI transitions | MIT open source |
| **GSAP** | ~23KB core | Complex timelines, scroll effects, SVG | Free (Webflow-owned) |
| **anime.js** | ~75KB | Lightweight, quick implementations | MIT |
| **Lenis** | ~3KB | Smooth scroll normalization | MIT |

**Motion** (formerly Framer Motion) is the fastest-growing animation library, passing 12 million monthly downloads. It's MIT licensed and sponsored by Framer, Figma, Sanity, Tailwind CSS, and LottieFiles.

**GSAP** was acquired by Webflow. Now free to use, but licensing prohibits use in tools that compete with Webflow. Core is modular (~23KB gzip) with extensive plugin ecosystem: ScrollTrigger, MorphSVG, Draggable.

**Lenis** is the current production standard for smooth scroll. Ultra-lightweight (3KB), works with native `position: sticky`, integrates well with GSAP ScrollTrigger.

### when to choose each

| scenario | recommendation |
|----------|---------------|
| React app, UI transitions | Motion |
| Complex scroll sequences | GSAP + ScrollTrigger |
| SVG morphing, timelines | GSAP |
| Smooth scroll foundation | Lenis |
| Quick prototype, simple animations | anime.js or CSS |
| Maximum performance, simple effects | CSS-only |

**Source**: [Motion vs GSAP comparison](https://motion.dev/docs/gsap-vs-motion), [GSAP vs Anime.js](https://dev.to/ahmed_niazy/gsap-vs-animejs-a-comprehensive-guide-ncb)

---

## performance fundamentals

### the 60fps constraint

16.67ms per frame at 60fps. Every frame that exceeds this budget causes jank.

### GPU-accelerated properties

**Only animate these for compositor-only updates:**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (with caveats)

**Properties that trigger layout (avoid animating):**
- `width`, `height`, `margin`, `padding`
- `top`, `left`, `right`, `bottom`
- `font-size`, `border-width`

```css
/* Bad: triggers layout on every frame */
.animate-width {
  animation: grow 300ms;
}
@keyframes grow {
  from { width: 100px; }
  to { width: 200px; }
}

/* Good: compositor-only */
.animate-scale {
  animation: grow 300ms;
}
@keyframes grow {
  from { transform: scaleX(0.5); }
  to { transform: scaleX(1); }
}
```

### will-change usage

**Use sparingly.** Creates compositor layer, consumes GPU memory.

```css
/* Apply only when animation will start */
.card:hover {
  will-change: transform;
}

/* Or via class before animation */
.will-animate {
  will-change: transform, opacity;
}
```

**Don't spray across all elements.** Mobile devices have limited GPU memory - too many layers can crash the page.

### layout thrashing

**The pattern to avoid:**

```javascript
// BAD: forces synchronous layout on each iteration
elements.forEach(el => {
  el.style.height = el.offsetHeight + 10 + 'px'; // read + write interleaved
});

// GOOD: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // all reads first
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // all writes after
});
```

**Use `requestAnimationFrame` for DOM writes:**

```javascript
// Batch DOM modifications to frame boundary
requestAnimationFrame(() => {
  element.style.transform = 'translateX(100px)';
});
```

**Source**: [web.dev layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing), [Paul Irish reflow list](https://gist.github.com/paulirish/5d52fb081b3570c81e3a)

---

## scroll-triggered patterns

### intersection observer

Native browser API. Efficient because it uses callbacks, not constant scroll polling.

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, {
  threshold: 0.1,  // trigger at 10% visibility
  rootMargin: '-50px'  // offset trigger point
});

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### CSS scroll-driven animations

**Browser support (2025):**
- Chrome 115+: full support
- Safari 26 beta: landed
- Firefox: behind flag

The new native API runs animations off the main thread:

```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.scroll-reveal {
  animation: fade-in linear;
  animation-timeline: scroll();
  animation-range: entry 0% entry 100%;
}
```

**For cross-browser compatibility**, use polyfill with `@supports` fallback:

```css
@supports (animation-timeline: scroll()) {
  .scroll-reveal {
    animation-timeline: scroll();
  }
}
```

### GSAP ScrollTrigger

Production workhorse for scroll sequences:

```javascript
gsap.to('.hero-text', {
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top center',
    end: 'bottom center',
    scrub: true,  // animation progress tied to scroll
  },
  y: -50,
  opacity: 0,
});
```

**Lenis + ScrollTrigger** is the current production pattern for award-winning sites (Awwwards).

**Source**: [Chrome scroll-driven animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations), [WebKit scroll animations guide](https://webkit.org/blog/17101/a-guide-to-scroll-driven-animations-with-just-css/)

---

## view transitions API

**Browser support (October 2025):**
- Same-document: Baseline Newly Available (Chrome 111+, Edge 111+, Firefox 144+, Safari 18+)
- Cross-document: Chrome 126+, Edge 126+, Safari 18.2+ (no Firefox yet)

```javascript
// Basic usage
document.startViewTransition(() => {
  updateDOM();
});

// With customization
document.startViewTransition(async () => {
  await updateDOM();
});
```

```css
/* Style the transition */
::view-transition-old(root) {
  animation: fade-out 300ms ease-out;
}
::view-transition-new(root) {
  animation: fade-in 300ms ease-in;
}

/* Named transitions for specific elements */
.hero-image {
  view-transition-name: hero;
}
```

**Graceful degradation** - if unsupported, DOM updates still work, just without animation.

**Source**: [Chrome View Transitions 2025](https://developer.chrome.com/blog/view-transitions-in-2025), [MDN View Transitions](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

---

## timing and easing

### duration guidelines

| element type | duration | rationale |
|-------------|----------|-----------|
| Micro-interactions (buttons, toggles) | 100-200ms | Quick feedback |
| Small components | 200-300ms | Perceivable but snappy |
| Page transitions | 300-500ms | Substantial but not sluggish |
| Complex sequences (5+ elements) | 500-700ms total | Stagger within this |

**Key insight:** Human visual perception averages 230ms. Animations under 200ms may not be consciously perceived.

### easing functions

| easing | use case |
|--------|----------|
| `ease-out` | Elements entering (deceleration feels natural) |
| `ease-in` | Elements exiting (acceleration into removal) |
| `ease-in-out` | Position changes, looping animations |
| `linear` | Progress indicators, scroll-linked |

### spring physics

Springs define animation via **stiffness**, **damping**, and **mass** rather than duration and easing.

**Advantages:**
- Natural, physical feel
- Interruptible without jarring
- Bounce effects impossible with cubic-bezier

**CSS solution:** `linear()` timing function (2023+) approximates springs:

```css
/* Spring-like bounce */
.bounce {
  animation-timing-function: linear(
    0, 0.22, 0.36, 0.51, 0.67,
    0.84, 1, 0.89, 0.85, 0.91,
    1, 0.97, 1
  );
}
```

**For true springs, use Motion or GSAP:**

```jsx
// Motion spring
<motion.div animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 300, damping: 20 }} />
```

**Source**: [Josh Comeau spring physics](https://www.joshwcomeau.com/animation/a-friendly-introduction-to-spring-physics/), [Josh Comeau linear() function](https://www.joshwcomeau.com/animation/linear-timing-function/)

---

## micro-interactions

### what makes them polished vs gimmicky

**Polished:**
- Purposeful (provides feedback, communicates state)
- Subtle (doesn't compete for attention)
- Fast (100-200ms for direct responses)
- Consistent (same patterns throughout)

**Gimmicky:**
- Gratuitous (animation for animation's sake)
- Distracting (draws attention from content)
- Slow (delays user flow)
- Inconsistent (random effects scattered)

### the four parts (Dan Saffer)

1. **Trigger** - user action or system event
2. **Rules** - what happens after trigger
3. **Feedback** - visual/audio response
4. **Loops and Modes** - repetition, state changes

### production patterns

| interaction | animation | duration |
|-------------|-----------|----------|
| Button press | Scale 0.95 + darken | 100ms |
| Toggle state | Background slide + color | 200ms |
| Form validation | Shake + red border | 300ms |
| Loading | Pulse or skeleton | Continuous |
| Success | Checkmark draw + green | 400ms |
| Hover reveal | Opacity + slight Y translate | 150ms |

**Source**: [NN/g Microinteractions](https://www.nngroup.com/articles/microinteractions/), [IxDF Microinteractions](https://www.interaction-design.org/literature/article/micro-interactions-ux)

---

## accessibility

### prefers-reduced-motion

**Non-negotiable.** Over 70 million people affected by vestibular disorders.

```css
/* Safe default */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### alternative approaches

**Nuclear option** (remove all motion):

```css
@media (prefers-reduced-motion: reduce) {
  .animated { animation: none; }
}
```

**Provide alternative** (still communicate state):

```css
@media (prefers-reduced-motion: reduce) {
  .loading-spinner {
    animation: none;
  }
  .loading-spinner::after {
    content: 'Loading...';
  }
}
```

**Best practice:** Default to reduced motion, enhance for users who want it:

```css
/* No-motion-first approach */
.element {
  /* static styles */
}

@media (prefers-reduced-motion: no-preference) {
  .element {
    animation: slide-in 300ms ease-out;
  }
}
```

**Testing:**
- Chrome DevTools: Rendering > Emulate CSS media feature prefers-reduced-motion
- macOS: System Settings > Accessibility > Display > Reduce motion
- Windows: Settings > Accessibility > Visual effects > Animation effects

**Source**: [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), [Tatiana Mac no-motion-first](https://www.tatianamac.com/posts/prefers-reduced-motion)

---

## staggered animations

### pattern

Delay each child element slightly to create cascading effect:

```css
.stagger-item {
  opacity: 0;
  transform: translateY(20px);
  animation: fade-up 300ms ease-out forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 50ms; }
.stagger-item:nth-child(3) { animation-delay: 100ms; }
/* etc */
```

### dynamic stagger (JavaScript)

```javascript
// Calculate delay from index
items.forEach((item, i) => {
  item.style.animationDelay = `${i * 50}ms`;
});
```

### Motion stagger

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i} variants={item} />
  ))}
</motion.ul>
```

### GSAP stagger

```javascript
gsap.from('.items', {
  opacity: 0,
  y: 30,
  stagger: {
    each: 0.05,
    from: 'start',  // or 'center', 'end', 'random'
    ease: 'power2.out'
  }
});
```

**Source**: [CSS-Tricks staggered animation](https://css-tricks.com/different-approaches-for-creating-a-staggered-animation/), [GSAP Staggers](https://gsap.com/resources/getting-started/Staggers/)

---

## what high-quality sites actually use

### common patterns from Awwwards winners

| technique | implementation |
|-----------|---------------|
| Smooth scroll | Lenis or custom (not native) |
| Scroll-triggered | GSAP ScrollTrigger |
| Page transitions | View Transitions API or custom |
| Micro-interactions | Motion for React, GSAP otherwise |
| 3D effects | Three.js / React Three Fiber |

### the stack

**Award-winning sites typically combine:**
1. **Lenis** - smooth scroll foundation
2. **GSAP + ScrollTrigger** - scroll sequences, complex timelines
3. **Motion/Framer Motion** - React component animations
4. **CSS** - simple hovers, transitions

**Source**: [Awwwards GSAP collection](https://www.awwwards.com/websites/gsap/), [Awwwards animation libraries](https://www.awwwards.com/awwwards/collections/animation-libraries-examples-inspiration/)

---

## safari-specific caveats

Safari uses macOS Core Animation, not a dedicated compositor. This means:
- `playbackRate !== 1` disables hardware acceleration
- Some CSS animations fall back to main thread
- Test thoroughly on real Safari, not just Chrome

---

## synthesis: what Claude doesn't already know

### production-specific knowledge gaps

1. **Lenis as smooth scroll standard** - The current production pattern is Lenis + GSAP ScrollTrigger, not Locomotive Scroll or native smooth scroll.

2. **GSAP licensing post-Webflow acquisition** - Free to use, but prohibited in Webflow-competing tools.

3. **Scroll-driven animations are production-ready** - Safari 26 landed support. The `animation-timeline: scroll()` pattern works cross-browser with polyfill.

4. **View Transitions API is Baseline** - As of October 2025, same-document transitions work across all major browsers. Cross-document still Chromium + Safari only.

5. **linear() timing function** - CSS-native spring approximation, avoiding JavaScript for bounce effects.

6. **Duration tokens** - Design systems create named duration increments (F1 = 100ms, F2 = 200ms) for consistency.

7. **No-motion-first approach** - Progressive enhancement pattern: start without animation, add for users who prefer it.

8. **Layout thrashing detection** - Chrome DevTools Performance panel identifies forced reflows; ESLint can flag `offsetWidth`/`scrollTop` reads.

### decision framework

| question | answer |
|----------|--------|
| React app with UI transitions? | Motion |
| Complex scroll sequences? | GSAP + ScrollTrigger |
| Smooth scroll foundation? | Lenis |
| Page-to-page transitions? | View Transitions API |
| Maximum performance? | CSS-only with compositor properties |
| Spring physics? | Motion (React) or linear() (CSS) |
| Accessibility? | prefers-reduced-motion, no-motion-first |
