# Scrollytelling

Scroll-driven storytelling. Production patterns from award-winning projects.

## Award-Winning Examples

### The Pudding (Benchmark Standard)

| Project | Pattern | Technique |
|---------|---------|-----------|
| [Film Dialogue by Gender](https://pudding.cool/2017/03/film-dialogue/) | Sticky + Steps | SVG chart transforms on step enter |
| [CNN/MSNBC/FOX Coverage](https://pudding.cool/2018/01/chyrons/) | Video + Steps | Video scrub synced to scroll |
| [Stand-Up Comedy Structure](https://pudding.cool/2018/02/stand-up/) | Audio + Transcript | Audio timeline scrub |

**Pudding patterns:**
- Russell Goldenberg's Scrollama library
- Sticky graphic + scrollable text
- Step-based triggers (not continuous scrub)
- High-contrast text overlays

**Source**: [Pudding Process](https://pudding.cool/process/introducing-scrollama/)

### New York Times Interactive

| Project | Pattern | Technique |
|---------|---------|-----------|
| [Snow Fall](https://www.nytimes.com/projects/2012/snow-fall/) | Parallax + Video | Pioneered long-form web storytelling |
| [Racial Injustice](https://www.nytimes.com/interactive/2021/us/racial-injustice.html) | Grid + Scroll | Image grid with scroll-triggered zoom |

**NYT insight**: Snow Fall team toned down "spectacular" transitions. Less is more.

### Apple Product Pages

Pattern: Canvas-based product animations
- Frame-by-frame image sequences
- Scroll position maps to frame number
- Heavy preloading for smooth playback

## Library Decision

| Tool | Use When | Gotcha |
|------|----------|--------|
| Scrollama | Step triggers, lightweight | Intersection-based, not scroll position |
| GSAP ScrollTrigger | Complex scrub/pin/snap | **Must kill on destroy** |
| Lenis | Smooth scroll foundation | **Combine with ScrollTrigger** |
| CSS scroll-driven | Progressive enhancement | Still limited support |
| IntersectionObserver | Simplest triggers | No scrub capability |

**What Claude doesn't know:**
- Lenis + ScrollTrigger is the Awwwards stack (not Locomotive)
- Locomotive Scroll breaks `position: sticky`
- `scroll-snap-type: mandatory` is dangerous with tall content
- Passive listeners are non-negotiable
- `scrub: 0.5` not `scrub: true` for smoothness

## Pattern Decision Tree

```
What scroll behavior?
├── Step triggers only (enter/exit)
│   ├── Lightweight → IntersectionObserver
│   └── With helpers → Scrollama
├── Continuous animation (scrub)
│   └── GSAP ScrollTrigger
│       ├── User controls pace → scrub: true (or scrub: 0.5)
│       ├── Snap to sections → snap: 1
│       └── Pin element → pin: true
├── Smooth/inertia scrolling
│   └── Lenis + ScrollTrigger
└── 3D scroll-driven
    └── Three.js + ScrollTrigger
```

## Layout Patterns

### Sticky + Steps (Pudding Standard)

Most common, most reliable. Visual stays fixed, text scrolls.

```html
<section class="sticky-container">
  <!-- Sticky visual (left) -->
  <div class="sticky-graphic">
    <figure class="visual">
      <!-- Chart, image, or visualization -->
    </figure>
  </div>

  <!-- Scrollable steps (right) -->
  <div class="steps">
    <article class="step">Step 1 content</article>
    <article class="step">Step 2 content</article>
    <article class="step">Step 3 content</article>
  </div>
</section>
```

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
  display: flex;
  align-items: center;
  justify-content: center;
}

.steps {
  flex: 1;
}

.step {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 2rem;
}
```

**Key decisions:**
- Flexbox for side-by-side (simpler than grid)
- `sticky top-0` keeps visual in viewport
- `min-height: 100vh` ensures scroll room

### Overlay Pattern (Background + Foreground)

Visual fills screen, text overlays. Cinematic feel.

```html
<section class="overlay-container">
  <div class="sticky-background">
    <img src="background.jpg" alt="" />
    <div class="gradient-overlay"></div>
  </div>

  <div class="floating-cards">
    <article class="card">Card 1</article>
    <article class="card">Card 2</article>
  </div>
</section>
```

```css
.overlay-container {
  position: relative;
}

.sticky-background {
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: -1;
}

.sticky-background img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gradient-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}

.floating-cards {
  position: relative;
  min-height: 200vh;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 50vh 0;
}

.card {
  max-width: 32rem;
  margin: 0 auto;
  padding: 2rem;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(8px);
}
```

### Horizontal Scroll Section

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const track = document.querySelector('.track');
const totalWidth = track.scrollWidth - window.innerWidth;

gsap.to(track, {
  x: -totalWidth,
  ease: 'none',
  scrollTrigger: {
    trigger: '.container',
    start: 'top top',
    end: () => `+=${totalWidth}`,
    pin: true,
    scrub: 1,
    anticipatePin: 1
  }
});
```

### Video Scrub (Apple Style)

```javascript
const video = document.querySelector('video');

ScrollTrigger.create({
  trigger: '.video-container',
  start: 'top top',
  end: 'bottom bottom',
  scrub: true,
  onUpdate: (self) => {
    video.currentTime = self.progress * video.duration;
  }
});
```

## ScrollTrigger Essentials

### Basic Setup

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animate on enter
gsap.from('.element', {
  y: 50,
  opacity: 0,
  scrollTrigger: {
    trigger: '.element',
    start: 'top 80%',
    end: 'bottom 20%',
    toggleActions: 'play none none reverse'
  }
});

// Scrub animation
gsap.to('.parallax', {
  y: -100,
  scrollTrigger: {
    trigger: '.section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 0.5  // 0.5s smoothing (NOT scrub: true)
  }
});
```

### Pin Pattern

```javascript
ScrollTrigger.create({
  trigger: '.panel',
  start: 'top top',
  end: '+=500',     // Pin for 500px of scroll
  pin: true,
  pinSpacing: true  // Add space after (usually want this)
});
```

### Snap Pattern

```javascript
ScrollTrigger.create({
  trigger: '.sections',
  start: 'top top',
  end: 'bottom bottom',
  snap: {
    snapTo: 1 / 4,  // 4 sections
    duration: 0.3,
    ease: 'power2.inOut'
  }
});
```

### Cleanup (Critical)

```javascript
// React
useEffect(() => {
  const triggers = [];

  triggers.push(
    ScrollTrigger.create({ /* config */ })
  );

  return () => {
    triggers.forEach(t => t.kill());
  };
}, []);
```

```svelte
<!-- Svelte -->
<script>
  import { onMount, onDestroy } from 'svelte';

  let triggers = [];

  onMount(() => {
    triggers.push(
      ScrollTrigger.create({ /* config */ })
    );
  });

  onDestroy(() => {
    triggers.forEach(t => t.kill());
  });
</script>
```

## Lenis + ScrollTrigger

The production standard for smooth scrolling.

```javascript
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({
  lerp: 0.1,          // Smoothness (0-1)
  wheelMultiplier: 1,
  touchMultiplier: 2
});

// Sync Lenis with ScrollTrigger
lenis.on('scroll', ScrollTrigger.update);

// Use GSAP ticker for smooth RAF
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);
```

**Source**: [Lenis GitHub](https://github.com/darkroomengineering/lenis)

## Mobile Gotchas

### Viewport Height

| Problem | Fix |
|---------|-----|
| `100vh` jumps on mobile | Use `100dvh` |
| iOS Safari address bar | Fixed pixel heights |
| Resize on scroll | Only listen to `orientationchange` |

```css
.section {
  height: 100vh;
  height: 100dvh;  /* Dynamic viewport height */
}
```

```javascript
// JS fallback
function setViewportHeight() {
  document.documentElement.style.setProperty(
    '--vh',
    `${window.innerHeight}px`
  );
}

window.addEventListener('orientationchange', setViewportHeight);
setViewportHeight();
```

### Performance

```javascript
ScrollTrigger.config({
  ignoreMobileResize: true,
  autoRefreshEvents: 'visibilitychange,DOMContentLoaded,load'
});

ScrollTrigger.create({
  fastScrollEnd: true,
  preventOverlaps: true
});
```

## CSS Scroll-Driven Animations

Progressive enhancement for modern browsers.

```css
@supports (animation-timeline: scroll()) {
  .reveal {
    animation: reveal linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }

  @keyframes reveal {
    from {
      opacity: 0;
      transform: translateY(50px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .parallax-bg {
    animation: parallax linear both;
    animation-timeline: scroll();
  }

  @keyframes parallax {
    from { transform: translateY(0); }
    to { transform: translateY(-20%); }
  }
}
```

**Source**: [MDN Scroll-driven Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations)

## Accessibility

### Requirements

| Requirement | Implementation |
|-------------|----------------|
| Reduced motion | Disable/reduce animations |
| Keyboard nav | `tabindex="0"` on sections |
| Skip link | Link to end of experience |
| Aria labels | Describe the experience |

```html
<a href="#after-experience" class="skip-link">
  Skip scrolling experience
</a>

<section
  role="region"
  aria-label="Interactive data visualization"
  tabindex="0"
>
  <!-- Content -->
</section>

<div id="after-experience">
  <!-- Content after -->
</div>
```

### Reduced Motion

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Show static version or reduce animation intensity
  ScrollTrigger.getAll().forEach(st => st.kill());
}
```

### Scrolljacking: When It's OK

| Acceptable | Not Acceptable |
|------------|----------------|
| Scroll-linked animation | Overriding scroll distance |
| Optional snap | Hijacking scroll direction |
| Pin during sequence | Preventing scroll entirely |
| Progress indicators | Unpredictable behavior |

**Source**: [NN/g Scrolljacking 101](https://www.nngroup.com/articles/scrolljacking-101/)

## Sources

- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
- [Scrollama](https://github.com/russellgoldenberg/scrollama)
- [Lenis](https://github.com/darkroomengineering/lenis)
- [Pudding Scrollytelling Process](https://pudding.cool/process/scrollytelling-sticky/)
- [Web.dev Viewport Units](https://web.dev/blog/viewport-units)
