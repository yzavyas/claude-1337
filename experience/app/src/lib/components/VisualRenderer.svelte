<script lang="ts">
	interface Props {
		name: string;
	}

	const { name }: Props = $props();

	// Dynamically import all visual components at build time
	const visuals = import.meta.glob('../visuals/*.svelte');

	let Component = $state<any>(null);
	let error = $state<string | null>(null);

	$effect(() => {
		const path = `../visuals/${name.trim()}.svelte`;

		if (visuals[path]) {
			visuals[path]().then((module: any) => {
				Component = module.default;
				error = null;
			}).catch((e: Error) => {
				error = `Failed to load visual: ${e.message}`;
			});
		} else {
			error = `Visual not found: ${name}`;
			console.warn(`Available visuals:`, Object.keys(visuals));
		}
	});
</script>

<div class="visual-wrapper">
	{#if error}
		<div class="visual-error">
			<span class="error-icon">!</span>
			<span>{error}</span>
		</div>
	{:else if Component}
		<Component />
	{:else}
		<div class="visual-loading">
			<div class="loading-pulse"></div>
		</div>
	{/if}
</div>

<style>
	.visual-wrapper {
		margin: var(--space-xl, 2rem) 0;
		min-height: 200px;
	}

	.visual-error {
		color: #ef4444;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		font-family: monospace;
		font-size: 0.875rem;
		padding: 2rem;
		background: rgba(239, 68, 68, 0.1);
		border: 1px solid rgba(239, 68, 68, 0.2);
		border-radius: 8px;
	}

	.error-icon {
		background: #ef4444;
		color: white;
		width: 1.25rem;
		height: 1.25rem;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		font-size: 0.75rem;
	}

	.visual-loading {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 300px;
	}

	.loading-pulse {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: rgba(99, 102, 241, 0.3);
		animation: pulse 1.5s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% {
			transform: scale(0.8);
			opacity: 0.5;
		}
		50% {
			transform: scale(1.2);
			opacity: 1;
		}
	}
</style>
