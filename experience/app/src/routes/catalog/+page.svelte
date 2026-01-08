<script lang="ts">
	import CopyCommand from '$lib/components/CopyCommand.svelte';

	let { data } = $props();
	const plugins = data.plugins;

	// Category filter
	let activeCategory = $state<string | null>(null);

	const categories = [...new Set(plugins.map(p => p.category))];

	const filteredPlugins = $derived(
		activeCategory ? plugins.filter(p => p.category === activeCategory) : plugins
	);

	function toggleCategory(cat: string) {
		activeCategory = activeCategory === cat ? null : cat;
	}
</script>

<svelte:head>
	<title>Catalog — claude-1337</title>
	<meta name="description" content="Browse cognitive extensions in the claude-1337 marketplace." />
</svelte:head>

<main class="catalog-page">
	<header class="page-header">
		<h1>Extensions</h1>
		<p class="subtitle">Cognitive extensions for Claude Code</p>
	</header>

	<section class="install-section">
		<p class="install-label">Add marketplace</p>
		<CopyCommand command="/plugin marketplace add yzavyas/claude-1337" />
	</section>

	<nav class="category-filter">
		{#each categories as cat}
			<button
				class="category-chip"
				class:active={activeCategory === cat}
				onclick={() => toggleCategory(cat)}
			>
				{cat}
			</button>
		{/each}
	</nav>

	<section class="plugins-grid">
		{#each filteredPlugins as plugin}
			<article class="plugin-card">
				<header class="plugin-header">
					<h2 class="plugin-name">{plugin.displayName}</h2>
					<span class="plugin-category">{plugin.category}</span>
				</header>
				<p class="plugin-description">{plugin.description}</p>
				<button class="plugin-install" onclick={() => navigator.clipboard.writeText(plugin.name)}>
					<span class="install-name">{plugin.name}</span>
					<span class="install-hint">copy</span>
				</button>
			</article>
		{/each}
	</section>
</main>

<style>
	.catalog-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 1000px;
		margin: 0 auto;
	}

	.page-header {
		text-align: center;
		margin-bottom: var(--space-8);
	}

	.page-header h1 {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.subtitle {
		font-size: var(--text-base);
		color: var(--color-text-tertiary);
	}

	.install-section {
		max-width: 460px;
		margin: 0 auto var(--space-8);
	}

	.install-label {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--color-text-muted);
		margin-bottom: var(--space-2);
	}

	.category-filter {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
		gap: var(--space-2);
		margin-bottom: var(--space-8);
	}

	.category-chip {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		padding: var(--space-2) var(--space-3);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-full);
		color: var(--color-text-muted);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.category-chip:hover {
		border-color: var(--color-accent);
		color: var(--color-text-secondary);
	}

	.category-chip.active {
		background: var(--color-accent-muted);
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.plugins-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: var(--space-4);
	}

	.plugin-card {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.plugin-card:hover {
		border-color: var(--color-accent);
	}

	.plugin-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: var(--space-3);
	}

	.plugin-name {
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.plugin-category {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.plugin-description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.plugin-install {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		margin-top: auto;
		padding: var(--space-2) var(--space-3);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.plugin-install:hover {
		border-color: var(--color-accent);
	}

	.install-name {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-secondary);
	}

	.install-hint {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		opacity: 0;
		transition: opacity var(--duration-fast) var(--ease-out);
	}

	.plugin-install:hover .install-hint {
		opacity: 1;
	}

	@media (max-width: 640px) {
		.catalog-page {
			padding-top: 100px;
		}

		.page-header h1 {
			font-size: var(--text-3xl);
		}

		.plugins-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
