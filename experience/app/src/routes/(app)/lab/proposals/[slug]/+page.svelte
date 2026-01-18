<script lang="ts">
	import { marked } from 'marked';

	let { data } = $props();

	// Configure marked
	marked.setOptions({
		gfm: true,
		breaks: false
	});

	const proposalHtml = $derived(marked.parse(data.content));
	const ripHtml = $derived(data.rip ? marked.parse(data.rip.content) : null);

	// Status colors
	const statusConfig: Record<string, { label: string; color: string }> = {
		draft: { label: 'Draft', color: 'var(--color-text-muted)' },
		discussion: { label: 'Discussion', color: 'var(--color-accent)' },
		fcp: { label: 'Final Comment Period', color: 'var(--color-accent-warning)' },
		accepted: { label: 'Accepted', color: 'var(--color-accent-positive)' },
		rejected: { label: 'Rejected', color: 'var(--color-accent-negative)' },
		postponed: { label: 'Postponed', color: 'var(--color-text-tertiary)' },
		implemented: { label: 'Implemented', color: 'var(--color-accent-positive)' }
	};

	let showRip = $state(false);
</script>

<svelte:head>
	<title>{data.title} — Lab — claude-1337</title>
</svelte:head>

<main class="proposal-page">
	<nav class="breadcrumb">
		<a href="/lab">Lab</a>
		<span class="sep">/</span>
		<span class="current">REP-{data.id}</span>
	</nav>

	<header class="proposal-header">
		<div class="meta-row">
			<span class="proposal-id">REP-{data.id}</span>
			<span
				class="status-badge"
				style="--badge-color: {statusConfig[data.status]?.color || 'var(--color-text-muted)'}"
			>
				{statusConfig[data.status]?.label || data.status}
			</span>
		</div>

		{#if data.created || data.authors}
			<div class="meta-info">
				{#if data.created}
					<span class="meta-item">Created: {data.created}</span>
				{/if}
				{#if data.authors}
					<span class="meta-item">Authors: {data.authors}</span>
				{/if}
			</div>
		{/if}

		<!-- Linked artifacts -->
		<div class="artifact-links">
			{#if data.rip}
				<button class="artifact-link" class:active={showRip} onclick={() => showRip = !showRip}>
					RIP-{data.id}
				</button>
			{/if}
			{#if data.experimentSlug}
				<a href="/lab/experiments/{data.experimentSlug}" class="artifact-link">
					Experiment
				</a>
			{/if}
			{#if data.findingsSlug}
				<a href="/lab/findings/{data.findingsSlug}" class="artifact-link primary">
					Findings
				</a>
			{/if}
		</div>
	</header>

	<article class="proposal-content markdown-content">
		{@html proposalHtml}
	</article>

	{#if data.rip && showRip}
		<article id="implementation" class="rip-content markdown-content">
			<h2 class="rip-heading">Research Implementation Plan (RIP-{data.id})</h2>
			{@html ripHtml}
		</article>
	{/if}

	<footer class="proposal-footer">
		<a href="/lab" class="back-link">← Back to Lab</a>
	</footer>
</main>

<style>
	.proposal-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 800px;
		margin: 0 auto;
	}

	.breadcrumb {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-6);
	}

	.breadcrumb a {
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.breadcrumb a:hover {
		color: var(--color-accent);
	}

	.breadcrumb .sep {
		margin: 0 var(--space-2);
		opacity: 0.5;
	}

	.breadcrumb .current {
		color: var(--color-text-tertiary);
	}

	.proposal-header {
		margin-bottom: var(--space-8);
		padding-bottom: var(--space-6);
		border-bottom: 1px solid var(--color-border);
	}

	.meta-row {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-3);
	}

	.proposal-id {
		font-family: var(--font-mono);
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
	}

	.status-badge {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--badge-color);
		background: color-mix(in srgb, var(--badge-color) 15%, transparent);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.meta-info {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-4);
		margin-bottom: var(--space-4);
	}

	.meta-item {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.artifact-links {
		display: flex;
		gap: var(--space-2);
	}

	.artifact-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-md);
		text-decoration: none;
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.artifact-link:hover,
	.artifact-link.active {
		background: var(--color-accent-muted);
		border-color: var(--color-accent);
	}

	.artifact-link.primary {
		background: var(--color-accent);
		color: var(--color-bg);
		border-color: var(--color-accent);
	}

	.artifact-link.primary:hover {
		opacity: 0.9;
	}

	/* Markdown content styling */
	.markdown-content {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-8);
	}

	.markdown-content :global(h1) {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-3);
		border-bottom: 2px solid var(--color-border);
	}

	.markdown-content :global(h2) {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-8);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.markdown-content :global(h3) {
		font-size: var(--text-base);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.markdown-content :global(p) {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.markdown-content :global(strong) {
		color: var(--color-text-primary);
		font-weight: var(--font-semibold);
	}

	.markdown-content :global(ul),
	.markdown-content :global(ol) {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	.markdown-content :global(li) {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-2);
	}

	.markdown-content :global(blockquote) {
		border-left: 3px solid var(--color-accent);
		padding-left: var(--space-4);
		margin: var(--space-4) 0;
		color: var(--color-text-tertiary);
		font-style: italic;
	}

	.markdown-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-surface);
		padding: 2px var(--space-1);
		border-radius: var(--radius-sm);
	}

	.markdown-content :global(pre) {
		background: var(--color-bg-surface);
		padding: var(--space-4);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--space-4) 0;
	}

	.markdown-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.markdown-content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-4) 0;
	}

	.markdown-content :global(th),
	.markdown-content :global(td) {
		text-align: left;
		padding: var(--space-2) var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.markdown-content :global(th) {
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.markdown-content :global(td) {
		color: var(--color-text-secondary);
	}

	.markdown-content :global(a) {
		color: var(--color-accent);
		text-decoration: none;
	}

	.markdown-content :global(a:hover) {
		text-decoration: underline;
	}

	/* IMP section */
	.rip-content {
		margin-top: var(--space-8);
		border-color: var(--color-accent);
	}

	.rip-heading {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-accent);
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-3);
		border-bottom: 2px solid var(--color-accent);
	}

	.proposal-footer {
		margin-top: var(--space-8);
		padding-top: var(--space-4);
	}

	.back-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-decoration: none;
	}

	.back-link:hover {
		color: var(--color-accent);
	}

	@media (max-width: 640px) {
		.proposal-page {
			padding-top: 100px;
		}

		.markdown-content {
			padding: var(--space-5);
		}

		.artifact-links {
			flex-wrap: wrap;
		}
	}
</style>
