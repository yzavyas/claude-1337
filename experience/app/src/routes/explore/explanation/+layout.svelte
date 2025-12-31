<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/explanation/*
	const explanationItems = buildNavItems('explore/explanation', `${base}/explore/explanation`);
</script>

<Sidebar section="explanation" items={explanationItems} />

{@render children()}
