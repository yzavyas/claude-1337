<script lang="ts">
	import { onMount } from 'svelte';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	let mounted = $state(false);
	const progress = tweened(0, { duration: 2000, easing: cubicOut });

	onMount(() => {
		mounted = true;
		progress.set(1);
	});

	// Generate smooth curve points
	function generatePath(direction: 'up' | 'down'): string {
		const points: string[] = [];
		const startX = 100;
		const endX = 700;
		const startY = 200;

		for (let i = 0; i <= 100; i++) {
			const t = i / 100;
			const x = startX + (endX - startX) * t;

			// Exponential divergence - foundations compound
			const divergence = Math.pow(t, 2) * 120;
			const y = direction === 'up'
				? startY - divergence
				: startY + divergence;

			points.push(`${x},${y}`);
		}

		return `M ${points.join(' L ')}`;
	}

	const upPath = generatePath('up');
	const downPath = generatePath('down');
</script>

{#if mounted}
<div class="visual-container">
	<svg viewBox="0 0 800 400" class="trajectory-visual">
		<defs>
			<!-- Gradient for growth path -->
			<linearGradient id="growthGradient" x1="0%" y1="0%" x2="100%" y2="0%">
				<stop offset="0%" stop-color="#6366f1" />
				<stop offset="50%" stop-color="#22d3ee" />
				<stop offset="100%" stop-color="#10b981" />
			</linearGradient>

			<!-- Gradient for decay path -->
			<linearGradient id="decayGradient" x1="0%" y1="0%" x2="100%" y2="0%">
				<stop offset="0%" stop-color="#f59e0b" />
				<stop offset="50%" stop-color="#ef4444" />
				<stop offset="100%" stop-color="#7f1d1d" />
			</linearGradient>

			<!-- Glow filters -->
			<filter id="glowUp" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur stdDeviation="4" result="blur"/>
				<feMerge>
					<feMergeNode in="blur"/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
			<filter id="glowDown" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur stdDeviation="4" result="blur"/>
				<feMerge>
					<feMergeNode in="blur"/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
		</defs>

		<!-- Grid lines for context -->
		<g class="grid" opacity="0.1">
			{#each [100, 200, 300] as y}
				<line x1="100" y1={y} x2="700" y2={y} stroke="currentColor" stroke-dasharray="4 4"/>
			{/each}
		</g>

		<!-- Starting point marker -->
		<circle cx="100" cy="200" r="6" fill="#94a3b8" class="origin-point"/>

		<!-- Growth path (complementary) -->
		<path
			d={upPath}
			fill="none"
			stroke="url(#growthGradient)"
			stroke-width="3"
			stroke-linecap="round"
			filter="url(#glowUp)"
			stroke-dasharray="1000"
			stroke-dashoffset={1000 - ($progress * 1000)}
			class="path-line"
		/>

		<!-- Decay path (substitutive) -->
		<path
			d={downPath}
			fill="none"
			stroke="url(#decayGradient)"
			stroke-width="3"
			stroke-linecap="round"
			filter="url(#glowDown)"
			stroke-dasharray="1000"
			stroke-dashoffset={1000 - ($progress * 1000)}
			class="path-line"
		/>

		<!-- End markers -->
		{#if $progress > 0.9}
			<g class="end-markers" style="opacity: {($progress - 0.9) * 10}">
				<!-- Growth end -->
				<circle cx="700" cy="80" r="8" fill="#10b981"/>
				<text x="700" y="55" text-anchor="middle" class="label growth-label">capability grows</text>

				<!-- Decay end -->
				<circle cx="700" cy="320" r="8" fill="#7f1d1d"/>
				<text x="700" y="355" text-anchor="middle" class="label decay-label">capability atrophies</text>
			</g>
		{/if}

		<!-- Labels -->
		<text x="100" y="235" text-anchor="middle" class="label origin-label">
			today
		</text>
		<text x="700" y="200" text-anchor="middle" class="label time-label">
			time →
		</text>

		<!-- Path labels that appear mid-animation -->
		{#if $progress > 0.5}
			<g style="opacity: {($progress - 0.5) * 2}">
				<text x="400" y="100" text-anchor="middle" class="path-label up">
					complementary
				</text>
				<text x="400" y="310" text-anchor="middle" class="path-label down">
					substitutive
				</text>
			</g>
		{/if}
	</svg>

	<p class="caption">
		Foundations compound. The path you choose determines the trajectory.
	</p>
</div>
{/if}

<style>
	.visual-container {
		width: 100%;
		padding: 2rem 1rem;
		background: linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 100%);
		border-radius: 12px;
		border: 1px solid rgba(255,255,255,0.05);
	}

	.trajectory-visual {
		width: 100%;
		height: auto;
		max-height: 400px;
	}

	.grid {
		color: #fff;
	}

	.origin-point {
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 0.6; r: 6; }
		50% { opacity: 1; r: 8; }
	}

	.path-line {
		transition: stroke-dashoffset 2s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.label {
		font-family: var(--font-mono, monospace);
		font-size: 11px;
		fill: #6b7280;
		text-transform: lowercase;
		letter-spacing: 0.05em;
	}

	.origin-label {
		fill: #94a3b8;
	}

	.time-label {
		fill: #4b5563;
	}

	.growth-label {
		fill: #10b981;
	}

	.decay-label {
		fill: #ef4444;
	}

	.path-label {
		font-family: var(--font-sans, system-ui);
		font-size: 13px;
		font-weight: 500;
		letter-spacing: 0.02em;
	}

	.path-label.up {
		fill: #22d3ee;
	}

	.path-label.down {
		fill: #f59e0b;
	}

	.caption {
		margin-top: 1.5rem;
		text-align: center;
		font-size: 0.9rem;
		color: #6b7280;
		font-style: italic;
	}

	/* Responsive */
	@media (max-width: 640px) {
		.visual-container {
			padding: 1rem 0.5rem;
		}

		.label, .path-label {
			font-size: 9px;
		}
	}
</style>
