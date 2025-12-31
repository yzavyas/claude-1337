<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/tutorials/*
	const tutorialItems = buildNavItems('explore/tutorials', `${base}/explore/tutorials`);
</script>

<Sidebar section="tutorials" items={tutorialItems} />

{@render children()}
