<script lang="ts">
	/**
	 * REP Page — Full REP Document View
	 *
	 * Uses REPDocument component to render markdown.
	 * The markdown file IS the source of truth.
	 */
	import { base } from '$app/paths';
	import REPDocument from '$lib/components/lab/REPDocument.svelte';

	let { data } = $props();

	// Extract ID from slug for title (use $derived for reactive state)
	const repId = $derived.by(() => {
		const idMatch = data.slug.match(/^rep-(\d+)/);
		return idMatch?.[1] || '000';
	});
</script>

<svelte:head>
	<title>REP-{repId} — Lab — claude-1337</title>
</svelte:head>

<main class="rep-page">
	<nav class="breadcrumb">
		<a href="{base}/lab">Lab</a>
		<span class="sep">/</span>
		<span class="current">REP-{repId}</span>
	</nav>

	<REPDocument slug={data.slug} markdown={data.markdown} experimentSlug={data.experimentSlug} />

	<footer class="rep-footer">
		<a href="{base}/lab" class="back-link">← Back to Lab</a>
	</footer>
</main>

<style>
	.rep-page {
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

	.rep-footer {
		margin-top: var(--space-10);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.back-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.back-link:hover {
		color: var(--color-accent);
	}

	@media (max-width: 640px) {
		.rep-page {
			padding-top: 100px;
		}
	}
</style>
