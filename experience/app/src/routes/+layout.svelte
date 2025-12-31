<script lang="ts">
	import { page } from '$app/stores';
	import { base } from '$app/paths';
	import '$lib/styles/terminal.css';

	let { children } = $props();

	// Check if we're on a page that needs sidebar (explore section)
	const showSidebar = $derived($page.url.pathname.includes('/explore'));

	// Mobile menu toggle
	let mobileMenuOpen = $state(false);

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}
</script>

<svelte:head>
	<title>claude-1337 | 1337 plugins for claude code</title>
	<meta name="description" content="Data-driven decisions from production codebases, research and field testing" />
</svelte:head>

<svelte:body class:has-sidebar={showSidebar} />

<div class="container">
	<header>
		<h1><strong>claude-1337</strong></h1>
		<a href="https://github.com/yzavyas/claude-1337" class="github-link">github</a>
		<button class="mobile-menu-toggle" onclick={toggleMobileMenu} aria-label="Toggle menu">
			<span class="hamburger"></span>
		</button>
	</header>

	<nav class:mobile-open={mobileMenuOpen}>
		<ul>
			<li><a href="{base}/start/" class:active={$page.url.pathname.includes('/start')} onclick={() => mobileMenuOpen = false}>start</a></li>
			<li><a href="{base}/ethos/" class:active={$page.url.pathname.includes('/ethos')} onclick={() => mobileMenuOpen = false}>ethos</a></li>
			<li><a href="{base}/explore/" class:active={$page.url.pathname.includes('/explore')} onclick={() => mobileMenuOpen = false}>explore</a></li>
		</ul>
	</nav>

	<main>
		{@render children()}
	</main>
</div>

<style>
	.github-link {
		position: absolute;
		top: 2rem;
		right: 2rem;
		color: var(--fg-dim);
		font-size: 0.85rem;
	}

	.github-link::after {
		content: none;
	}

	header {
		position: relative;
	}
</style>
