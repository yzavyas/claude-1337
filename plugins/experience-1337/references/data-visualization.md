# Data Visualization

Production patterns for charts, graphs, and data-driven experiences.

## Library Decision

| Library | Best For | Bundle | Learning Curve |
|---------|----------|--------|----------------|
| **Layer Cake** | Svelte scrollytelling | ~10KB | Medium |
| D3.js | Custom, complex | ~75KB | High |
| Observable Plot | Quick charts | ~50KB | Low |
| Chart.js | Simple charts | ~60KB | Low |
| ECharts | Dashboards | ~300KB | Medium |

### Decision Tree

```
What do you need?
├── Svelte app
│   ├── Scrollytelling → Layer Cake (The Pudding's choice)
│   ├── Quick chart → Observable Plot
│   └── Custom/complex → D3.js direct
├── Framework-agnostic
│   ├── Quick chart → Observable Plot or Chart.js
│   ├── Full custom → D3.js
│   └── Dashboard → ECharts
└── Vanilla JS
    ├── Simple → Chart.js
    └── Complex → D3.js
```

## Layer Cake (Svelte)

**The Pudding's data viz library.** Svelte components wrapping D3 scales.

```svelte
<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import Line from './Line.svelte';
  import AxisX from './AxisX.svelte';

  export let data;
</script>

<LayerCake
  x="date"
  y="value"
  {data}
>
  <Svg>
    <Line />
    <AxisX />
  </Svg>
</LayerCake>
```

**Why Layer Cake:**
- Built by The Pudding (scrollytelling experts)
- Server-side rendering support
- Responsive by default
- Composable layer architecture
- ~10KB — lightest serious option

**Source**: [layercake.graphics](https://layercake.graphics/)

## D3.js Fundamentals

### Core Concepts

| Concept | Purpose |
|---------|---------|
| Selections | Select and manipulate DOM |
| Scales | Map data to visual values |
| Axes | Generate axis elements |
| Shapes | Path generators |
| Transitions | Animate changes |

### Basic Pattern

```javascript
import * as d3 from 'd3';

// Select container
const svg = d3.select('#chart')
  .append('svg')
  .attr('width', width)
  .attr('height', height);

// Create scales
const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, width]);

const yScale = d3.scaleBand()
  .domain(data.map(d => d.name))
  .range([0, height])
  .padding(0.1);

// Draw bars
svg.selectAll('rect')
  .data(data)
  .join('rect')
  .attr('x', 0)
  .attr('y', d => yScale(d.name))
  .attr('width', d => xScale(d.value))
  .attr('height', yScale.bandwidth())
  .attr('fill', 'steelblue');
```

### Svelte Integration

```svelte
<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let { data } = $props();
  let svg;

  onMount(() => {
    const selection = d3.select(svg);
    // Draw chart...
  });

  $effect(() => {
    if (!svg) return;
    const selection = d3.select(svg);
    selection.selectAll('*').remove();
    // Redraw when data changes...
  });
</script>

<svg bind:this={svg} width={400} height={100}></svg>
```

## Observable Plot

Quick, declarative charts. Framework-agnostic.

```javascript
import * as Plot from '@observablehq/plot';

// Simple bar chart
const chart = Plot.plot({
  marks: [
    Plot.barY(data, { x: 'name', y: 'value', fill: 'steelblue' })
  ]
});

document.getElementById('chart').append(chart);
```

### Svelte Integration

```svelte
<script>
  import * as Plot from '@observablehq/plot';
  import { onMount } from 'svelte';

  let { data } = $props();
  let container;

  onMount(() => {
    const chart = Plot.plot({
      marks: [
        Plot.dot(data, { x: 'x', y: 'y', stroke: 'category' })
      ]
    });
    container.replaceChildren(chart);
    return () => chart.remove();
  });
</script>

<div bind:this={container}></div>
```

## Common Chart Types

### Line Chart

```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);  // Smooth curve

svg.append('path')
  .datum(data)
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', 'steelblue')
  .attr('stroke-width', 2);
```

### Area Chart

```javascript
const area = d3.area()
  .x(d => xScale(d.date))
  .y0(height)
  .y1(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

svg.append('path')
  .datum(data)
  .attr('d', area)
  .attr('fill', 'steelblue')
  .attr('fill-opacity', 0.3);
```

### Pie/Donut Chart

```javascript
const pie = d3.pie()
  .value(d => d.value)
  .sort(null);

const arc = d3.arc()
  .innerRadius(50)  // 0 for pie, >0 for donut
  .outerRadius(100);

svg.selectAll('path')
  .data(pie(data))
  .join('path')
  .attr('d', arc)
  .attr('fill', d => colorScale(d.data.name));
```

## Scales

| Scale | Use |
|-------|-----|
| `scaleLinear` | Continuous numeric |
| `scaleLog` | Logarithmic |
| `scaleTime` | Date/time |
| `scaleBand` | Categorical (bars) |
| `scaleOrdinal` | Categorical (colors) |
| `scaleSequential` | Color gradients |

```javascript
// Numeric
const x = d3.scaleLinear()
  .domain([0, 100])
  .range([0, width]);

// Categorical
const color = d3.scaleOrdinal()
  .domain(['A', 'B', 'C'])
  .range(['#e41a1c', '#377eb8', '#4daf4a']);

// Time
const time = d3.scaleTime()
  .domain([new Date('2020-01-01'), new Date('2024-01-01')])
  .range([0, width]);

// Sequential color
const heat = d3.scaleSequential()
  .domain([0, 100])
  .interpolator(d3.interpolateViridis);
```

## Axes

```javascript
// Create axes
const xAxis = d3.axisBottom(xScale)
  .ticks(5)
  .tickFormat(d3.format('.0%'));

const yAxis = d3.axisLeft(yScale)
  .tickSize(-width);  // Grid lines

// Render
svg.append('g')
  .attr('transform', `translate(0, ${height})`)
  .call(xAxis);

svg.append('g')
  .call(yAxis)
  .selectAll('.tick line')
  .attr('stroke-opacity', 0.1);  // Subtle grid
```

## Transitions

```javascript
// Animated enter
bars.transition()
  .duration(750)
  .delay((d, i) => i * 50)
  .attr('width', d => xScale(d.value));

// Update pattern
svg.selectAll('rect')
  .data(newData)
  .join(
    enter => enter.append('rect')
      .attr('x', 0)
      .attr('width', 0)
      .call(enter => enter.transition()
        .duration(500)
        .attr('width', d => xScale(d.value))),
    update => update.call(update => update.transition()
      .duration(500)
      .attr('width', d => xScale(d.value))),
    exit => exit.call(exit => exit.transition()
      .duration(500)
      .attr('width', 0)
      .remove())
  );
```

## Responsive Charts

```javascript
function createChart(containerWidth) {
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  const width = containerWidth - margin.left - margin.right;
  const height = width * 0.6;  // Aspect ratio

  // Update scales
  xScale.range([0, width]);
  yScale.range([height, 0]);

  // Redraw...
}

// ResizeObserver
const observer = new ResizeObserver(entries => {
  createChart(entries[0].contentRect.width);
});
observer.observe(container);
```

## Accessibility

### Chart Accessibility

```javascript
// Add role and label
svg.attr('role', 'img')
   .attr('aria-label', 'Bar chart showing sales by month');

// Add title and desc
svg.append('title').text('Monthly Sales');
svg.append('desc').text('Bar chart showing sales figures...');

// Data table fallback
function renderTable(data) {
  return `
    <table class="sr-only">
      <caption>Sales Data</caption>
      <thead><tr><th>Month</th><th>Sales</th></tr></thead>
      <tbody>
        ${data.map(d => `<tr><td>${d.month}</td><td>${d.sales}</td></tr>`).join('')}
      </tbody>
    </table>
  `;
}
```

### Color Accessibility

```javascript
// Use colorblind-safe palettes
const colorblindSafe = [
  '#1b9e77',  // teal
  '#d95f02',  // orange
  '#7570b3',  // purple
  '#e7298a',  // pink
  '#66a61e',  // green
  '#e6ab02',  // yellow
];

// Or use patterns in addition to color
svg.append('defs')
  .append('pattern')
  .attr('id', 'diagonal')
  .attr('patternUnits', 'userSpaceOnUse')
  .attr('width', 4)
  .attr('height', 4)
  .append('path')
  .attr('d', 'M0,4 L4,0')
  .attr('stroke', '#000')
  .attr('stroke-width', 1);
```

## Scrollytelling + Data

### GSAP ScrollTrigger Integration

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animate bars on scroll
ScrollTrigger.create({
  trigger: '#chart',
  start: 'top center',
  onEnter: () => {
    d3.selectAll('rect')
      .transition()
      .duration(750)
      .delay((d, i) => i * 50)
      .attr('width', d => xScale(d.value));
  }
});
```

### Step-based Visualization

```javascript
const steps = [
  { filter: d => d.category === 'A', highlight: 'A' },
  { filter: d => d.category === 'B', highlight: 'B' },
  { filter: d => true, highlight: null }
];

function updateChart(stepIndex) {
  const step = steps[stepIndex];

  bars.transition()
    .duration(500)
    .attr('opacity', d => step.filter(d) ? 1 : 0.2)
    .attr('fill', d => d.category === step.highlight ? 'orange' : 'steelblue');
}

// Connect to Scrollama or ScrollTrigger
```

## Performance

### Large Datasets

```javascript
// Canvas for many points
const canvas = d3.select('#chart')
  .append('canvas')
  .attr('width', width)
  .attr('height', height);

const ctx = canvas.node().getContext('2d');

function draw() {
  ctx.clearRect(0, 0, width, height);
  data.forEach(d => {
    ctx.beginPath();
    ctx.arc(xScale(d.x), yScale(d.y), 2, 0, 2 * Math.PI);
    ctx.fill();
  });
}
```

### Data Aggregation

```javascript
// Bin continuous data
const bins = d3.bin()
  .value(d => d.value)
  .thresholds(20)(data);

// Rollup for aggregation
const byCategory = d3.rollup(
  data,
  v => d3.sum(v, d => d.value),
  d => d.category
);
```

## High-Performance Visualization

### Why This Matters

| Data Points | Technology | Reason |
|-------------|------------|--------|
| < 1,000 | SVG (D3) | Simple, interactive |
| 1,000-10,000 | Canvas (uPlot, ECharts) | Good balance |
| 10,000-100,000 | WebGL (PixiJS + D3) | GPU acceleration needed |
| 100,000+ | Specialized (Datoviz) | Native graphics pipelines |

**The bottleneck**: SVG creates DOM nodes for every data point. At ~1,000 points, DOM overhead dominates.

### uPlot (Time Series)

**The smallest serious charting library.** ~48KB, handles 100k points at 60fps.

```bash
bun add uplot uplot-wrappers
```

**Svelte integration:**
```svelte
<script>
  import { UplotSvelte } from 'uplot-wrappers';

  let { data } = $props();

  const options = {
    width: 800,
    height: 400,
    series: [
      {},
      { stroke: '#3b82f6', width: 2 }
    ]
  };
</script>

<UplotSvelte {options} {data} />
```

**Why uPlot:**
- 48KB vs 254KB Chart.js vs 1000KB ECharts
- Linear performance scaling (~100k points/ms after init)
- Cold start: 34ms for 166,650 points
- At 3,600 points: 10% CPU vs Chart.js 40% CPU

**Trade-off**: Documentation is sparse — expect to read TypeScript definitions.

### D3 + PixiJS (Graphs, Scatter)

**Use D3 for data/scales, PixiJS for rendering.**

```javascript
import * as d3 from 'd3';
import * as PIXI from 'pixi.js';

// D3 handles simulation
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links))
  .force('charge', d3.forceManyBody())
  .force('center', d3.forceCenter(width / 2, height / 2));

// PixiJS handles rendering
const app = new PIXI.Application();
await app.init({ width, height });

const nodeGraphics = nodes.map(node => {
  const g = new PIXI.Graphics();
  g.circle(0, 0, 5).fill('#3b82f6');
  app.stage.addChild(g);
  return g;
});

simulation.on('tick', () => {
  nodes.forEach((node, i) => {
    nodeGraphics[i].x = node.x;
    nodeGraphics[i].y = node.y;
  });
});
```

**Why this pattern:**
- D3 SVG caps at ~1,000 nodes
- PixiJS handles 10,000+ with batching
- D3's force simulation is framework-agnostic

### Canvas Fallback

When you don't need full WebGL but SVG is too slow:

```javascript
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

function draw(data) {
  ctx.clearRect(0, 0, width, height);

  ctx.fillStyle = '#3b82f6';
  data.forEach(d => {
    ctx.beginPath();
    ctx.arc(xScale(d.x), yScale(d.y), 2, 0, Math.PI * 2);
    ctx.fill();
  });
}
```

### Performance Testing

| Metric | What It Tells You |
|--------|-------------------|
| **Frame time** | Consistency matters more than raw FPS |
| **Time to interactive** | How fast can users pan/zoom? |
| **Memory** | Does it grow unbounded? |

**Target**: Stable 16ms frames under interaction, not 1000fps when idle.

## Sources

- [D3.js Docs](https://d3js.org/)
- [Observable Plot](https://observablehq.com/plot/)
- [D3 Gallery](https://observablehq.com/@d3/gallery)
- [Layer Cake](https://layercake.graphics/)
- [uPlot GitHub](https://github.com/leeoniya/uPlot)
- [uplot-wrappers](https://github.com/skalinichev/uplot-wrappers)
- [Rendering 1M Points with D3 + WebGL](https://blog.scottlogic.com/2020/05/01/rendering-one-million-points-with-d3.html)
- [PixiJS Performance Tips](https://pixijs.com/guides/production/performance-tips)
