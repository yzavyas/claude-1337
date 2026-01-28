<script lang="ts">
	/**
	 * FindingDialog — Lab Component
	 *
	 * Modal dialog showing full hypothesis + findings before navigating to REP.
	 * Uses native <dialog> element for accessibility.
	 */
	import { base } from '$app/paths';
	import { marked } from 'marked';
	import StatusBadge from './StatusBadge.svelte';

	marked.setOptions({ gfm: true, breaks: true });

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
		open = $bindable(false),
		onclose
	}: {
		finding: Finding;
		open?: boolean;
		onclose?: () => void;
	} = $props();

	let dialogRef: HTMLDialogElement | undefined = $state();

	// Sync open state with dialog
	$effect(() => {
		if (!dialogRef) return;

		if (open && !dialogRef.open) {
			dialogRef.showModal();
		} else if (!open && dialogRef.open) {
			dialogRef.close();
		}
	});

	function handleClose() {
		open = false;
		onclose?.();
	}

	function handleBackdropClick(e: MouseEvent) {
		if (e.target === dialogRef) {
			handleClose();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			handleClose();
		}
	}

	// Render findings markdown
	function renderFindings(raw: string): string {
		if (!raw) return '';
		return marked.parse(raw) as string;
	}
</script>

<dialog
	bind:this={dialogRef}
	class="finding-dialog"
	onclick={handleBackdropClick}
	onkeydown={handleKeydown}
	onclose={handleClose}
>
	<div class="dialog-content">
		<header class="dialog-header">
			<div class="header-meta">
				<span class="finding-id">REP-{finding.id}</span>
				<StatusBadge status="implemented" />
			</div>
			<button type="button" class="close-button" onclick={handleClose} aria-label="Close dialog">
				<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
					<path d="M15 5L5 15M5 5l10 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
				</svg>
			</button>
		</header>

		<h2 class="dialog-title">{finding.title}</h2>

		{#if finding.hypothesis}
			<div class="hypothesis-section">
				<h3 class="section-label">Hypothesis</h3>
				<blockquote class="hypothesis">{finding.hypothesis}</blockquote>
			</div>
		{/if}

		{#if finding.findingsRaw}
			<div class="findings-section">
				<h3 class="section-label">Findings</h3>
				<div class="findings-content">
					{@html renderFindings(finding.findingsRaw)}
				</div>
			</div>
		{:else}
			<div class="findings-section">
				<h3 class="section-label">Summary</h3>
				<p class="summary">{finding.summary}</p>
			</div>
		{/if}

		<footer class="dialog-footer">
			<a href="{base}{finding.links.rep}" class="action-button primary">
				Read Full REP
				<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
					<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
				</svg>
			</a>
			{#if finding.links.experiment}
				<a href="{base}{finding.links.experiment}" class="action-button secondary">
					View Experiment
				</a>
			{/if}
		</footer>
	</div>
</dialog>

<style>
	.finding-dialog {
		position: fixed;
		max-width: 720px;
		width: calc(100% - var(--space-8));
		max-height: calc(100vh - var(--space-16));
		margin: auto;
		padding: 0;
		border: 1px solid var(--color-border);
		border-radius: var(--radius-xl);
		background: var(--color-bg-surface);
		box-shadow: var(--shadow-xl);
		overflow: hidden;
	}

	.finding-dialog::backdrop {
		background: hsl(0 0% 0% / 0.5);
		backdrop-filter: blur(4px);
	}

	.finding-dialog[open] {
		animation: dialogIn var(--duration-normal) var(--ease-out);
	}

	@keyframes dialogIn {
		from {
			opacity: 0;
			transform: scale(0.95) translateY(10px);
		}
		to {
			opacity: 1;
			transform: scale(1) translateY(0);
		}
	}

	.dialog-content {
		padding: var(--space-6);
		max-height: calc(100vh - var(--space-16));
		overflow-y: auto;
	}

	.dialog-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: var(--space-4);
	}

	.header-meta {
		display: flex;
		align-items: center;
		gap: var(--space-3);
	}

	.finding-id {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.close-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 32px;
		height: 32px;
		padding: 0;
		border: none;
		border-radius: var(--radius-md);
		background: transparent;
		color: var(--color-text-muted);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.close-button:hover {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}

	.dialog-title {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-5);
	}

	.section-label {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: var(--font-medium);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: var(--space-2);
	}

	.hypothesis-section {
		margin-bottom: var(--space-5);
	}

	.hypothesis {
		font-family: var(--font-reading);
		font-size: var(--text-base);
		font-style: italic;
		color: var(--color-text-secondary);
		padding: var(--space-3) var(--space-4);
		border-left: 3px solid var(--color-accent);
		background: var(--color-bg-elevated);
		margin: 0;
	}

	.findings-section {
		margin-bottom: var(--space-6);
	}

	.findings-content {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.findings-content :global(h4) {
		font-family: var(--font-display);
		font-size: var(--text-base);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin: var(--space-4) 0 var(--space-2);
	}

	.findings-content :global(h5) {
		font-family: var(--font-display);
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin: var(--space-3) 0 var(--space-1);
	}

	.findings-content :global(strong) {
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.findings-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-bg-elevated);
		padding: 0.1em 0.3em;
		border-radius: var(--radius-sm);
	}

	.findings-content :global(pre) {
		background: var(--color-bg-elevated);
		padding: var(--space-3);
		border-radius: var(--radius-md);
		overflow-x: auto;
		margin: var(--space-3) 0;
	}

	.findings-content :global(pre code) {
		background: none;
		padding: 0;
	}

	.findings-content :global(li) {
		margin-left: var(--space-4);
		margin-bottom: var(--space-1);
	}

	.findings-content :global(tr) {
		display: table-row;
	}

	.findings-content :global(th),
	.findings-content :global(td) {
		padding: var(--space-2) var(--space-3);
		border: 1px solid var(--color-border);
		text-align: left;
	}

	.findings-content :global(th) {
		background: var(--color-bg-elevated);
		font-weight: var(--font-medium);
	}

	.summary {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.dialog-footer {
		display: flex;
		gap: var(--space-3);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border);
	}

	.action-button {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-medium);
		text-decoration: none;
		padding: var(--space-2-5) var(--space-4);
		border-radius: var(--radius-md);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.action-button.primary {
		background: var(--color-accent);
		color: var(--color-text-inverse);
	}

	.action-button.primary:hover {
		background: var(--color-accent-hover);
	}

	.action-button.secondary {
		background: transparent;
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border);
	}

	.action-button.secondary:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-primary);
	}
</style>
