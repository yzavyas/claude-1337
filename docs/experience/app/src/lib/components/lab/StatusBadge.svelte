<script lang="ts">
	/**
	 * StatusBadge — Lab Component
	 *
	 * Accessible status indicator with color + icon pairing.
	 * Color alone is not sufficient for 8% of males with color vision deficiency.
	 *
	 * Research: WCAG 1.4.1 requires information not conveyed by color alone.
	 * Each status has a unique icon shape for discrimination regardless of color perception.
	 */
	type Status = 'draft' | 'discussion' | 'fcp' | 'accepted' | 'rejected' | 'implemented' | 'interim' | 'postponed';

	let { status }: { status: Status } = $props();

	// Icon paths (24x24 viewBox, stroke-based)
	const icons: Record<Status, string> = {
		draft: 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z',
		discussion: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
		fcp: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
		accepted: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
		rejected: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
		implemented: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
		interim: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
		postponed: 'M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z'
	};

	const labels: Record<Status, string> = {
		draft: 'Draft',
		discussion: 'Discussion',
		fcp: 'Final Comment',
		accepted: 'Accepted',
		rejected: 'Rejected',
		implemented: 'Published',
		interim: 'Interim',
		postponed: 'Postponed'
	};
</script>

<span class="status-badge" data-status={status}>
	<svg
		class="status-icon"
		viewBox="0 0 24 24"
		fill="none"
		stroke="currentColor"
		stroke-width="2"
		aria-hidden="true"
	>
		<path d={icons[status]} stroke-linecap="round" stroke-linejoin="round" />
	</svg>
	<span class="status-label">{labels[status]}</span>
</span>

<style>
	.status-badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1-5);
		padding: var(--space-1) var(--space-2-5);
		border-radius: var(--radius-full);
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: capitalize;

		/* Ensure 44x44 touch target even for small visual size */
		min-height: 28px;
		position: relative;
	}

	.status-badge::before {
		content: '';
		position: absolute;
		inset: -8px;
		/* Expands touch target to ~44px */
	}

	.status-icon {
		width: 14px;
		height: 14px;
		flex-shrink: 0;
	}

	/* Color + icon pairing for each status */
	[data-status="draft"] {
		background: var(--color-status-draft-bg);
		color: var(--color-status-draft);
	}

	[data-status="discussion"] {
		background: var(--color-status-discussion-bg);
		color: var(--color-status-discussion);
	}

	[data-status="fcp"] {
		background: var(--color-status-fcp-bg);
		color: var(--color-status-fcp);
	}

	[data-status="accepted"] {
		background: var(--color-status-accepted-bg);
		color: var(--color-status-accepted);
	}

	[data-status="rejected"] {
		background: var(--color-status-rejected-bg);
		color: var(--color-status-rejected);
	}

	[data-status="implemented"] {
		background: var(--color-status-implemented-bg);
		color: var(--color-status-implemented);
	}

	[data-status="interim"] {
		background: var(--color-status-interim-bg, var(--color-status-fcp-bg));
		color: var(--color-status-interim, var(--color-status-fcp));
	}

	[data-status="postponed"] {
		background: var(--color-status-postponed-bg);
		color: var(--color-status-postponed);
	}
</style>
