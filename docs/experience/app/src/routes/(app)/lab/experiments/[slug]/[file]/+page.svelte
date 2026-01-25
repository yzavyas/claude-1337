<script lang="ts">
	import { base } from '$app/paths';
	import { marked } from 'marked';

	let { data } = $props();

	marked.setOptions({ gfm: true, breaks: false });

	const htmlContent = $derived(marked.parse(data.content));
</script>

<svelte:head>
	<title>{data.title} — Lab — claude-1337</title>
</svelte:head>

<main class="analysis-page">
	<nav class="breadcrumb">
		<a href="{base}/lab">Lab</a>
		<span class="sep">/</span>
		<a href="{base}/lab/experiments/{data.slug}">{data.slug}</a>
		<span class="sep">/</span>
		<span class="current">Analysis</span>
	</nav>

	<article class="analysis-content">
		{@html htmlContent}
	</article>

	<footer class="analysis-footer">
		<p>Verified with Strawberry | Lab-1337</p>
	</footer>
</main>

<style>
	.analysis-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 800px;
		margin: 0 auto;
	}

	.breadcrumb {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-8);
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

	.analysis-content {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-8);
	}

	/* Markdown styling */
	.analysis-content :global(h1) {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-3);
		border-bottom: 2px solid var(--color-border);
	}

	.analysis-content :global(h2) {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-8);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.analysis-content :global(h3) {
		font-size: var(--text-base);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.analysis-content :global(p) {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.analysis-content :global(strong) {
		color: var(--color-text-primary);
		font-weight: var(--font-semibold);
	}

	.analysis-content :global(ul),
	.analysis-content :global(ol) {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	.analysis-content :global(li) {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-2);
	}

	.analysis-content :global(details) {
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-md);
		padding: var(--space-4);
		margin: var(--space-4) 0;
	}

	.analysis-content :global(summary) {
		font-weight: var(--font-semibold);
		color: var(--color-text-secondary);
		cursor: pointer;
	}

	.analysis-content :global(details[open] summary) {
		margin-bottom: var(--space-3);
	}

	.analysis-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-surface);
		padding: 2px var(--space-1);
		border-radius: var(--radius-sm);
	}

	.analysis-content :global(pre) {
		background: var(--color-bg-surface);
		padding: var(--space-4);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--space-4) 0;
	}

	.analysis-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.analysis-footer {
		text-align: center;
		margin-top: var(--space-8);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border-subtle);
	}

	.analysis-footer p {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	@media (max-width: 640px) {
		.analysis-page {
			padding-top: 100px;
		}

		.analysis-content {
			padding: var(--space-5);
		}
	}
</style>
