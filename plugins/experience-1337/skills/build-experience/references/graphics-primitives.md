# Graphics Primitives

SVG, Canvas, sprites, and 2D rendering for experiences.

## Why This Matters

| Rendering | Best For | Limitation |
|-----------|----------|------------|
| **SVG** | Icons, illustrations, simple animations | ~1,000 elements before jank |
| **Canvas 2D** | Games, visualizations, real-time | No DOM, manual hit testing |
| **WebGL (PixiJS)** | 10k+ elements, complex effects | GPU required, more setup |

**The decision**: Start with SVG. Move to Canvas when you hit performance walls. Use PixiJS/WebGL for demanding experiences.

## SVG

### Why SVG?

- **Resolution independent** — crisp at any scale
- **DOM-based** — style with CSS, animate with GSAP
- **Accessible** — screen readers can parse `<title>`, `<desc>`
- **Small files** — vectors compress well

### Svelte SVG Patterns

**Inline SVG component:**
```svelte
<script>
  let { size = 24, color = 'currentColor' } = $props();
</script>

<svg
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke={color}
  stroke-width="2"
>
  <path d="M12 2L2 7l10 5 10-5-10-5z" />
  <path d="M2 17l10 5 10-5" />
</svg>
```

**Dynamic SVG with reactivity:**
```svelte
<script>
  let progress = $state(0);

  // Circumference for stroke-dasharray animation
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = $derived(circumference - (progress / 100) * circumference);
</script>

<svg viewBox="0 0 100 100">
  <circle
    cx="50" cy="50" r={radius}
    fill="none"
    stroke="currentColor"
    stroke-width="8"
    stroke-dasharray={circumference}
    stroke-dashoffset={offset}
    transform="rotate(-90 50 50)"
  />
</svg>
```

### SVG Animation

**CSS transitions (simple):**
```css
svg path {
  transition: stroke-dashoffset 0.5s ease-out;
}
```

**GSAP (complex):**
```javascript
import gsap from 'gsap';

gsap.to('svg path', {
  strokeDashoffset: 0,
  duration: 1,
  ease: 'power2.out'
});
```

### SVG Optimization

| Tool | Use |
|------|-----|
| **SVGO** | Optimize SVG files (remove metadata, simplify paths) |
| **SVGOMG** | Web UI for SVGO |
| **svg-sprite** | Combine icons into sprite sheet |

```bash
bunx svgo input.svg -o output.svg
```

## Canvas 2D

### Why Canvas?

- **Performance** — direct pixel manipulation, no DOM overhead
- **Games** — frame-by-frame rendering, collision detection
- **Real-time** — visualizations, audio waveforms, particle effects

### Svelte Canvas Pattern

```svelte
<script>
  import { onMount } from 'svelte';

  let canvas;
  let ctx;

  onMount(() => {
    ctx = canvas.getContext('2d');

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Your drawing code
      ctx.fillStyle = '#3b82f6';
      ctx.fillRect(50, 50, 100, 100);

      requestAnimationFrame(draw);
    }

    draw();
  });
</script>

<canvas bind:this={canvas} width={800} height={600}></canvas>
```

### Canvas Performance Tips

| Do | Don't | Why |
|----|-------|-----|
| Batch draw calls | Draw one shape at a time | Reduces state changes |
| Use `requestAnimationFrame` | Use `setInterval` | Syncs with display refresh |
| Cache repeated shapes | Redraw complex shapes | Draw to offscreen canvas once |
| Use integer coordinates | Use float coordinates | Avoids anti-aliasing overhead |

**Offscreen canvas caching:**
```javascript
// Create offscreen canvas for complex static shape
const offscreen = document.createElement('canvas');
offscreen.width = 100;
offscreen.height = 100;
const offCtx = offscreen.getContext('2d');
// Draw complex shape once
offCtx.beginPath();
// ... complex drawing

// In render loop, just stamp it
ctx.drawImage(offscreen, x, y);
```

## Sprites

### Why Sprites?

| Problem | Sprite Solution |
|---------|-----------------|
| Many HTTP requests for images | Single file, one request |
| GPU texture switching | Single texture, batched draws |
| Animation frames scattered | Sequential frames in one image |

### Sprite Sheet Pattern

**Structure:**
```
sprite.png: [frame1][frame2][frame3][frame4]
            64px    64px    64px    64px
```

**Canvas sprite animation:**
```javascript
const sprite = {
  image: new Image(),
  frameWidth: 64,
  frameHeight: 64,
  totalFrames: 4,
  currentFrame: 0
};

sprite.image.src = '/sprites/character.png';

function drawSprite(ctx, x, y) {
  ctx.drawImage(
    sprite.image,
    sprite.currentFrame * sprite.frameWidth, 0,  // Source x, y
    sprite.frameWidth, sprite.frameHeight,        // Source w, h
    x, y,                                         // Dest x, y
    sprite.frameWidth, sprite.frameHeight         // Dest w, h
  );
}

// Animation loop
let frameCount = 0;
function animate() {
  if (frameCount % 10 === 0) {  // Change frame every 10 ticks
    sprite.currentFrame = (sprite.currentFrame + 1) % sprite.totalFrames;
  }
  frameCount++;
  requestAnimationFrame(animate);
}
```

### Sprite Tools

| Tool | Use |
|------|-----|
| **TexturePacker** | Professional sprite sheet generation |
| **Aseprite** | Pixel art + sprite animation |
| **free-tex-packer** | Open source alternative |

## PixiJS

### Why PixiJS?

| Scenario | Use |
|----------|-----|
| 10k+ animated elements | PixiJS (WebGL batching) |
| Force graphs with many nodes | PixiJS + D3 simulation |
| Games with complex sprites | PixiJS (texture atlases) |
| Real-time data viz | PixiJS (GPU acceleration) |

### Svelte + PixiJS

**svelte-pixi** library:
```bash
bun add pixi.js svelte-pixi
```

```svelte
<script>
  import { Application, Sprite, Container } from 'svelte-pixi';
</script>

<Application width={800} height={600}>
  <Container x={400} y={300}>
    <Sprite
      texture="/sprites/bunny.png"
      anchor={0.5}
    />
  </Container>
</Application>
```

**Manual integration:**
```svelte
<script>
  import { onMount, onDestroy } from 'svelte';
  import * as PIXI from 'pixi.js';

  let container;
  let app;

  onMount(async () => {
    app = new PIXI.Application();
    await app.init({
      width: 800,
      height: 600,
      backgroundAlpha: 0
    });
    container.appendChild(app.canvas);

    // Create sprites
    const sprite = PIXI.Sprite.from('/sprites/bunny.png');
    sprite.anchor.set(0.5);
    sprite.x = app.screen.width / 2;
    sprite.y = app.screen.height / 2;
    app.stage.addChild(sprite);

    // Animation loop
    app.ticker.add((delta) => {
      sprite.rotation += 0.01 * delta.deltaTime;
    });
  });

  onDestroy(() => {
    app?.destroy(true, { children: true });
  });
</script>

<div bind:this={container}></div>
```

### PixiJS Performance

| Technique | Impact | When |
|-----------|--------|------|
| **Sprite batching** | 10-100x | Many similar sprites |
| **Texture atlases** | 5-10x | Multiple sprite types |
| **cacheAsBitmap** | 50-100x | Static complex graphics |
| **Container culling** | Variable | Off-screen elements |

```javascript
// Cache static graphics as bitmap
complexGraphic.cacheAsBitmap = true;

// Enable culling for containers
container.cullable = true;
```

## Decision Framework

```
How many animated elements?
├── < 100 → SVG + CSS/GSAP
├── 100-1,000 → Canvas 2D
├── 1,000-10,000 → Canvas 2D (optimized) or PixiJS
└── 10,000+ → PixiJS (WebGL required)

What kind of graphics?
├── Icons, illustrations → SVG
├── Data visualization → Canvas or PixiJS
├── Games, particles → PixiJS
└── Photo manipulation → Canvas 2D
```

## Sources

- [MDN Canvas Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial)
- [PixiJS Docs](https://pixijs.com/)
- [PixiJS Performance Tips](https://pixijs.com/guides/production/performance-tips)
- [svelte-pixi](https://github.com/mattjennings/svelte-pixi)
- [SVGO](https://github.com/svg/svgo)
- [Sprite Animation Tutorial](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Create_the_Canvas_and_draw_on_it)
