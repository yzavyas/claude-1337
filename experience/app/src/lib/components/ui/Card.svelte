<script lang="ts">
	/**
	 * Card — UI Primitive
	 *
	 * Generic card container with optional header/footer slots.
	 * Can be interactive (link) or static.
	 */
	import type { Snippet } from 'svelte';

	type Variant = 'default' | 'elevated' | 'outlined';

	let {
		variant = 'default',
		href,
		header,
		children,
		footer,
		padding = true,
		class: className = ''
	}: {
		variant?: Variant;
		href?: string;
		header?: Snippet;
		children: Snippet;
		footer?: Snippet;
		padding?: boolean;
		class?: string;
	} = $props();

	const interactive = $derived(!!href);
</script>

{#if href}
	<a {href} class="card {variant} {className}" class:interactive class:no-padding={!padding}>
		{#if header}
			<div class="card-header">
				{@render header()}
			</div>
		{/if}
		<div class="card-body">
			{@render children()}
		</div>
		{#if footer}
			<div class="card-footer">
				{@render footer()}
			</div>
		{/if}
	</a>
{:else}
	<div class="card {variant} {className}" class:no-padding={!padding}>
		{#if header}
			<div class="card-header">
				{@render header()}
			</div>
		{/if}
		<div class="card-body">
			{@render children()}
		</div>
		{#if footer}
			<div class="card-footer">
				{@render footer()}
			</div>
		{/if}
	</div>
{/if}

<style>
	.card {
		display: flex;
		flex-direction: column;
		border-radius: var(--radius-lg);
		text-decoration: none;
		color: inherit;
		transition:
			border-color var(--duration-fast) var(--ease-out),
			box-shadow var(--duration-fast) var(--ease-out),
			transform var(--duration-fast) var(--ease-out);
	}

	/* Variants */
	.default {
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
	}

	.elevated {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		box-shadow: var(--shadow-sm);
	}

	.outlined {
		background: transparent;
		border: 1px solid var(--color-border-strong);
	}

	/* Interactive */
	.interactive {
		cursor: pointer;
	}

	.interactive:hover {
		border-color: var(--color-border-strong);
		transform: translateY(-2px);
	}

	.interactive.elevated:hover {
		box-shadow: var(--shadow-md);
	}

	.interactive:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
	}

	/* Sections */
	.card-header {
		padding: var(--space-4) var(--space-5);
		border-bottom: 1px solid var(--color-border);
	}

	.card-body {
		padding: var(--space-5);
		flex: 1;
	}

	.card-footer {
		padding: var(--space-4) var(--space-5);
		border-top: 1px solid var(--color-border);
	}

	.no-padding .card-header,
	.no-padding .card-body,
	.no-padding .card-footer {
		padding: 0;
	}

	.no-padding .card-header {
		border-bottom: none;
	}

	.no-padding .card-footer {
		border-top: none;
	}
</style>
