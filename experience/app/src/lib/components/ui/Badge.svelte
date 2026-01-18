<script lang="ts">
	/**
	 * Badge — UI Primitive
	 *
	 * Status indicator badge with semantic variants.
	 */
	import type { Snippet } from 'svelte';

	type Variant = 'default' | 'sage' | 'gold' | 'rust' | 'muted' | 'plum' | 'ocean';

	let {
		variant = 'default',
		children,
		class: className = ''
	}: {
		variant?: Variant;
		children: Snippet;
		class?: string;
	} = $props();
</script>

<span class="badge {variant} {className}">
	{@render children()}
</span>

<style>
	.badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		padding: var(--space-1) var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: var(--font-medium);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		border-radius: var(--radius-sm);
		white-space: nowrap;
	}

	/* Variants */
	.default {
		background: var(--color-bg-surface);
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.sage {
		background: oklch(from var(--color-status-sage) l c h / 0.15);
		color: var(--color-status-sage);
		border: 1px solid oklch(from var(--color-status-sage) l c h / 0.3);
	}

	.gold {
		background: oklch(from var(--color-accent) l c h / 0.15);
		color: var(--color-accent);
		border: 1px solid oklch(from var(--color-accent) l c h / 0.3);
	}

	.rust {
		background: oklch(from var(--color-status-rust) l c h / 0.15);
		color: var(--color-status-rust);
		border: 1px solid oklch(from var(--color-status-rust) l c h / 0.3);
	}

	.muted {
		background: var(--color-bg-elevated);
		color: var(--color-text-muted);
		border: 1px solid var(--color-border);
	}

	.plum {
		background: var(--color-status-discussion-bg);
		color: var(--color-status-discussion);
		border: 1px solid oklch(from var(--color-status-discussion) l c h / 0.3);
	}

	.ocean {
		background: var(--color-status-accepted-bg);
		color: var(--color-status-accepted);
		border: 1px solid oklch(from var(--color-status-accepted) l c h / 0.3);
	}
</style>
