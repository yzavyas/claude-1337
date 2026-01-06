<script lang="ts">
	import { fade, fly } from 'svelte/transition';

	interface Plugin {
		name: string;
		description: string;
		components?: string[];
		keywords?: string[];
	}

	interface Props {
		plugins: Plugin[];
		format?: 'cards' | 'list';
	}

	let { plugins = [], format = 'cards' }: Props = $props();

	let searchTerm = $state('');
	let selectedComponent = $state('all');
	let expandedPlugin = $state<string | null>(null);
	let copiedPlugin = $state<string | null>(null);

	// Component types for filtering
	const componentTypes = ['all', 'skills', 'hooks', 'agents', 'commands', 'mcp'];

	const filteredPlugins = $derived(
		plugins.filter((plugin) => {
			const matchesSearch =
				!searchTerm ||
				plugin.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
				plugin.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
				(plugin.keywords || []).some((k) => k.toLowerCase().includes(searchTerm.toLowerCase()));

			const matchesComponent =
				selectedComponent === 'all' ||
				(plugin.components && plugin.components.includes(selectedComponent));

			return matchesSearch && matchesComponent;
		})
	);

	function toggleExpand(pluginName: string) {
		expandedPlugin = expandedPlugin === pluginName ? null : pluginName;
	}

	async function copyInstallCommand(pluginName: string) {
		const command = `/plugin install ${pluginName}@claude-1337`;
		try {
			await navigator.clipboard.writeText(command);
			copiedPlugin = pluginName;
			setTimeout(() => (copiedPlugin = null), 2000);
		} catch (err) {
			console.error('Failed to copy:', err);
		}
	}
</script>

<div class="plugin-catalog">
	{#if format === 'cards'}
		<div class="controls">
			<div class="search-wrapper">
				<span class="search-prompt">$</span>
				<input
					type="text"
					placeholder="search plugins, keywords..."
					bind:value={searchTerm}
					class="search-input"
				/>
			</div>

			<div class="component-filter">
				{#each componentTypes as component}
					<button
						class="component-btn"
						class:active={selectedComponent === component}
						onclick={() => (selectedComponent = component)}
					>
						[{component}]
					</button>
				{/each}
			</div>
		</div>

		<div class="plugin-grid">
			{#each filteredPlugins as plugin, i}
				<div
					class="plugin-card"
					class:expanded={expandedPlugin === plugin.name}
					in:fly={{ y: 20, duration: 300, delay: i * 50 }}
				>
					<div class="plugin-header" onclick={() => toggleExpand(plugin.name)} role="button" tabindex="0">
						<h3>{plugin.name}</h3>
						<span class="expand-icon">{expandedPlugin === plugin.name ? '−' : '+'}</span>
					</div>

					<p class="plugin-desc">{plugin.description}</p>

					{#if plugin.components && plugin.components.length > 0}
						<div class="components">
							{#each plugin.components as component}
								<span class="component-badge" data-component={component}>
									{component}
								</span>
							{/each}
						</div>
					{/if}

					{#if plugin.keywords && plugin.keywords.length > 0}
						<div class="keywords">
							{#each plugin.keywords.slice(0, 3) as keyword}
								<span class="keyword">#{keyword}</span>
							{/each}
						</div>
					{/if}

					{#if expandedPlugin === plugin.name}
						<div class="plugin-details" transition:fade={{ duration: 200 }}>
							<button
								class="copy-btn"
								class:copied={copiedPlugin === plugin.name}
								onclick={(e) => {
									e.stopPropagation();
									copyInstallCommand(plugin.name);
								}}
							>
								{copiedPlugin === plugin.name ? '✓ copied!' : '> copy install command'}
							</button>

							{#if plugin.keywords && plugin.keywords.length > 3}
								<div class="all-keywords">
									{#each plugin.keywords.slice(3) as keyword}
										<span class="keyword">#{keyword}</span>
									{/each}
								</div>
							{/if}
						</div>
					{/if}
				</div>
			{/each}
		</div>

		{#if filteredPlugins.length === 0}
			<p class="no-results">no plugins match your search.</p>
		{/if}
	{:else}
		<ul class="plugin-list">
			{#each filteredPlugins as plugin}
				<li>
					<a href={`/explore/reference/${plugin.name}/`}>{plugin.name}</a>
					{#if plugin.keywords}
						— {plugin.keywords.slice(0, 4).join(', ')}
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.plugin-catalog {
		width: 100%;
	}

	.controls {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
		margin-bottom: var(--space-xl);
	}

	.search-wrapper {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		background: var(--bg-surface);
		border: 1px solid var(--border-default);
		border-radius: var(--radius-md);
		padding: var(--space-sm) var(--space-md);
		transition: border-color var(--transition-fast);
	}

	.search-wrapper:focus-within {
		border-color: var(--accent);
	}

	.search-prompt {
		font-family: var(--font-mono);
		font-size: 0.9rem;
		color: var(--accent);
		font-weight: 500;
	}

	.search-input {
		flex: 1;
		background: transparent;
		border: none;
		font-family: var(--font-mono);
		font-size: 0.9rem;
		color: var(--text-primary);
		outline: none;
	}

	.search-input::placeholder {
		color: var(--text-muted);
	}

	.component-filter {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs);
	}

	.component-btn {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--text-secondary);
		background: transparent;
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-sm);
		padding: var(--space-xs) var(--space-sm);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.component-btn:hover {
		border-color: var(--border-default);
		color: var(--text-primary);
	}

	.component-btn.active {
		background: var(--accent-muted);
		border-color: var(--accent);
		color: var(--accent);
	}

	.plugin-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: var(--space-md);
	}

	.plugin-card {
		background: var(--bg-surface);
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-md);
		padding: var(--space-md);
		transition: all var(--transition-fast);
	}

	.plugin-card:hover {
		border-color: var(--border-default);
	}

	.plugin-card.expanded {
		border-color: var(--accent);
	}

	.plugin-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		cursor: pointer;
		margin-bottom: var(--space-sm);
	}

	.plugin-header h3 {
		font-family: var(--font-mono);
		font-size: 0.95rem;
		font-weight: 500;
		color: var(--text-primary);
		margin: 0;
	}

	.expand-icon {
		font-family: var(--font-mono);
		color: var(--text-muted);
		font-size: 1.1rem;
		line-height: 1;
	}

	.plugin-desc {
		font-size: 0.85rem;
		color: var(--text-secondary);
		line-height: 1.5;
		margin: 0 0 var(--space-sm) 0;
	}

	.components {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs);
		margin-bottom: var(--space-sm);
	}

	.component-badge {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		padding: 2px 6px;
		border-radius: var(--radius-sm);
		background: var(--bg-elevated);
		color: var(--text-secondary);
		border: 1px solid var(--border-subtle);
	}

	.component-badge[data-component="skills"] {
		border-color: #4ade80;
		color: #4ade80;
	}

	.component-badge[data-component="hooks"] {
		border-color: #60a5fa;
		color: #60a5fa;
	}

	.component-badge[data-component="agents"] {
		border-color: #f472b6;
		color: #f472b6;
	}

	.component-badge[data-component="commands"] {
		border-color: #fbbf24;
		color: #fbbf24;
	}

	.component-badge[data-component="mcp"] {
		border-color: #a78bfa;
		color: #a78bfa;
	}

	.keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs);
	}

	.keyword {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		color: var(--text-muted);
	}

	.plugin-details {
		margin-top: var(--space-md);
		padding-top: var(--space-md);
		border-top: 1px solid var(--border-subtle);
	}

	.copy-btn {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--text-secondary);
		background: var(--bg-elevated);
		border: 1px solid var(--border-default);
		border-radius: var(--radius-sm);
		padding: var(--space-sm) var(--space-md);
		cursor: pointer;
		transition: all var(--transition-fast);
		width: 100%;
	}

	.copy-btn:hover {
		background: var(--accent-muted);
		border-color: var(--accent);
		color: var(--accent);
	}

	.copy-btn.copied {
		background: rgba(74, 222, 128, 0.1);
		border-color: #4ade80;
		color: #4ade80;
	}

	.all-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-xs);
		margin-top: var(--space-sm);
	}

	.no-results {
		font-family: var(--font-mono);
		font-size: 0.9rem;
		color: var(--text-muted);
		text-align: center;
		padding: var(--space-xl);
	}

	.plugin-list {
		list-style: none;
		padding: 0;
	}

	.plugin-list li {
		font-family: var(--font-mono);
		font-size: 0.9rem;
		color: var(--text-secondary);
		padding: var(--space-sm) 0;
		border-bottom: 1px solid var(--border-subtle);
	}

	.plugin-list a {
		color: var(--link);
		text-decoration: none;
	}

	.plugin-list a:hover {
		color: var(--link-hover);
		text-decoration: underline;
	}

	@media (max-width: 640px) {
		.plugin-grid {
			grid-template-columns: 1fr;
		}

		.component-filter {
			overflow-x: auto;
			flex-wrap: nowrap;
			padding-bottom: var(--space-xs);
		}

		.component-btn {
			flex-shrink: 0;
		}
	}
</style>
