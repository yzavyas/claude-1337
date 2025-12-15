<script>
  import { onMount } from 'svelte';

  export let plugins = [];
  export let format = 'cards'; // 'cards' | 'list'

  let searchTerm = '';
  let selectedComponent = 'all';
  let expandedPlugin = null;
  let copiedPlugin = null;

  // Component types for filtering
  const componentTypes = ['all', 'skills', 'hooks', 'agents', 'commands', 'mcp'];

  $: filteredPlugins = plugins.filter(plugin => {
    const matchesSearch = !searchTerm ||
      plugin.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      plugin.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (plugin.keywords || []).some(k => k.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesComponent = selectedComponent === 'all' ||
      (plugin.components && plugin.components.includes(selectedComponent));

    return matchesSearch && matchesComponent;
  });

  function toggleExpand(pluginName) {
    expandedPlugin = expandedPlugin === pluginName ? null : pluginName;
  }

  async function copyInstallCommand(pluginName) {
    const command = `/plugin install ${pluginName}@claude-1337`;
    try {
      await navigator.clipboard.writeText(command);
      copiedPlugin = pluginName;
      setTimeout(() => copiedPlugin = null, 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  }
</script>

<div class="plugin-catalog">
  {#if format === 'cards'}
    <div class="controls">
      <input
        type="text"
        placeholder="search plugins, keywords..."
        bind:value={searchTerm}
        class="search-input"
      />

      <div class="component-filter">
        {#each componentTypes as component}
          <button
            class="component-btn"
            class:active={selectedComponent === component}
            on:click={() => selectedComponent = component}
          >
            {component}
          </button>
        {/each}
      </div>
    </div>

    <div class="plugin-grid">
      {#each filteredPlugins as plugin}
        <div class="plugin-card" class:expanded={expandedPlugin === plugin.name}>
          <div class="plugin-header" on:click={() => toggleExpand(plugin.name)}>
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
                <span class="keyword">{keyword}</span>
              {/each}
            </div>
          {/if}

          {#if expandedPlugin === plugin.name}
            <div class="plugin-details">
              <button
                class="copy-btn"
                class:copied={copiedPlugin === plugin.name}
                on:click|stopPropagation={() => copyInstallCommand(plugin.name)}
              >
                {copiedPlugin === plugin.name ? '✓ copied' : 'copy install command'}
              </button>

              {#if plugin.keywords && plugin.keywords.length > 3}
                <div class="all-keywords">
                  {#each plugin.keywords.slice(3) as keyword}
                    <span class="keyword">{keyword}</span>
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
          <a href={`/claude-1337/reference/${plugin.name}/`}>{plugin.name}</a>
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

  .search-input {
    width: 100%;
    padding: 0.875rem 1.25rem;
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    font-size: 0.95rem;
    background: var(--bg-alt);
    border: 2px solid var(--fg-dim);
    border-radius: 6px;
    margin-bottom: 1.25rem;
    transition: all 0.3s ease;
    color: var(--fg);
  }

  .search-input::placeholder {
    color: var(--fg-dim);
    opacity: 0.6;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--green);
    background: var(--bg);
    box-shadow: 0 0 0 3px rgba(158, 206, 106, 0.1), 0 0 12px rgba(158, 206, 106, 0.3);
    transform: translateY(-1px);
  }

  .component-filter {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .component-btn {
    padding: 0.625rem 1.25rem;
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    font-size: 0.875rem;
    background: rgba(26, 26, 26, 0.5);
    border: 2px solid var(--fg-dim);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: lowercase;
    color: var(--fg-dim);
    position: relative;
    overflow: hidden;
  }

  .component-btn::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--green);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .component-btn:hover {
    border-color: var(--green);
    color: var(--green);
    background: rgba(34, 34, 34, 0.8);
    transform: translateY(-1px);
  }

  .component-btn:hover::after {
    transform: translateX(0);
  }

  .component-btn.active {
    background: rgba(34, 34, 34, 0.9);
    color: var(--green);
    border-color: var(--green);
    text-shadow: 0 0 8px rgba(158, 206, 106, 0.5);
    box-shadow: 0 0 12px rgba(158, 206, 106, 0.15);
  }

  .component-btn.active::after {
    transform: translateX(0);
  }

  .components {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
  }

  .component-badge {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    background: rgba(26, 26, 26, 0.6);
    border: 1px solid rgba(158, 206, 106, 0.4);
    border-radius: 4px;
    color: var(--green);
    text-shadow: 0 0 8px rgba(158, 206, 106, 0.5);
    text-transform: lowercase;
    transition: all 0.2s ease;
  }

  .component-badge:hover {
    background: rgba(158, 206, 106, 0.1);
    border-color: var(--green);
    text-shadow: 0 0 10px rgba(158, 206, 106, 0.7);
  }

  .plugin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .plugin-card {
    padding: 1.5rem;
    background: var(--bg-alt);
    border: 1px solid var(--fg-dim);
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
    background: linear-gradient(90deg, transparent, var(--green), transparent);
    transition: left 0.5s ease;
  }

  .plugin-card:hover::before {
    left: 100%;
  }

  .plugin-card:hover {
    border-color: var(--green);
    background: rgba(34, 34, 34, 0.8);
    box-shadow: 0 4px 20px rgba(158, 206, 106, 0.15);
    transform: translateY(-2px);
  }

  .plugin-card.expanded {
    border-color: var(--green);
    background: rgba(34, 34, 34, 0.9);
    box-shadow: 0 8px 24px rgba(158, 206, 106, 0.2);
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
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    color: var(--fg);
  }

  .expand-icon {
    font-size: 1.5rem;
    color: var(--green);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-shadow: 0 0 8px rgba(158, 206, 106, 0.5);
  }

  .plugin-card:hover .expand-icon {
    transform: rotate(90deg);
    text-shadow: 0 0 12px rgba(158, 206, 106, 0.7);
  }

  .plugin-card.expanded .expand-icon {
    transform: rotate(180deg);
  }

  .plugin-desc {
    font-size: 0.9rem;
    color: var(--fg-dim);
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
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    background: rgba(26, 26, 26, 0.5);
    border: 1px solid rgba(200, 200, 200, 0.2);
    border-radius: 3px;
    color: var(--fg-dim);
  }

  .plugin-details {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
    animation: slideDown 0.3s ease;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .copy-btn {
    padding: 0.5rem 1rem;
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
    font-size: 0.85rem;
    background: rgba(26, 26, 26, 0.8);
    color: var(--green);
    border: 1px solid var(--green);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.75rem;
  }

  .copy-btn:hover {
    background: var(--green);
    color: var(--bg);
    box-shadow: 0 0 12px rgba(158, 206, 106, 0.4);
  }

  .copy-btn.copied {
    background: var(--green);
    color: var(--bg);
    text-shadow: none;
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
    font-style: italic;
  }

  .plugin-list {
    list-style: none;
    padding: 0;
  }

  .plugin-list li {
    margin-bottom: 0.75rem;
    font-family: ui-monospace, 'SF Mono', 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, monospace;
  }

  .plugin-list a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid var(--fg-dim);
    transition: border-color 0.2s;
  }

  .plugin-list a:hover {
    border-bottom-color: var(--green);
    text-shadow: 0 0 8px rgba(158, 206, 106, 0.4);
  }
</style>
