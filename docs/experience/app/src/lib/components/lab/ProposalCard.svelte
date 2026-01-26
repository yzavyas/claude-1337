<script lang="ts">
	/**
	 * ProposalCard — Lab Component
	 *
	 * Card for active proposals. Dashed border (draft convention).
	 * Status determines accent color and badge variant.
	 */
	import { base } from '$app/paths';
	import Badge from '$lib/components/ui/Badge.svelte';

	type Status = 'draft' | 'discussion' | 'fcp' | 'accepted';

	interface Proposal {
		id: string;
		title: string;
		summary: string;
		status: Status;
		date: string;
		keywords: string[];
		links: {
			proposal: string;
			experiment?: string;
		};
	}

	let {
		proposal,
		onKeywordClick
	}: {
		proposal: Proposal;
		onKeywordClick?: (keyword: string) => void;
	} = $props();

	const statusVariant = {
		draft: 'muted',
		discussion: 'plum',
		fcp: 'rust',
		accepted: 'ocean'
	} as const;

	const statusLabel = {
		draft: 'Draft',
		discussion: 'Discussion',
		fcp: 'Final Comment',
		accepted: 'Accepted'
	} as const;

	// Show left accent for active proposals (not draft)
	const hasAccent = $derived(proposal.status !== 'draft');
</script>

<article
	class="proposal-card"
	class:has-accent={hasAccent}
	data-status={proposal.status}
>
	<header class="card-header">
		<span class="proposal-id">REP-{proposal.id}</span>
		<Badge variant={statusVariant[proposal.status]}>
			{statusLabel[proposal.status]}
		</Badge>
	</header>

	<h3 class="proposal-title">
		<a href="{base}{proposal.links.proposal}">{proposal.title}</a>
	</h3>

	<p class="proposal-summary">{proposal.summary}</p>

	<div class="proposal-keywords">
		{#each proposal.keywords.slice(0, 4) as keyword}
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
		<span class="proposal-date">{proposal.date}</span>
		<div class="proposal-links">
			<a href="{base}{proposal.links.proposal}" class="proposal-link primary">Proposal</a>
			{#if proposal.links.experiment}
				<a href="{base}{proposal.links.experiment}" class="proposal-link">Experiment</a>
			{/if}
		</div>
	</footer>
</article>

<style>
	.proposal-card {
		position: relative;
		background: var(--color-bg-elevated);
		border: 1px dashed var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		transition:
			border-color var(--duration-fast) var(--ease-out),
			border-style var(--duration-fast) var(--ease-out);
	}

	.proposal-card:hover {
		border-color: var(--color-border-strong);
		border-style: solid;
	}

	/* Left accent for active proposals */
	.proposal-card.has-accent {
		border-left-style: solid;
		border-left-width: 2px;
	}

	.proposal-card[data-status="discussion"] {
		border-left-color: var(--color-status-discussion);
	}

	.proposal-card[data-status="fcp"] {
		border-left-color: var(--color-status-fcp);
	}

	.proposal-card[data-status="accepted"] {
		border-left-color: var(--color-status-accepted);
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-3);
	}

	.proposal-id {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.proposal-title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
		margin-bottom: var(--space-2);
	}

	.proposal-title a {
		color: inherit;
		text-decoration: none;
	}

	.proposal-title a:hover {
		color: var(--color-accent);
	}

	.proposal-summary {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.proposal-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-4);
	}

	.keyword-chip {
		font-family: var(--font-mono);
		font-size: 10px;
		color: var(--color-text-tertiary);
		background: var(--color-bg-surface);
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

	.proposal-date {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		font-variant-numeric: tabular-nums;
	}

	.proposal-links {
		display: flex;
		gap: var(--space-3);
	}

	.proposal-link {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.proposal-link:hover {
		color: var(--color-accent);
	}

	.proposal-link.primary {
		color: var(--color-accent);
	}
</style>
