<script lang="ts">
	/**
	 * FindingCard — Lab Component
	 *
	 * Card for published findings. Solid presence with sage accent.
	 * Pinned items get a gold ribbon marker.
	 */
	import { base } from '$app/paths';
	import Badge from '$lib/components/ui/Badge.svelte';

	interface Finding {
		id: string;
		title: string;
		subtitle?: string;
		summary: string;
		date: string;
		keywords: string[];
		links: {
			findings: string;
			proposal?: string;
		};
	}

	let {
		finding,
		pinned = false,
		onKeywordClick
	}: {
		finding: Finding;
		pinned?: boolean;
		onKeywordClick?: (keyword: string) => void;
	} = $props();
</script>

<article class="finding-card" class:pinned>
	<header class="card-header">
		<span class="finding-id">REP-{finding.id}</span>
		<Badge variant="sage">Published</Badge>
	</header>

	<h3 class="finding-title">
		<a href="{base}{finding.links.findings}">{finding.title}</a>
	</h3>

	{#if finding.subtitle}
		<p class="finding-subtitle">{finding.subtitle}</p>
	{/if}

	{#if finding.summary}
		<p class="finding-summary">{finding.summary}</p>
	{/if}

	<div class="finding-keywords">
		{#each finding.keywords.slice(0, 4) as keyword}
			<button
				type="button"
				class="keyword-chip"
				onclick={() => onKeywordClick?.(keyword)}
			>
				{keyword}
			</button>
		{/each}
	</div>

	<footer class="card-footer">
		<span class="finding-date">{finding.date}</span>
		<div class="finding-links">
			<a href="{base}{finding.links.findings}" class="finding-link primary">Findings</a>
			{#if finding.links.proposal}
				<a href="{base}{finding.links.proposal}" class="finding-link">Proposal</a>
			{/if}
		</div>
	</footer>
</article>

<style>
	.finding-card {
		position: relative;
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-left: 4px solid var(--color-status-implemented);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		box-shadow: var(--shadow-sm);
		transition:
			border-color var(--duration-fast) var(--ease-out),
			box-shadow var(--duration-fast) var(--ease-out);
	}

	.finding-card:hover {
		border-color: var(--color-accent);
		border-left-color: var(--color-accent);
		box-shadow: var(--shadow-md);
	}

	/* Gold ribbon for pinned findings */
	.finding-card.pinned::after {
		content: '';
		position: absolute;
		top: -4px;
		left: var(--space-4);
		width: 8px;
		height: 24px;
		background: linear-gradient(
			135deg,
			var(--primitive-gold-300) 0%,
			var(--primitive-gold-500) 50%,
			var(--primitive-gold-300) 100%
		);
		border-radius: 0 0 2px 2px;
		box-shadow: 0 2px 4px hsl(35 30% 15% / 20%);
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-3);
	}

	.finding-id {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.finding-title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
		margin-bottom: var(--space-2);
	}

	.finding-title a {
		color: inherit;
		text-decoration: none;
	}

	.finding-title a:hover {
		color: var(--color-accent);
	}

	.finding-subtitle {
		font-size: var(--text-sm);
		font-style: italic;
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-3);
	}

	.finding-summary {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.finding-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-4);
	}

	.keyword-chip {
		font-family: var(--font-mono);
		font-size: 10px;
		color: var(--color-text-tertiary);
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		padding: 2px var(--space-2);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.keyword-chip:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-secondary);
	}

	.card-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.finding-date {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		font-variant-numeric: tabular-nums;
	}

	.finding-links {
		display: flex;
		gap: var(--space-3);
	}

	.finding-link {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.finding-link:hover {
		color: var(--color-accent);
	}

	.finding-link.primary {
		color: var(--color-accent);
	}
</style>
