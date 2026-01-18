<script lang="ts">
	import { base } from '$app/paths';
	import { marked } from 'marked';

	let { data } = $props();

	// Rewrite internal links in the HTML output to include base path
	function rewriteLinks(html: string): string {
		// Replace href="/..." with href="{base}/..."
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
	<meta name="description" content="{data.title}" />
</svelte:head>

<main class="content-page">
	{#if breadcrumbs.length > 0}
		<nav class="breadcrumb">
			{#each breadcrumbs as crumb, i}
				<a href={crumb.href}>{crumb.label}</a>
				<span class="separator">/</span>
			{/each}
			<span class="current">{data.title}</span>
		</nav>
	{/if}

	<article class="content">
		{@html htmlContent}
	</article>

	{#if breadcrumbs.length > 0}
		<footer class="page-footer">
			<a href={breadcrumbs[breadcrumbs.length - 1]?.href || base + '/'} class="back-link">
				← Back
			</a>
		</footer>
	{/if}
</main>

<style>
	.content-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 800px;
		margin: 0 auto;
	}

	.breadcrumb {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		margin-bottom: var(--space-8);
	}

	.breadcrumb a {
		color: var(--color-accent);
		text-decoration: none;
	}

	.breadcrumb a:hover {
		text-decoration: underline;
	}

	.separator {
		color: var(--color-text-muted);
	}

	.current {
		color: var(--color-text-secondary);
	}

	.content {
		line-height: var(--leading-relaxed);
	}

	.content :global(h1) {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.content :global(h1 + p) {
		font-size: var(--text-lg);
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-8);
	}

	.content :global(h2) {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-top: var(--space-10);
		margin-bottom: var(--space-4);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.content :global(h3) {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.content :global(p) {
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	.content :global(hr) {
		border: none;
		border-top: 1px solid var(--color-border);
		margin: var(--space-8) 0;
	}

	.content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-6) 0;
		font-size: var(--text-sm);
	}

	.content :global(th) {
		text-align: left;
		padding: var(--space-3);
		border-bottom: 2px solid var(--color-border);
		font-family: var(--font-mono);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		background: var(--color-bg-elevated);
	}

	.content :global(td) {
		padding: var(--space-3);
		border-bottom: 1px solid var(--color-border);
		color: var(--color-text-secondary);
	}

	.content :global(tr:hover td) {
		background: var(--color-bg-surface);
	}

	.content :global(strong) {
		color: var(--color-text-primary);
		font-weight: var(--font-semibold);
	}

	.content :global(em) {
		font-style: italic;
	}

	.content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-surface);
		padding: 0.1em 0.3em;
		border-radius: var(--radius-sm);
	}

	.content :global(pre) {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-4);
		overflow-x: auto;
		margin: var(--space-6) 0;
	}

	.content :global(pre code) {
		background: none;
		padding: 0;
	}

	.content :global(blockquote) {
		border-left: 3px solid var(--color-accent);
		padding-left: var(--space-4);
		margin: var(--space-6) 0;
		color: var(--color-text-tertiary);
		font-style: italic;
	}

	/* Progressive Disclosure — Details/Summary */
	.content :global(details) {
		margin: var(--space-3) 0;
		padding: var(--space-4);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-md);
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.content :global(details:hover) {
		border-color: var(--color-border);
	}

	.content :global(details[open]) {
		border-color: var(--color-accent-muted);
	}

	.content :global(summary) {
		display: flex;
		align-items: flex-start;
		gap: var(--space-3);
		cursor: pointer;
		font-weight: var(--font-normal);
		color: var(--color-text-secondary);
		line-height: var(--leading-snug);
		list-style: none;
	}

	.content :global(summary::-webkit-details-marker) {
		display: none;
	}

	.content :global(summary)::before {
		content: '';
		flex-shrink: 0;
		width: 1.25em;
		height: 1.25em;
		margin-top: 0.1em;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23b8860b'%3E%3Cpath fill-rule='evenodd' d='M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z' clip-rule='evenodd'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: center;
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.content :global(details[open] > summary)::before {
		transform: rotate(90deg);
	}

	.content :global(summary:hover) {
		color: var(--color-text);
	}

	.content :global(summary:focus-visible) {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
		border-radius: var(--radius-sm);
	}

	.content :global(summary strong) {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		color: var(--color-accent);
		white-space: nowrap;
	}

	.content :global(details[open] summary) {
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.content :global(details > p:first-of-type) {
		margin-top: 0;
	}

	.content :global(details > p:last-child) {
		margin-bottom: 0;
	}

	.content :global(details blockquote) {
		margin: var(--space-4) 0 0 0;
		font-size: var(--text-sm);
	}

	.content :global(details + details) {
		margin-top: var(--space-2);
	}

	@media (prefers-reduced-motion: reduce) {
		.content :global(summary)::before {
			transition: none;
		}
	}

	.content :global(ul),
	.content :global(ol) {
		margin: var(--space-4) 0;
		padding-left: var(--space-6);
		color: var(--color-text-secondary);
	}

	.content :global(li) {
		margin-bottom: var(--space-2);
	}

	.content :global(a) {
		color: var(--color-accent);
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	.content :global(a:hover) {
		color: var(--color-accent-hover);
	}

	.page-footer {
		margin-top: var(--space-12);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border);
	}

	.back-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		text-decoration: none;
	}

	.back-link:hover {
		text-decoration: underline;
	}

	@media (max-width: 640px) {
		.content-page {
			padding-top: var(--space-12);
		}

		.content :global(h1) {
			font-size: var(--text-2xl);
		}

		.content :global(table) {
			font-size: var(--text-xs);
		}

		.content :global(th),
		.content :global(td) {
			padding: var(--space-2);
		}
	}
</style>
