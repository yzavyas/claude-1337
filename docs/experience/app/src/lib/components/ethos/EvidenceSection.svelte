<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, ScrollTrigger, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	const findings = [
		{ label: 'Transparency', value: 0.415, isNegative: false, stat: 'Strong effect' },
		{ label: 'Process Control', value: 0.507, isNegative: false, stat: 'Strongest effect' },
		{ label: 'Engagement', value: 0.555, isNegative: true, stat: 'Negative effect' }
	];

	// Normalize values for bar widths (max value determines 100%)
	const maxValue = Math.max(...findings.map((f) => f.value));
	const getBarWidth = (value: number) => (value / maxValue) * 70; // 70% max width

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			// Section intro animation
			gsap.fromTo(
				'.evidence-intro',
				{ opacity: 0, y: 40 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.evidence-intro',
						start: 'top 80%'
					}
				}
			);

			// Stagger the effect bars
			findings.forEach((_, index) => {
				const bar = section.querySelector(`.effect-bar-${index}`);
				if (!bar) return;

				const tl = gsap.timeline({
					scrollTrigger: {
						trigger: bar,
						start: 'top 85%'
					}
				});

				// Bar row fade in
				tl.fromTo(
					bar,
					{ opacity: 0, x: -20 },
					{ opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' }
				);

				// Bar fill animation
				tl.fromTo(
					bar.querySelector('.bar-fill'),
					{ scaleX: 0 },
					{ scaleX: 1, duration: 0.8, ease: 'power2.out' },
					'-=0.2'
				);

				// Value reveal
				tl.fromTo(
					bar.querySelector('.stat-value'),
					{ opacity: 0 },
					{ opacity: 1, duration: 0.4 },
					'-=0.4'
				);
			});

			// Pull quote animation
			gsap.fromTo(
				'.pull-quote',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.pull-quote',
						start: 'top 80%'
					}
				}
			);

		});

		return () => {
			cleanup?.();
		};
	});
</script>

<section bind:this={section} class="evidence-section">
	<div class="content">
		<div class="evidence-intro">
			<h2>What makes collaboration work</h2>
			<p class="intro-text">
				Blaurock et al. analyzed 106 studies asking: what makes AI collaboration work? Three factors showed strong effects:
			</p>
		</div>

		<div class="effect-bars">
			{#each findings as finding, index}
				<div class="effect-bar effect-bar-{index}" class:negative={finding.isNegative}>
					<div class="bar-header">
						<span class="bar-label">{finding.label}</span>
						<span class="stat-value">{finding.stat}</span>
					</div>
					<div class="bar-track">
						<div
							class="bar-fill"
							class:positive={!finding.isNegative}
							class:negative={finding.isNegative}
							style="--bar-width: {getBarWidth(finding.value)}%"
						></div>
					</div>
					{#if finding.isNegative}
						<p class="bar-note">When the AI asks questions, frequent users performed <em>worse</em></p>
					{/if}
				</div>
			{/each}
		</div>

		<blockquote class="pull-quote">
			<p>"Show your work. Let them steer. Don't interrupt with questions."</p>
			<cite>— Synthesized from Blaurock et al. (2024), Journal of Service Research</cite>
		</blockquote>

	</div>
</section>

<style>
	.evidence-section {
		min-height: 100vh;
		padding: var(--space-24) var(--space-6);
		display: flex;
		align-items: center;
	}

	.content {
		max-width: var(--content-width);
		width: 100%;
		margin: 0 auto;
	}

	.evidence-intro {
		margin-bottom: var(--space-12);
	}

	h2 {
		font-size: var(--text-2xl);
		margin-bottom: var(--space-4);
	}

	.intro-text {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
	}

	/* Effect Bars */
	.effect-bars {
		display: flex;
		flex-direction: column;
		gap: var(--space-8);
		margin: var(--space-12) 0;
	}

	.effect-bar {
		padding: var(--space-4);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
	}

	.effect-bar.negative {
		border-color: oklch(62% 0.10 25 / 0.5);
	}

	.bar-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		margin-bottom: var(--space-3);
	}

	.bar-label {
		font-size: var(--text-base);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	.stat-value {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.bar-track {
		height: 24px;
		background: var(--color-bg-deep);
		border-radius: var(--radius-sm);
		overflow: hidden;
	}

	.bar-fill {
		height: 100%;
		width: var(--bar-width);
		border-radius: var(--radius-sm);
		transform-origin: left center;
	}

	.bar-fill.positive {
		background: linear-gradient(90deg, var(--color-accent-positive), oklch(75% 0.12 160));
	}

	.bar-fill.negative {
		background: linear-gradient(90deg, var(--color-accent-negative), oklch(55% 0.10 25));
	}

	.bar-note {
		margin-top: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-accent-negative);
		font-style: italic;
	}

	/* Pull Quote */
	.pull-quote {
		margin: var(--space-16) 0;
		padding: var(--space-6) var(--space-8);
		border-left: 3px solid var(--color-accent-positive);
		background: var(--color-bg-surface);
		border-radius: 0 var(--radius-md) var(--radius-md) 0;
	}

	.pull-quote p {
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
		margin: 0;
	}

	.pull-quote cite {
		display: block;
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		font-style: normal;
		color: var(--color-text-tertiary);
	}



	/* Mobile */
	@media (max-width: 640px) {
		.evidence-section {
			padding: var(--space-16) var(--space-4);
		}

		.pull-quote {
			padding: var(--space-4) var(--space-5);
		}

		.pull-quote p {
			font-size: var(--text-lg);
		}

		.stat-highlight {
			flex-direction: column;
			gap: var(--space-1);
		}
	}
</style>
