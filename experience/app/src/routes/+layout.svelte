<script lang="ts">
	import '$lib/styles/global.css';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { initSmoothScroll, destroySmoothScroll } from '$lib/utils/scroll';

	let { children } = $props();

	onMount(() => {
		if (browser) {
			initSmoothScroll();
		}
	});

	onDestroy(() => {
		if (browser) {
			destroySmoothScroll();
		}
	});
</script>

<svelte:head>
	<title>claude-1337 — Cognitive Extensions</title>
	<meta name="description" content="Cognitive extensions for effective collaborative intelligence." />
	<meta name="theme-color" content="#0a0f14" />
</svelte:head>

<!-- Closed Alpha Banner -->
<div class="alpha-banner">
	<span class="alpha-badge">closed alpha</span>
	<span class="alpha-text">This marketplace is in early development. Extensions are experimental.</span>
</div>

<!-- Navigation -->
<nav class="main-nav">
	<a href="/" class="nav-brand">claude-1337</a>
	<div class="nav-links">
		<a href="/ethos/">Ethos</a>
		<a href="/catalog/">Catalog</a>
		<a href="/reference/">Reference</a>
	</div>
</nav>

<!-- GiTS Background Effects -->
<div class="bg-effects" aria-hidden="true">
	<div class="gradient-orb orb-1"></div>
	<div class="gradient-orb orb-2"></div>
	<div class="grid-overlay"></div>
	<div class="scanlines"></div>
	<div class="noise-overlay"></div>
</div>

{@render children()}

<style>
	/* Closed Alpha Banner */
	.alpha-banner {
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

	.alpha-badge {
		font-family: var(--font-mono);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.alpha-text {
		color: var(--color-text-muted);
	}

	/* Navigation */
	.main-nav {
		position: fixed;
		top: 36px;
		left: 0;
		right: 0;
		z-index: 99;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-3) var(--space-6);
		background: var(--color-bg-deep);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.nav-brand {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		text-decoration: none;
	}

	.nav-brand:hover {
		color: var(--color-accent);
	}

	.nav-links {
		display: flex;
		gap: var(--space-6);
	}

	.nav-links a {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.nav-links a:hover {
		color: var(--color-accent);
	}

	/* GiTS Cyberpunk Background */
	.bg-effects {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: -1;
		overflow: hidden;
	}

	.gradient-orb {
		position: absolute;
		border-radius: 50%;
		filter: blur(80px);
		opacity: 0.4;
		animation: float 20s ease-in-out infinite;
	}

	.orb-1 {
		width: 600px;
		height: 600px;
		background: radial-gradient(circle, #22d3ee 0%, transparent 70%);
		top: -200px;
		right: -200px;
		animation-delay: 0s;
	}

	.orb-2 {
		width: 500px;
		height: 500px;
		background: radial-gradient(circle, #6366f1 0%, transparent 70%);
		bottom: -150px;
		left: -150px;
		animation-delay: -10s;
	}

	@keyframes float {
		0%, 100% {
			transform: translate(0, 0) scale(1);
		}
		25% {
			transform: translate(30px, -30px) scale(1.05);
		}
		50% {
			transform: translate(-20px, 20px) scale(0.95);
		}
		75% {
			transform: translate(-30px, -20px) scale(1.02);
		}
	}

	.grid-overlay {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(#1a2530 1px, transparent 1px),
			linear-gradient(90deg, #1a2530 1px, transparent 1px);
		background-size: 40px 40px;
		opacity: 0.35;
		mask-image: radial-gradient(ellipse at 50% 0%, black 0%, transparent 70%);
		-webkit-mask-image: radial-gradient(ellipse at 50% 0%, black 0%, transparent 70%);
	}

	/* CRT scanline effect */
	.scanlines {
		position: absolute;
		inset: 0;
		background: repeating-linear-gradient(
			0deg,
			transparent 0px,
			transparent 2px,
			rgba(0, 0, 0, 0.1) 2px,
			rgba(0, 0, 0, 0.1) 4px
		);
		opacity: 0.12;
	}

	.noise-overlay {
		position: absolute;
		inset: 0;
		opacity: 0.03;
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
	}
</style>
