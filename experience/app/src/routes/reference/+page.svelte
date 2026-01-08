<script lang="ts">
	import { base } from '$app/paths';

	let expandedPaper = $state<string | null>(null);

	function togglePaper(id: string) {
		expandedPaper = expandedPaper === id ? null : id;
	}

	const sections = [
		{
			title: 'Cognitive Offloading & Skill Decay',
			papers: [
				{
					id: 'budzyn-2025',
					authors: 'Budzyń, B. et al.',
					year: 2025,
					title: 'Effect of AI-Assisted Colonoscopy on Adenoma Detection',
					venue: 'Lancet Gastroenterology & Hepatology',
					url: 'https://doi.org/10.1016/S2468-1253(25)00133-5',
					finding: '20% skill degradation in 3 months',
					abstract: 'A crossover randomized controlled trial examining endoscopist performance after AI assistance removal. After 3 months of AI-assisted colonoscopy, physicians showed a 20% reduction in adenoma detection rate when the AI was turned off, suggesting skill atrophy from over-reliance on AI cues.'
				},
				{
					id: 'gerlich-2025',
					authors: 'Gerlich, M.',
					year: 2025,
					title: 'AI Tools in Society: Impacts on Cognitive Offloading and the Future of Critical Thinking',
					venue: 'Societies',
					url: 'https://doi.org/10.3390/soc15010006',
					finding: 'r = -0.75 AI use vs critical thinking',
					abstract: 'Cross-sectional analysis of 666 participants examining the relationship between AI tool usage and cognitive abilities. Found a strong negative correlation (r = -0.75) between frequent AI use and critical thinking scores, with memory and problem-solving also affected.'
				},
				{
					id: 'kosmyna-2025',
					authors: 'Kosmyna, N. et al.',
					year: 2025,
					title: 'Your Brain on ChatGPT: How AI Writing Tools Reshape Memory and Cognition',
					venue: 'MIT Media Lab',
					url: 'https://www.media.mit.edu/publications/your-brain-on-chatgpt/',
					finding: '83% couldn\'t recall AI-assisted writing',
					abstract: 'Experimental study using EEG to examine memory encoding during AI-assisted vs unassisted writing. Participants showed significantly reduced memory retention for AI-assisted content, with 83% unable to recall key points from text they "wrote" with AI help.'
				},
				{
					id: 'lee-2025',
					authors: 'Lee, H.P. et al.',
					year: 2025,
					title: 'The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects',
					venue: 'CHI \'25',
					url: 'https://doi.org/10.1145/3706598.3713778',
					finding: 'Higher AI confidence → less critical thinking (β = -0.69)',
					abstract: 'Survey of 319 knowledge workers examining how AI confidence affects human critical thinking. Found that higher confidence in AI outputs correlates with reduced critical evaluation (β = -0.69), with users more likely to accept AI suggestions without scrutiny.'
				}
			]
		},
		{
			title: 'Metacognition & Calibration',
			papers: [
				{
					id: 'fan-2024',
					authors: 'Fan, X. et al.',
					year: 2024,
					title: 'Beware of Metacognitive Laziness: Effects of Generative AI on Learning Motivation',
					venue: 'British Journal of Educational Technology',
					url: 'https://doi.org/10.1111/bjet.13544',
					finding: 'AI reduces learning motivation and metacognitive processes',
					abstract: 'Experimental study examining how generative AI affects learning behavior. Students using AI showed reduced metacognitive monitoring and decreased motivation to learn underlying concepts, preferring to rely on AI for future similar tasks.'
				},
				{
					id: 'fernandes-2025',
					authors: 'Fernandes, S. et al.',
					year: 2025,
					title: 'AI Makes You Smarter, but None the Wiser: The Effects of LLMs on Knowledge Acquisition',
					venue: 'Computers in Human Behavior',
					url: 'https://doi.org/10.1016/j.chb.2025.108779',
					finding: 'Knowledge without wisdom - information access without deep understanding',
					abstract: 'Study examining the difference between knowledge acquisition and wisdom development when using LLMs. While users gained factual knowledge, they showed reduced ability to apply knowledge flexibly or develop deeper understanding of domains.'
				},
				{
					id: 'ma-2024',
					authors: 'Ma, S. et al.',
					year: 2024,
					title: 'Understanding Self-Confidence Calibration in AI-Assisted Decision Making',
					venue: 'CHI \'24',
					url: 'https://doi.org/10.1145/3613904.3642671',
					finding: 'Systematic miscalibration in human-AI teams',
					abstract: 'Analysis of confidence calibration when humans make decisions with AI assistance. Found that humans tend to be overconfident in AI-assisted decisions while underestimating their own contributions, leading to systematic miscalibration.'
				}
			]
		},
		{
			title: 'Human-AI Collaboration',
			papers: [
				{
					id: 'blaurock-2024',
					authors: 'Blaurock, M. et al.',
					year: 2024,
					title: 'Designing for Complementarity: AI-Based Service Experience Contingencies',
					venue: 'Journal of Service Research',
					url: 'https://doi.org/10.1177/10946705241238751',
					finding: 'Transparency + control = complementary outcomes',
					abstract: 'Meta-analysis of 106 studies on human-AI interaction. Identified that transparency (seeing AI reasoning) and user control (shaping process and outcomes) are the strongest predictors of complementary rather than substitutive AI use.'
				},
				{
					id: 'vaccaro-2024',
					authors: 'Vaccaro, M. et al.',
					year: 2024,
					title: 'When Combinations of Humans and AI Are Useful: A Systematic Review and Meta-Analysis',
					venue: 'Nature Human Behaviour',
					url: 'https://doi.org/10.1038/s41562-024-02024-1',
					finding: 'Conditions for genuine human-AI complementarity',
					abstract: 'Systematic review identifying when human-AI collaboration outperforms either alone. Key factors include task complexity, human expertise level, and the degree to which AI augments rather than replaces human judgment.'
				},
				{
					id: 'hemmer-2025',
					authors: 'Hemmer, P. et al.',
					year: 2025,
					title: 'Complementarity in Human-AI Collaboration: Concept, Operationalizations, and Results',
					venue: 'European Journal of Information Systems',
					url: 'https://doi.org/10.1080/0960085X.2025.2475962',
					finding: 'Framework for achieving genuine collaboration',
					abstract: 'Theoretical and empirical framework for understanding human-AI complementarity. Proposes operationalizations for measuring genuine collaboration vs. substitution and identifies design patterns that promote complementary outcomes.'
				}
			]
		},
		{
			title: 'Software Engineering',
			papers: [
				{
					id: 'metr-2025',
					authors: 'METR',
					year: 2025,
					title: 'Measuring the Impact of Early AI Assistance on Experienced Open-Source Developers',
					venue: 'arXiv',
					url: 'https://arxiv.org/abs/2507.09089',
					finding: 'Felt 24% faster, actually 19% slower',
					abstract: 'Randomized controlled trial with 16 experienced open-source developers working on their own mature repositories. Despite feeling 24% faster with AI assistance, actual task completion was 19% slower. Suggests a gap between perceived and actual productivity benefits.'
				},
				{
					id: 'ziegler-2024',
					authors: 'Ziegler, A. et al.',
					year: 2024,
					title: 'Measuring GitHub Copilot\'s Impact on Productivity',
					venue: 'Communications of the ACM',
					url: 'https://doi.org/10.1145/3633453',
					finding: 'Productivity metrics and acceptance rates in practice',
					abstract: 'Large-scale observational study of GitHub Copilot usage patterns. Examines acceptance rates, time savings, and developer satisfaction, while acknowledging limitations in measuring true productivity impact.'
				},
				{
					id: 'fu-2024',
					authors: 'Fu, Y. et al.',
					year: 2024,
					title: 'Security Weaknesses of Copilot-Generated Code in GitHub',
					venue: 'ACM Transactions on Software Engineering and Methodology',
					url: 'https://doi.org/10.1145/3716848',
					finding: 'Systematic security vulnerabilities in AI-generated code',
					abstract: 'Analysis of code generated by GitHub Copilot in real repositories. Found recurring patterns of security vulnerabilities including injection flaws, improper input validation, and authentication weaknesses.'
				}
			]
		},
		{
			title: 'Theoretical Foundations',
			papers: [
				{
					id: 'clark-1998',
					authors: 'Clark, A. & Chalmers, D.',
					year: 1998,
					title: 'The Extended Mind',
					venue: 'Analysis',
					url: 'https://www.jstor.org/stable/3328150',
					finding: 'External processes can constitute genuine cognition',
					abstract: 'Foundational paper arguing that cognitive processes can extend beyond the brain into the environment. Introduces the "parity principle": if an external process functions equivalently to an internal one, it should be considered part of the cognitive system.'
				},
				{
					id: 'nonaka-1995',
					authors: 'Nonaka, I. & Takeuchi, H.',
					year: 1995,
					title: 'The Knowledge-Creating Company',
					venue: 'Oxford University Press',
					url: 'https://global.oup.com/academic/product/the-knowledge-creating-company-9780195092691',
					finding: 'SECI model and Ba concept for knowledge creation',
					abstract: 'Seminal work on organizational knowledge creation. Introduces the SECI model (Socialization, Externalization, Combination, Internalization) and the concept of "Ba" as a shared context for knowledge creation.'
				},
				{
					id: 'hutchins-1995',
					authors: 'Hutchins, E.',
					year: 1995,
					title: 'Cognition in the Wild',
					venue: 'MIT Press',
					url: 'https://mitpress.mit.edu/9780262581462/cognition-in-the-wild/',
					finding: 'Distributed cognition across people and artifacts',
					abstract: 'Ethnographic study of navigation on naval ships demonstrating how cognitive work is distributed across individuals and artifacts. Shows that complex cognitive tasks emerge from the coordination of multiple agents and tools.'
				}
			]
		}
	];
</script>

<svelte:head>
	<title>Research — claude-1337</title>
	<meta name="description" content="Research foundation for cognitive extension methodology." />
</svelte:head>

<main class="reference-page">
	<header class="page-header">
		<h1>Research</h1>
		<p class="subtitle">Foundation for cognitive extension methodology</p>
		<p class="compiled">Compiled January 2026. Citations verified against primary sources.</p>
	</header>

	{#each sections as section}
		<section class="research-section">
			<h2 class="section-title">{section.title}</h2>
			<div class="papers">
				{#each section.papers as paper}
					<article class="paper" class:expanded={expandedPaper === paper.id}>
						<button class="paper-header" onclick={() => togglePaper(paper.id)}>
							<div class="paper-meta">
								<span class="authors">{paper.authors}</span>
								<span class="year">{paper.year}</span>
							</div>
							<h3 class="paper-title">{paper.title}</h3>
							<p class="venue">{paper.venue}</p>
							<p class="finding">{paper.finding}</p>
							<span class="expand-hint">{expandedPaper === paper.id ? '−' : '+'}</span>
						</button>
						{#if expandedPaper === paper.id}
							<div class="paper-details">
								<p class="abstract">{paper.abstract}</p>
								<a href={paper.url} target="_blank" rel="noopener noreferrer" class="paper-link">
									View paper →
								</a>
							</div>
						{/if}
					</article>
				{/each}
			</div>
		</section>
	{/each}

	<footer class="page-footer">
		<p>All citations link to original sources. <a href="{base}/ethos/">Back to ethos</a>.</p>
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
		overflow: hidden;
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.paper:hover {
		border-color: var(--color-accent);
	}

	.paper.expanded {
		border-color: var(--color-accent);
	}

	.paper-header {
		width: 100%;
		padding: var(--space-4);
		background: none;
		border: none;
		cursor: pointer;
		text-align: left;
		position: relative;
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
		padding-right: var(--space-6);
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

	.expand-hint {
		position: absolute;
		top: var(--space-4);
		right: var(--space-4);
		font-family: var(--font-mono);
		font-size: var(--text-lg);
		color: var(--color-text-muted);
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper:hover .expand-hint {
		color: var(--color-accent);
	}

	.paper-details {
		padding: 0 var(--space-4) var(--space-4);
		border-top: 1px solid var(--color-border);
		margin-top: var(--space-2);
		padding-top: var(--space-4);
	}

	.abstract {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.paper-link {
		display: inline-flex;
		align-items: center;
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.paper-link:hover {
		color: var(--color-accent-hover);
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
