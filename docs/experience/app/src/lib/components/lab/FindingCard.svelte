<script lang="ts">
	/**
	 * FindingCard — Lab Component
	 *
	 * Card for published REPs with findings. Click opens a dialog preview.
	 */
	import StatusBadge from './StatusBadge.svelte';
	import FindingDialog from './FindingDialog.svelte';

	interface Finding {
		id: string;
		title: string;
		summary: string;
		hypothesis?: string;
		findingsRaw?: string;
		date: string;
		keywords: string[];
		links: {
			rep: string;
			experiment?: string;
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

	let dialogOpen = $state(false);

	function openDialog() {
		dialogOpen = true;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			openDialog();
		}
	}

	function handleKeywordClick(e: MouseEvent, keyword: string) {
		e.stopPropagation();
		onKeywordClick?.(keyword);
	}
</script>

<article
	class="finding-card"
	class:pinned
	onclick={openDialog}
	onkeydown={handleKeydown}
	role="button"
	tabindex="0"
	aria-haspopup="dialog"
>
	<header class="card-header">
		<span class="finding-id">REP-{finding.id}</span>
		<StatusBadge status="implemented" />
	</header>

	<h3 class="finding-title">{finding.title}</h3>

	{#if finding.keywords.length > 0}
		<div class="finding-keywords">
			{#each finding.keywords.slice(0, 4) as keyword}
				<button
					type="button"
					class="keyword-chip"
					onclick={(e) => handleKeywordClick(e, keyword)}
				>
					{keyword}
				</button>
			{/each}
		</div>
	{/if}

	<div class="card-hint">
		<span class="hint-text">Click to preview</span>
		<svg class="hint-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
			<path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		</svg>
	</div>
</article>

<FindingDialog {finding} bind:open={dialogOpen} />

<style>
	.finding-card {
		position: relative;
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-left: 4px solid var(--color-status-implemented);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		box-shadow: var(--shadow-sm);
		cursor: pointer;
		transition:
			border-color var(--duration-fast) var(--ease-out),
			box-shadow var(--duration-fast) var(--ease-out),
			transform var(--duration-fast) var(--ease-out);
	}

	.finding-card:hover {
		border-color: var(--color-border-strong);
		box-shadow: var(--shadow-md);
		transform: translateY(-2px);
	}

	.finding-card:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
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
		margin-bottom: var(--space-3);
	}

	.finding-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-3);
	}

	.keyword-chip {
		font-family: var(--font-mono);
		font-size: 10px;
		color: var(--color-text-tertiary);
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.keyword-chip:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-secondary);
	}

	.card-hint {
		display: flex;
		align-items: center;
		gap: var(--space-1);
		padding-top: var(--space-3);
		border-top: 1px dashed var(--color-border);
	}

	.hint-text {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.hint-icon {
		color: var(--color-text-muted);
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.finding-card:hover .hint-icon {
		transform: translateX(2px);
	}

	/* Pinned ribbon */
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
</style>
