# webgl-3d

3D and WebGL production patterns for web experiences.

---

## framework decision matrix

### when Three.js?

| scenario | recommendation | why |
|----------|---------------|-----|
| Non-React stack | **Three.js** | No React overhead, direct control |
| Complex games, custom shaders | **Three.js** | Fine-grained GPU control needed |
| Granular optimization needed | **Three.js** | Direct access to all internals |
| Learning fundamentals | **Three.js** | Understand before abstracting |

### when React Three Fiber?

| scenario | recommendation | why |
|----------|---------------|-----|
| React application | **R3F** | Declarative, component-based |
| Product configurators | **R3F** | State management built-in |
| Interactive dashboards | **R3F** | Integrates with React ecosystem |
| Rapid development | **R3F** | Lower boilerplate |

### when vanilla WebGL?

| scenario | recommendation | why |
|----------|---------------|-----|
| Banner ads, tiny demos | **vanilla** | ~150KB+ savings on Three.js |
| Single shader effects | **vanilla** | Full library overkill |
| Maximum control | **vanilla** | No abstraction overhead |

**Sources:**
- [Three.js Journey - R3F Lesson](https://threejs-journey.com/lessons/what-are-react-and-react-three-fiber)
- [Three.js Forum Discussion](https://discourse.threejs.org/t/react-three-fiber-or-plain-three-js/24435)
- [GraffersID Comparison 2026](https://graffersid.com/react-three-fiber-vs-three-js/)

---

## performance patterns

### draw call optimization

Draw calls are the primary bottleneck, especially on mobile.

| technique | how it works | impact |
|-----------|-------------|--------|
| **Batching** | Group objects with same material/texture | Fewer gl calls |
| **Texture atlasing** | Multiple images in one texture | Combine draw batches |
| **Instancing** | Same geometry, different transforms | 7k to 100k objects |
| **State sorting** | Group by shader/material/texture | Reduce state changes |

**Key insight:** From 7,000 spheres with regular meshes to 100,000 with instanced geometry.

### Level of Detail (LOD)

| distance | polygon count | purpose |
|----------|---------------|---------|
| Close | High | Full detail visible |
| Medium | Medium | Reduce load |
| Far | Low | Background detail |

Swap models dynamically based on camera distance.

### GPU memory patterns

| pattern | implementation |
|---------|----------------|
| BufferGeometry | Efficient vertex data storage |
| Static VAOs | Cache fetch limits, faster than mutating |
| Texture compression | ASTC (mobile), DXT/BCn (desktop) |
| Geometry compression | Draco: up to 90% reduction |

**Sources:**
- [MDN WebGL Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)
- [Velasquez - 100k Spheres](https://velasquezdaniel.com/blog/rendering-100k-spheres-instantianing-and-draw-calls/)
- [Wonderland Engine Performance](https://wonderlandengine.com/about/webgl-performance/)

---

## mobile production gotchas

### iOS/Safari specific

| issue | mitigation |
|-------|-----------|
| Memory limits per tab | Aggressive asset management |
| ANGLE WebGL 2.0 issues | Test extensively, expect workarounds |
| Lambert vs Phong cost | Phong drops 60fps to 15fps on iOS |
| Audio handling | Keep simple, compressed causes crackling |

### universal mobile patterns

| pattern | implementation |
|---------|----------------|
| Object pooling | Pre-create all objects at init |
| No runtime allocation | Avoid GC pauses during animation |
| Draw call budget | Treat like 2015 mobile device |
| Conditional loading | Skip 3D on small screens entirely |

**Key insight:** `Application.isMobilePlatform` returns false for iPads. Use user agent sniffing.

**Sources:**
- [Airtight Interactive - 60fps Mobile](https://www.airtightinteractive.com/2015/01/building-a-60fps-webgl-game-on-mobile/)
- [Radiator Blog - Unity WebGL Tips](https://www.blog.radiator.debacle.us/2023/01/unity-webgl-tips-advice-in-2023.html)

---

## scroll integration patterns

### fixed canvas architecture

```
[Fixed Canvas] -----> Position: fixed, z-index: -1
     |
[Scrollable Content] -> Position: relative, 500vh height
     |
[ScrollTrigger] -----> onUpdate: progress (0 to 1)
     |
[Three.js Scene] ----> Update camera/models based on progress
```

### GSAP ScrollTrigger integration

| pattern | use case |
|---------|----------|
| Camera path animation | Cinematic scroll experiences |
| Model rotation | 360 product views |
| Progress-based morph | State transitions on scroll |

**Implementation:**
1. Canvas fixed behind content, always visible
2. ScrollTrigger reports progress (0 = start, 1 = end)
3. Map progress to Three.js scene state

**Sources:**
- [Codrops - Cinematic 3D Scroll](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/)
- [Frontend Horse - Three.js + ScrollTrigger](https://frontend.horse/episode/using-threejs-with-gsap-scrolltrigger/)

---

## canvas vs DOM decision

### when canvas over DOM

| condition | recommendation |
|-----------|---------------|
| 100+ animated objects | Canvas |
| Pixel-level control | Canvas |
| Complex particle systems | Canvas |
| Consistent frame rates | Canvas |

### when DOM over canvas

| condition | recommendation |
|-----------|---------------|
| UI elements | DOM |
| < 100 animated elements | DOM |
| Accessibility required | DOM |
| SEO needed | DOM |
| Per-element interactivity | DOM |

### hybrid approach (best practice)

The production pattern is hybrid:
- **Canvas**: Game elements, 3D, particles
- **DOM**: UI, menus, buttons, text

Google Docs uses canvas for rendering but maintains a "side DOM" for accessibility.

**Sources:**
- [Kirupa - DOM vs Canvas](https://www.kirupa.com/html5/dom_vs_canvas.htm)
- [Pocket City - DOM for UI](https://blog.pocketcitygame.com/5-reasons-to-use-dom-instead-of-canvas-for-ui-in-html5-games/)

---

## bundle optimization

### Three.js bundle impact

| metric | value |
|--------|-------|
| Stat size | 1.23 MB |
| Parsed | 658 KB |
| Gzipped | 155 KB |

### mitigation strategies

| strategy | implementation |
|----------|----------------|
| Code splitting | `React.lazy` + `Suspense` for 3D components |
| Conditional loading | Don't load on mobile/small screens |
| Tree shaking | `sideEffects: false` in package.json |
| Vendor splitting | Separate third-party for caching |

**Pattern:** Load 3D conditionally, not at initial page load.

**Sources:**
- [Gatsby - Three.js Performance](https://www.gatsbyjs.com/blog/performance-optimization-for-three-js-web-animations/)
- [Three.js Forum - Bundle Size](https://discourse.threejs.org/t/bundle-size-reduction/38602)

---

## asset optimization

### texture compression by platform

| platform | format | notes |
|----------|--------|-------|
| Desktop | DXT/BCn | Wide support |
| Mobile Android | ASTC | Modern GPUs since ~2015 |
| Mobile iOS | ASTC | Supported |
| Fallback | ETC2 | OpenGL ES 3.0 baseline |

### geometry compression

**Draco compression:**
- Up to 90% mesh size reduction
- WebAssembly decoder required
- Adds decode time (tradeoff: smaller download vs decode cost)
- Parallel decode via Web Workers

**glTF Transform** for optimization:
- Compress with Draco or Meshoptimizer
- Optimize textures (WebP: 50-70% savings vs JPEG/PNG)
- Remove unused data

**Sources:**
- [Cesium - Draco Compression](https://cesium.com/blog/2018/04/09/draco-compression/)
- [glTF Transform](https://gltf-transform.dev/)

---

## context loss handling

WebGL contexts can be lost. Production apps must handle this.

### causes

| cause | description |
|-------|-------------|
| Resource exhaustion | Low GPU memory |
| Tab switching | Browser reclaims resources |
| Monitor changes | GPU switch on laptops |
| Multiple contexts | Browser drops LRU context |

### recovery pattern

```javascript
canvas.addEventListener('webglcontextlost', (e) => {
  e.preventDefault(); // Required for recovery
  cancelAnimationFrame(animationId);
});

canvas.addEventListener('webglcontextrestored', () => {
  // Reinitialize all WebGL resources
  // Textures, buffers, shaders are invalid
});
```

**Key insight:** Mozilla plans to increasingly lose contexts for inactive tabs. Handle this now.

**Sources:**
- [Khronos - Handling Context Lost](https://www.khronos.org/webgl/wiki/HandlingContextLost)
- [MDN - webglcontextrestored](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/webglcontextrestored_event)

---

## shader optimization

### move work to vertex shader

Fragment shaders run per-pixel, vertex shaders per-vertex. Do calculations in vertex shader when possible.

### cost hierarchy

| operation | relative cost |
|-----------|---------------|
| Multiply | Cheap |
| Division | Expensive (use `* 0.5` not `/ 2.0`) |
| Trigonometry | Expensive |
| Texture lookups | Expensive |
| Branching | Variable (often computes both paths) |

### MAD optimization

Multiply-Add (MAD) operations are often single-cycle:
```glsl
// Slow
value = value / 2.0 + offset;

// Fast (MAD)
value = value * 0.5 + offset;
```

### precision

Use `lowp` for values in [-2, 2] range on mobile.

**Sources:**
- [MDN - WebGL Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)
- [Khronos - GLSL Optimizations](https://www.khronos.org/opengl/wiki/GLSL_Optimizations)

---

## postprocessing

### pmndrs/postprocessing (recommended)

Preferred over Three.js built-in EffectComposer:
- **Effect merging**: Combines effects into single passes
- **Single triangle rendering**: Optimized for GPU patterns
- **WebGL2 MSAA**: High-quality anti-aliasing

### performance tradeoffs

| effect | cost | notes |
|--------|------|-------|
| Bloom | Medium-High | Kernel size affects cost |
| DOF | High | Multiple samples |
| SSAO | High | Many samples |
| Color grading | Low | Simple math |

### HDR considerations

Default: sRGB buffers (8-bit) cause banding in dark scenes.
Production: Use `HalfFloatType` for HDR workflows.

**Sources:**
- [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing)
- [React Postprocessing](https://react-postprocessing.docs.pmnd.rs/effects/bloom)

---

## OffscreenCanvas for performance

### what it enables

Move Three.js rendering to Web Worker, unblocking main thread.

| benefit | impact |
|---------|--------|
| UI responsiveness | Main thread free for events |
| Lighthouse scores | 95 to 100 improvement observed |
| Animation smoothness | Decoupled from main thread load |

### caveats

| caveat | workaround |
|--------|-----------|
| Safari unsupported | Fallback to main thread |
| No DOM APIs in worker | Provide style.width/height manually |
| Textures need workarounds | Transfer via messages |
| Single worker preferred | Multiple workers can crash |

**Sources:**
- [Evil Martians - OffscreenCanvas](https://evilmartians.com/chronicles/faster-webgl-three-js-3d-graphics-with-offscreencanvas-and-web-workers)
- [web.dev - OffscreenCanvas](https://web.dev/articles/offscreen-canvas)

---

## Spline production considerations

### when Spline works

| scenario | viability |
|----------|-----------|
| Simple, single 3D element | Good |
| Quick prototypes | Good |
| No-code requirement | Good |
| Complex multi-embed | Avoid |

### performance guidelines

| guideline | detail |
|-----------|--------|
| Max embeds per page | 1-2, avoid 3+ |
| Polygon count | Lower = faster |
| Subdivision levels | Keep at 1, not 2 |
| Use spline-viewer | Lazy loading support |
| Consider alternatives | GIFs/MP4 for non-interactive |

**Key insight:** Check Performance Panel in Export Panel for size estimation.

**Sources:**
- [Spline - How to Optimize](https://docs.spline.design/doc/how-to-optimize-your-scene/doczPMIye7Ko)
- [Spline FAQ](https://docs.spline.design/doc/faq/docJF3WvgXVz)

---

## React Three Fiber ecosystem

### drei helpers (production essentials)

| helper | purpose |
|--------|---------|
| OrbitControls | Camera manipulation |
| Environment | HDR lighting |
| useGLTF | Model loading |
| Html | DOM overlay in 3D |
| Bounds | Auto-center content |

### full ecosystem

| package | purpose |
|---------|---------|
| @react-three/drei | Helpers and abstractions |
| @react-three/postprocessing | Effects |
| @react-three/gltfjsx | GLTF to JSX |
| @react-three/offscreen | Web Worker rendering |
| @react-three/flex | Flexbox layout |

**Sources:**
- [Drei GitHub](https://github.com/pmndrs/drei)
- [R3F Documentation](https://docs.pmnd.rs/react-three-fiber)

---

## what Claude may not know

Based on this research, knowledge gaps that benefit from explicit documentation:

| gap | detail |
|-----|--------|
| iOS-specific Phong cost | 60fps to 15fps, use Lambert |
| iPad detection | `isMobilePlatform` returns false |
| Context loss frequency | Mozilla increasing context drops |
| Safari OffscreenCanvas | Not supported, needs fallback |
| Spline embed limits | Max 1-2 per page |
| MAD optimization | `* 0.5` vs `/ 2.0` matters |
| ASTC mobile support | Since 2015 on most GPUs |
| Draco decode tradeoff | Smaller download vs decode time |

These are production-specific patterns that documentation alone doesn't convey.
