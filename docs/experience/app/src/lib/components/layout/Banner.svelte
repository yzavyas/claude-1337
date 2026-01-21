<script lang="ts">
	/**
	 * Top Banner Component
	 *
	 * Displays site-wide notice (e.g., alpha status, announcements).
	 * Fixed at top, shifts content down.
	 */
	let {
		badge = 'closed alpha',
		message = 'This marketplace is in early development. Extensions are experimental.'
	}: {
		badge?: string;
		message?: string;
	} = $props();
</script>

<div class="banner" role="status" aria-label="Site notice">
	<span class="banner-badge">{badge}</span>
	<span class="banner-message">{message}</span>
</div>

<style>
	.banner {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-3);
		padding: var(--space-2) var(--space-4);
		background: var(--color-bg-elevated);
		border-bottom: 1px solid var(--color-border);
		font-size: var(--text-xs);
	}

	.banner-badge {
		font-family: var(--font-mono);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.banner-message {
		color: var(--color-text-muted);
	}

	/* Mobile: hide long text, keep badge */
	@media (max-width: 640px) {
		.banner {
			padding: var(--space-1) var(--space-3);
		}

		.banner-message {
			display: none;
		}
	}
</style>
