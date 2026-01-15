<script lang="ts">
	import { base } from '$app/paths';
	import { marked } from 'marked';

	let { data } = $props();

	// Rewrite internal links in the HTML output to include base path
	function rewriteLinks(html: string): string {
		return html.replace(/href="\/(?!\/)/g, `href="${base}/`);
	}

	// Configure marked for clean output
	marked.setOptions({
		gfm: true,
		breaks: false
	});

	const htmlContent = $derived(rewriteLinks(marked.parse(data.content) as string));

	// Build breadcrumb links
	function buildBreadcrumbs(parts: string[]) {
		const crumbs: { label: string; href: string }[] = [];
		let path = '';

		for (const part of parts.slice(0, -1)) {
			path += '/' + part;
			crumbs.push({
				label: part.charAt(0).toUpperCase() + part.slice(1).replace(/-/g, ' '),
				href: base + path
			});
		}

		return crumbs;
	}

	const breadcrumbs = $derived(buildBreadcrumbs(data.pathParts));
</script>

<svelte:head>
	<title>{data.title} — claude-1337</title>
</svelte:head>

<div class="content-page">
	{#if breadcrumbs.length > 0}
		<nav class="breadcrumb">
			{#each breadcrumbs as crumb}
				<a href={crumb.href}>{crumb.label}</a>
				<span class="separator">/</span>
			{/each}
			<span class="current">{data.title}</span>
		</nav>
	{/if}

	<article class="prose">
		{@html htmlContent}
	</article>

	{#if breadcrumbs.length > 0}
		<footer>
			<a href={breadcrumbs[breadcrumbs.length - 1]?.href || base + '/'} class="back-link">
				<span class="arrow">&larr;</span>
				<span>Back</span>
			</a>
		</footer>
	{/if}
</div>

<style>
	.content-page {
		padding: var(--space-8) var(--space-4);
		max-width: var(--max-width-prose);
		margin: 0 auto;
	}

	/* Breadcrumb navigation */
	.breadcrumb {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		margin-bottom: var(--space-8);
		color: var(--ink-tertiary);
	}

	.breadcrumb a {
		color: var(--ink-secondary);
	}

	.breadcrumb a:hover {
		color: var(--ink-primary);
	}

	.separator {
		color: var(--ink-subtle);
	}

	.current {
		color: var(--ink-primary);
		font-weight: 500;
	}

	/* Prose styles for markdown content */
	.prose :global(h1) {
		font-size: var(--text-3xl);
		font-weight: 500;
		letter-spacing: var(--tracking-tight);
		margin-bottom: var(--space-4);
	}

	.prose :global(h2) {
		font-size: var(--text-2xl);
		font-weight: 500;
		letter-spacing: var(--tracking-tight);
		margin-top: var(--space-10);
		margin-bottom: var(--space-4);
		padding-top: var(--space-6);
		border-top: 1px solid var(--border-subtle);
	}

	.prose :global(h3) {
		font-size: var(--text-xl);
		font-weight: 500;
		margin-top: var(--space-8);
		margin-bottom: var(--space-3);
	}

	.prose :global(h4) {
		font-size: var(--text-lg);
		font-weight: 500;
		margin-top: var(--space-6);
		margin-bottom: var(--space-2);
	}

	.prose :global(p) {
		margin-bottom: var(--space-4);
		color: var(--ink-secondary);
		max-width: var(--measure-normal);
	}

	.prose :global(strong) {
		font-weight: 600;
		color: var(--ink-primary);
	}

	.prose :global(em) {
		font-style: italic;
	}

	/* Lists */
	.prose :global(ul),
	.prose :global(ol) {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	.prose :global(li) {
		margin-bottom: var(--space-2);
		color: var(--ink-secondary);
	}

	.prose :global(li::marker) {
		color: var(--ink-tertiary);
	}

	/* Tables */
	.prose :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-6) 0;
		font-size: var(--text-sm);
	}

	.prose :global(th),
	.prose :global(td) {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--border-subtle);
		text-align: left;
	}

	.prose :global(th) {
		font-weight: 600;
		color: var(--ink-primary);
		background: var(--surface-subtle);
	}

	.prose :global(td) {
		color: var(--ink-secondary);
	}

	/* Code */
	.prose :global(code) {
		font-family: var(--font-mono);
		font-size: 0.875em;
		background: var(--surface-sunken);
		padding: 0.15em 0.4em;
		border-radius: var(--radius-sm);
	}

	.prose :global(pre) {
		background: var(--surface-sunken);
		padding: var(--space-4);
		overflow-x: auto;
		margin: var(--space-6) 0;
		border-radius: var(--radius-md);
		font-size: var(--text-sm);
	}

	.prose :global(pre code) {
		background: none;
		padding: 0;
		font-size: inherit;
	}

	/* Blockquotes */
	.prose :global(blockquote) {
		border-left: 3px solid var(--border-strong);
		padding-left: var(--space-4);
		margin: var(--space-6) 0;
		color: var(--ink-tertiary);
		font-style: italic;
	}

	.prose :global(blockquote p) {
		color: inherit;
	}

	/* Links */
	.prose :global(a) {
		color: var(--ink-primary);
		text-decoration: underline;
		text-underline-offset: 2px;
		text-decoration-thickness: 1px;
	}

	.prose :global(a:hover) {
		text-decoration-thickness: 2px;
	}

	/* Horizontal rules */
	.prose :global(hr) {
		border: none;
		border-top: 1px solid var(--border-subtle);
		margin: var(--space-8) 0;
	}

	/* Footer */
	footer {
		margin-top: var(--space-12);
		padding-top: var(--space-6);
		border-top: 1px solid var(--border-subtle);
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		color: var(--ink-secondary);
		transition: color var(--duration-fast) var(--ease-out);
	}

	.back-link:hover {
		color: var(--ink-primary);
	}

	.back-link .arrow {
		transition: transform var(--duration-normal) var(--ease-spring);
	}

	.back-link:hover .arrow {
		transform: translateX(-4px);
	}
</style>
