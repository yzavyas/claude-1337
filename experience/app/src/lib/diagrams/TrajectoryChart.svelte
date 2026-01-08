<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, fly } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	let visible = $state(false);

	onMount(() => {
		visible = true;
	});

	const nodes = {
		start: { x: 80, y: 150, label: 'Human-AI\nCollaboration', color: '#374151' },
		good: { x: 280, y: 60, label: 'Transparency\n+ Control', color: '#1e3a5f' },
		engage: { x: 480, y: 60, label: 'Engage\n& Learn', color: '#1e3a5f' },
		grow: { x: 680, y: 60, label: 'Capability\nGrows', color: '#059669' },
		bad: { x: 280, y: 240, label: 'Passive\nConsumption', color: '#3d1f1f' },
		offload: { x: 480, y: 240, label: 'Offload\n& Depend', color: '#3d1f1f' },
		atrophy: { x: 680, y: 240, label: 'Capability\nAtrophies', color: '#dc2626' },
	};

	const edges = [
		{ from: 'start', to: 'good', delay: 400 },
		{ from: 'start', to: 'bad', delay: 400 },
		{ from: 'good', to: 'engage', delay: 700 },
		{ from: 'engage', to: 'grow', delay: 1000 },
		{ from: 'bad', to: 'offload', delay: 700 },
		{ from: 'offload', to: 'atrophy', delay: 1000 },
	];

	function getPath(from: string, to: string): string {
		const f = nodes[from as keyof typeof nodes];
		const t = nodes[to as keyof typeof nodes];
		const midX = (f.x + t.x) / 2;
		return `M ${f.x + 70} ${f.y} C ${midX} ${f.y}, ${midX} ${t.y}, ${t.x - 70} ${t.y}`;
	}
</script>

{#if visible}
<div class="diagram-container">
	<svg viewBox="0 0 800 300" class="trajectory-svg">
		<defs>
			<!-- Gradient for good path -->
			<linearGradient id="goodGradient" x1="0%" y1="0%" x2="100%" y2="0%">
				<stop offset="0%" stop-color="#22d3ee" />
				<stop offset="100%" stop-color="#059669" />
			</linearGradient>
			<!-- Gradient for bad path -->
			<linearGradient id="badGradient" x1="0%" y1="0%" x2="100%" y2="0%">
				<stop offset="0%" stop-color="#f87171" />
				<stop offset="100%" stop-color="#dc2626" />
			</linearGradient>
			<!-- Animated dash -->
			<filter id="glow">
				<feGaussianBlur stdDeviation="2" result="coloredBlur"/>
				<feMerge>
					<feMergeNode in="coloredBlur"/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
		</defs>

		<!-- Edges with animation -->
		{#each edges as edge, i}
			{@const isGood = edge.from === 'start' ? edge.to === 'good' : ['good', 'engage', 'grow'].includes(edge.from)}
			<g in:fade={{ delay: edge.delay, duration: 500 }}>
				<path
					d={getPath(edge.from, edge.to)}
					fill="none"
					stroke={isGood ? 'url(#goodGradient)' : 'url(#badGradient)'}
					stroke-width="2"
					class="edge-path"
					class:good-path={isGood}
					class:bad-path={!isGood}
				/>
			</g>
		{/each}

		<!-- Nodes -->
		{#each Object.entries(nodes) as [id, node], i}
			<g
				in:fly={{ y: 20, delay: i * 150, duration: 400, easing: cubicOut }}
				class="node-group"
			>
				<rect
					x={node.x - 70}
					y={node.y - 30}
					width="140"
					height="60"
					rx="8"
					fill={node.color}
					class="node-rect"
					class:glow={id === 'grow' || id === 'atrophy'}
				/>
				{#each node.label.split('\n') as line, lineIdx}
					<text
						x={node.x}
						y={node.y + (lineIdx - 0.5) * 16 + 4}
						text-anchor="middle"
						class="node-text"
					>
						{line}
					</text>
				{/each}
			</g>
		{/each}

		<!-- Labels for paths -->
		<text x="400" y="20" text-anchor="middle" class="path-label good-label" in:fade={{ delay: 1200, duration: 400 }}>
			Complementary Path
		</text>
		<text x="400" y="290" text-anchor="middle" class="path-label bad-label" in:fade={{ delay: 1200, duration: 400 }}>
			Substitutive Path
		</text>
	</svg>
</div>

<div class="diagram-caption">
	<p>Foundations compound. The path you choose determines whether capability grows or atrophies over time.</p>
</div>
{/if}

<style>
	.diagram-container {
		width: 100%;
		padding: 1rem;
		background: linear-gradient(135deg, #0a0f14 0%, #111820 100%);
		border-radius: 12px;
		border: 1px solid #1a2530;
	}

	.trajectory-svg {
		width: 100%;
		height: auto;
		max-height: 350px;
	}

	.node-rect {
		transition: all 0.3s ease;
		filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
	}

	.node-group:hover .node-rect {
		transform: scale(1.02);
		filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.4));
	}

	.node-rect.glow {
		filter: drop-shadow(0 0 8px currentColor);
	}

	.node-text {
		fill: #e0f2fe;
		font-size: 12px;
		font-weight: 500;
		font-family: var(--font-sans, system-ui);
		pointer-events: none;
	}

	.edge-path {
		stroke-dasharray: 8 4;
		animation: flowDash 1s linear infinite;
	}

	.good-path {
		animation-direction: normal;
	}

	.bad-path {
		animation-direction: normal;
	}

	@keyframes flowDash {
		to {
			stroke-dashoffset: -12;
		}
	}

	.path-label {
		font-size: 11px;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		font-family: var(--font-sans, system-ui);
	}

	.good-label {
		fill: #22d3ee;
	}

	.bad-label {
		fill: #f87171;
	}

	.diagram-caption {
		margin-top: 1rem;
		font-size: 0.875rem;
		color: var(--text-muted, #9ca3af);
		text-align: center;
	}

	.diagram-caption p {
		margin: 0;
	}
</style>
