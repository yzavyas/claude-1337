<script lang="ts">
	/**
	 * Shell Component
	 *
	 * Compound component that provides the app layout structure.
	 * Uses Svelte 5 snippets for flexible slot composition.
	 *
	 * Usage:
	 *   <Shell>
	 *     <Content />
	 *   </Shell>
	 *
	 *   <!-- With custom banner -->
	 *   <Shell>
	 *     {#snippet banner()}
	 *       <CustomBanner />
	 *     {/snippet}
	 *     <Content />
	 *   </Shell>
	 */
	import type { Snippet } from 'svelte';
	import Banner from './Banner.svelte';
	import Nav from './Nav.svelte';
	import Footer from './Footer.svelte';

	let {
		banner,
		nav,
		children,
		footer,
		hideBanner = false,
		hideNav = false,
		hideFooter = false
	}: {
		banner?: Snippet;
		nav?: Snippet;
		children: Snippet;
		footer?: Snippet;
		hideBanner?: boolean;
		hideNav?: boolean;
		hideFooter?: boolean;
	} = $props();
</script>

{#if !hideBanner}
	{#if banner}
		{@render banner()}
	{:else}
		<Banner />
	{/if}
{/if}

{#if !hideNav}
	{#if nav}
		{@render nav()}
	{:else}
		<Nav />
	{/if}
{/if}

<main class="shell-main" class:no-banner={hideBanner} class:no-nav={hideNav}>
	{@render children()}
</main>

{#if !hideFooter}
	{#if footer}
		{@render footer()}
	{:else}
		<Footer />
	{/if}
{/if}

<style>
	.shell-main {
		min-height: 100vh;
		padding-top: calc(36px + 52px); /* banner (36px) + nav (52px) */
	}

	.shell-main.no-banner {
		padding-top: 52px; /* nav only */
	}

	.shell-main.no-nav {
		padding-top: 36px; /* banner only */
	}

	.shell-main.no-banner.no-nav {
		padding-top: 0;
	}
</style>
