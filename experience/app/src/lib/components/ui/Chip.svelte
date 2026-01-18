<script lang="ts">
	/**
	 * Chip — UI Primitive
	 *
	 * Small inline element for tags, filters, keywords.
	 * Can be static, clickable, or removable.
	 */
	import type { Snippet } from 'svelte';

	type Variant = 'default' | 'accent' | 'subtle';

	let {
		variant = 'default',
		selected = false,
		removable = false,
		onclick,
		onremove,
		children,
		class: className = ''
	}: {
		variant?: Variant;
		selected?: boolean;
		removable?: boolean;
		onclick?: () => void;
		onremove?: () => void;
		children: Snippet;
		class?: string;
	} = $props();

	const interactive = $derived(!!onclick);

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onclick?.();
		}
	}

	function handleRemove(event: MouseEvent) {
		event.stopPropagation();
		onremove?.();
	}

	function handleRemoveKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			event.stopPropagation();
			onremove?.();
		}
	}
</script>

{#if interactive}
	<button
		type="button"
		class="chip {variant} {className}"
		class:interactive
		class:selected
		{onclick}
		onkeydown={handleKeydown}
	>
		<span class="chip-content">
			{@render children()}
		</span>
		{#if removable}
			<span
				role="button"
				tabindex={0}
				class="chip-remove"
				aria-label="Remove"
				onclick={handleRemove}
				onkeydown={handleRemoveKeydown}
			>
				<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
					<path
						d="M3 3L9 9M9 3L3 9"
						stroke="currentColor"
						stroke-width="1.5"
						stroke-linecap="round"
					/>
				</svg>
			</span>
		{/if}
	</button>
{:else}
	<span class="chip {variant} {className}" class:selected>
		<span class="chip-content">
			{@render children()}
		</span>
		{#if removable}
			<button
				type="button"
				class="chip-remove"
				aria-label="Remove"
				onclick={handleRemove}
				onkeydown={handleRemoveKeydown}
			>
				<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
					<path
						d="M3 3L9 9M9 3L3 9"
						stroke="currentColor"
						stroke-width="1.5"
						stroke-linecap="round"
					/>
				</svg>
			</button>
		{/if}
	</span>
{/if}

<style>
	/* Reset button styles when chip is interactive */
	button.chip {
		background: none;
		border: none;
		font: inherit;
		cursor: pointer;
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		padding: var(--space-1) var(--space-3);
		font-size: var(--text-sm);
		border-radius: var(--radius-full);
		transition:
			background-color var(--duration-fast) var(--ease-out),
			border-color var(--duration-fast) var(--ease-out);
	}

	/* Variants */
	.default {
		background: var(--color-bg-surface);
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.accent {
		background: oklch(from var(--color-accent) l c h / 0.1);
		color: var(--color-accent);
		border: 1px solid oklch(from var(--color-accent) l c h / 0.25);
	}

	.subtle {
		background: transparent;
		color: var(--color-text-muted);
		border: 1px solid transparent;
	}

	/* Interactive */
	.interactive {
		cursor: pointer;
	}

	.interactive:hover {
		background: var(--color-bg-elevated);
		border-color: var(--color-border-strong);
	}

	.interactive:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	/* Selected */
	.selected {
		background: var(--color-text);
		color: var(--color-bg);
		border-color: var(--color-text);
	}

	.selected:hover {
		background: var(--color-text-secondary);
		border-color: var(--color-text-secondary);
	}

	/* Content */
	.chip-content {
		line-height: 1;
	}

	/* Remove button */
	.chip-remove {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 16px;
		height: 16px;
		padding: 0;
		margin-left: var(--space-1);
		margin-right: calc(-1 * var(--space-1));
		background: transparent;
		border: none;
		border-radius: var(--radius-full);
		color: inherit;
		opacity: 0.6;
		cursor: pointer;
		transition:
			opacity var(--duration-fast) var(--ease-out),
			background-color var(--duration-fast) var(--ease-out);
	}

	.chip-remove:hover {
		opacity: 1;
		background: oklch(0 0 0 / 0.1);
	}

	.selected .chip-remove:hover {
		background: oklch(1 0 0 / 0.2);
	}

	.chip-remove:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 1px;
	}
</style>
