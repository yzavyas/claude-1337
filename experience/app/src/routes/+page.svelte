<script lang="ts">
	import { base } from '$app/paths';
	import CopyCommand from '$lib/components/CopyCommand.svelte';

	const installCommand = '/plugin marketplace add yzavyas/claude-1337';
</script>

<svelte:head>
	<title>claude-1337 — Extensions that make you better</title>
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
		<div class="badge">
			<span class="badge-dot" aria-hidden="true"></span>
			<span class="badge-text">marketplace</span>
		</div>

		<h1 class="headline">Extensions that make you better</h1>

		<p class="description">
			Research-backed frameworks that shape how Claude thinks.<br />
			Readable. Forkable. Yours to verify.
		</p>

		<div class="install">
			<CopyCommand command={installCommand} />
			<p class="install-note">
				Run in Claude Code, then browse with <code>/plugin</code>
			</p>
			<div class="troubleshoot">
				<p class="troubleshoot-label">Known issues</p>
				<p class="troubleshoot-links">
					<a href="https://github.com/anthropics/claude-code/issues/14815" target="_blank" rel="noopener">#14815</a>,
					<a href="https://github.com/anthropics/claude-code/issues/14061" target="_blank" rel="noopener">#14061</a>,
					<a href="https://github.com/anthropics/claude-code/issues/15369" target="_blank" rel="noopener">#15369</a>
				</p>
				<p class="troubleshoot-links">
					Workaround → <a href="{base}/explore/how-to/troubleshoot">How-To</a>
				</p>
			</div>
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

	.badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-1) var(--space-4);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-8);
	}

	.badge-dot {
		width: 6px;
		height: 6px;
		background: var(--color-accent);
		border-radius: 50%;
	}

	.badge-text {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
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

	.troubleshoot {
		margin-top: var(--space-6);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.troubleshoot-label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		margin-bottom: var(--space-2);
	}

	.troubleshoot-links {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.troubleshoot-links a {
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.troubleshoot-links a:hover {
		color: var(--color-accent);
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
