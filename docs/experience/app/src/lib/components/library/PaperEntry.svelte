<script lang="ts">
	/**
	 * PaperEntry — Library Component
	 *
	 * Compact list-style entry for academic papers.
	 * Click to expand abstract and link.
	 */
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	interface Paper {
		id: string;
		authors: string;
		year: number;
		title: string;
		venue: string;
		url: string;
		finding: string;
		abstract: string;
	}

	let {
		paper,
		expanded = false,
		ontoggle
	}: {
		paper: Paper;
		expanded?: boolean;
		ontoggle?: () => void;
	} = $props();
</script>

<article class="paper-entry" class:expanded>
	<button type="button" class="paper-header" onclick={ontoggle}>
		<div class="paper-meta">
			<span class="paper-authors">{paper.authors}</span>
			<span class="paper-year">{paper.year}</span>
		</div>
		<h3 class="paper-title">{paper.title}</h3>
		<p class="paper-venue">{paper.venue}</p>
		<p class="paper-finding">{paper.finding}</p>
		<span class="expand-hint">{expanded ? '−' : '+'}</span>
	</button>

	{#if expanded}
		<div class="paper-details" transition:slide={{ duration: 200, easing: quintOut }}>
			<p class="paper-abstract">{paper.abstract}</p>
			<a href={paper.url} target="_blank" rel="noopener noreferrer" class="paper-link">
				View paper →
			</a>
		</div>
	{/if}
</article>

<style>
	.paper-entry {
		border-bottom: 1px solid var(--color-border-subtle);
		transition: background var(--duration-fast) var(--ease-out);
	}

	.paper-entry:last-child {
		border-bottom: none;
	}

	.paper-entry:hover {
		background: var(--color-bg-surface);
	}

	.paper-entry.expanded {
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border-bottom: none;
		margin-bottom: var(--space-2);
	}

	.paper-header {
		width: 100%;
		padding: var(--space-3) var(--space-4);
		background: none;
		border: none;
		cursor: pointer;
		text-align: left;
		position: relative;
	}

	.paper-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--space-4);
		margin-bottom: var(--space-1);
	}

	.paper-authors {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-year {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		background: var(--color-bg-elevated);
		padding: var(--space-0-5) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper-title {
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		color: var(--color-text);
		line-height: var(--leading-snug);
		margin-bottom: var(--space-1);
		padding-right: var(--space-6);
	}

	.paper-venue {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		font-style: italic;
		margin-bottom: var(--space-2);
	}

	.paper-finding {
		font-size: var(--text-xs);
		color: var(--color-text-secondary);
		background: var(--color-bg-elevated);
		padding: var(--space-1-5) var(--space-3);
		border-radius: var(--radius-sm);
		border-left: 2px solid var(--color-accent-muted);
	}

	.expand-hint {
		position: absolute;
		top: var(--space-3);
		right: var(--space-4);
		font-family: var(--font-mono);
		font-size: var(--text-base);
		color: var(--color-text-muted);
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper-entry:hover .expand-hint {
		color: var(--color-accent);
	}

	.paper-details {
		padding: 0 var(--space-4) var(--space-4);
		border-top: 1px solid var(--color-border);
		margin-top: var(--space-2);
		padding-top: var(--space-3);
	}

	.paper-abstract {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-3);
		max-width: 65ch; /* Optimal reading measure */
	}

	.paper-link {
		display: inline-flex;
		align-items: center;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-accent);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper-link:hover {
		color: var(--color-accent-hover);
	}
</style>
