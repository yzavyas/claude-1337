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
						<h3>
							<span class="bracket">[</span>{plugin.name}<span class="bracket">]</span>
						</h3>
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
			<p class="no-results">
				<span class="error-prompt">[!]</span> no plugins match your search.
			</p>
		{/if}
	{:else}
		<ul class="plugin-list">
			{#each filteredPlugins as plugin}
				<li>
					<a href={`/claude-1337/explore/reference/${plugin.name}/`}>{plugin.name}</a>
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
		margin: 2rem 0;
	}

	.controls {
		margin-bottom: 2rem;
	}

	.search-wrapper {
		position: relative;
		display: flex;
		align-items: center;
		margin-bottom: 1.25rem;
	}

	.search-prompt {
		position: absolute;
		left: 1rem;
		color: var(--accent);
		text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
		font-family: 'Courier New', monospace;
		font-size: 1rem;
		pointer-events: none;
		z-index: 1;
	}

	.search-input {
		width: 100%;
		padding: 0.875rem 1.25rem 0.875rem 2.5rem;
		font-family: 'Courier New', monospace;
		font-size: 0.95rem;
		background: var(--bg-alt);
		border: 2px solid var(--green);
		box-shadow: 0 0 10px var(--glow);
		transition: all 0.3s ease;
		color: var(--green);
	}

	.search-input::placeholder {
		color: var(--fg-dim);
		opacity: 0.6;
	}

	.search-input:focus {
		outline: none;
		border-color: var(--green);
		background: var(--bg);
		box-shadow: 0 0 20px var(--glow-strong), 0 0 30px var(--glow), inset 0 0 10px rgba(0, 255, 65, 0.1);
		text-shadow: 0 0 5px var(--glow);
	}

	.component-filter {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.component-btn {
		padding: 0.5rem 1rem;
		font-family: 'Courier New', monospace;
		font-size: 0.875rem;
		background: var(--bg-alt);
		border: 2px solid var(--fg-dim);
		cursor: pointer;
		transition: all 0.25s ease;
		text-transform: lowercase;
		color: var(--fg-dim);
		position: relative;
	}

	.component-btn:hover {
		border-color: var(--green);
		color: var(--green);
		background: var(--bg);
		box-shadow: 0 0 15px var(--glow);
		text-shadow: 0 0 8px var(--glow-strong);
	}

	.component-btn.active {
		background: var(--bg);
		color: var(--green);
		border-color: var(--green);
		text-shadow: 0 0 10px var(--glow-strong);
		box-shadow: 0 0 20px var(--glow-strong), inset 0 0 15px rgba(0, 255, 65, 0.1);
	}

	.components {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		margin-bottom: 0.75rem;
	}

	.component-badge {
		padding: 0.3rem 0.6rem;
		font-size: 0.75rem;
		font-family: 'Courier New', monospace;
		background: rgba(0, 255, 65, 0.1);
		border: 1px solid var(--green);
		color: var(--green);
		text-shadow: 0 0 5px var(--glow);
		text-transform: lowercase;
		transition: all 0.2s ease;
	}

	.component-badge:hover {
		background: rgba(0, 255, 65, 0.2);
		box-shadow: 0 0 10px var(--glow-strong);
		text-shadow: 0 0 8px var(--glow-strong);
	}

	.plugin-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
	}

	.plugin-card {
		padding: 1.5rem;
		background: var(--bg-alt);
		border: 2px solid var(--green);
		box-shadow: 0 0 15px var(--glow);
		transition: all 0.3s ease;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.plugin-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 2px;
		background: linear-gradient(
			90deg,
			transparent,
			var(--accent),
			var(--green),
			var(--accent),
			transparent
		);
		transition: left 0.6s ease;
		box-shadow: 0 0 10px var(--accent);
	}

	.plugin-card:hover::before {
		left: 100%;
	}

	.plugin-card:hover {
		border-color: var(--green);
		background: var(--bg);
		box-shadow: 0 0 30px var(--glow-strong), 0 0 50px var(--glow),
			inset 0 0 20px rgba(0, 255, 65, 0.05);
		transform: translateY(-4px);
	}

	.plugin-card.expanded {
		border-color: var(--accent);
		background: var(--bg);
		box-shadow: 0 0 40px var(--glow-strong), 0 0 60px var(--glow),
			inset 0 0 25px rgba(0, 255, 65, 0.1);
	}

	.plugin-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.75rem;
	}

	.plugin-header h3 {
		margin: 0;
		font-size: 1.1rem;
		font-family: 'Courier New', monospace;
		color: var(--green);
		text-shadow: 0 0 10px var(--glow-strong);
		font-weight: bold;
	}

	.bracket {
		color: var(--accent);
		text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
	}

	.expand-icon {
		font-size: 1.5rem;
		color: var(--accent);
		transition: all 0.3s ease;
		text-shadow: 0 0 10px rgba(0, 255, 255, 0.6);
	}

	.plugin-card:hover .expand-icon {
		transform: scale(1.2);
		text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
	}

	.plugin-card.expanded .expand-icon {
		transform: rotate(180deg);
		color: var(--green);
		text-shadow: 0 0 15px var(--glow-strong);
	}

	.plugin-desc {
		font-size: 0.9rem;
		color: var(--fg);
		margin-bottom: 0.75rem;
		line-height: 1.5;
	}

	.keywords {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		margin-bottom: 0.5rem;
	}

	.keyword {
		padding: 0.25rem 0.5rem;
		font-size: 0.75rem;
		font-family: 'Courier New', monospace;
		background: rgba(0, 255, 65, 0.05);
		border: 1px solid rgba(0, 255, 65, 0.3);
		color: var(--fg-dim);
	}

	.plugin-details {
		margin-top: 1rem;
		padding-top: 1rem;
		border-top: 2px solid var(--green);
		box-shadow: 0 -2px 10px var(--glow);
	}

	.copy-btn {
		padding: 0.5rem 1rem;
		font-family: 'Courier New', monospace;
		font-size: 0.85rem;
		background: var(--bg-alt);
		color: var(--green);
		border: 2px solid var(--green);
		cursor: pointer;
		transition: all 0.2s ease;
		margin-bottom: 0.75rem;
		text-shadow: 0 0 5px var(--glow);
		box-shadow: 0 0 10px var(--glow);
	}

	.copy-btn:hover {
		background: var(--green);
		color: var(--bg);
		box-shadow: 0 0 25px var(--glow-strong), 0 0 35px var(--glow);
		text-shadow: none;
		transform: translateY(-2px);
	}

	.copy-btn.copied {
		background: var(--accent);
		color: var(--bg);
		border-color: var(--accent);
		text-shadow: none;
		box-shadow: 0 0 25px rgba(0, 255, 255, 0.8);
	}

	.all-keywords {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.no-results {
		text-align: center;
		color: var(--fg-dim);
		padding: 2rem;
		font-family: 'Courier New', monospace;
	}

	.error-prompt {
		color: var(--red);
		text-shadow: 0 0 10px rgba(255, 0, 85, 0.8);
		margin-right: 0.5rem;
	}

	.plugin-list {
		list-style: none;
		padding: 0;
	}

	.plugin-list li {
		margin-bottom: 0.75rem;
		font-family: 'Courier New', monospace;
	}

	.plugin-list a {
		color: var(--accent);
		text-decoration: none;
		border-bottom: 1px solid var(--fg-dim);
		transition: all 0.2s ease;
	}

	.plugin-list a:hover {
		border-bottom-color: var(--green);
		text-shadow: 0 0 8px var(--glow-strong);
		color: var(--green);
	}
</style>
