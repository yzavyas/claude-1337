<script lang="ts">
	/**
	 * SectionHeader — UI Primitive
	 *
	 * Consistent section header with mono font, uppercase, optional count.
	 * Used in Lab and Library pages.
	 */
	let {
		title,
		count,
		variant = 'default'
	}: {
		title: string;
		count?: number;
		variant?: 'default' | 'gold';
	} = $props();
</script>

<header class="section-header {variant}">
	<h2 class="section-title">{title}</h2>
	{#if count !== undefined}
		<span class="section-count" aria-label="{count} items">{count}</span>
	{/if}
</header>

<style>
	.section-header {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--space-3);
		margin-bottom: var(--space-5);
		padding-bottom: var(--space-3);
		border-bottom: 2px solid var(--color-border);
	}

	.section-header.gold {
		border-bottom-color: var(--color-accent-muted);
	}

	.section-title {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-text-secondary);
	}

	.section-header.gold .section-title {
		color: var(--color-accent);
	}

	.section-count {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}
</style>
