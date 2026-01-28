<script lang="ts">
	import { base } from '$app/paths';
	import CopyCommand from '$lib/components/CopyCommand.svelte';
	import FlipTerm from '$lib/components/FlipTerm.svelte';

	const installCommand = '/plugin marketplace add yzavyas/claude-1337';
</script>

<svelte:head>
	<title>claude-1337 — Cognitive Extensions for Effective Collaborative Intelligence</title>
</svelte:head>

<nav class="landing-nav">
	<a href="{base}/" class="nav-brand">claude-1337</a>
	<div class="nav-links">
		<a href="{base}/catalog/">Catalog</a>
		<a href="{base}/lab/">Lab</a>
		<a href="{base}/library/">Library</a>
		<a href="{base}/ethos/">Ethos</a>
		<a href="https://github.com/yzavyas/claude-1337" target="_blank" rel="noopener">GitHub ↗</a>
		<a href="https://github.com/yzavyas/claude-1337/discussions" target="_blank" rel="noopener">Forum ↗</a>
	</div>
</nav>

<main class="landing">
	<section class="hero">
		<h1 class="headline">
			<span class="headline-line"><FlipTerm term="Cognitive Extensions" definition="External processes that become part of thinking" /></span>
			<span class="headline-line"><FlipTerm term="for Effective" definition="Complementary · Transparent · Reliable" /></span>
			<span class="headline-line nowrap"><FlipTerm term="Collaborative Intelligence" definition="Human-AI cognitive partnership" /></span>
		</h1>

		<p class="description">
			Capability extensions for AI-enhanced builders.<br />
			Learn with your agents. Grow your knowledge through collaboration.
		</p>

		<div class="install">
			<CopyCommand command={installCommand} />
			<p class="install-note">
				Run in Claude Code, then browse with <code>/plugin</code>
			</p>
		</div>

		<div class="secondary-actions">
			<a href="{base}/catalog/">Browse extensions</a>
			<span class="separator" aria-hidden="true">·</span>
			<a href="{base}/ethos/">Why this approach</a>
		</div>
	</section>
</main>

<style>
	.landing {
		min-height: 100vh;
		min-height: 100dvh;
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: var(--space-6);
		background: var(--color-bg);
	}

	.hero {
		max-width: 560px;
		text-align: center;
		margin: 0 auto;
	}

	.headline {
		font-family: var(--font-heading);
		font-size: var(--text-4xl);
		font-weight: var(--font-medium);
		letter-spacing: var(--tracking-tighter);
		line-height: var(--leading-tight);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.headline-line {
		display: block;
	}

	.headline-line.nowrap {
		white-space: nowrap;
	}

	.description {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-8);
	}

	.install {
		margin-bottom: var(--space-8);
	}

	.install-note {
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.install-note code {
		font-family: var(--font-mono);
		color: var(--color-text-secondary);
	}

	.secondary-actions {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--space-3);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
	}

	.secondary-actions a {
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.secondary-actions a:hover {
		color: var(--color-accent);
	}

	.separator {
		color: var(--color-text-muted);
	}

	/* Landing Nav */
	.landing-nav {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-3) var(--space-6);
		background: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
		z-index: 100;
	}

	.nav-brand {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-text);
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
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.nav-links a:hover {
		color: var(--color-accent);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.landing {
			padding: var(--space-4);
		}

		.headline {
			font-size: var(--text-2xl);
		}

		.secondary-actions {
			flex-direction: column;
			gap: var(--space-2);
		}

		.separator {
			display: none;
		}

		.landing-nav {
			padding: var(--space-2) var(--space-4);
		}

		.nav-links {
			gap: var(--space-4);
		}

		.nav-links a,
		.nav-brand {
			font-size: var(--text-xs);
		}
	}
</style>
