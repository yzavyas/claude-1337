<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	const principles = [
		{
			name: 'Collaborative agency',
			description:
				'Both human and AI retain agency. You see the reasoning. You can redirect. You stay in control.'
		},
		{
			name: 'Bidirectional learning',
			description:
				'The human grows, not just consumes. Each interaction leaves you more capable, not more dependent.'
		},
		{
			name: 'Transparent abstractions',
			description:
				'Extensions are readable text, not black boxes. You can fork them, modify them, understand them.'
		},
		{
			name: 'Compounding value',
			description:
				'Each solution makes the next one easier. What you learn today becomes a foundation for tomorrow.'
		}
	];

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			// Header
			gsap.fromTo(
				'.principles-header',
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

			// Principles stagger
			gsap.fromTo(
				'.principle',
				{ opacity: 0, y: 40 },
				{
					opacity: 1,
					y: 0,
					duration: 0.6,
					stagger: 0.12,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: '.principles-list',
						start: 'top 75%'
					}
				}
			);
		});

		return () => {
			cleanup?.();
		};
	});
</script>

<section bind:this={section} class="principles-section">
	<div class="content">
		<div class="principles-header">
			<h2>Design principles</h2>
			<p class="lead">These principles guide how we build cognitive extensions.</p>
		</div>

		<ol class="principles-list">
			{#each principles as principle, index}
				<li class="principle">
					<span class="principle-number">{String(index + 1).padStart(2, '0')}</span>
					<div class="principle-content">
						<h3 class="principle-name">{principle.name}</h3>
						<p class="principle-description">{principle.description}</p>
					</div>
				</li>
			{/each}
		</ol>
	</div>
</section>

<style>
	.principles-section {
		min-height: 80vh;
		padding: var(--space-24) var(--space-6);
		display: flex;
		align-items: center;
	}

	.content {
		max-width: var(--content-width);
		width: 100%;
		margin: 0 auto;
	}

	.principles-header {
		margin-bottom: var(--space-12);
	}

	h2 {
		font-size: var(--text-2xl);
		margin-bottom: var(--space-3);
	}

	.lead {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
	}

	/* Principles List */
	.principles-list {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: var(--space-6);
	}

	.principle {
		display: flex;
		gap: var(--space-5);
		padding: var(--space-5);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border-subtle);
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.principle:hover {
		border-color: var(--color-border);
	}

	.principle-number {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent-positive);
		opacity: 0.7;
		flex-shrink: 0;
		padding-top: 2px;
	}

	.principle-content {
		flex: 1;
	}

	.principle-name {
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.principle-description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.principle {
			flex-direction: column;
			gap: var(--space-2);
		}

		.principle-number {
			font-size: var(--text-xs);
		}
	}
</style>
