<script lang="ts">
	/**
	 * Article Component
	 *
	 * Academic-quality article layout with:
	 * - 65ch max-width for optimal reading
	 * - Font toggle context for sans/serif switching
	 * - Optional aside slot for table of contents
	 * - Semantic HTML structure
	 */
	import type { Snippet } from 'svelte';
	import { setContext } from 'svelte';

	let {
		title,
		subtitle,
		date,
		readingTime,
		children,
		aside,
		class: className = ''
	}: {
		title: string;
		subtitle?: string;
		date?: string;
		readingTime?: string;
		children: Snippet;
		aside?: Snippet;
		class?: string;
	} = $props();

	// Font state for toggle
	let fontFamily = $state<'sans' | 'serif'>('sans');

	// Provide font context for nested components (like FontToggle)
	setContext('article', {
		get fontFamily() {
			return fontFamily;
		},
		toggleFont: () => {
			fontFamily = fontFamily === 'sans' ? 'serif' : 'sans';
		}
	});
</script>

<article class="article {className}" class:serif={fontFamily === 'serif'}>
	<header class="article-header">
		<h1 class="article-title">{title}</h1>
		{#if subtitle}
			<p class="article-subtitle">{subtitle}</p>
		{/if}
		{#if date || readingTime}
			<div class="article-meta">
				{#if date}
					<time datetime={date}>{date}</time>
				{/if}
				{#if date && readingTime}
					<span class="meta-separator" aria-hidden="true">·</span>
				{/if}
				{#if readingTime}
					<span class="reading-time">{readingTime}</span>
				{/if}
			</div>
		{/if}
	</header>

	<div class="article-layout">
		<div class="article-content">
			{@render children()}
		</div>

		{#if aside}
			<aside class="article-aside">
				{@render aside()}
			</aside>
		{/if}
	</div>
</article>

<style>
	.article {
		--content-max: 65ch;
		padding: var(--space-8) var(--page-padding-x);
	}

	.article.serif {
		font-family: var(--font-reading);
	}

	.article-header {
		max-width: var(--content-max);
		margin: 0 auto var(--space-8);
	}

	.article-title {
		font-size: var(--text-3xl);
		line-height: var(--leading-tight);
		letter-spacing: var(--tracking-tight);
		margin-bottom: var(--space-3);
	}

	.article-subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.article-meta {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		margin-top: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.meta-separator {
		opacity: 0.5;
	}

	.article-layout {
		display: grid;
		grid-template-columns: minmax(0, var(--content-max)) 1fr;
		gap: var(--space-12);
		max-width: var(--content-width-full);
		margin: 0 auto;
	}

	.article-content {
		min-width: 0; /* Prevent overflow */
	}

	.article-aside {
		position: sticky;
		top: calc(36px + 52px + var(--space-8)); /* banner + nav + padding */
		align-self: start;
		max-height: calc(100vh - 36px - 52px - var(--space-16));
		overflow-y: auto;
	}

	/* Hide aside on smaller screens */
	@media (max-width: 1024px) {
		.article-layout {
			grid-template-columns: 1fr;
		}

		.article-aside {
			display: none;
		}
	}

	/* Tablet */
	@media (max-width: 768px) {
		.article {
			padding: var(--space-6) var(--page-padding-x);
		}

		.article-title {
			font-size: var(--text-2xl);
		}

		.article-subtitle {
			font-size: var(--text-base);
		}
	}
</style>
