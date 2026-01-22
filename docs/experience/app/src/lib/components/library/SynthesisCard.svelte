<script lang="ts">
	/**
	 * SynthesisCard — Library Component
	 *
	 * Prominent card for research syntheses (your own analysis).
	 * Gold accent treatment to distinguish from cited papers.
	 */
	interface Synthesis {
		href: string;
		title: string;
		description: string;
	}

	let { synthesis }: { synthesis: Synthesis } = $props();
</script>

<a href={synthesis.href} class="synthesis-card">
	<h3 class="synthesis-title">{synthesis.title}</h3>
	<p class="synthesis-description">{synthesis.description}</p>
	<span class="synthesis-arrow">→</span>
</a>

<style>
	.synthesis-card {
		display: block;
		position: relative;
		padding: var(--space-6);
		background: linear-gradient(
			135deg,
			oklch(from var(--color-accent) l c h / 0.08) 0%,
			var(--color-bg-elevated) 100%
		);
		border: 1px solid var(--color-accent-muted);
		border-left: 4px solid var(--color-accent);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-sm);
		text-decoration: none;
		transition:
			transform var(--duration-fast) var(--ease-out),
			box-shadow var(--duration-fast) var(--ease-out);
	}

	.synthesis-card:hover {
		transform: translateY(-3px);
		box-shadow: var(--shadow-md);
	}

	.synthesis-card:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	.synthesis-title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-semibold);
		color: var(--color-text);
		margin-bottom: var(--space-2);
		padding-right: var(--space-8);
	}

	.synthesis-description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.synthesis-arrow {
		position: absolute;
		top: var(--space-6);
		right: var(--space-6);
		font-family: var(--font-mono);
		font-size: var(--text-lg);
		color: var(--color-accent);
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.synthesis-card:hover .synthesis-arrow {
		transform: translateX(4px);
	}
</style>
