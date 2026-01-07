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
			theme: 'dark',
			themeVariables: {
				primaryColor: '#22d3ee',
				primaryTextColor: '#e0e0dc',
				primaryBorderColor: '#22d3ee',
				lineColor: '#4a5568',
				secondaryColor: '#1a1a2e',
				tertiaryColor: '#0a0f14'
			}
		});

		const id = `mermaid-${Math.random().toString(36).slice(2)}`;
		const { svg } = await mermaid.render(id, code);
		const sanitized = DOMPurify.sanitize(svg, { USE_PROFILES: { svg: true } });
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

	.mermaid-loading {
		color: var(--text-muted);
		font-size: 0.85rem;
	}
</style>
