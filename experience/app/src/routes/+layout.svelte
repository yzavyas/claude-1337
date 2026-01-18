<script lang="ts">
	/**
	 * Root layout - minimal, no Shell
	 * Shell is added in (app)/+layout.svelte for pages that need it
	 */
	import '$lib/styles/global.css';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { initSmoothScroll, destroySmoothScroll } from '$lib/utils/scroll';
	import { setupViewTransitions } from '$lib/utils/viewTransitions';

	let { children } = $props();

	onMount(() => {
		if (browser) {
			initSmoothScroll();
			setupViewTransitions();
		}
	});

	onDestroy(() => {
		if (browser) {
			destroySmoothScroll();
		}
	});
</script>

<svelte:head>
	<title>claude-1337 — Cognitive Extensions</title>
	<meta name="description" content="Cognitive extensions for effective collaborative intelligence." />
	<meta name="theme-color" content="#f5f0e8" />
</svelte:head>

{@render children()}
