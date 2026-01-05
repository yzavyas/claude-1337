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
