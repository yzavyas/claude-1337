<script lang="ts">
	import { page } from '$app/stores';

	interface Props {
		section: string;
		items: Array<{ href: string; label: string }>;
	}

	let { section, items }: Props = $props();
</script>

<aside class="sidebar">
	<nav class="sidebar-nav">
		<div class="section-title">
			<span class="prompt">$</span>
			{section}/
		</div>
		<ul>
			{#each items as item}
				<li>
					<a
						href={item.href}
						class="nav-link"
						class:active={$page.url.pathname === item.href ||
							$page.url.pathname === item.href.replace(/\/$/, '')}
					>
						<span class="file-icon">├─</span>
						{item.label}
					</a>
				</li>
			{/each}
		</ul>
	</nav>
</aside>

<style>
	.sidebar {
		position: fixed;
		left: 0;
		top: 0;
		width: 240px;
		height: 100vh;
		background: var(--bg-alt);
		border-right: 2px solid var(--green);
		box-shadow: 0 0 20px var(--glow);
		padding: 6rem 0 2rem 0;
		overflow-y: auto;
		z-index: 100;
	}

	.sidebar-nav {
		padding: 0 1.5rem;
	}

	.section-title {
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		color: var(--green);
		margin-bottom: 1.5rem;
		font-weight: bold;
		text-shadow: 0 0 10px var(--glow-strong);
		border-bottom: 1px solid var(--green);
		padding-bottom: 0.5rem;
	}

	.prompt {
		color: var(--accent);
		text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
	}

	.sidebar-nav ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.sidebar-nav li {
		margin: 0.25rem 0;
	}

	.nav-link {
		display: flex;
		align-items: center;
		padding: 0.5rem 0.75rem;
		font-family: 'Courier New', monospace;
		font-size: 0.85rem;
		color: var(--fg-dim);
		text-decoration: none;
		transition: all 0.2s ease;
		position: relative;
		border-left: 2px solid transparent;
	}

	.file-icon {
		color: var(--green);
		margin-right: 0.5rem;
		opacity: 0.6;
	}

	.nav-link:hover {
		background: rgba(0, 255, 65, 0.05);
		color: var(--green);
		text-shadow: 0 0 8px var(--glow);
		border-left-color: var(--green);
		padding-left: 1rem;
	}

	.nav-link:hover .file-icon {
		opacity: 1;
		text-shadow: 0 0 8px var(--glow-strong);
	}

	.nav-link.active {
		background: rgba(0, 255, 65, 0.1);
		color: var(--green);
		text-shadow: 0 0 10px var(--glow-strong);
		border-left-color: var(--green);
		border-left-width: 3px;
		padding-left: 1rem;
	}

	.nav-link.active .file-icon {
		opacity: 1;
		text-shadow: 0 0 10px var(--glow-strong);
	}

	/* Scrollbar styling */
	.sidebar::-webkit-scrollbar {
		width: 6px;
	}

	.sidebar::-webkit-scrollbar-track {
		background: transparent;
	}

	.sidebar::-webkit-scrollbar-thumb {
		background: var(--green);
		border-radius: 3px;
		box-shadow: 0 0 5px var(--glow);
	}

	.sidebar::-webkit-scrollbar-thumb:hover {
		background: var(--green);
		box-shadow: 0 0 10px var(--glow-strong);
	}

	@media (max-width: 1024px) {
		.sidebar {
			display: none;
		}
	}
</style>
