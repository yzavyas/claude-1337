<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, ScrollTrigger, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			const tl = gsap.timeline({
				scrollTrigger: {
					trigger: section,
					start: 'top 80%',
					end: 'center center',
					scrub: false,
					toggleActions: 'play none none reverse'
				}
			});

			// Animate the hook text
			tl.fromTo(
				'.hook-text',
				{ opacity: 0, y: 30 },
				{ opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' }
			);

			// Animate the gap visualization
			tl.fromTo(
				'.gap-viz',
				{ opacity: 0 },
				{ opacity: 1, duration: 0.4 },
				'-=0.4'
			);

			// Animate expected bar (right)
			tl.fromTo(
				'.bar-expected .bar-fill',
				{ scaleX: 0 },
				{ scaleX: 1, duration: 0.8, ease: 'power2.out' },
				'-=0.2'
			);

			// Animate actual bar (left - negative direction)
			tl.fromTo(
				'.bar-actual .bar-fill',
				{ scaleX: 0 },
				{ scaleX: 1, duration: 0.8, ease: 'power2.out' },
				'-=0.6'
			);

			// Reveal gap label
			tl.fromTo(
				'.gap-label',
				{ opacity: 0, scale: 0.9 },
				{ opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.7)' },
				'-=0.2'
			);

		});

		return () => {
			cleanup?.();
		};
	});
</script>

<section bind:this={section} class="hook-section">
	<div class="content">
		<div class="hook-text">
			<p class="stat-lead">
				Developers using AI felt <span class="stat-number positive">24% faster</span>
			</p>
			<p class="stat-lead">
				They were <span class="stat-number negative">19% slower</span>
			</p>
		</div>

		<div class="gap-viz">
			<div class="bar-row">
				<span class="bar-label">Perceived</span>
				<div class="bar bar-expected">
					<div class="bar-fill positive"></div>
					<span class="bar-value">+24%</span>
				</div>
			</div>

			<div class="bar-center-line"></div>

			<div class="bar-row actual-row">
				<span class="bar-label">Actual</span>
				<div class="bar bar-actual">
					<div class="bar-fill negative"></div>
					<span class="bar-value">−19%</span>
				</div>
			</div>

			<div class="gap-label">
				<span class="gap-number">43</span>
				<span class="gap-unit">point gap</span>
			</div>
		</div>

		<p class="source">
			METR 2025 — <span class="source-detail">n=16 experienced developers, mature codebases</span>
		</p>

		<p class="mechanism">
			You spend less time writing, more time checking. The AI writes fast. Finding bugs in plausible-but-wrong code is slow.
		</p>
	</div>
</section>

<style>
	.hook-section {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--space-16) var(--space-6);
	}

	.content {
		max-width: var(--content-width);
		width: 100%;
	}

	.hook-text {
		margin-bottom: var(--space-12);
	}

	.stat-lead {
		font-size: var(--text-3xl);
		font-weight: var(--font-semibold);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-2);
		color: var(--color-text-primary);
	}

	.stat-number {
		font-family: var(--font-mono);
		font-variant-numeric: tabular-nums;
	}

	.stat-number.negative {
		color: var(--color-accent-negative);
	}

	.stat-number.positive {
		color: var(--color-accent-positive);
	}

	/* Gap Visualization */
	.gap-viz {
		position: relative;
		margin: var(--space-12) 0;
		padding: var(--space-8) 0;
	}

	.bar-row {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		margin-bottom: var(--space-4);
	}

	.bar-row.actual-row {
		margin-bottom: 0;
	}

	.bar-label {
		font-size: var(--text-sm);
		color: var(--color-text-tertiary);
		width: 80px;
		text-align: right;
		font-family: var(--font-mono);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	.bar {
		flex: 1;
		height: 32px;
		background: var(--color-bg-surface);
		border-radius: var(--radius-sm);
		position: relative;
		overflow: visible;
	}

	.bar-fill {
		height: 100%;
		border-radius: var(--radius-sm);
		transform-origin: left center;
	}

	.bar-expected .bar-fill {
		width: 60%;
		background: var(--color-accent-positive);
		transform-origin: left center;
	}

	.bar-actual .bar-fill {
		width: 48%;
		background: var(--color-accent-negative);
		transform-origin: right center;
		margin-left: auto;
	}

	.bar-value {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.bar-expected .bar-value {
		right: calc(40% + var(--space-3));
	}

	.bar-actual .bar-value {
		left: calc(52% + var(--space-3));
	}

	.bar-center-line {
		position: absolute;
		left: calc(80px + var(--space-4) + 50%);
		top: 0;
		bottom: 0;
		width: 1px;
		background: var(--color-border);
	}

	.gap-label {
		position: absolute;
		left: 50%;
		bottom: calc(-1 * var(--space-8));
		transform: translateX(-50%);
		text-align: center;
		background: var(--color-bg-elevated);
		padding: var(--space-2) var(--space-4);
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
	}

	.gap-number {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-2xl);
		font-weight: var(--font-bold);
		color: var(--color-text-primary);
		line-height: 1;
	}

	.gap-unit {
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	.source {
		margin-top: var(--space-16);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.source-detail {
		color: var(--color-text-tertiary);
	}

	.mechanism {
		margin-top: var(--space-6);
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		max-width: 500px;
	}

	/* Mobile adjustments */
	@media (max-width: 640px) {
		.stat-lead {
			font-size: var(--text-2xl);
		}

		.bar-label {
			width: 60px;
			font-size: var(--text-xs);
		}

		.bar {
			height: 24px;
		}

		.gap-label {
			bottom: calc(-1 * var(--space-10));
		}
	}
</style>
