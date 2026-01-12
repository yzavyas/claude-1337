<script lang="ts">
	import { base } from '$app/paths';

	let copied = $state(false);
	const installCommand = '/plugin marketplace add yzavyas/claude-1337';

	async function copyCommand() {
		await navigator.clipboard.writeText(installCommand);
		copied = true;
		setTimeout(() => copied = false, 2000);
	}
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

		<p class="headline-intro">Cognitive extensions for</p>
		<h1 class="headline">
			<span class="headline-primary">Effective Collaborative Intelligence</span>
		</h1>

		<p class="description">
			Collaboration that compounds capability.
		</p>

		<div class="actions">
			<a href="{base}/ethos/" class="primary-action">
				<span>Understand the approach</span>
				<span class="arrow">→</span>
			</a>
		</div>
	</section>

	<section class="install">
		<h2 class="install-heading">Add to Claude Code</h2>
		<button class="install-command" onclick={copyCommand}>
			<span class="command-code">{installCommand}</span>
			<span class="copy-hint">{copied ? 'Copied!' : 'copy'}</span>
		</button>
		<p class="install-note">Then browse and install individual plugins with <code>/plugin</code></p>

		<div class="troubleshoot">
			<p class="troubleshoot-label">Known issues</p>
			<p class="troubleshoot-links">
				<a href="https://github.com/anthropics/claude-code/issues/14815">#14815</a>,
				<a href="https://github.com/anthropics/claude-code/issues/14061">#14061</a>,
				<a href="https://github.com/anthropics/claude-code/issues/15369">#15369</a>
			</p>
			<p class="troubleshoot-links">
				Workaround → <a href="{base}/explore/how-to/troubleshoot">How-To</a>
			</p>
		</div>
	</section>

	<div class="secondary-link">
		<a href="{base}/catalog/">Browse extensions</a>
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

	.headline-intro {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.15em;
		margin-bottom: var(--space-3);
		animation: fadeIn 600ms ease 50ms both;
	}

	.headline {
		margin-bottom: var(--space-6);
		animation: fadeIn 600ms ease 100ms both;
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

	/* Install Section */
	.install {
		max-width: 560px;
		margin: 0 auto var(--space-16);
		animation: fadeIn 600ms ease 400ms both;
		text-align: center;
	}

	.install-heading {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin-bottom: var(--space-4);
	}

	.install-command {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-4);
		width: 100%;
		padding: var(--space-3) var(--space-4);
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		margin-bottom: var(--space-3);
		cursor: pointer;
		transition:
			border-color var(--duration-fast) var(--ease-out),
			background var(--duration-fast) var(--ease-out);
	}

	.install-command:hover {
		border-color: var(--color-accent);
		background: var(--color-bg-surface);
	}

	.install-command:active {
		transform: scale(0.98);
	}

	.command-code {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.copy-hint {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		opacity: 0;
		transition: opacity var(--duration-fast) var(--ease-out);
	}

	.install-command:hover .copy-hint {
		opacity: 1;
	}

	.install-note {
		font-size: var(--text-xs);
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
		.headline-primary {
			font-size: var(--text-3xl);
		}

		.command-code {
			font-size: var(--text-xs);
		}
	}
</style>
