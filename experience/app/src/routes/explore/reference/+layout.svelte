<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/reference/*
	const referenceItems = buildNavItems('explore/reference', `${base}/explore/reference`);
</script>

<Sidebar section="reference" items={referenceItems} />

{@render children()}
