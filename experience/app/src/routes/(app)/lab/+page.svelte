<script lang="ts">
	import SectionHeader from '$lib/components/ui/SectionHeader.svelte';
	import FindingCard from '$lib/components/lab/FindingCard.svelte';
	import ProposalCard from '$lib/components/lab/ProposalCard.svelte';
	import LabFilters from '$lib/components/lab/LabFilters.svelte';

	let { data } = $props();
	let activeKeyword = $state<string | null>(null);

	// Separate findings from proposals
	const allFindings = $derived(data.papers.filter(p => p.status === 'published'));
	const allProposals = $derived(data.papers.filter(p => p.status !== 'published'));

	// Apply keyword filter (non-null assertion safe after truthy check)
	const findings = $derived(
		activeKeyword
			? allFindings.filter(p => p.keywords.includes(activeKeyword!))
			: allFindings
	);

	const proposals = $derived(
		activeKeyword
			? allProposals.filter(p => p.keywords.includes(activeKeyword!))
			: allProposals
	);

	// Map status for ProposalCard (in-progress → fcp, draft → draft)
	function mapProposalStatus(status: string): 'draft' | 'discussion' | 'fcp' | 'accepted' {
		if (status === 'in-progress') return 'fcp';
		return 'draft';
	}
</script>

<svelte:head>
	<title>Lab — claude-1337</title>
	<meta name="description" content="Research experiments in collaborative intelligence." />
</svelte:head>

<main class="lab-page">
	<header class="lab-header">
		<h1>Experimentation Lab</h1>
		<p class="lab-tagline">Evidence over opinions. Measurement over intuition.</p>
	</header>

	<LabFilters
		keywords={data.allKeywords}
		active={activeKeyword}
		count={findings.length + proposals.length}
		onchange={(k) => activeKeyword = k}
	/>

	<!-- Findings Section -->
	{#if findings.length > 0}
		<section class="lab-section">
			<SectionHeader title="Published Findings" count={findings.length} variant="gold" />
			<div class="findings-grid">
				{#each findings as finding, i}
					<FindingCard
						finding={{
							id: finding.id,
							title: finding.title,
							subtitle: finding.subtitle,
							summary: finding.summary,
							date: finding.date,
							keywords: finding.keywords,
							links: {
								findings: finding.links.findings || '',
								proposal: finding.links.proposal
							}
						}}
						pinned={i === 0}
						onKeywordClick={(k) => activeKeyword = k}
					/>
				{/each}
			</div>
		</section>
	{/if}

	<!-- Active Proposals Section -->
	{#if proposals.length > 0}
		<section class="lab-section">
			<SectionHeader title="Active Proposals" count={proposals.length} />
			<div class="proposals-grid">
				{#each proposals as proposal}
					<ProposalCard
						proposal={{
							id: proposal.id,
							title: proposal.title,
							summary: proposal.summary,
							status: mapProposalStatus(proposal.status),
							date: proposal.date,
							keywords: proposal.keywords,
							links: {
								proposal: proposal.links.proposal || '',
								experiment: proposal.links.experiment
							}
						}}
						onKeywordClick={(k) => activeKeyword = k}
					/>
				{/each}
			</div>
		</section>
	{/if}

	<!-- Empty state -->
	{#if findings.length === 0 && proposals.length === 0}
		<div class="empty-state">
			<p>No papers match this filter.</p>
			<button type="button" class="reset-filter" onclick={() => activeKeyword = null}>
				Show all papers
			</button>
		</div>
	{/if}
</main>

<style>
	.lab-page {
		min-height: 100vh;
		padding: var(--space-20) 0 var(--space-12);
	}

	.lab-header {
		text-align: center;
		max-width: 800px;
		margin: 0 auto var(--space-8);
		padding: 0 var(--space-6);
	}

	.lab-header h1 {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-medium);
		color: var(--color-text);
		margin-bottom: var(--space-2);
	}

	.lab-tagline {
		font-family: var(--font-reading);
		font-size: var(--text-lg);
		color: var(--color-text-tertiary);
		font-style: italic;
	}

	.lab-section {
		max-width: 1200px;
		margin: 0 auto;
		padding: var(--space-8);
	}

	.findings-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: var(--space-6);
	}

	.proposals-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: var(--space-5);
	}

	.empty-state {
		text-align: center;
		padding: var(--space-16);
		color: var(--color-text-secondary);
	}

	.empty-state p {
		margin-bottom: var(--space-4);
	}

	.reset-filter {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		background: transparent;
		border: 1px solid var(--color-accent);
		padding: var(--space-2) var(--space-4);
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.reset-filter:hover {
		background: var(--color-accent);
		color: var(--color-text-inverse);
	}

	@media (max-width: 640px) {
		.lab-page {
			padding-top: var(--space-12);
		}

		.lab-header h1 {
			font-size: var(--text-2xl);
		}

		.lab-section {
			padding: var(--space-4);
		}

		.findings-grid,
		.proposals-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
