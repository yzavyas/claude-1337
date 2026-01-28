<script lang="ts">
	/**
	 * REPDocument — Lab Component
	 *
	 * Renders a REP (Research Enhancement Proposal) from raw markdown.
	 * Handles all parsing: title, subtitle, status, metadata, and content.
	 * The markdown IS the source of truth.
	 */
	import { base } from '$app/paths';
	import { marked } from 'marked';
	import StatusBadge from './StatusBadge.svelte';

	marked.setOptions({ gfm: true, breaks: true });

	type REPStatus = 'draft' | 'discussion' | 'fcp' | 'accepted' | 'implemented' | 'interim';

	interface ParsedREP {
		id: string;
		title: string;
		subtitle?: string;
		status: REPStatus;
		statusLabel: string;
		created: string;
		updated?: string;
		authors: string;
		content: string;
	}

	let {
		slug,
		markdown,
		experimentSlug
	}: {
		slug: string;
		markdown: string;
		experimentSlug?: string;
	} = $props();

	// Parse the REP markdown into structured data
	function parseREP(content: string, slug: string): ParsedREP {
		// Strip frontmatter
		const bodyMatch = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
		const body = bodyMatch ? bodyMatch[1] : content;

		const titleMatch = body.match(/^#\s+(.+?)(?:\n|$)/m);
		const rawTitle = titleMatch?.[1] || 'Untitled';
		// Strip "REP-XXX:" prefix if present (we add it back in the template)
		const title = rawTitle.replace(/^REP-\d+:\s*/i, '');

		// Extract subtitle (italic line after title)
		const subtitleMatch = body.match(/^#\s+.+\n\n\*([^*]+)\*/m);
		const subtitle = subtitleMatch?.[1];

		const statusMatch = body.match(/\*\*Status\*\*:\s*(\w+)/i);
		const rawStatus = statusMatch?.[1]?.toLowerCase() || 'draft';
		const status = rawStatus as REPStatus;

		// Human-readable status label
		const statusLabels: Record<string, string> = {
			draft: 'Draft',
			discussion: 'In Discussion',
			fcp: 'Final Comment Period',
			accepted: 'Accepted',
			implemented: 'Implemented',
			interim: 'Interim Results'
		};
		const statusLabel = statusLabels[status] || status;

		const createdMatch = body.match(/\*\*Created\*\*:\s*(.+)/i);
		const created = createdMatch?.[1] || '';

		const updatedMatch = body.match(/\*\*Updated\*\*:\s*(.+)/i);
		const updated = updatedMatch?.[1];

		const authorsMatch = body.match(/\*\*Authors\*\*:\s*(.+)/i);
		const authors = authorsMatch?.[1] || '';

		const idMatch = slug.match(/^rep-(\d+)/);
		const id = idMatch?.[1] || '000';

		// Strip metadata section - start from ## Summary
		const summaryIndex = body.indexOf('## Summary');
		const articleContent = summaryIndex !== -1 ? body.slice(summaryIndex) : body;

		return {
			id,
			title,
			subtitle,
			status,
			statusLabel,
			created,
			updated,
			authors,
			content: articleContent
		};
	}

	const rep = $derived(parseREP(markdown, slug));
	const renderedContent = $derived(marked.parse(rep.content) as string);
</script>

<article class="rep-document">
	<header class="rep-header">
		<div class="rep-meta">
			<span class="rep-id">REP-{rep.id}</span>
			<StatusBadge status={rep.status} />
		</div>

		<h1 class="rep-title">{rep.title}</h1>

		{#if rep.subtitle}
			<p class="rep-subtitle">{rep.subtitle}</p>
		{/if}

		<div class="rep-info">
			<span class="info-item">
				<span class="info-label">Created</span>
				<span class="info-value">{rep.created}</span>
			</span>
			{#if rep.updated}
				<span class="info-item">
					<span class="info-label">Updated</span>
					<span class="info-value">{rep.updated}</span>
				</span>
			{/if}
			<span class="info-item">
				<span class="info-label">Authors</span>
				<span class="info-value">{rep.authors}</span>
			</span>
		</div>

		{#if experimentSlug}
			<a href="{base}/lab/experiments/{experimentSlug}" class="experiment-link">
				View Experiment
				<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
					<path
						d="M3 8h10M9 4l4 4-4 4"
						stroke="currentColor"
						stroke-width="1.5"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</a>
		{/if}
	</header>

	<div class="rep-content prose">
		{@html renderedContent}
	</div>
</article>

<style>
	.rep-document {
		max-width: 720px;
		margin: 0 auto;
	}

	.rep-header {
		margin-bottom: var(--space-8);
		padding-bottom: var(--space-6);
		border-bottom: 1px solid var(--color-border);
	}

	.rep-meta {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.rep-id {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.rep-title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-2);
	}

	.rep-subtitle {
		font-family: var(--font-reading);
		font-size: var(--text-lg);
		font-style: italic;
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	.rep-info {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-6);
		margin-bottom: var(--space-4);
	}

	.info-item {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.info-label {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-text-muted);
	}

	.info-value {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.experiment-link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.experiment-link:hover {
		color: var(--color-accent-hover);
	}

	/* Prose styles for rendered markdown */
	.rep-content :global(h2) {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-8);
		margin-bottom: var(--space-4);
	}

	.rep-content :global(h3) {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.rep-content :global(h4) {
		font-family: var(--font-display);
		font-size: var(--text-base);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-top: var(--space-5);
		margin-bottom: var(--space-2);
	}

	.rep-content :global(p) {
		font-family: var(--font-reading);
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.rep-content :global(strong) {
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.rep-content :global(blockquote) {
		font-family: var(--font-reading);
		font-style: italic;
		color: var(--color-text-secondary);
		padding: var(--space-3) var(--space-4);
		border-left: 3px solid var(--color-accent);
		background: var(--color-bg-elevated);
		margin: var(--space-4) 0;
	}

	.rep-content :global(ul),
	.rep-content :global(ol) {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	.rep-content :global(li) {
		font-family: var(--font-reading);
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-2);
	}

	.rep-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-elevated);
		padding: 0.1em 0.3em;
		border-radius: var(--radius-sm);
	}

	.rep-content :global(pre) {
		background: var(--color-bg-elevated);
		padding: var(--space-4);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--space-4) 0;
	}

	.rep-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.rep-content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-4) 0;
		font-size: var(--text-sm);
	}

	.rep-content :global(th),
	.rep-content :global(td) {
		padding: var(--space-2) var(--space-3);
		border: 1px solid var(--color-border);
		text-align: left;
	}

	.rep-content :global(th) {
		background: var(--color-bg-elevated);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	.rep-content :global(td) {
		color: var(--color-text-secondary);
	}

	.rep-content :global(a) {
		color: var(--color-accent);
		text-decoration: none;
	}

	.rep-content :global(a:hover) {
		text-decoration: underline;
	}

	.rep-content :global(hr) {
		border: none;
		border-top: 1px solid var(--color-border);
		margin: var(--space-8) 0;
	}

	/* Mobile */
	@media (max-width: 640px) {
		.rep-title {
			font-size: var(--text-2xl);
		}

		.rep-info {
			gap: var(--space-4);
		}
	}
</style>
