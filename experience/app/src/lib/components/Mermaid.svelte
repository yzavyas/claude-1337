<script lang="ts">
	import { onMount } from 'svelte';
	import DOMPurify from 'dompurify';

	interface Props {
		code: string;
	}

	const { code }: Props = $props();

	let container: HTMLDivElement;
	let rendered = $state(false);

	onMount(async () => {
		const mermaid = (await import('mermaid')).default;
		mermaid.initialize({
			startOnLoad: false,
			theme: 'base',
			themeVariables: {
				// Dark background with light text
				background: '#1f2937',
				primaryColor: '#374151',
				primaryTextColor: '#f3f4f6',
				primaryBorderColor: '#6b7280',
				secondaryColor: '#4b5563',
				secondaryTextColor: '#f3f4f6',
				tertiaryColor: '#374151',
				tertiaryTextColor: '#f3f4f6',
				// Lines and edges
				lineColor: '#9ca3af',
				textColor: '#f3f4f6',
				// Flowchart
				nodeBkg: '#374151',
				nodeBorder: '#6b7280',
				clusterBkg: '#1f2937',
				clusterBorder: '#4b5563',
				defaultLinkColor: '#9ca3af',
				edgeLabelBackground: '#1f2937',
				// Font
				fontFamily: 'inherit'
			}
		});

		const id = `mermaid-${Math.random().toString(36).slice(2)}`;
		const { svg } = await mermaid.render(id, code);
		// Mermaid uses foreignObject with HTML for text labels
		// Must use both svg and html profiles for complete rendering
		const sanitized = DOMPurify.sanitize(svg, {
			USE_PROFILES: { svg: true, svgFilters: true, html: true },
			ADD_TAGS: ['foreignObject'],
			ADD_ATTR: ['requiredExtensions', 'xmlns', 'dominant-baseline', 'text-anchor']
		});
		container.innerHTML = sanitized;
		rendered = true;
	});
</script>

<div class="mermaid-wrapper" class:rendered bind:this={container}>
	{#if !rendered}
		<pre class="mermaid-loading">{code}</pre>
	{/if}
</div>

<style>
	.mermaid-wrapper {
		margin: var(--space-lg) 0;
		padding: var(--space-md);
		background: var(--bg-secondary);
		border: 1px solid var(--border-subtle);
		border-radius: 4px;
		overflow-x: auto;
	}

	.mermaid-wrapper :global(svg) {
		max-width: 100%;
		height: auto;
	}

	/* Force text visibility in mermaid diagrams */
	.mermaid-wrapper :global(.nodeLabel),
	.mermaid-wrapper :global(.edgeLabel),
	.mermaid-wrapper :global(.label),
	.mermaid-wrapper :global(text) {
		fill: #f3f4f6 !important;
		color: #f3f4f6 !important;
	}

	.mermaid-wrapper :global(.node rect),
	.mermaid-wrapper :global(.node polygon) {
		fill: #374151 !important;
		stroke: #6b7280 !important;
	}

	.mermaid-loading {
		color: var(--text-muted);
		font-size: 0.85rem;
	}
</style>
