<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	const types = [
		{
			name: 'Complementary',
			role: 'Learns, guides, improves',
			outcome: 'Better with and without AI',
			highlight: true
		},
		{
			name: 'Constitutive',
			role: 'Learns, guides new capability',
			outcome: 'Does what was impossible alone',
			highlight: false
		},
		{
			name: 'Substitutive',
			role: 'Passively consumes',
			outcome: 'Skills atrophy',
			highlight: false,
			warning: true
		}
	];

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			// Intro animation
			gsap.fromTo(
				'.framework-intro',
				{ opacity: 0, y: 40 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.framework-intro',
						start: 'top 80%'
					}
				}
			);

			// Type cards stagger
			gsap.fromTo(
				'.type-card',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.6,
					stagger: 0.15,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.types-grid',
						start: 'top 80%'
					}
				}
			);

			// Key insight
			gsap.fromTo(
				'.key-insight',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.key-insight',
						start: 'top 80%'
					}
				}
			);

			// Bastani proof
			gsap.fromTo(
				'.bastani-proof',
				{ opacity: 0, y: 40 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.bastani-proof',
						start: 'top 80%'
					}
				}
			);

			// Comparison bars animation
			gsap.fromTo(
				'.comparison-bar .fill',
				{ scaleX: 0 },
				{
					scaleX: 1,
					duration: 0.8,
					stagger: 0.2,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.comparison',
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

<section bind:this={section} class="framework-section">
	<div class="content">
		<div class="framework-intro">
			<h2>Three ways AI extends capability</h2>
		</div>

		<div class="types-grid">
			{#each types as type}
				<div
					class="type-card"
					class:highlight={type.highlight}
					class:warning={type.warning}
				>
					<h3 class="type-name">{type.name}</h3>
					<div class="type-detail">
						<span class="detail-label">Human role</span>
						<span class="detail-value">{type.role}</span>
					</div>
					<div class="type-detail">
						<span class="detail-label">Outcome</span>
						<span class="detail-value" class:warning-text={type.warning}>{type.outcome}</span>
					</div>
				</div>
			{/each}
		</div>

		<div class="key-insight">
			<p class="insight-text">
				The distinction isn't <em>what</em> task you're doing.<br />
				It's <em>how</em> you're doing it.
			</p>
		</div>

		<div class="bastani-proof">
			<h3>Proof: Design determines outcome</h3>
			<p class="proof-setup">Harvard researchers gave students the same AI tutor. The only difference was how it was designed.</p>

			<div class="comparison">
				<div class="comparison-row">
					<div class="comparison-label">
						<span class="label-text">Unrestricted access</span>
					</div>
					<div class="comparison-bar negative">
						<div class="fill"></div>
						<span class="bar-value">−17%</span>
					</div>
					<span class="outcome-text">exam performance</span>
				</div>

				<div class="comparison-row">
					<div class="comparison-label">
						<span class="label-text">Guided step-by-step</span>
					</div>
					<div class="comparison-bar neutral">
						<div class="fill"></div>
						<span class="bar-value">~0%</span>
					</div>
					<span class="outcome-text">no significant harm</span>
				</div>
			</div>

			<p class="proof-conclusion">
				Same AI. Same students. Design made the difference.
			</p>

			<p class="source">Bastani et al. (2025), PNAS — randomized controlled trial, n=1,000+</p>
		</div>
	</div>
</section>

<style>
	.framework-section {
		min-height: 100vh;
		padding: var(--space-24) var(--space-6);
		display: flex;
		align-items: center;
	}

	.content {
		max-width: var(--content-width-wide);
		width: 100%;
		margin: 0 auto;
	}

	.framework-intro {
		margin-bottom: var(--space-10);
	}

	h2 {
		font-size: var(--text-2xl);
	}

	/* Types Grid */
	.types-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: var(--space-4);
		margin-bottom: var(--space-12);
	}

	.type-card {
		padding: var(--space-5);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.type-card.highlight {
		border-color: var(--color-accent-positive);
		background: linear-gradient(
			135deg,
			var(--color-bg-surface) 0%,
			oklch(16% 0.02 70 / 0.3) 100%
		);
	}

	.type-card.warning {
		border-color: var(--color-accent-negative);
		background: linear-gradient(
			135deg,
			var(--color-bg-surface) 0%,
			oklch(16% 0.02 25 / 0.2) 100%
		);
	}

	.type-name {
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		margin-bottom: var(--space-4);
		color: var(--color-text-primary);
	}

	.type-card.highlight .type-name {
		color: var(--color-accent-positive);
	}

	.type-card.warning .type-name {
		color: var(--color-accent-negative);
	}

	.type-detail {
		margin-bottom: var(--space-2);
	}

	.detail-label {
		display: block;
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		margin-bottom: var(--space-1);
	}

	.detail-value {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.warning-text {
		color: var(--color-accent-negative);
	}

	/* Key Insight */
	.key-insight {
		text-align: center;
		padding: var(--space-10) var(--space-6);
		margin: var(--space-8) 0;
	}

	.insight-text {
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		line-height: var(--leading-relaxed);
	}

	.insight-text em {
		color: var(--color-accent-positive);
		font-style: normal;
		font-weight: var(--font-semibold);
	}

	/* Bastani Proof */
	.bastani-proof {
		margin-top: var(--space-12);
		padding: var(--space-8);
		background: var(--color-bg-surface);
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.bastani-proof h3 {
		font-size: var(--text-lg);
		margin-bottom: var(--space-2);
	}

	.proof-setup {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	/* Comparison */
	.comparison {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.comparison-row {
		display: grid;
		grid-template-columns: 140px 1fr auto;
		align-items: center;
		gap: var(--space-4);
	}

	.comparison-label {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.comparison-bar {
		height: 28px;
		background: var(--color-bg-deep);
		border-radius: var(--radius-sm);
		position: relative;
		overflow: hidden;
	}

	.comparison-bar .fill {
		height: 100%;
		border-radius: var(--radius-sm);
		transform-origin: left center;
	}

	.comparison-bar.negative .fill {
		width: 45%;
		background: var(--color-accent-negative);
	}

	.comparison-bar.neutral .fill {
		width: 5%;
		background: var(--color-text-muted);
	}

	.bar-value {
		position: absolute;
		right: var(--space-3);
		top: 50%;
		transform: translateY(-50%);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.outcome-text {
		font-size: var(--text-sm);
		color: var(--color-text-tertiary);
	}

	.proof-conclusion {
		margin-top: var(--space-6);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		font-style: italic;
	}

	.source {
		margin-top: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.types-grid {
			grid-template-columns: 1fr;
		}

		.comparison-row {
			grid-template-columns: 1fr;
			gap: var(--space-2);
		}

		.comparison-bar {
			order: -1;
		}

		.outcome-text {
			text-align: right;
		}
	}
</style>
