<script lang="ts">
	import { marked } from 'marked';

	let { data } = $props();

	marked.setOptions({ gfm: true, breaks: false });

	const htmlContent = $derived(marked.parse(data.content));
</script>

<svelte:head>
	<title>{data.title} — Lab — claude-1337</title>
</svelte:head>

<main class="findings-page">
	<nav class="breadcrumb">
		<a href="/lab">Lab</a>
		<span class="sep">/</span>
		<span class="current">REP-{data.repId} Findings</span>
	</nav>

	<header class="findings-header">
		<div class="meta-row">
			<span class="rep-id">REP-{data.repId}</span>
			{#if data.status}
				<span class="status-badge">{data.status}</span>
			{/if}
		</div>

		{#if data.date}
			<div class="meta-info">
				<span class="date">Published: {data.date}</span>
			</div>
		{/if}

		<div class="artifact-links">
			{#if data.proposalSlug}
				<a href="/lab/proposals/{data.proposalSlug}" class="artifact-link">
					View Proposal
				</a>
			{/if}
			{#if data.experimentSlug}
				<a href="/lab/experiments/{data.experimentSlug}" class="artifact-link">
					View Experiment
				</a>
			{/if}
		</div>
	</header>

	<article class="findings-content markdown-content">
		{@html htmlContent}
	</article>

	<footer class="findings-footer">
		<a href="/lab" class="back-link">← Back to Lab</a>
	</footer>
</main>

<style>
	.findings-page {
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

	.findings-header {
		margin-bottom: var(--space-8);
		padding-bottom: var(--space-6);
		border-bottom: 2px solid var(--color-accent);
	}

	.meta-row {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-3);
	}

	.rep-id {
		font-family: var(--font-mono);
		font-size: var(--text-lg);
		color: var(--color-accent);
	}

	.status-badge {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-accent-positive);
		background: color-mix(in srgb, var(--color-accent-positive) 15%, transparent);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.meta-info {
		margin-bottom: var(--space-4);
	}

	.date {
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
		color: var(--color-text-secondary);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-md);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.artifact-link:hover {
		background: var(--color-bg-elevated);
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.markdown-content {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-accent);
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

	.markdown-content :global(hr) {
		border: none;
		border-top: 1px solid var(--color-border-subtle);
		margin: var(--space-8) 0;
	}

	.markdown-content :global(em) {
		color: var(--color-text-tertiary);
	}

	.findings-footer {
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
		.findings-page {
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
