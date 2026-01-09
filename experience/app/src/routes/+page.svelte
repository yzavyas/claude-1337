<script lang="ts">
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
			<a href="{base}/catalog/" class="primary-action">
				<span>Browse extensions</span>
				<span class="arrow">→</span>
			</a>
		</div>
	</section>

	<section class="install">
		<h2 class="install-heading">Install</h2>
		<div class="install-steps">
			<div class="install-step">
				<span class="step-number">1</span>
				<div class="step-content">
					<p class="step-label">Clone the marketplace</p>
					<code class="step-code">git clone https://github.com/yzavyas/claude-1337.git</code>
				</div>
			</div>
			<div class="install-step">
				<span class="step-number">2</span>
				<div class="step-content">
					<p class="step-label">Add to Claude Code settings</p>
					<code class="step-code">~/.claude/settings.json → "pluginDirectories"</code>
				</div>
			</div>
			<div class="install-step">
				<span class="step-number">3</span>
				<div class="step-content">
					<p class="step-label">Skills auto-load when relevant</p>
					<code class="step-code">Use when: triggers activation</code>
				</div>
			</div>
		</div>
	</section>

	<div class="secondary-link">
		<a href="{base}/ethos/">Understand the approach</a>
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

	/* Install Section */
	.install {
		max-width: 560px;
		margin: 0 auto var(--space-16);
		animation: fadeIn 600ms ease 400ms both;
	}

	.install-heading {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin-bottom: var(--space-6);
		text-align: center;
	}

	.install-steps {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.install-step {
		display: flex;
		align-items: flex-start;
		gap: var(--space-4);
		padding: var(--space-4);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
	}

	.step-number {
		flex-shrink: 0;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-accent-muted);
		color: var(--color-accent);
		border-radius: var(--radius-full);
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: var(--font-semibold);
	}

	.step-content {
		flex: 1;
		min-width: 0;
	}

	.step-label {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-1);
	}

	.step-code {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		background: var(--color-bg-elevated);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-sm);
		overflow-x: auto;
	}

	/* Mobile */
	@media (max-width: 640px) {
		.headline-primary {
			font-size: var(--text-3xl);
		}

		.install-step {
			flex-direction: column;
			gap: var(--space-2);
		}

		.step-code {
			font-size: 11px;
		}
	}
</style>
