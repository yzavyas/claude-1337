<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/stores';
	import '$lib/styles/global.css';

	let { children } = $props();

	// Hide nav on homepage for cleaner signal
	const isHome = $derived($page.url.pathname === '/' || $page.url.pathname === base + '/');
</script>

<svelte:head>
	<title>claude-1337</title>
	<meta name="description" content="Extensions for thinking." />
</svelte:head>

<div class="layout">
	{#if !isHome}
		<header>
			<nav>
				<a href="{base}/" class="wordmark">claude-1337</a>
				<div class="nav-links">
					<a href="{base}/explore/">Explore</a>
				</div>
			</nav>
		</header>
	{/if}

	<main>
		{@render children()}
	</main>
</div>

<style>
	.layout {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	header {
		position: sticky;
		top: 0;
		z-index: 100;
		background: var(--surface-base);
		border-bottom: 1px solid var(--border-subtle);
	}

	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--space-4) var(--space-6);
		max-width: var(--max-width-content);
		margin: 0 auto;
		width: 100%;
	}

	.wordmark {
		font-family: var(--font-mono);
		font-weight: 500;
		font-size: var(--text-xs);
		letter-spacing: var(--tracking-wide);
	}

	.nav-links {
		display: flex;
		gap: var(--space-5);
	}

	.nav-links a {
		font-size: var(--text-sm);
		color: var(--ink-secondary);
	}

	.nav-links a:hover {
		color: var(--ink-primary);
	}

	main {
		flex: 1;
	}
</style>
