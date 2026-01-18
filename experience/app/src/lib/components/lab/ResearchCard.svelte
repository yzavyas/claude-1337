<script lang="ts">
	/**
	 * ResearchCard — Lab Component
	 *
	 * Displays a research paper (proposal or finding) with craft aesthetic.
	 * Featured papers get a gilded left edge.
	 */
	import Badge from '$lib/components/ui/Badge.svelte';

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
		paper,
		featured = false,
		onKeywordClick
	}: {
		paper: Paper;
		featured?: boolean;
		onKeywordClick?: (keyword: string) => void;
	} = $props();

	const statusVariant = {
		draft: 'muted',
		'in-progress': 'rust',
		published: 'sage'
	} as const;

	const statusLabel = {
		draft: 'Draft',
		'in-progress': 'In Progress',
		published: 'Published'
	} as const;

	// Primary link - findings if published, otherwise proposal
	const primaryLink = $derived(paper.links.findings || paper.links.proposal);
</script>

<article class="research-card" class:featured>
	<header class="card-header">
		<span class="paper-id">REP-{paper.id}</span>
		<Badge variant={statusVariant[paper.status]}>
			{statusLabel[paper.status]}
		</Badge>
	</header>

	<h3 class="paper-title">
		{#if primaryLink}
			<a href={primaryLink}>{paper.title}</a>
		{:else}
			{paper.title}
		{/if}
	</h3>

	{#if paper.subtitle}
		<p class="paper-subtitle">{paper.subtitle}</p>
	{/if}

	<p class="paper-summary">{paper.summary}</p>

	<div class="paper-keywords">
		{#each paper.keywords.slice(0, 4) as keyword}
			<button
				type="button"
				class="keyword-chip"
				onclick={() => onKeywordClick?.(keyword)}
			>
				{keyword}
			</button>
		{/each}
	</div>

	<footer class="card-footer">
		<span class="paper-date">{paper.date}</span>
		<div class="paper-links">
			{#if paper.links.findings}
				<a href={paper.links.findings} class="paper-link primary">Findings</a>
			{/if}
			{#if paper.links.proposal}
				<a href={paper.links.proposal} class="paper-link">Proposal</a>
			{/if}
		</div>
	</footer>
</article>

<style>
	.research-card {
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-6);
		box-shadow: var(--shadow-sm);
		transition:
			border-color var(--duration-fast) var(--ease-out),
			box-shadow var(--duration-fast) var(--ease-out);
	}

	.research-card:hover {
		border-color: var(--color-accent);
		box-shadow: var(--shadow-md);
	}

	/* Featured card - gilded left edge */
	.research-card.featured {
		border-left: 4px solid var(--color-accent);
		box-shadow: var(--shadow-lg);
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-3);
	}

	.paper-id {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
		margin-bottom: var(--space-2);
	}

	.paper-title a {
		color: inherit;
		text-decoration: none;
	}

	.paper-title a:hover {
		color: var(--color-accent);
	}

	.paper-subtitle {
		font-size: var(--text-sm);
		font-style: italic;
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-3);
	}

	.paper-summary {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.paper-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-4);
	}

	.keyword-chip {
		font-family: var(--font-mono);
		font-size: 10px;
		color: var(--color-text-tertiary);
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		padding: 2px var(--space-2);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.keyword-chip:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-secondary);
	}

	.card-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.paper-date {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-links {
		display: flex;
		gap: var(--space-3);
	}

	.paper-link {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper-link:hover {
		color: var(--color-accent);
	}

	.paper-link.primary {
		color: var(--color-accent);
	}
</style>
