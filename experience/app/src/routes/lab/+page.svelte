<script lang="ts">
	let { data } = $props();

	// Filter state
	let activeKeyword = $state<string | null>(null);

	// Filtered papers
	const filteredPapers = $derived(
		activeKeyword !== null
			? data.papers.filter(p => p.keywords.includes(activeKeyword as string))
			: data.papers
	);

	// Featured paper for hero (first published finding)
	const featured = $derived(data.papers.find(p => p.status === 'published'));

	function toggleKeyword(keyword: string) {
		activeKeyword = activeKeyword === keyword ? null : keyword;
	}
</script>

<svelte:head>
	<title>Lab — claude-1337</title>
	<meta name="description" content="Research library for the agentic era. Evidence over opinions." />
</svelte:head>

<main class="lab-page">
	<!-- Hero Section with Holographic Featured Research -->
	{#if featured}
		<section class="hero">
			<div class="hero-glow"></div>
			<div class="hero-grid"></div>

			<div class="hero-content">
				<span class="hero-label">Latest Research</span>
				<h1 class="hero-title">{featured.title}</h1>
				<p class="hero-summary">{featured.summary}</p>

				<div class="hero-keywords">
					{#each featured.keywords as keyword}
						<span class="keyword-tag">{keyword}</span>
					{/each}
				</div>

				<div class="hero-actions">
					<a href={featured.links.findings} class="hero-cta">
						Read Findings
						<span class="cta-arrow">→</span>
					</a>
					{#if featured.links.proposal}
						<a href={featured.links.proposal} class="hero-secondary">
							View Proposal
						</a>
					{/if}
				</div>
			</div>

			<div class="hero-card">
				<div class="card-hologram">
					<div class="hologram-ring ring-1"></div>
					<div class="hologram-ring ring-2"></div>
					<div class="hologram-ring ring-3"></div>
					<div class="hologram-core">
						<span class="core-id">REP-{featured.id}</span>
						<span class="core-status">Published</span>
					</div>
				</div>
			</div>
		</section>
	{/if}

	<!-- Filter Bar -->
	<section class="filter-section">
		<div class="filter-header">
			<h2>Research Library</h2>
			<span class="paper-count">{filteredPapers.length} papers</span>
		</div>

		<div class="filter-keywords">
			<button
				class="filter-chip"
				class:active={activeKeyword === null}
				onclick={() => activeKeyword = null}
			>
				All
			</button>
			{#each data.allKeywords as keyword}
				<button
					class="filter-chip"
					class:active={activeKeyword === keyword}
					onclick={() => toggleKeyword(keyword)}
				>
					{keyword}
				</button>
			{/each}
		</div>
	</section>

	<!-- Research Grid -->
	<section class="research-grid">
		{#each filteredPapers as paper}
			<article class="research-card" class:published={paper.status === 'published'}>
				<header class="card-header">
					<span class="paper-id">REP-{paper.id}</span>
					<span class="paper-status" class:published={paper.status === 'published'}>
						{paper.status === 'published' ? 'Published' : paper.status === 'in-progress' ? 'In Progress' : 'Draft'}
					</span>
				</header>

				<h3 class="paper-title">{paper.title}</h3>
				{#if paper.subtitle}
					<p class="paper-subtitle">{paper.subtitle}</p>
				{/if}

				<p class="paper-summary">{paper.summary}</p>

				<div class="paper-keywords">
					{#each paper.keywords.slice(0, 4) as keyword}
						<button
							class="keyword-chip"
							class:active={activeKeyword === keyword}
							onclick={() => toggleKeyword(keyword)}
						>
							{keyword}
						</button>
					{/each}
				</div>

				<footer class="card-footer">
					<span class="paper-date">{paper.date}</span>
					<div class="paper-links">
						{#if paper.links.findings}
							<a href={paper.links.findings} class="paper-link primary">Findings</a>
						{/if}
						{#if paper.links.proposal}
							<a href={paper.links.proposal} class="paper-link">Proposal</a>
						{/if}
					</div>
				</footer>

				<!-- Holographic accent for published papers -->
				{#if paper.status === 'published'}
					<div class="card-glow"></div>
				{/if}
			</article>
		{/each}
	</section>

	{#if filteredPapers.length === 0}
		<div class="empty-state">
			<p>No papers match this filter.</p>
			<button class="reset-filter" onclick={() => activeKeyword = null}>
				Show all papers
			</button>
		</div>
	{/if}

	<!-- Footer -->
	<footer class="lab-footer">
		<div class="footer-content">
			<p class="footer-mission">
				Evidence over opinions. Measurement over intuition.
			</p>
		</div>
	</footer>
</main>

<style>
	.lab-page {
		min-height: 100vh;
		padding-top: 80px;
	}

	/* ============ Hero Section ============ */
	.hero {
		position: relative;
		min-height: 500px;
		display: grid;
		grid-template-columns: 1fr 300px;
		gap: var(--space-12);
		align-items: center;
		padding: var(--space-16) var(--space-8);
		max-width: 1200px;
		margin: 0 auto;
		overflow: hidden;
	}

	.hero-glow {
		position: absolute;
		top: 50%;
		right: 10%;
		width: 600px;
		height: 600px;
		background: radial-gradient(ellipse, rgba(34, 211, 238, 0.15) 0%, transparent 70%);
		transform: translate(50%, -50%);
		pointer-events: none;
	}

	.hero-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(34, 211, 238, 0.03) 1px, transparent 1px),
			linear-gradient(90deg, rgba(34, 211, 238, 0.03) 1px, transparent 1px);
		background-size: 40px 40px;
		mask-image: radial-gradient(ellipse at 70% 50%, black 20%, transparent 70%);
		pointer-events: none;
	}

	.hero-content {
		position: relative;
		z-index: 1;
	}

	.hero-label {
		display: inline-block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.15em;
		color: var(--color-accent);
		background: var(--color-accent-muted);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-sm);
		margin-bottom: var(--space-4);
	}

	.hero-title {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-4);
	}

	.hero-summary {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		max-width: 500px;
		margin-bottom: var(--space-6);
	}

	.hero-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2);
		margin-bottom: var(--space-8);
	}

	.keyword-tag {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		background: var(--color-bg-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		border: 1px solid var(--color-border);
	}

	.hero-actions {
		display: flex;
		gap: var(--space-4);
		align-items: center;
	}

	.hero-cta {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-bg-deep);
		background: var(--color-accent);
		padding: var(--space-3) var(--space-5);
		border-radius: var(--radius-md);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.hero-cta:hover {
		background: var(--color-accent-hover);
		transform: translateX(2px);
	}

	.cta-arrow {
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.hero-cta:hover .cta-arrow {
		transform: translateX(4px);
	}

	.hero-secondary {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.hero-secondary:hover {
		color: var(--color-accent);
	}

	/* Holographic Card */
	.hero-card {
		position: relative;
		z-index: 1;
	}

	.card-hologram {
		position: relative;
		width: 200px;
		height: 200px;
		margin: 0 auto;
	}

	.hologram-ring {
		position: absolute;
		inset: 0;
		border: 1px solid var(--color-accent);
		border-radius: 50%;
		opacity: 0.3;
		animation: pulse 3s ease-in-out infinite;
	}

	.hologram-ring.ring-1 {
		animation-delay: 0s;
	}

	.hologram-ring.ring-2 {
		inset: 20px;
		animation-delay: 0.5s;
	}

	.hologram-ring.ring-3 {
		inset: 40px;
		animation-delay: 1s;
	}

	@keyframes pulse {
		0%, 100% {
			opacity: 0.2;
			transform: scale(1);
		}
		50% {
			opacity: 0.5;
			transform: scale(1.05);
		}
	}

	.hologram-core {
		position: absolute;
		inset: 60px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-accent);
		border-radius: 50%;
		box-shadow: 0 0 30px rgba(34, 211, 238, 0.3);
	}

	.core-id {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-accent);
	}

	.core-status {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-accent-positive);
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}

	/* ============ Filter Section ============ */
	.filter-section {
		max-width: 1200px;
		margin: 0 auto;
		padding: var(--space-8);
		border-top: 1px solid var(--color-border);
	}

	.filter-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-4);
	}

	.filter-header h2 {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	.paper-count {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.filter-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2);
	}

	.filter-chip {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-full);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.filter-chip:hover {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.filter-chip.active {
		background: var(--color-accent);
		border-color: var(--color-accent);
		color: var(--color-bg-deep);
	}

	/* ============ Research Grid ============ */
	.research-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		gap: var(--space-6);
		max-width: 1200px;
		margin: 0 auto;
		padding: var(--space-4) var(--space-8) var(--space-16);
	}

	.research-card {
		position: relative;
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-lg);
		padding: var(--space-6);
		transition: all var(--duration-fast) var(--ease-out);
		overflow: hidden;
	}

	.research-card:hover {
		border-color: var(--color-accent);
		transform: translateY(-2px);
	}

	.research-card.published {
		border-color: rgba(34, 211, 238, 0.3);
	}

	.card-glow {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 2px;
		background: linear-gradient(90deg, transparent, var(--color-accent), transparent);
		opacity: 0;
		transition: opacity var(--duration-fast) var(--ease-out);
	}

	.research-card:hover .card-glow {
		opacity: 1;
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-3);
	}

	.paper-id {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-status {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-text-tertiary);
		background: var(--color-bg-surface);
		padding: 2px var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper-status.published {
		color: var(--color-accent-positive);
		background: color-mix(in srgb, var(--color-accent-positive) 15%, transparent);
	}

	.paper-title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
		margin-bottom: var(--space-2);
	}

	.paper-subtitle {
		font-size: var(--text-sm);
		font-style: italic;
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-3);
	}

	.paper-summary {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.paper-keywords {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-1);
		margin-bottom: var(--space-4);
	}

	.keyword-chip {
		font-family: var(--font-mono);
		font-size: 10px;
		color: var(--color-text-muted);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border-subtle);
		padding: 2px var(--space-2);
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.keyword-chip:hover,
	.keyword-chip.active {
		border-color: var(--color-accent);
		color: var(--color-accent);
	}

	.card-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border-subtle);
	}

	.paper-date {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-links {
		display: flex;
		gap: var(--space-3);
	}

	.paper-link {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper-link:hover {
		color: var(--color-accent);
	}

	.paper-link.primary {
		color: var(--color-accent);
	}

	/* ============ Empty State ============ */
	.empty-state {
		text-align: center;
		padding: var(--space-16);
		color: var(--color-text-secondary);
	}

	.reset-filter {
		margin-top: var(--space-4);
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
		color: var(--color-bg-deep);
	}

	/* ============ Footer ============ */
	.lab-footer {
		border-top: 1px solid var(--color-border);
		padding: var(--space-12) var(--space-8);
	}

	.footer-content {
		max-width: 1200px;
		margin: 0 auto;
		text-align: center;
	}

	.footer-mission {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
	}

	/* ============ Responsive ============ */
	@media (max-width: 900px) {
		.hero {
			grid-template-columns: 1fr;
			padding: var(--space-8);
			min-height: auto;
		}

		.hero-card {
			display: none;
		}

		.hero-title {
			font-size: var(--text-3xl);
		}
	}

	@media (max-width: 640px) {
		.research-grid {
			grid-template-columns: 1fr;
			padding: var(--space-4);
		}

		.filter-section {
			padding: var(--space-4);
		}

		.filter-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--space-2);
		}
	}
</style>
