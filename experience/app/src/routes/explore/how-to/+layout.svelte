<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/how-to/*
	const howToItems = buildNavItems('explore/how-to', `${base}/explore/how-to`);
</script>

<div class="section-layout">
	<Sidebar section="how-to" items={howToItems} />
	<article class="section-content">
		{@render children()}
	</article>
</div>

<style>
	.section-layout {
		display: grid;
		grid-template-columns: 200px 1fr;
		gap: var(--space-xl);
		align-items: start;
	}

	.section-content {
		min-width: 0;
	}

	@media (max-width: 768px) {
		.section-layout {
			grid-template-columns: 1fr;
			gap: 0;
		}
	}
</style>
