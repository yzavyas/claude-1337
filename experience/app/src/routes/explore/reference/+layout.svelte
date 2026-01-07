<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/reference/*
	const referenceItems = buildNavItems('explore/reference', `${base}/explore/reference`);
</script>

<div class="section-layout">
	<Sidebar section="reference" items={referenceItems} />
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
