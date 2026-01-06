<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import { base } from '$app/paths';
	import { getContent } from '$lib/content';

	const content = getContent('start');

	// Typing animation for the tagline
	let displayed = $state('');
	const fullText = 'engineering excellence through collaboration';

	$effect(() => {
		let i = 0;
		const interval = setInterval(() => {
			if (i <= fullText.length) {
				displayed = fullText.slice(0, i);
				i++;
			} else {
				clearInterval(interval);
			}
		}, 40);
		return () => clearInterval(interval);
	});
</script>

<!-- Hero Section -->
<section class="hero">
	<div class="hero-badge">
		<span class="badge-dot"></span>
		<span class="badge-text">marketplace</span>
	</div>

	<h1 class="hero-title">
		<span class="title-line">
			<span class="prompt">$</span>
			<span class="highlight">claude-1337</span>
		</span>
	</h1>

	<p class="hero-tagline">
		cognitive extensions for
		<span class="emphasis">effective collaborative intelligence</span>
	</p>

	<p class="hero-typing">
		<span class="typing-text">{displayed}</span>
		<span class="cursor">▊</span>
	</p>

	<div class="hero-description">
		<p>Extensions that make engineers <strong>more capable</strong>, not more dependent.</p>
		<p>Five extension types — skills, hooks, agents, commands, MCP. Knowledge that compounds. You grow, the system learns.</p>
	</div>

	<div class="hero-actions">
		<a href="{base}/explore/reference/catalog/" class="btn-primary">
			<span class="btn-icon">→</span>
			browse catalog
		</a>
		<a href="{base}/explore/" class="btn-secondary">
			explore docs
		</a>
	</div>

	<div class="hero-install">
		<code class="install-cmd">
			<span class="cmd-prompt">$</span>
			<span class="cmd-text">/plugin marketplace add yzavyas/claude-1337</span>
		</code>
	</div>
</section>

<!-- Divider -->
<div class="section-divider">
	<span class="divider-text">why this exists</span>
</div>

<!-- Content from markdown -->
<article class="markdown-content home-content">
	{#if content}
		<SvelteMarkdown source={content} />
	{:else}
		<p>Loading content...</p>
	{/if}
</article>

<style>
	/* ═══════════════════════════════════════════════════════════════
	   Hero Section
	   ═══════════════════════════════════════════════════════════════ */

	.hero {
		text-align: center;
		padding: var(--space-2xl) 0 var(--space-3xl);
		animation: heroFadeIn 600ms ease;
	}

	@keyframes heroFadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.hero-badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-xs) var(--space-md);
		background: var(--bg-surface);
		border: 1px solid var(--border-default);
		border-radius: 999px;
		margin-bottom: var(--space-xl);
		animation: badgePulse 3s ease-in-out infinite;
	}

	@keyframes badgePulse {
		0%, 100% { box-shadow: 0 0 0 0 var(--accent-muted); }
		50% { box-shadow: 0 0 0 8px transparent; }
	}

	.badge-dot {
		width: 8px;
		height: 8px;
		background: var(--success);
		border-radius: 50%;
		animation: dotPulse 2s ease-in-out infinite;
	}

	@keyframes dotPulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}

	.badge-text {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}

	.hero-title {
		font-size: clamp(2.5rem, 8vw, 4rem);
		font-weight: 600;
		line-height: 1.1;
		margin-bottom: var(--space-md);
		letter-spacing: -0.03em;
	}

	.title-line {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-md);
	}

	.prompt {
		font-family: var(--font-mono);
		color: var(--accent);
		font-size: 0.8em;
		animation: promptBlink 1.5s ease-in-out infinite;
	}

	@keyframes promptBlink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.6; }
	}

	.highlight {
		font-family: var(--font-mono);
		background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent) 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-tagline {
		font-size: 1.25rem;
		color: var(--text-secondary);
		margin-bottom: var(--space-md);
		line-height: 1.4;
	}

	.emphasis {
		color: var(--text-primary);
		font-weight: 500;
	}

	.hero-typing {
		font-family: var(--font-mono);
		font-size: 1rem;
		color: var(--accent);
		margin-bottom: var(--space-xl);
		min-height: 1.5em;
	}

	.cursor {
		animation: cursorBlink 1s step-end infinite;
		opacity: 1;
	}

	@keyframes cursorBlink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0; }
	}

	.hero-description {
		max-width: 500px;
		margin: 0 auto var(--space-xl);
	}

	.hero-description p {
		font-size: 1rem;
		color: var(--text-secondary);
		line-height: 1.6;
		margin-bottom: var(--space-sm);
	}

	.hero-description strong {
		color: var(--text-primary);
	}

	.hero-actions {
		display: flex;
		gap: var(--space-md);
		justify-content: center;
		margin-bottom: var(--space-xl);
		flex-wrap: wrap;
	}

	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-lg);
		background: var(--accent);
		color: #0a0a0b;
		font-family: var(--font-mono);
		font-size: 0.9rem;
		font-weight: 500;
		text-decoration: none;
		border-radius: var(--radius-md);
		transition: all var(--transition-fast);
	}

	.btn-primary:hover {
		background: var(--accent-hover);
		transform: translateY(-2px);
		box-shadow: 0 8px 20px -8px var(--accent);
	}

	.btn-icon {
		transition: transform var(--transition-fast);
	}

	.btn-primary:hover .btn-icon {
		transform: translateX(4px);
	}

	.btn-secondary {
		display: inline-flex;
		align-items: center;
		padding: var(--space-sm) var(--space-lg);
		background: transparent;
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 0.9rem;
		text-decoration: none;
		border: 1px solid var(--border-default);
		border-radius: var(--radius-md);
		transition: all var(--transition-fast);
	}

	.btn-secondary:hover {
		border-color: var(--border-strong);
		color: var(--text-primary);
		background: var(--bg-surface);
	}

	.hero-install {
		display: flex;
		justify-content: center;
	}

	.install-cmd {
		display: inline-flex;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-md);
		background: var(--bg-elevated);
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-md);
		font-family: var(--font-mono);
		font-size: 0.85rem;
		transition: all var(--transition-fast);
		cursor: pointer;
	}

	.install-cmd:hover {
		border-color: var(--accent);
		background: var(--bg-surface);
	}

	.cmd-prompt {
		color: var(--accent);
	}

	.cmd-text {
		color: var(--text-secondary);
	}

	/* ═══════════════════════════════════════════════════════════════
	   Section Divider
	   ═══════════════════════════════════════════════════════════════ */

	.section-divider {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		margin: var(--space-3xl) 0 var(--space-xl);
	}

	.section-divider::before,
	.section-divider::after {
		content: '';
		flex: 1;
		height: 1px;
		background: linear-gradient(90deg, transparent, var(--border-default), transparent);
	}

	.divider-text {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}

	/* ═══════════════════════════════════════════════════════════════
	   Home Content (after hero)
	   ═══════════════════════════════════════════════════════════════ */

	.home-content {
		padding-bottom: var(--space-2xl);
	}

	/* Hide the first h1 since we have the hero */
	.home-content :global(h1:first-child) {
		display: none;
	}

	/* ═══════════════════════════════════════════════════════════════
	   Responsive
	   ═══════════════════════════════════════════════════════════════ */

	@media (max-width: 640px) {
		.hero {
			padding: var(--space-lg) 0 var(--space-2xl);
		}

		.hero-title {
			font-size: 2rem;
		}

		.title-line {
			flex-direction: column;
			gap: var(--space-xs);
		}

		.prompt {
			font-size: 1.2rem;
		}

		.hero-tagline {
			font-size: 1.1rem;
		}

		.hero-typing {
			font-size: 0.85rem;
		}

		.hero-actions {
			flex-direction: column;
			align-items: stretch;
		}

		.btn-primary,
		.btn-secondary {
			justify-content: center;
		}

		.install-cmd {
			font-size: 0.75rem;
		}
	}
</style>
