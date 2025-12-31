<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/how-to/*
	const howToItems = buildNavItems('explore/how-to', `${base}/explore/how-to`);
</script>

<Sidebar section="how-to" items={howToItems} />

{@render children()}
