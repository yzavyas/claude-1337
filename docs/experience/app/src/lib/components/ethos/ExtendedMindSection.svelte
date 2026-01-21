<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			// Header animation
			gsap.fromTo(
				'.extended-header',
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

			// Otto/Inga comparison
			gsap.fromTo(
				'.comparison-block',
				{ opacity: 0, y: 20 },
				{
					opacity: 1,
					y: 0,
					duration: 0.6,
					stagger: 0.15,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.comparison',
						start: 'top 75%'
					}
				}
			);

			// Parity principle
			gsap.fromTo(
				'.parity',
				{ opacity: 0 },
				{
					opacity: 1,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.parity',
						start: 'top 80%'
					}
				}
			);

			// Reframe
			gsap.fromTo(
				'.reframe',
				{ opacity: 0, y: 20 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.reframe',
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

<section bind:this={section} class="extended-section">
	<div class="content">
		<div class="extended-header">
			<h2>Cognitive extensions</h2>
			<p class="source">Clark & Chalmers (1998), "The Extended Mind"</p>
		</div>

		<div class="comparison">
			<div class="comparison-block otto">
				<span class="name">Otto</span>
				<span class="desc">uses a notebook to remember addresses</span>
			</div>
			<div class="comparison-block inga">
				<span class="name">Inga</span>
				<span class="desc">uses biological memory</span>
			</div>
			<div class="comparison-block conclusion">
				<p>If we call Inga's process "remembering," we should call Otto's the same.</p>
				<p class="emphasis">The notebook is part of Otto's mind.</p>
			</div>
		</div>

		<div class="parity">
			<p class="parity-text">
				<span class="label">The parity principle:</span>
				If a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's <em>cognitive extension</em>.
			</p>
		</div>

		<div class="reframe">
			<p class="reframe-lead">This is why we call them cognitive extensions, not tools.</p>
			<p class="reframe-question">
				The question isn't "is AI helpful?" but <strong>"what kind of mind are you building?"</strong>
			</p>
		</div>
	</div>
</section>

<style>
	.extended-section {
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

	.extended-header {
		margin-bottom: var(--space-12);
	}

	h2 {
		font-size: var(--text-3xl);
		margin-bottom: var(--space-2);
	}

	.source {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		font-style: italic;
	}

	/* Comparison */
	.comparison {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
		margin-bottom: var(--space-12);
	}

	.comparison-block {
		padding: var(--space-4) var(--space-5);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border-left: 3px solid var(--color-border);
	}

	.comparison-block.otto {
		border-left-color: var(--color-accent);
	}

	.comparison-block.inga {
		border-left-color: var(--color-text-tertiary);
	}

	.comparison-block.conclusion {
		border-left-color: var(--color-accent-positive);
		background: var(--color-bg-elevated);
	}

	.name {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
	}

	.desc {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
	}

	.conclusion p {
		margin-bottom: var(--space-2);
		color: var(--color-text-secondary);
	}

	.conclusion p:last-child {
		margin-bottom: 0;
	}

	.conclusion .emphasis {
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	/* Parity */
	.parity {
		margin-bottom: var(--space-12);
		padding: var(--space-6);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
	}

	.parity-text {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
	}

	.parity .label {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		margin-bottom: var(--space-2);
	}

	.parity em {
		color: var(--color-accent);
		font-style: normal;
		font-weight: var(--font-medium);
	}

	/* Reframe */
	.reframe {
		text-align: center;
	}

	.reframe-lead {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	.reframe-question {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
	}

	.reframe-question strong {
		color: var(--color-accent);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.extended-section {
			padding: var(--space-16) var(--space-4);
		}
	}
</style>
