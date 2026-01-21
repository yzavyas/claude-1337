<script lang="ts">
	interface Props {
		name: string;
	}

	const { name }: Props = $props();

	// Dynamically import all diagram components at build time
	const diagrams = import.meta.glob('../diagrams/*.svelte');

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let Component = $state<any>(null);
	let error = $state<string | null>(null);

	$effect(() => {
		const path = `../diagrams/${name.trim()}.svelte`;

		if (diagrams[path]) {
			diagrams[path]().then((module: any) => {
				Component = module.default;
				error = null;
			}).catch((e: Error) => {
				error = `Failed to load diagram: ${e.message}`;
			});
		} else {
			error = `Diagram not found: ${name}`;
			// Log available diagrams for debugging
			console.warn(`Available diagrams:`, Object.keys(diagrams));
		}
	});
</script>

<div class="diagram-container">
	{#if error}
		<div class="diagram-error">
			<span class="error-icon">!</span>
			<span>{error}</span>
		</div>
	{:else if Component}
		<Component />
	{:else}
		<div class="diagram-loading">
			Loading diagram...
		</div>
	{/if}
</div>

<style>
	.diagram-container {
		margin: var(--space-lg, 1.5rem) 0;
		padding: var(--space-md, 1rem);
		background: var(--bg-secondary, #1f2937);
		border: 1px solid var(--border-subtle, #374151);
		border-radius: 8px;
		min-height: 200px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.diagram-error {
		color: #ef4444;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-family: monospace;
		font-size: 0.875rem;
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

	.diagram-loading {
		color: var(--text-muted, #9ca3af);
		font-size: 0.875rem;
	}
</style>
