<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/explanation/*
	const explanationItems = buildNavItems('explore/explanation', `${base}/explore/explanation`);
</script>

<div class="section-layout">
	<Sidebar section="explanation" items={explanationItems} />
	<article class="section-content markdown-content">
		{@render children()}
	</article>
</div>

<style>
	.section-layout {
		display: grid;
		grid-template-columns: 180px 1fr;
		gap: var(--space-2xl);
		align-items: start;
	}

	.section-content {
		min-width: 0;
	}

	@media (max-width: 768px) {
		.section-layout {
			grid-template-columns: 1fr;
			gap: var(--space-lg);
		}
	}
</style>
