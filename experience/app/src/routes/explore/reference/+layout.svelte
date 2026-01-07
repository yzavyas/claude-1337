<script lang="ts">
	import { base } from '$app/paths';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { buildNavItems } from '$lib/content';

	const { children } = $props();

	// Dynamically build nav from content/explore/reference/*
	const referenceItems = buildNavItems('explore/reference', `${base}/explore/reference`);
</script>

<div class="gits-section">
	<!-- Scanline effect -->
	<div class="scanlines" aria-hidden="true"></div>

	<div class="section-layout">
		<Sidebar section="reference" items={referenceItems} />
		<article class="section-content markdown-content">
			{@render children()}
		</article>
	</div>
</div>

<style>
	/* ═══════════════════════════════════════════════════════════════
	   GiTS Theme - Cyberpunk data visualization
	   Ghost in the Shell inspired: playful but technical
	   ═══════════════════════════════════════════════════════════════ */

	.gits-section {
		/* Neon cyan palette */
		--accent: #22d3ee;
		--accent-hover: #67e8f9;
		--accent-muted: rgba(34, 211, 238, 0.12);
		--accent-glow: rgba(34, 211, 238, 0.4);

		--bg-primary: #0a0f14;
		--bg-secondary: #0d1419;
		--bg-surface: #111820;
		--bg-elevated: #151d26;

		--border-subtle: #1a2530;
		--border-default: #223040;
		--border-strong: #2a3a4d;

		--text-primary: #e0f2fe;
		--text-secondary: #7dd3fc;
		--text-muted: #38bdf8;

		--link: #22d3ee;
		--link-hover: #67e8f9;

		/* Section styling */
		margin: calc(-1 * var(--space-xl)) calc(-1 * var(--space-lg));
		padding: var(--space-2xl) var(--space-xl);
		background: var(--bg-primary);
		min-height: 80vh;
		position: relative;
		overflow: hidden;
	}

	/* Subtle circuit pattern background */
	.gits-section::before {
		content: '';
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(90deg, var(--border-subtle) 1px, transparent 1px),
			linear-gradient(var(--border-subtle) 1px, transparent 1px);
		background-size: 40px 40px;
		opacity: 0.3;
		mask-image: radial-gradient(ellipse at 50% 0%, black 0%, transparent 70%);
	}

	/* CRT scanline effect - subtle */
	.scanlines {
		position: absolute;
		inset: 0;
		pointer-events: none;
		background: repeating-linear-gradient(
			0deg,
			transparent 0px,
			transparent 2px,
			rgba(0, 0, 0, 0.1) 2px,
			rgba(0, 0, 0, 0.1) 4px
		);
		opacity: 0.15;
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
		animation: gitsFadeIn 600ms ease-out;
	}

	@keyframes gitsFadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Typography - terminal feel with glow */
	.section-content :global(h1) {
		font-family: var(--font-mono);
		font-size: 2rem;
		font-weight: 500;
		letter-spacing: -0.02em;
		color: var(--accent);
		text-shadow: 0 0 30px var(--accent-glow);
		margin-bottom: var(--space-lg);
	}

	.section-content :global(h2) {
		font-family: var(--font-mono);
		font-size: 1.1rem;
		font-weight: 500;
		color: var(--text-secondary);
		margin-top: var(--space-2xl);
		margin-bottom: var(--space-md);
		padding-left: var(--space-md);
		border-left: 2px solid var(--accent);
	}

	.section-content :global(h3) {
		font-family: var(--font-mono);
		font-size: 0.95rem;
		color: var(--text-muted);
		margin-top: var(--space-lg);
	}

	.section-content :global(p) {
		color: var(--text-secondary);
		line-height: 1.7;
	}

	.section-content :global(strong) {
		color: var(--text-primary);
	}

	/* Code with neon glow */
	.section-content :global(code) {
		font-family: var(--font-mono);
		background: rgba(34, 211, 238, 0.1);
		color: var(--accent);
		border: 1px solid var(--border-subtle);
		padding: 0.1em 0.4em;
		border-radius: 3px;
	}

	.section-content :global(pre) {
		background: #0a0f14;
		border: 1px solid var(--border-default);
		border-radius: 4px;
		position: relative;
	}

	.section-content :global(pre)::before {
		content: '>';
		position: absolute;
		top: var(--space-md);
		left: var(--space-md);
		color: var(--accent);
		font-family: var(--font-mono);
		opacity: 0.5;
	}

	.section-content :global(pre code) {
		background: none;
		border: none;
		color: var(--text-secondary);
	}

	/* Tables - data terminal style */
	.section-content :global(table) {
		border: 1px solid var(--border-default);
		background: rgba(0, 0, 0, 0.3);
		border-radius: 4px;
		overflow: hidden;
	}

	.section-content :global(th) {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		background: rgba(34, 211, 238, 0.08);
		color: var(--accent);
		border-bottom: 1px solid var(--accent-muted);
	}

	.section-content :global(td) {
		font-family: var(--font-mono);
		font-size: 0.9rem;
		color: var(--text-secondary);
		border-bottom: 1px solid var(--border-subtle);
	}

	.section-content :global(tr:hover td) {
		background: rgba(34, 211, 238, 0.05);
	}

	/* Links with glow on hover */
	.section-content :global(a) {
		color: var(--accent);
		text-decoration: none;
		transition: all 200ms ease;
	}

	.section-content :global(a:hover) {
		text-shadow: 0 0 8px var(--accent-glow);
	}

	/* Lists with terminal markers */
	.section-content :global(ul) {
		list-style: none;
		padding-left: var(--space-lg);
	}

	.section-content :global(li) {
		position: relative;
		color: var(--text-secondary);
	}

	.section-content :global(li)::before {
		content: '>';
		position: absolute;
		left: calc(-1 * var(--space-md));
		color: var(--accent);
		font-family: var(--font-mono);
		opacity: 0.6;
	}

	/* Blockquotes - terminal output */
	.section-content :global(blockquote) {
		border-left: 2px solid var(--accent);
		background: rgba(34, 211, 238, 0.05);
		padding: var(--space-md) var(--space-lg);
		font-family: var(--font-mono);
		font-size: 0.9rem;
	}

	/* HR - data separator */
	.section-content :global(hr) {
		border: none;
		height: 1px;
		background: linear-gradient(90deg, transparent, var(--accent-muted), transparent);
		margin: var(--space-2xl) 0;
	}

	@media (max-width: 768px) {
		.gits-section {
			margin: calc(-1 * var(--space-md));
			padding: var(--space-lg) var(--space-md);
		}

		.section-layout {
			grid-template-columns: 1fr;
			gap: var(--space-lg);
		}

		.section-content :global(h1) {
			font-size: 1.5rem;
		}
	}
</style>
