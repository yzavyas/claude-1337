<script lang="ts">
	import { page } from '$app/stores';
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Extract section from URL: /explore/{section}/... → section
	const section = $derived(() => {
		const path = $page.url.pathname.replace(base, '');
		const parts = path.split('/').filter(Boolean);
		// parts[0] = 'explore', parts[1] = section
		return parts[1] || 'explanation';
	});

	// Build nav items dynamically based on current section
	const navItems = $derived(buildNavItems(`explore/${section()}`, `${base}/explore/${section()}`));
</script>

<div class="section-layout">
	<Sidebar section={section()} items={navItems} />
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
