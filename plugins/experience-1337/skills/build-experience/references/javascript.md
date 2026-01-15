# JavaScript Reference

Language patterns, performance, and Web APIs for experience engineering.

---

## Event Loop

Understanding execution order:

```
┌─────────────────────────────┐
│         Call Stack          │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│      Microtask Queue        │ ← Promises, queueMicrotask
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│      Macrotask Queue        │ ← setTimeout, setInterval, I/O
└─────────────────────────────┘
```

**Order:** Sync code → All microtasks → One macrotask → All microtasks → ...

```javascript
console.log('1'); // sync
setTimeout(() => console.log('2'), 0); // macrotask
Promise.resolve().then(() => console.log('3')); // microtask
console.log('4'); // sync
// Output: 1, 4, 3, 2
```

---

## Animation Timing

### requestAnimationFrame

```javascript
// Good: synced with display refresh
function animate(time) {
  element.style.transform = `translateX(${time * 0.1}px)`;
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// With cleanup
let rafId;
function start() {
  rafId = requestAnimationFrame(animate);
}
function stop() {
  cancelAnimationFrame(rafId);
}
```

### When to Use What

| API | Use | Timing |
|-----|-----|--------|
| `requestAnimationFrame` | Visual animations | Before repaint (~16ms) |
| `setTimeout` | Delayed execution | After delay |
| `queueMicrotask` | ASAP, before repaint | After current task |
| `requestIdleCallback` | Non-urgent work | When idle |

---

## Async Patterns

### Promise Composition

```javascript
// Sequential
const results = [];
for (const item of items) {
  results.push(await process(item));
}

// Parallel
const results = await Promise.all(items.map(process));

// Parallel with error handling
const results = await Promise.allSettled(items.map(process));
```

### AbortController

```javascript
const controller = new AbortController();

fetch(url, { signal: controller.signal })
  .then(response => response.json())
  .catch(err => {
    if (err.name === 'AbortError') return; // cancelled
    throw err;
  });

// Cancel after timeout
setTimeout(() => controller.abort(), 5000);
```

---

## Memory Management

### Common Leak Patterns

```javascript
// Leak: closure holds reference
function setup() {
  const largeData = new Array(1000000);
  element.addEventListener('click', () => {
    console.log(largeData.length); // largeData never GC'd
  });
}

// Fix: weak reference or cleanup
function setup() {
  const largeData = new Array(1000000);
  const handler = () => console.log('clicked');
  element.addEventListener('click', handler);

  return () => element.removeEventListener('click', handler);
}
```

### WeakMap/WeakSet

```javascript
// For metadata that shouldn't prevent GC
const metadata = new WeakMap();

function track(element) {
  metadata.set(element, { created: Date.now() });
}
// When element is removed from DOM, metadata auto-cleans
```

---

## DOM Performance

### Batch Operations

```javascript
// Bad: multiple reflows
items.forEach(item => {
  container.appendChild(createEl(item)); // reflow each time
});

// Good: single reflow
const fragment = document.createDocumentFragment();
items.forEach(item => {
  fragment.appendChild(createEl(item));
});
container.appendChild(fragment); // one reflow
```

### Read/Write Separation

```javascript
// Bad: layout thrashing
elements.forEach(el => {
  const height = el.offsetHeight; // read (forces layout)
  el.style.height = height * 2 + 'px'; // write
});

// Good: batch reads, then writes
const heights = elements.map(el => el.offsetHeight); // all reads
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2 + 'px'; // all writes
});
```

---

## Intersection Observer

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // one-time
      }
    });
  },
  {
    threshold: 0.1, // 10% visible
    rootMargin: '50px', // trigger 50px before
  }
);

elements.forEach(el => observer.observe(el));
```

**Use for:**
- Lazy loading images
- Infinite scroll
- Scroll-triggered animations
- Analytics (viewport tracking)

---

## Resize Observer

```javascript
const observer = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    // Respond to size change
  }
});

observer.observe(element);
```

**Use for:**
- Container queries (polyfill)
- Canvas resizing
- Responsive component logic

---

## Web Animations API

```javascript
// Programmatic CSS animations
const animation = element.animate(
  [
    { transform: 'translateX(0)', opacity: 1 },
    { transform: 'translateX(100px)', opacity: 0 }
  ],
  {
    duration: 300,
    easing: 'ease-out',
    fill: 'forwards'
  }
);

animation.finished.then(() => {
  console.log('done');
});

// Control
animation.pause();
animation.reverse();
animation.cancel();
```

---

## Proxy for Reactivity

```javascript
function reactive(obj) {
  return new Proxy(obj, {
    set(target, key, value) {
      target[key] = value;
      notify(key, value); // trigger updates
      return true;
    },
    get(target, key) {
      track(key); // track access
      return target[key];
    }
  });
}

const state = reactive({ count: 0 });
state.count++; // triggers notification
```

---

## Modern Features

### Private Fields

```javascript
class Component {
  #state = {};

  #privateMethod() {
    return this.#state;
  }

  publicMethod() {
    return this.#privateMethod();
  }
}
```

### Nullish Coalescing & Optional Chaining

```javascript
// Only null/undefined, not 0 or ''
const value = data ?? 'default';

// Safe property access
const name = user?.profile?.name;
const result = api?.call?.();
```

### Structured Clone

```javascript
// Deep clone (replaces JSON.parse(JSON.stringify()))
const clone = structuredClone(original);
// Works with Date, Map, Set, ArrayBuffer
```

---

## Performance Debugging

### Performance API

```javascript
// Measure code execution
performance.mark('start');
// ... code ...
performance.mark('end');
performance.measure('operation', 'start', 'end');

const measure = performance.getEntriesByName('operation')[0];
console.log(`Took ${measure.duration}ms`);
```

### Memory Profiling

```javascript
// Check memory (Chrome only)
if (performance.memory) {
  console.log({
    used: performance.memory.usedJSHeapSize,
    total: performance.memory.totalJSHeapSize
  });
}
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `for...in` on arrays | Use `for...of` or `.forEach()` |
| `==` comparisons | Use `===` always |
| Mutating in `.map()` | Return new values, or use `.forEach()` |
| `async` in `.forEach()` | Use `for...of` with `await` |
| `setTimeout(fn, 0)` for animation | Use `requestAnimationFrame` |
| Creating closures in loops | Use `let` or extract function |

---

## Sources

- JavaScript: The Definitive Guide [Flanagan 2020]
- MDN Web Docs [Mozilla 2025]
- V8 Blog [Google 2025]
- web.dev Performance guides [Google 2025]
