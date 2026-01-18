<script lang="ts">
	/**
	 * LabGrid — Lab Component
	 *
	 * CSS Grid container for research cards.
	 * Handles empty state.
	 */
	import ResearchCard from './ResearchCard.svelte';

	interface Paper {
		id: string;
		title: string;
		subtitle?: string;
		summary: string;
		status: 'draft' | 'in-progress' | 'published';
		keywords: string[];
		date: string;
		links: {
			findings?: string;
			proposal?: string;
			experiment?: string;
		};
	}

	let {
		papers,
		onKeywordClick,
		onReset
	}: {
		papers: Paper[];
		onKeywordClick?: (keyword: string) => void;
		onReset?: () => void;
	} = $props();
</script>

{#if papers.length > 0}
	<section class="research-grid">
		{#each papers as paper, i}
			<ResearchCard
				{paper}
				{onKeywordClick}
				featured={paper.status === 'published' && i === 0}
			/>
		{/each}
	</section>
{:else}
	<div class="empty-state">
		<p>No papers match this filter.</p>
		{#if onReset}
			<button type="button" class="reset-filter" onclick={onReset}>
				Show all papers
			</button>
		{/if}
	</div>
{/if}

<style>
	.research-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: var(--space-6);
		max-width: 1200px;
		margin: 0 auto;
		padding: var(--space-8);
	}

	.empty-state {
		text-align: center;
		padding: var(--space-16);
		color: var(--color-text-secondary);
	}

	.empty-state p {
		margin-bottom: var(--space-4);
	}

	.reset-filter {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		background: transparent;
		border: 1px solid var(--color-accent);
		padding: var(--space-2) var(--space-4);
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.reset-filter:hover {
		background: var(--color-accent);
		color: var(--color-text-inverse);
	}

	.reset-filter:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	@media (max-width: 640px) {
		.research-grid {
			grid-template-columns: 1fr;
			padding: var(--space-4);
		}
	}
</style>
