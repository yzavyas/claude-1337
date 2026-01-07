<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/explanation/*
	const explanationItems = buildNavItems('explore/explanation', `${base}/explore/explanation`);
</script>

<div class="shadowist-section">
	<div class="section-layout">
		<Sidebar section="explanation" items={explanationItems} />
		<article class="section-content markdown-content">
			{@render children()}
		</article>
	</div>
</div>

<style>
	/* ═══════════════════════════════════════════════════════════════
	   Shadowist Theme - Tension through darkness
	   ═══════════════════════════════════════════════════════════════ */

	.shadowist-section {
		/* Override theme variables for this section */
		--bg-primary: #050506;
		--bg-secondary: #0a0a0b;
		--bg-surface: #0f0f10;
		--bg-elevated: #141416;

		--border-subtle: #1a1a1d;
		--border-default: #222225;
		--border-strong: #2a2a2e;

		--text-primary: #e0e0dc;
		--text-secondary: #7a7a7a;
		--text-muted: #4a4a4a;

		/* Single accent - cold crimson */
		--accent: #dc2626;
		--accent-hover: #ef4444;
		--accent-muted: rgba(220, 38, 38, 0.12);

		--link: #dc2626;
		--link-hover: #ef4444;

		/* Apply to section */
		margin: calc(-1 * var(--space-xl)) calc(-1 * var(--space-lg));
		padding: var(--space-2xl) var(--space-xl);
		background: var(--bg-primary);
		min-height: 80vh;
		position: relative;
	}

	/* Subtle vignette for depth */
	.shadowist-section::before {
		content: '';
		position: absolute;
		inset: 0;
		background: radial-gradient(
			ellipse at center,
			transparent 0%,
			rgba(0, 0, 0, 0.4) 100%
		);
		pointer-events: none;
	}

	.section-layout {
		display: grid;
		grid-template-columns: 180px 1fr;
		gap: var(--space-2xl);
		align-items: start;
		position: relative;
		z-index: 1;
	}

	.section-content {
		min-width: 0;
		animation: shadowistReveal 800ms ease-out;
	}

	@keyframes shadowistReveal {
		from {
			opacity: 0;
			transform: translateY(16px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Typography overrides for shadowist */
	.section-content :global(h1) {
		font-size: 2.5rem;
		font-weight: 300;
		letter-spacing: -0.04em;
		margin-bottom: var(--space-xl);
		color: var(--text-primary);
		text-shadow: 0 0 60px rgba(220, 38, 38, 0.15);
	}

	.section-content :global(h2) {
		font-size: 1.25rem;
		font-weight: 500;
		letter-spacing: 0.02em;
		text-transform: lowercase;
		margin-top: var(--space-3xl);
		margin-bottom: var(--space-lg);
		color: var(--accent);
		border-bottom: 1px solid var(--border-subtle);
		padding-bottom: var(--space-sm);
	}

	.section-content :global(h3) {
		font-size: 1rem;
		font-weight: 500;
		color: var(--text-secondary);
		margin-top: var(--space-xl);
	}

	.section-content :global(p) {
		color: var(--text-secondary);
		line-height: 1.8;
		max-width: 65ch;
	}

	.section-content :global(strong) {
		color: var(--text-primary);
		font-weight: 500;
	}

	/* Tables with dramatic styling */
	.section-content :global(table) {
		border: 1px solid var(--border-subtle);
		background: rgba(0, 0, 0, 0.3);
	}

	.section-content :global(th) {
		background: rgba(220, 38, 38, 0.08);
		color: var(--accent);
		font-weight: 500;
		text-transform: lowercase;
		letter-spacing: 0.05em;
		border-bottom: 1px solid var(--accent-muted);
	}

	.section-content :global(td) {
		border-bottom: 1px solid var(--border-subtle);
	}

	.section-content :global(tr:hover td) {
		background: rgba(220, 38, 38, 0.04);
	}

	/* Links with accent */
	.section-content :global(a) {
		color: var(--accent);
		text-decoration: none;
		border-bottom: 1px solid transparent;
		transition: border-color 300ms ease;
	}

	.section-content :global(a:hover) {
		border-bottom-color: var(--accent);
	}

	/* Code blocks - darker */
	.section-content :global(pre) {
		background: #0a0a0b;
		border: 1px solid var(--border-subtle);
	}

	.section-content :global(code) {
		background: rgba(220, 38, 38, 0.08);
		color: var(--text-primary);
		border-color: var(--border-subtle);
	}

	/* Blockquotes with left accent */
	.section-content :global(blockquote) {
		border-left: 2px solid var(--accent);
		background: rgba(220, 38, 38, 0.04);
		padding: var(--space-md) var(--space-lg);
		margin: var(--space-lg) 0;
	}

	/* Horizontal rules - subtle */
	.section-content :global(hr) {
		border-top: 1px solid var(--border-subtle);
		margin: var(--space-3xl) 0;
	}

	@media (max-width: 768px) {
		.shadowist-section {
			margin: calc(-1 * var(--space-md));
			padding: var(--space-lg) var(--space-md);
		}

		.section-layout {
			grid-template-columns: 1fr;
			gap: var(--space-lg);
		}

		.section-content :global(h1) {
			font-size: 1.8rem;
		}
	}
</style>
