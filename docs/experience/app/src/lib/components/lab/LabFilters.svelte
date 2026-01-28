<script lang="ts">
	/**
	 * LabFilters — Lab Component
	 *
	 * Filter bar for research papers with keyword chips.
	 * Includes accessibility: aria-pressed on chips, aria-live on count.
	 */
	let {
		keywords,
		active,
		count,
		onchange
	}: {
		keywords: string[];
		active: string | null;
		count: number;
		onchange: (keyword: string | null) => void;
	} = $props();
</script>

<section class="filter-section">
	<div class="filter-header">
		<h2>Findings & Proposals</h2>
		<span class="result-count" aria-live="polite">
			{count} {count === 1 ? 'entry' : 'entries'}
		</span>
	</div>

	<div class="filter-keywords" role="group" aria-label="Filter by keyword">
		<button
			type="button"
			class="filter-chip"
			class:active={active === null}
			aria-pressed={active === null}
			onclick={() => onchange(null)}
		>
			All
		</button>
		{#each keywords as keyword}
			<button
				type="button"
				class="filter-chip"
				class:active={active === keyword}
				aria-pressed={active === keyword}
				onclick={() => onchange(active === keyword ? null : keyword)}
			>
				{keyword}
			</button>
		{/each}
	</div>
</section>

<style>
	.filter-section {
		max-width: 1200px;
		margin: 0 auto;
		padding: var(--space-8);
		border-bottom: 1px solid var(--color-border);
	}

	.filter-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-4);
	}

	.filter-header h2 {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		/* Use accent color for visibility on dark backgrounds */
		color: var(--color-accent);
	}

	.result-count {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.filter-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2);
	}

	.filter-chip {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-full);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.filter-chip:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-secondary);
	}

	.filter-chip:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	.filter-chip.active {
		background: var(--color-accent);
		border-color: var(--color-accent);
		color: var(--color-text-inverse);
	}

	@media (max-width: 640px) {
		.filter-section {
			padding: var(--space-4);
		}

		.filter-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--space-2);
		}
	}
</style>
