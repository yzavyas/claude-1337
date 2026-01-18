<script lang="ts">
	/**
	 * Button — UI Primitive
	 *
	 * Accessible button with craft aesthetic.
	 * Uses Bits UI Button for accessibility.
	 */
	import { Button as ButtonPrimitive } from 'bits-ui';
	import type { Snippet } from 'svelte';

	type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';
	type Size = 'sm' | 'md' | 'lg';

	let {
		variant = 'primary',
		size = 'md',
		disabled = false,
		href,
		children,
		class: className = '',
		onclick
	}: {
		variant?: Variant;
		size?: Size;
		disabled?: boolean;
		href?: string;
		children: Snippet;
		class?: string;
		onclick?: (e: MouseEvent) => void;
	} = $props();
</script>

{#if href}
	<a
		{href}
		class="button {variant} {size} {className}"
		class:disabled
		aria-disabled={disabled}
	>
		{@render children()}
	</a>
{:else}
	<ButtonPrimitive.Root
		class="button {variant} {size} {className}"
		{disabled}
		{onclick}
	>
		{@render children()}
	</ButtonPrimitive.Root>
{/if}

<style>
	.button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-2);
		font-family: var(--font-sans);
		font-weight: var(--font-medium);
		border-radius: var(--radius-md);
		cursor: pointer;
		transition:
			background-color var(--duration-fast) var(--ease-out),
			border-color var(--duration-fast) var(--ease-out),
			transform var(--duration-fast) var(--ease-out);
		text-decoration: none;
		border: 1px solid transparent;
	}

	.button:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	.button:active:not(.disabled) {
		transform: scale(0.98);
	}

	/* Sizes */
	.sm {
		padding: var(--space-1) var(--space-3);
		font-size: var(--text-sm);
		height: 32px;
	}

	.md {
		padding: var(--space-2) var(--space-4);
		font-size: var(--text-base);
		height: 40px;
	}

	.lg {
		padding: var(--space-3) var(--space-6);
		font-size: var(--text-lg);
		height: 48px;
	}

	/* Variants */
	.primary {
		background: var(--color-text);
		color: var(--color-bg);
		border-color: var(--color-text);
	}

	.primary:hover:not(.disabled) {
		background: var(--color-text-secondary);
		border-color: var(--color-text-secondary);
	}

	.secondary {
		background: transparent;
		color: var(--color-text);
		border-color: var(--color-border-strong);
	}

	.secondary:hover:not(.disabled) {
		background: var(--color-bg-surface);
		border-color: var(--color-text-muted);
	}

	.ghost {
		background: transparent;
		color: var(--color-text-secondary);
		border-color: transparent;
	}

	.ghost:hover:not(.disabled) {
		background: var(--color-bg-surface);
		color: var(--color-text);
	}

	.danger {
		background: var(--color-status-rust);
		color: var(--color-bg);
		border-color: var(--color-status-rust);
	}

	.danger:hover:not(.disabled) {
		background: oklch(from var(--color-status-rust) calc(l - 0.1) c h);
	}

	/* Disabled */
	.disabled {
		opacity: 0.5;
		cursor: not-allowed;
		pointer-events: none;
	}
</style>
