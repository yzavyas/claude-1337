<script lang="ts">
	import { base } from '$app/paths';
	import { marked } from 'marked';

	let { data } = $props();

	marked.setOptions({ gfm: true, breaks: false });

	const readmeHtml = $derived(data.readme ? marked.parse(data.readme) : null);
</script>

<svelte:head>
	<title>{data.name} — Lab — claude-1337</title>
</svelte:head>

<main class="experiment-page">
	<nav class="breadcrumb">
		<a href="{base}/lab">Lab</a>
		<span class="sep">/</span>
		<span class="current">{data.slug}</span>
	</nav>

	<header class="experiment-header">
		<h1>{data.name}</h1>
		{#if data.repId}
			<a href="{base}/lab/proposals/rep-{data.repId}-rigor-is-what-you-want" class="rep-link">
				REP-{data.repId}
			</a>
		{/if}
	</header>

	{#if readmeHtml}
		<section class="readme markdown-content">
			{@html readmeHtml}
		</section>
	{/if}

	{#if data.results.length > 0}
		<section class="results-section">
			<h2>Results</h2>
			<div class="results-grid">
				{#each data.results as result}
					<article class="result-card">
						<header class="result-header">
							<span class="result-name">{result.name}</span>
							<span class="result-model">{result.model}</span>
						</header>

						<div class="metrics">
							<div class="metric">
								<span class="metric-label">Single-shot</span>
								<span class="metric-value" class:success={result.summary.singleShot.passRate >= 0.9}>
									{(result.summary.singleShot.passRate * 100).toFixed(0)}%
								</span>
								<span class="metric-detail">
									{result.summary.singleShot.passed}/{result.summary.singleShot.total}
								</span>
								{#if result.summary.singleShot.avgTokens > 0}
									<span class="metric-tokens">~{Math.round(result.summary.singleShot.avgTokens)} tokens</span>
								{/if}
							</div>
							<div class="metric">
								<span class="metric-label">Ralph-style</span>
								<span class="metric-value" class:success={result.summary.ralphStyle.passRate >= 0.9}>
									{(result.summary.ralphStyle.passRate * 100).toFixed(0)}%
								</span>
								<span class="metric-detail">
									{result.summary.ralphStyle.passed}/{result.summary.ralphStyle.total}
								</span>
								{#if result.summary.ralphStyle.avgTokens > 0}
									<span class="metric-tokens">~{Math.round(result.summary.ralphStyle.avgTokens)} tokens</span>
								{/if}
							</div>
						</div>

						{#if result.summary.ralphStyle.passed > result.summary.singleShot.passed}
							<div class="recovery">
								+{result.summary.ralphStyle.passed - result.summary.singleShot.passed} recovered via iteration
							</div>
						{/if}

						<footer class="result-footer">
							<span class="timestamp">
								{new Date(result.timestamp).toLocaleDateString('en-US', {
									year: 'numeric',
									month: 'short',
									day: 'numeric'
								})}
							</span>
							{#if result.hasAnalysis}
								<a href={result.analysisPath} class="analysis-link">View Analysis</a>
							{/if}
						</footer>
					</article>
				{/each}
			</div>
		</section>
	{:else}
		<div class="empty-state">
			<p>No results yet for this experiment.</p>
			<p class="hint">Run the experiment with <code>lab-1337 run {data.slug}</code></p>
		</div>
	{/if}

	<footer class="page-footer">
		<a href="{base}/lab" class="back-link">← Back to Lab</a>
	</footer>
</main>

<style>
	.experiment-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 1000px;
		margin: 0 auto;
	}

	.breadcrumb {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-6);
	}

	.breadcrumb a {
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.breadcrumb a:hover {
		color: var(--color-accent);
	}

	.breadcrumb .sep {
		margin: 0 var(--space-2);
		opacity: 0.5;
	}

	.breadcrumb .current {
		color: var(--color-text-tertiary);
	}

	.experiment-header {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		margin-bottom: var(--space-8);
	}

	.experiment-header h1 {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	.rep-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-sm);
		text-decoration: none;
	}

	.readme {
		margin-bottom: var(--space-10);
	}

	.markdown-content {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-8);
	}

	.markdown-content :global(h1) {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.markdown-content :global(h2) {
		font-size: var(--text-lg);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	.markdown-content :global(p) {
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.markdown-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-surface);
		padding: 2px var(--space-1);
		border-radius: var(--radius-sm);
	}

	.markdown-content :global(pre) {
		background: var(--color-bg-surface);
		padding: var(--space-4);
		border-radius: var(--radius-md);
		overflow-x: auto;
	}

	.markdown-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.markdown-content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-4) 0;
	}

	.markdown-content :global(th),
	.markdown-content :global(td) {
		text-align: left;
		padding: var(--space-2) var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.results-section h2 {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.results-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: var(--space-4);
	}

	.result-card {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
	}

	.result-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-4);
	}

	.result-name {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-primary);
	}

	.result-model {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.metrics {
		display: flex;
		gap: var(--space-6);
		margin-bottom: var(--space-4);
	}

	.metric {
		flex: 1;
	}

	.metric-label {
		display: block;
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: var(--space-1);
	}

	.metric-value {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-secondary);
	}

	.metric-value.success {
		color: var(--color-accent-positive);
	}

	.metric-detail {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.metric-tokens {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		margin-top: var(--space-1);
	}

	.recovery {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent-positive);
		background: color-mix(in srgb, var(--color-accent-positive) 10%, transparent);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-sm);
		text-align: center;
		margin-bottom: var(--space-4);
	}

	.result-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: var(--space-3);
		border-top: 1px solid var(--color-border-subtle);
	}

	.timestamp {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.analysis-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		text-decoration: none;
	}

	.empty-state {
		text-align: center;
		padding: var(--space-12);
		color: var(--color-text-secondary);
	}

	.empty-state .hint {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-top: var(--space-2);
	}

	.empty-state code {
		font-family: var(--font-mono);
		background: var(--color-bg-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.page-footer {
		margin-top: var(--space-10);
		padding-top: var(--space-4);
	}

	.back-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		text-decoration: none;
	}

	.back-link:hover {
		color: var(--color-accent);
	}

	@media (max-width: 640px) {
		.experiment-page {
			padding-top: 100px;
		}

		.experiment-header {
			flex-direction: column;
			align-items: flex-start;
		}

		.results-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
