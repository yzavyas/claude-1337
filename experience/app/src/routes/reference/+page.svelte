<script lang="ts">
	const sections = [
		{
			title: 'Cognitive Offloading & Skill Decay',
			papers: [
				{ authors: 'Budzyń et al.', year: 2025, title: 'Endoscopist deskilling risk after exposure to AI', venue: 'Lancet Gastroenterology', finding: '20% skill degradation in 3 months' },
				{ authors: 'Gerlich', year: 2025, title: 'AI tools in society: impacts on cognitive offloading', venue: 'Societies', finding: 'r = -0.75 AI use vs critical thinking' },
				{ authors: 'Kosmyna et al.', year: 2025, title: 'Your brain on ChatGPT', venue: 'MIT Media Lab', finding: '83% couldn\'t recall AI-assisted writing' },
				{ authors: 'Lee et al.', year: 2025, title: 'Impact of generative AI on critical thinking', venue: 'CHI \'25', finding: 'Higher AI confidence → less critical thinking (β = -0.69)' }
			]
		},
		{
			title: 'Metacognition & Calibration',
			papers: [
				{ authors: 'Fan et al.', year: 2024, title: 'Beware of metacognitive laziness', venue: 'British Journal of Ed Tech', finding: 'AI reduces learning motivation and processes' },
				{ authors: 'Fernandes et al.', year: 2025, title: 'AI makes you smarter, but none the wiser', venue: 'Computers in Human Behavior', finding: 'Knowledge without wisdom' },
				{ authors: 'Ma et al.', year: 2024, title: 'Understanding self-confidence calibration in AI-assisted decisions', venue: 'CHI \'24', finding: 'Miscalibration in human-AI teams' }
			]
		},
		{
			title: 'Human-AI Collaboration',
			papers: [
				{ authors: 'Blaurock et al.', year: 2024, title: 'Designing collaborative intelligence systems', venue: 'Journal of Service Research', finding: 'Transparency + control = complementary outcomes' },
				{ authors: 'Vaccaro et al.', year: 2024, title: 'When combinations of humans and AI are useful', venue: 'Nature Human Behaviour', finding: 'Meta-analysis of human-AI complementarity' },
				{ authors: 'Hemmer et al.', year: 2025, title: 'Complementarity in human-AI collaboration', venue: 'European Journal of IS', finding: 'Conditions for genuine collaboration' }
			]
		},
		{
			title: 'Software Engineering',
			papers: [
				{ authors: 'METR', year: 2025, title: 'AI impact on experienced open-source developers', venue: 'arXiv', finding: 'Felt 24% faster, actually 19% slower' },
				{ authors: 'Ziegler et al.', year: 2024, title: 'Measuring GitHub Copilot\'s impact', venue: 'CACM', finding: 'Productivity metrics in practice' },
				{ authors: 'Fu et al.', year: 2024, title: 'Security weaknesses of Copilot-generated code', venue: 'ACM TOSEM', finding: 'Security vulnerabilities in generated code' }
			]
		},
		{
			title: 'Theoretical Foundations',
			papers: [
				{ authors: 'Clark & Chalmers', year: 1998, title: 'The Extended Mind', venue: 'Analysis', finding: 'External processes can be cognitive' },
				{ authors: 'Nonaka & Takeuchi', year: 1995, title: 'The Knowledge-Creating Company', venue: 'Oxford UP', finding: 'SECI model, Ba concept' },
				{ authors: 'Hutchins', year: 1995, title: 'Cognition in the Wild', venue: 'MIT Press', finding: 'Distributed cognition framework' }
			]
		}
	];
</script>

<svelte:head>
	<title>Reference — claude-1337</title>
	<meta name="description" content="Research bibliography for cognitive extension methodology." />
</svelte:head>

<main class="reference-page">
	<header class="page-header">
		<h1>Reference</h1>
		<p class="subtitle">Research bibliography for cognitive extension methodology</p>
		<p class="compiled">Compiled January 2026. Citations verified against primary sources.</p>
	</header>

	{#each sections as section}
		<section class="research-section">
			<h2 class="section-title">{section.title}</h2>
			<div class="papers">
				{#each section.papers as paper}
					<article class="paper">
						<div class="paper-meta">
							<span class="authors">{paper.authors}</span>
							<span class="year">{paper.year}</span>
						</div>
						<h3 class="paper-title">{paper.title}</h3>
						<p class="venue">{paper.venue}</p>
						<p class="finding">{paper.finding}</p>
					</article>
				{/each}
			</div>
		</section>
	{/each}

	<footer class="page-footer">
		<p>Full citations with links available in the <a href="https://github.com/yzavyas/claude-1337">repository</a>.</p>
	</footer>
</main>

<style>
	.reference-page {
		min-height: 100vh;
		padding: 120px var(--space-6) var(--space-12);
		max-width: 800px;
		margin: 0 auto;
	}

	.page-header {
		margin-bottom: var(--space-12);
	}

	.page-header h1 {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.subtitle {
		font-size: var(--text-base);
		color: var(--color-text-tertiary);
		margin-bottom: var(--space-2);
	}

	.compiled {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.research-section {
		margin-bottom: var(--space-10);
	}

	.section-title {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-accent);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--color-border);
	}

	.papers {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.paper {
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-4);
	}

	.paper-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-2);
	}

	.authors {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.year {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		background: var(--color-bg-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper-title {
		font-size: var(--text-base);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
		line-height: var(--leading-snug);
	}

	.venue {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		font-style: italic;
		margin-bottom: var(--space-2);
	}

	.finding {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		background: var(--color-bg-surface);
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-sm);
		border-left: 2px solid var(--color-accent);
	}

	.page-footer {
		margin-top: var(--space-12);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border);
		text-align: center;
	}

	.page-footer p {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.page-footer a {
		color: var(--color-accent);
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	.page-footer a:hover {
		color: var(--color-accent-hover);
	}

	@media (max-width: 640px) {
		.reference-page {
			padding-top: var(--space-12);
		}

		.page-header h1 {
			font-size: var(--text-3xl);
		}
	}
</style>
