# 3D Experiences

WebGL and Three.js patterns for production experiences.

## Framework Decision

| Project | Use | Why |
|---------|-----|-----|
| Non-React app | Three.js direct | Full control, no wrapper overhead |
| React app | React Three Fiber | Declarative, hooks, ecosystem |
| Svelte app | Threlte 8 | Svelte-native, reactive |
| Banner/tiny embed | Vanilla WebGL | Smallest bundle |
| Low-code prototyping | Spline | Quick but **max 1-2 per page** |

## Object Count Decision

| Count | Geometry | Use | Why |
|-------|----------|-----|-----|
| 1-50 | Any | Individual meshes | Simple, full control |
| 50-10,000 | Same | InstancedMesh | Single draw call |
| 1,000+ | Points only | Points/Particles | GPU particles |
| 10,000+ | Same | Batched geometry | Merge into single buffer |

## Mobile Reality Check

**What Claude doesn't know:**

| Platform | Issue | Fix |
|----------|-------|-----|
| iOS | Phong material drops 60→15fps | Use Lambert or MeshStandard |
| iPad | `isMobilePlatform` returns false | Feature detect, not device detect |
| Safari | No OffscreenCanvas | Fallback to main thread |
| All mobile | Context drops for inactive tabs | Handle `contextlost` event |
| All mobile | GPU memory limited | LOD aggressively |

**Think 2015 mobile for draw call budget.**

## Three.js Essentials

### Basic Setup

```javascript
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,                           // FOV
  window.innerWidth / window.innerHeight,  // Aspect
  0.1,                          // Near
  1000                          // Far
);

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true,                  // Transparent background
  powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2x

document.body.appendChild(renderer.domElement);

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

### Context Loss Handling

```javascript
renderer.domElement.addEventListener('webglcontextlost', (e) => {
  e.preventDefault();
  // Show fallback UI
});

renderer.domElement.addEventListener('webglcontextrestored', () => {
  // Reinitialize scene
});
```

### Resize Handling

```javascript
function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', onResize);
```

## Performance Patterns

### Instancing (50-10,000 objects)

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const mesh = new THREE.InstancedMesh(geometry, material, 1000);

const matrix = new THREE.Matrix4();
const position = new THREE.Vector3();

for (let i = 0; i < 1000; i++) {
  position.set(
    Math.random() * 10 - 5,
    Math.random() * 10 - 5,
    Math.random() * 10 - 5
  );
  matrix.setPosition(position);
  mesh.setMatrixAt(i, matrix);
}

scene.add(mesh);
```

### Level of Detail (LOD)

```javascript
const lod = new THREE.LOD();

// High detail (close)
const highGeo = new THREE.SphereGeometry(1, 32, 32);
const highMesh = new THREE.Mesh(highGeo, material);
lod.addLevel(highMesh, 0);

// Medium detail
const medGeo = new THREE.SphereGeometry(1, 16, 16);
const medMesh = new THREE.Mesh(medGeo, material);
lod.addLevel(medMesh, 50);

// Low detail (far)
const lowGeo = new THREE.SphereGeometry(1, 8, 8);
const lowMesh = new THREE.Mesh(lowGeo, material);
lod.addLevel(lowMesh, 100);

scene.add(lod);
```

### Object Pooling

```javascript
class ObjectPool {
  constructor(factory, initialSize = 10) {
    this.factory = factory;
    this.pool = [];
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(factory());
    }
  }

  get() {
    return this.pool.pop() || this.factory();
  }

  release(obj) {
    this.pool.push(obj);
  }
}

// Usage
const pool = new ObjectPool(() => new THREE.Mesh(geometry, material));
const mesh = pool.get();
// ... use mesh
pool.release(mesh);
```

### Shader Optimization

```glsl
// BAD: division
float result = value / 2.0;

// GOOD: multiplication
float result = value * 0.5;

// BAD: expensive functions in fragment shader
float dist = length(uv - center);

// GOOD: skip sqrt when comparing
float distSq = dot(uv - center, uv - center);
if (distSq < radiusSq) { ... }
```

## React Three Fiber

### Basic Setup

```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function Scene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 75 }}
      dpr={[1, 2]}  // Pixel ratio range
    >
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Box />
      <OrbitControls />
    </Canvas>
  );
}

function Box() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}
```

### useFrame (Animation Loop)

```jsx
useFrame((state, delta) => {
  // state.clock - elapsed time
  // state.camera - camera reference
  // state.mouse - normalized mouse position
  // delta - time since last frame

  meshRef.current.rotation.y = state.clock.elapsedTime;
});
```

### Scroll Integration

```jsx
import { ScrollControls, Scroll, useScroll } from '@react-three/drei';

function App() {
  return (
    <Canvas>
      <ScrollControls pages={3} damping={0.1}>
        <Scene />
        <Scroll html>
          <div style={{ height: '300vh' }}>
            {/* HTML content */}
          </div>
        </Scroll>
      </ScrollControls>
    </Canvas>
  );
}

function Scene() {
  const scroll = useScroll();

  useFrame(() => {
    const offset = scroll.offset; // 0-1
    meshRef.current.rotation.y = offset * Math.PI * 2;
  });
}
```

**Source**: [React Three Fiber Docs](https://docs.pmnd.rs/react-three-fiber)

## Threlte 8 (Svelte)

### Basic Setup

```svelte
<script>
  import { Canvas } from '@threlte/core';
  import { OrbitControls } from '@threlte/extras';
  import Scene from './Scene.svelte';
</script>

<Canvas>
  <Scene />
  <OrbitControls />
</Canvas>
```

```svelte
<!-- Scene.svelte -->
<script>
  import { T, useTask } from '@threlte/core';
  import { spring } from 'svelte/motion';

  let rotation = $state({ x: 0, y: 0 });

  useTask((delta) => {
    rotation.y += delta;
  });
</script>

<T.AmbientLight intensity={0.5} />
<T.PointLight position={[10, 10, 10]} />

<T.Mesh rotation.y={rotation.y}>
  <T.BoxGeometry args={[1, 1, 1]} />
  <T.MeshStandardMaterial color="orange" />
</T.Mesh>
```

### SSR Guard

```svelte
<script>
  import { browser } from '$app/environment';
  let Scene;

  if (browser) {
    import('./Scene.svelte').then(m => Scene = m.default);
  }
</script>

{#if Scene}
  <svelte:component this={Scene} />
{/if}
```

### Render Modes

| Mode | Use When | Impact |
|------|----------|--------|
| `always` | Continuous animation | 60fps, battery drain |
| `on-demand` | Static with interactions | 0fps idle, efficient |
| `manual` | Full control | You call `advance()` |

```svelte
<Canvas renderMode="on-demand">
  <!-- Scene -->
</Canvas>
```

**Source**: [Threlte Docs](https://threlte.xyz/)

## Model Loading

### GLTF (Standard)

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

gltfLoader.load('/model.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

### Draco Compression Trade-off

| Draco | File Size | Decode Time |
|-------|-----------|-------------|
| Off | Larger | Instant |
| On | 50-90% smaller | 100-500ms |

**Use Draco** for large models where download is the bottleneck.
**Skip Draco** for small models or when decode time matters.

### Preloading

```jsx
// R3F with useGLTF
import { useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

// Preload on component mount
useGLTF.preload('/model.glb');
```

## Lighting for Performance

| Light Type | Cost | Shadows |
|------------|------|---------|
| AmbientLight | Cheapest | No |
| DirectionalLight | Medium | Yes (directional) |
| PointLight | Expensive | Yes (omnidirectional) |
| SpotLight | Expensive | Yes (cone) |

**Mobile rule**: Max 2-3 lights with shadows.

## Material Performance

| Material | Cost | Use |
|----------|------|-----|
| MeshBasicMaterial | Cheapest | Unlit, flat |
| MeshLambertMaterial | Cheap | Matte, no specular |
| MeshPhongMaterial | Medium | Shiny (but expensive on iOS) |
| MeshStandardMaterial | PBR | Realistic (use instead of Phong) |
| MeshPhysicalMaterial | Expensive | Glass, clearcoat |
| ShaderMaterial | Varies | Custom effects |

**iOS rule**: Avoid Phong, use Lambert or Standard.

## Cleanup

### Three.js Direct

```javascript
function dispose() {
  scene.traverse((object) => {
    if (object.geometry) object.geometry.dispose();
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach(m => m.dispose());
      } else {
        object.material.dispose();
      }
    }
  });
  renderer.dispose();
}
```

### React

```jsx
useEffect(() => {
  return () => {
    // R3F handles most cleanup automatically
    // Dispose custom textures/geometries manually
  };
}, []);
```

### Svelte

```svelte
<script>
  import { onDestroy } from 'svelte';

  onDestroy(() => {
    // Threlte handles cleanup automatically
    // Dispose custom resources manually
  });
</script>
```

## Sources

- [Three.js Docs](https://threejs.org/docs/)
- [Three.js Fundamentals](https://threejs.org/manual/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Threlte](https://threlte.xyz/)
- [Bruno Simon Three.js Journey](https://threejs-journey.com/)
