<script lang="ts">
	import CopyCommand from '$lib/components/CopyCommand.svelte';
	import { base } from '$app/paths';
</script>

<svelte:head>
	<title>Cognitive Extensions — claude-1337</title>
</svelte:head>

<main class="landing">
	<section class="hero">
		<div class="badge">
			<span class="badge-dot"></span>
			<span class="badge-text">marketplace</span>
		</div>

		<h1 class="headline">
			<span class="headline-primary">Effective Collaborative Intelligence</span>
		</h1>

		<p class="description">
			Cognitive extensions to enhance capability and limit dependency.
		</p>

		<div class="actions">
			<a href="{base}/ethos/" class="primary-action">
				<span>Understand the approach</span>
				<span class="arrow">→</span>
			</a>
		</div>
	</section>

	<div class="secondary-link">
		<a href="{base}/catalog/">Browse Extensions</a>
	</div>
</main>

<style>
	.landing {
		min-height: 100vh;
		padding: 100px var(--space-6) var(--space-12);
	}

	.hero {
		max-width: var(--content-width);
		text-align: center;
		margin: 0 auto var(--space-16);
	}

	.badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-1) var(--space-4);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-8);
		animation: fadeIn 600ms ease;
	}

	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(12px); }
		to { opacity: 1; transform: translateY(0); }
	}

	.badge-dot {
		width: 6px;
		height: 6px;
		background: var(--color-success);
		border-radius: 50%;
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}

	.badge-text {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}

	.headline {
		margin-bottom: var(--space-8);
		animation: fadeIn 600ms ease 100ms both;
	}

	.headline-secondary {
		display: block;
		font-size: var(--text-lg);
		font-weight: var(--font-normal);
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-2);
	}

	.headline-primary {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-medium);
		letter-spacing: var(--tracking-tighter);
		line-height: var(--leading-tight);
		color: var(--color-text-primary);
	}

	.description {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 480px;
		margin: 0 auto var(--space-10);
		line-height: var(--leading-relaxed);
		animation: fadeIn 600ms ease 200ms both;
	}

	.actions {
		animation: fadeIn 600ms ease 300ms both;
		margin-bottom: var(--space-16);
	}

	.primary-action {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-6);
		background: var(--color-accent);
		border-radius: var(--radius-md);
		color: var(--color-bg-deep);
		font-weight: var(--font-medium);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		text-decoration: none;
		transition:
			background var(--duration-fast) var(--ease-out),
			transform var(--duration-fast) var(--ease-out);
	}

	.primary-action:hover {
		background: var(--color-accent-hover);
		transform: translateY(-2px);
	}

	.primary-action .arrow {
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.primary-action:hover .arrow {
		transform: translateX(4px);
	}

	.secondary-link {
		text-align: center;
		animation: fadeIn 600ms ease 500ms both;
	}

	.secondary-link a {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.secondary-link a:hover {
		color: var(--color-accent);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.headline-secondary {
			font-size: var(--text-base);
		}

		.headline-primary {
			font-size: var(--text-3xl);
		}
	}
</style>
