<script lang="ts">
	import { base } from '$app/paths';
	import { browser } from '$app/environment';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

	let theme = $state<'light' | 'dark'>('dark');

	// Initialize theme from system preference or localStorage
	if (browser) {
		const stored = localStorage.getItem('theme');
		if (stored === 'light' || stored === 'dark') {
			theme = stored;
		} else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
			theme = 'light';
		}

		// Listen for system preference changes
		window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
			if (!localStorage.getItem('theme')) {
				theme = e.matches ? 'dark' : 'light';
			}
		});
	}

	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		if (browser) {
			localStorage.setItem('theme', theme);
		}
	}

	// Apply theme to document
	$effect(() => {
		if (browser) {
			document.documentElement.setAttribute('data-theme', theme);
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
	<title>claude-1337</title>
</svelte:head>

<div class="site" data-theme={theme}>
	<!-- Closed Alpha Banner -->
	<div class="alpha-banner">
		<span class="alpha-badge">closed alpha</span>
		<span class="alpha-text">This marketplace is in early development. Extensions are experimental.</span>
	</div>

	<nav class="nav">
		<a href="{base}/" class="logo">
			<span class="logo-prompt">$</span>
			<span class="logo-text">claude-1337</span>
		</a>
		<div class="nav-right">
			<div class="links">
				<a href="{base}/explore/">explore</a>
				<a href="{base}/ethos/">ethos</a>
			</div>
			<button class="theme-toggle" onclick={toggleTheme} aria-label="Toggle theme">
				{#if theme === 'dark'}
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<circle cx="12" cy="12" r="5"/>
						<path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
					</svg>
				{:else}
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
					</svg>
				{/if}
			</button>
		</div>
	</nav>

	<main>
		{@render children()}
	</main>

	<footer class="footer">
		<span class="footer-text">cognitive extensions for effective collaborative intelligence</span>
	</footer>
</div>

<!-- Background effects -->
<div class="bg-effects" aria-hidden="true">
	<div class="gradient-orb orb-1"></div>
	<div class="gradient-orb orb-2"></div>
	<div class="grid-overlay"></div>
	<div class="noise-overlay"></div>
</div>

<style>
	/* ═══════════════════════════════════════════════════════════════
	   Design System: CSS Custom Properties
	   ═══════════════════════════════════════════════════════════════ */

	:global(:root) {
		/* Typography */
		--font-sans: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
		--font-mono: 'JetBrains Mono', 'SF Mono', Monaco, monospace;

		/* Spacing */
		--space-xs: 0.25rem;
		--space-sm: 0.5rem;
		--space-md: 1rem;
		--space-lg: 1.5rem;
		--space-xl: 2rem;
		--space-2xl: 3rem;
		--space-3xl: 4rem;

		/* Transitions */
		--transition-fast: 150ms ease;
		--transition-base: 250ms ease;

		/* Border radius */
		--radius-sm: 4px;
		--radius-md: 6px;
		--radius-lg: 8px;
	}

	/* Dark theme (default) */
	:global(:root),
	:global([data-theme="dark"]) {
		--bg-primary: #0a0a0b;
		--bg-secondary: #111113;
		--bg-surface: #161618;
		--bg-elevated: #1c1c1f;

		--border-subtle: #232326;
		--border-default: #2a2a2e;
		--border-strong: #3a3a3f;

		--text-primary: #e8e8e6;
		--text-secondary: #a0a0a0;
		--text-muted: #6a6a6a;

		--accent: #e5a034;
		--accent-hover: #f0b050;
		--accent-muted: rgba(229, 160, 52, 0.15);

		--link: #6cb6ff;
		--link-hover: #8fc9ff;

		--code-bg: #1a1a1c;
		--code-text: #e0e0e0;

		--success: #4ade80;
		--warning: #fbbf24;
		--error: #f87171;
	}

	/* Light theme */
	:global([data-theme="light"]) {
		--bg-primary: #fafafa;
		--bg-secondary: #f5f5f5;
		--bg-surface: #ffffff;
		--bg-elevated: #ffffff;

		--border-subtle: #e8e8e8;
		--border-default: #e0e0e0;
		--border-strong: #d0d0d0;

		--text-primary: #1a1a1a;
		--text-secondary: #525252;
		--text-muted: #8a8a8a;

		--accent: #c47f17;
		--accent-hover: #a66a0f;
		--accent-muted: rgba(196, 127, 23, 0.1);

		--link: #0066cc;
		--link-hover: #0052a3;

		--code-bg: #f0f0f0;
		--code-text: #1a1a1a;

		--success: #16a34a;
		--warning: #ca8a04;
		--error: #dc2626;
	}

	/* ═══════════════════════════════════════════════════════════════
	   Global Reset & Base Styles
	   ═══════════════════════════════════════════════════════════════ */

	:global(*) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(html) {
		scroll-behavior: smooth;
	}

	:global(body) {
		font-family: var(--font-sans);
		font-size: 15px;
		line-height: 1.65;
		color: var(--text-primary);
		background: var(--bg-primary);
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		transition: background var(--transition-base), color var(--transition-base);
	}

	:global(::selection) {
		background: var(--accent-muted);
		color: var(--text-primary);
	}

	/* ═══════════════════════════════════════════════════════════════
	   Layout
	   ═══════════════════════════════════════════════════════════════ */

	.site {
		max-width: 52rem;
		margin: 0 auto;
		padding: var(--space-xl) var(--space-lg);
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	/* ═══════════════════════════════════════════════════════════════
	   Alpha Banner
	   ═══════════════════════════════════════════════════════════════ */

	.alpha-banner {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-sm);
		padding: var(--space-xs) var(--space-md);
		background: linear-gradient(90deg, var(--accent-muted), transparent, var(--accent-muted));
		border-bottom: 1px solid var(--accent-muted);
		font-size: 0.8rem;
	}

	.alpha-badge {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		padding: 2px 8px;
		background: var(--accent);
		color: var(--bg-primary);
		border-radius: var(--radius-sm);
	}

	.alpha-text {
		color: var(--text-secondary);
	}

	/* ═══════════════════════════════════════════════════════════════
	   Navigation
	   ═══════════════════════════════════════════════════════════════ */

	.nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-3xl);
		padding-bottom: var(--space-lg);
		border-bottom: 1px solid var(--border-subtle);
	}

	.logo {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		text-decoration: none;
		transition: opacity var(--transition-fast);
	}

	.logo:hover {
		opacity: 1;
	}

	.logo:hover .logo-prompt {
		text-shadow: 0 0 12px var(--accent);
	}

	.logo-prompt {
		font-family: var(--font-mono);
		font-size: 1rem;
		font-weight: 500;
		color: var(--accent);
		transition: text-shadow var(--transition-fast);
	}

	.logo-text {
		font-family: var(--font-mono);
		font-size: 1rem;
		font-weight: 500;
		color: var(--text-primary);
		letter-spacing: -0.01em;
	}

	.nav-right {
		display: flex;
		align-items: center;
		gap: var(--space-lg);
	}

	.links {
		display: flex;
		gap: var(--space-lg);
	}

	.links a {
		font-family: var(--font-mono);
		font-size: 0.85rem;
		color: var(--text-secondary);
		text-decoration: none;
		transition: color var(--transition-fast);
		position: relative;
	}

	.links a::after {
		content: '';
		position: absolute;
		bottom: -2px;
		left: 0;
		width: 0;
		height: 1px;
		background: var(--accent);
		transition: width var(--transition-fast);
	}

	.links a:hover {
		color: var(--text-primary);
	}

	.links a:hover::after {
		width: 100%;
		box-shadow: 0 0 8px var(--accent);
	}

	.theme-toggle {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		background: transparent;
		border: 1px solid var(--border-default);
		border-radius: var(--radius-md);
		color: var(--text-secondary);
		cursor: pointer;
		transition: all var(--transition-fast);
	}

	.theme-toggle:hover {
		border-color: var(--accent);
		color: var(--accent);
		background: var(--bg-surface);
		box-shadow: 0 0 16px -4px var(--accent);
	}

	/* ═══════════════════════════════════════════════════════════════
	   Main Content
	   ═══════════════════════════════════════════════════════════════ */

	main {
		flex: 1;
		animation: fadeIn 300ms ease;
	}

	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(8px); }
		to { opacity: 1; transform: translateY(0); }
	}

	/* ═══════════════════════════════════════════════════════════════
	   Footer
	   ═══════════════════════════════════════════════════════════════ */

	.footer {
		margin-top: var(--space-3xl);
		padding-top: var(--space-lg);
		border-top: 1px solid var(--border-subtle);
		text-align: center;
	}

	.footer-text {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--text-muted);
		letter-spacing: 0.02em;
	}

	/* ═══════════════════════════════════════════════════════════════
	   Markdown Content Styles
	   ═══════════════════════════════════════════════════════════════ */

	:global(.markdown-content) {
		max-width: 100%;
	}

	:global(.markdown-content h1) {
		font-size: 2rem;
		font-weight: 600;
		margin-bottom: var(--space-md);
		line-height: 1.2;
		color: var(--text-primary);
		letter-spacing: -0.02em;
	}

	:global(.markdown-content h2) {
		font-size: 1.35rem;
		font-weight: 600;
		margin-top: var(--space-2xl);
		margin-bottom: var(--space-md);
		color: var(--text-primary);
		letter-spacing: -0.01em;
	}

	:global(.markdown-content h3) {
		font-size: 1.1rem;
		font-weight: 600;
		margin-top: var(--space-xl);
		margin-bottom: var(--space-sm);
		color: var(--text-primary);
	}

	:global(.markdown-content p) {
		margin-bottom: var(--space-md);
		color: var(--text-secondary);
	}

	:global(.markdown-content a) {
		color: var(--link);
		text-decoration: none;
		transition: color var(--transition-fast);
	}

	:global(.markdown-content a:hover) {
		color: var(--link-hover);
		text-decoration: underline;
	}

	:global(.markdown-content code) {
		font-family: var(--font-mono);
		font-size: 0.85em;
		background: var(--code-bg);
		color: var(--code-text);
		padding: 0.15em 0.4em;
		border-radius: var(--radius-sm);
		border: 1px solid var(--border-subtle);
	}

	:global(.markdown-content pre) {
		background: var(--bg-elevated);
		border: 1px solid var(--border-default);
		padding: var(--space-md);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--space-md) 0;
	}

	:global(.markdown-content pre code) {
		background: none;
		border: none;
		padding: 0;
		font-size: 0.85rem;
		color: var(--code-text);
	}

	:global(.markdown-content ul),
	:global(.markdown-content ol) {
		margin: var(--space-md) 0;
		padding-left: var(--space-lg);
		color: var(--text-secondary);
	}

	:global(.markdown-content li) {
		margin-bottom: var(--space-xs);
	}

	:global(.markdown-content li::marker) {
		color: var(--text-muted);
	}

	:global(.markdown-content table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-md) 0;
		font-size: 0.9rem;
	}

	:global(.markdown-content th),
	:global(.markdown-content td) {
		text-align: left;
		padding: var(--space-sm) var(--space-md);
		border-bottom: 1px solid var(--border-default);
	}

	:global(.markdown-content th) {
		font-weight: 600;
		color: var(--text-primary);
		background: var(--bg-surface);
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	:global(.markdown-content td) {
		color: var(--text-secondary);
	}

	:global(.markdown-content tr:hover td) {
		background: var(--bg-surface);
	}

	:global(.markdown-content hr) {
		border: none;
		border-top: 1px solid var(--border-subtle);
		margin: var(--space-2xl) 0;
	}

	:global(.markdown-content blockquote) {
		border-left: 3px solid var(--accent);
		padding-left: var(--space-md);
		margin: var(--space-md) 0;
		color: var(--text-secondary);
		font-style: italic;
	}

	:global(.markdown-content em) {
		color: var(--text-secondary);
	}

	:global(.markdown-content strong) {
		font-weight: 600;
		color: var(--text-primary);
	}

	/* ═══════════════════════════════════════════════════════════════
	   Responsive
	   ═══════════════════════════════════════════════════════════════ */

	@media (max-width: 640px) {
		.site {
			padding: var(--space-md);
		}

		.nav {
			margin-bottom: var(--space-xl);
		}

		.links {
			gap: var(--space-md);
		}

		:global(.markdown-content h1) {
			font-size: 1.6rem;
		}

		:global(.markdown-content h2) {
			font-size: 1.2rem;
		}
	}

	/* ═══════════════════════════════════════════════════════════════
	   Background Effects & Flair
	   ═══════════════════════════════════════════════════════════════ */

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
		background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
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
			linear-gradient(var(--border-subtle) 1px, transparent 1px),
			linear-gradient(90deg, var(--border-subtle) 1px, transparent 1px);
		background-size: 60px 60px;
		opacity: 0.3;
		mask-image: radial-gradient(ellipse at center, black 0%, transparent 70%);
		-webkit-mask-image: radial-gradient(ellipse at center, black 0%, transparent 70%);
	}

	.noise-overlay {
		position: absolute;
		inset: 0;
		opacity: 0.03;
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
	}

	/* Light mode adjustments */
	:global([data-theme="light"]) .gradient-orb {
		opacity: 0.2;
	}

	:global([data-theme="light"]) .grid-overlay {
		opacity: 0.15;
	}

	:global([data-theme="light"]) .orb-1 {
		background: radial-gradient(circle, #f59e0b 0%, transparent 70%);
	}

	:global([data-theme="light"]) .orb-2 {
		background: radial-gradient(circle, #8b5cf6 0%, transparent 70%);
	}
</style>
