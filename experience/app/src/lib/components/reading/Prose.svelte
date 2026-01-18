<script lang="ts">
	/**
	 * Prose Component
	 *
	 * Typography styles for rendered markdown content.
	 * Provides consistent heading hierarchy, paragraph spacing,
	 * link styles, code formatting, and list styles.
	 *
	 * Usage:
	 *   <Prose>
	 *     {@html renderedMarkdown}
	 *   </Prose>
	 */
	import type { Snippet } from 'svelte';

	let {
		children,
		class: className = ''
	}: {
		children: Snippet;
		class?: string;
	} = $props();
</script>

<div class="prose {className}">
	{@render children()}
</div>

<style>
	.prose {
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
	}

	/* Headings */
	.prose :global(h1) {
		font-size: var(--text-3xl);
		font-weight: var(--font-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tight);
		margin-top: var(--space-12);
		margin-bottom: var(--space-4);
		color: var(--color-text);
	}

	.prose :global(h2) {
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tight);
		margin-top: var(--space-10);
		margin-bottom: var(--space-4);
		color: var(--color-text);
	}

	.prose :global(h3) {
		font-size: var(--text-xl);
		font-weight: var(--font-semibold);
		line-height: var(--leading-tight);
		margin-top: var(--space-8);
		margin-bottom: var(--space-3);
		color: var(--color-text);
	}

	.prose :global(h4) {
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		line-height: var(--leading-tight);
		margin-top: var(--space-6);
		margin-bottom: var(--space-2);
		color: var(--color-text);
	}

	/* First heading shouldn't have top margin */
	.prose :global(h1:first-child),
	.prose :global(h2:first-child),
	.prose :global(h3:first-child),
	.prose :global(h4:first-child) {
		margin-top: 0;
	}

	/* Paragraphs */
	.prose :global(p) {
		margin-bottom: var(--space-5);
	}

	/* Academic-style paragraph indentation (after first paragraph) */
	.prose :global(p + p) {
		text-indent: 1.5em;
	}

	/* Lead paragraph (first after heading) */
	.prose :global(h1 + p),
	.prose :global(h2 + p),
	.prose :global(h3 + p) {
		text-indent: 0;
	}

	/* Links */
	.prose :global(a) {
		color: var(--color-link);
		text-decoration: underline;
		text-decoration-color: var(--color-accent-muted);
		text-underline-offset: 3px;
		transition:
			color var(--duration-fast) var(--ease-out),
			text-decoration-color var(--duration-fast) var(--ease-out);
	}

	.prose :global(a:hover) {
		color: var(--color-link-hover);
		text-decoration-color: var(--color-link-hover);
	}

	/* Inline code */
	.prose :global(code) {
		font-family: var(--code-font);
		font-size: var(--code-font-size);
		background: var(--code-bg);
		padding: 0.1em var(--code-padding-inline);
		border: 1px solid var(--code-border);
		border-radius: var(--code-radius);
		color: var(--code-text);
	}

	/* Code blocks */
	.prose :global(pre) {
		margin: var(--space-6) 0;
		padding: var(--space-4);
		background: var(--code-bg);
		border: 1px solid var(--code-border);
		border-radius: var(--radius-md);
		overflow-x: auto;
	}

	.prose :global(pre code) {
		padding: 0;
		background: none;
		border: none;
		font-size: var(--text-sm);
		line-height: var(--leading-normal);
	}

	/* Shiki code block styling */
	.prose :global(pre.shiki) {
		background: var(--code-bg) !important;
		padding: var(--space-4);
		border: 1px solid var(--code-border);
		border-radius: var(--radius-md);
	}

	/* Blockquotes */
	.prose :global(blockquote) {
		margin: var(--space-6) 0;
		padding: var(--space-4) var(--space-5);
		background: var(--blockquote-bg);
		border-left: 3px solid var(--blockquote-border);
		border-radius: 0 var(--radius-md) var(--radius-md) 0;
		color: var(--blockquote-text);
		font-style: italic;
	}

	.prose :global(blockquote p) {
		margin-bottom: 0;
		text-indent: 0;
	}

	.prose :global(blockquote p + p) {
		margin-top: var(--space-3);
		text-indent: 0;
	}

	/* Lists */
	.prose :global(ul),
	.prose :global(ol) {
		margin-bottom: var(--space-5);
		padding-left: var(--space-6);
	}

	.prose :global(li) {
		margin-bottom: var(--space-2);
	}

	.prose :global(li::marker) {
		color: var(--color-text-muted);
	}

	/* Nested lists */
	.prose :global(li > ul),
	.prose :global(li > ol) {
		margin-top: var(--space-2);
		margin-bottom: 0;
	}

	/* Tables */
	.prose :global(table) {
		width: 100%;
		margin: var(--space-6) 0;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.prose :global(th),
	.prose :global(td) {
		padding: var(--table-cell-padding);
		text-align: left;
		border-bottom: 1px solid var(--table-border);
	}

	.prose :global(th) {
		font-weight: var(--font-semibold);
		color: var(--color-text);
		background: var(--table-header-bg);
	}

	.prose :global(tr:hover td) {
		background: var(--table-row-hover);
	}

	/* Horizontal rules */
	.prose :global(hr) {
		border: none;
		height: 1px;
		background: var(--color-border);
		margin: var(--space-10) 0;
	}

	/* Images */
	.prose :global(img) {
		max-width: 100%;
		height: auto;
		margin: var(--space-6) 0;
		border-radius: var(--radius-md);
	}

	/* Figures */
	.prose :global(figure) {
		margin: var(--space-8) 0;
	}

	.prose :global(figcaption) {
		margin-top: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-align: center;
	}

	/* Strong and emphasis */
	.prose :global(strong) {
		font-weight: var(--font-semibold);
		color: var(--color-text);
	}

	.prose :global(em) {
		font-style: italic;
	}

	/* Abbreviations */
	.prose :global(abbr[title]) {
		text-decoration: underline dotted;
		cursor: help;
	}

	/* Small text */
	.prose :global(small) {
		font-size: var(--text-sm);
	}

	/* Keyboard */
	.prose :global(kbd) {
		font-family: var(--font-mono);
		font-size: 0.85em;
		padding: 0.1em 0.4em;
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-sm);
		box-shadow: 0 1px 0 var(--color-border-strong);
	}
</style>
