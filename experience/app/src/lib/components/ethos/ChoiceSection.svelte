<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { base } from '$app/paths';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			// Header animation
			gsap.fromTo(
				'.choice-header',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: section,
						start: 'top 70%'
					}
				}
			);

			// SVG paths animation - diverging effect
			const pathTimeline = gsap.timeline({
				scrollTrigger: {
					trigger: '.diverging-viz',
					start: 'top 75%',
					end: 'bottom 60%',
					scrub: 1
				}
			});

			// Animate the paths being drawn
			pathTimeline
				.fromTo(
					'.path-upper',
					{ strokeDashoffset: 300 },
					{ strokeDashoffset: 0, duration: 1, ease: 'none' }
				)
				.fromTo(
					'.path-lower',
					{ strokeDashoffset: 300 },
					{ strokeDashoffset: 0, duration: 1, ease: 'none' },
					0
				);

			// Labels fade in
			gsap.fromTo(
				'.path-label',
				{ opacity: 0 },
				{
					opacity: 1,
					duration: 0.6,
					stagger: 0.2,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.diverging-viz',
						start: 'center 70%'
					}
				}
			);

			// Closing text
			gsap.fromTo(
				'.closing-text',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.closing-text',
						start: 'top 80%'
					}
				}
			);

			// CTA
			gsap.fromTo(
				'.cta',
				{ opacity: 0, y: 20 },
				{
					opacity: 1,
					y: 0,
					duration: 0.6,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.cta',
						start: 'top 85%'
					}
				}
			);
		});

		return () => {
			cleanup?.();
		};
	});
</script>

<section bind:this={section} class="choice-section">
	<div class="content">
		<div class="choice-header">
			<h2>Foundations compound</h2>
		</div>

		<div class="diverging-viz">
			<svg viewBox="0 0 400 200" class="diverging-svg" aria-hidden="true">
				<!-- Origin point -->
				<circle cx="40" cy="100" r="4" fill="var(--color-text-muted)" />

				<!-- Upper path - complementary -->
				<path
					class="path-upper"
					d="M 40 100 Q 120 100, 160 70 Q 200 40, 280 30 Q 340 20, 380 15"
					fill="none"
					stroke="var(--color-accent-positive)"
					stroke-width="2"
					stroke-linecap="round"
					stroke-dasharray="300"
					stroke-dashoffset="300"
				/>

				<!-- Lower path - substitutive -->
				<path
					class="path-lower"
					d="M 40 100 Q 120 100, 160 130 Q 200 160, 280 170 Q 340 180, 380 185"
					fill="none"
					stroke="var(--color-accent-negative)"
					stroke-width="2"
					stroke-linecap="round"
					stroke-dasharray="300"
					stroke-dashoffset="300"
				/>

				<!-- Time axis hint -->
				<line
					x1="40"
					y1="195"
					x2="380"
					y2="195"
					stroke="var(--color-border-subtle)"
					stroke-width="1"
				/>
				<text x="380" y="195" class="axis-label" fill="var(--color-text-muted)">time →</text>
			</svg>

			<div class="path-labels">
				<div class="path-label upper">
					<span class="label-title">Complementary</span>
					<span class="label-desc">Capability compounds</span>
				</div>
				<div class="path-label lower">
					<span class="label-title">Substitutive</span>
					<span class="label-desc">Atrophy compounds</span>
				</div>
			</div>
		</div>

		<div class="closing-text">
			<p class="conclusion">
				Every interaction either builds capability or erodes it. Small differences compound.
			</p>
			<p class="final-insight">
				These extensions are designed for the upper path.
			</p>
		</div>

		<div class="cta">
			<a href="{base}/catalog/" class="cta-link primary">
				<span class="cta-text">Browse Extensions</span>
				<span class="cta-arrow">→</span>
			</a>
			<a href="{base}/explore/reference/research/" class="cta-link secondary">
				<span class="cta-text">View Research</span>
			</a>
		</div>
	</div>
</section>

<style>
	.choice-section {
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

	.choice-header {
		margin-bottom: var(--space-10);
		text-align: center;
	}

	h2 {
		font-size: var(--text-3xl);
		font-weight: var(--font-bold);
	}

	/* Diverging Visualization */
	.diverging-viz {
		position: relative;
		margin: var(--space-12) 0;
	}

	.diverging-svg {
		width: 100%;
		height: auto;
		max-height: 250px;
	}

	.axis-label {
		font-family: var(--font-mono);
		font-size: 10px;
		text-anchor: end;
	}

	.path-labels {
		display: flex;
		justify-content: space-between;
		margin-top: var(--space-4);
	}

	.path-label {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.path-label.upper {
		align-items: flex-start;
	}

	.path-label.lower {
		align-items: flex-end;
		text-align: right;
	}

	.label-title {
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
	}

	.path-label.upper .label-title {
		color: var(--color-accent-positive);
	}

	.path-label.lower .label-title {
		color: var(--color-accent-negative);
	}

	.label-desc {
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
	}

	/* Closing Text */
	.closing-text {
		text-align: center;
		margin: var(--space-16) 0;
	}

	.conclusion {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.final-insight {
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	/* CTA */
	.cta {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-4);
		margin-top: var(--space-12);
	}

	.cta-link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-6);
		border-radius: var(--radius-md);
		font-weight: var(--font-medium);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.cta-link.primary {
		background: var(--color-accent);
		color: var(--color-bg-deep);
	}

	.cta-link.primary:hover {
		background: var(--color-accent-hover);
		transform: translateY(-2px);
	}

	.cta-link.secondary {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		padding: var(--space-2) var(--space-4);
	}

	.cta-link.secondary:hover {
		color: var(--color-accent);
	}

	.cta-arrow {
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.cta-link:hover .cta-arrow {
		transform: translateX(4px);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.diverging-svg {
			max-height: 180px;
		}

		.path-labels {
			flex-direction: column;
			gap: var(--space-3);
		}

		.path-label.lower {
			align-items: flex-start;
			text-align: left;
		}
	}
</style>
