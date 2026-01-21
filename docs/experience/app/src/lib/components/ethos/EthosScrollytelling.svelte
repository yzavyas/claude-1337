<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { base } from '$app/paths';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let container: HTMLElement;
	let cleanup: (() => void) | null = null;
	let currentStep = $state(0);
	let scrollProgress = $state(0);

	// The narrative steps
	const steps = [
		{
			id: 'hook',
			chapter: 1,
			content: {
				stat: { perceived: '+24%', actual: '−19%', gap: 43 },
				source: 'METR 2025 — n=16 experienced developers',
				insight: 'AI shifts work from generation to verification. Writing feels easier. Catching errors takes longer.'
			}
		},
		{
			id: 'evidence',
			chapter: 1,
			content: {
				findings: [
					{ stat: 'r = −0.75', label: 'AI use vs critical thinking', source: 'Gerlich 2025' },
					{ stat: '20%', label: 'skill decay in 3 months', source: 'Budzyń 2025' },
					{ stat: '83%', label: 'couldn\'t recall AI-assisted writing', source: 'Kosmyna MIT' }
				]
			}
		},
		{
			id: 'frame',
			chapter: 2,
			content: {
				title: 'What determines the outcome?',
				factors: [
					{ name: 'Transparency', effect: 'β = 0.415', desc: 'User sees reasoning' },
					{ name: 'Process Control', effect: 'β = 0.507', desc: 'User shapes how', highlight: true },
					{ name: 'Outcome Control', effect: 'β = 0.486', desc: 'User shapes what' }
				],
				source: 'Blaurock et al. 2024, Journal of Service Research'
			}
		},
		{
			id: 'paths',
			chapter: 3,
			content: {
				complementary: {
					title: 'Complementary',
					desc: 'Capability compounds',
					traits: ['Sees reasoning', 'Guides direction', 'Learns patterns']
				},
				substitutive: {
					title: 'Substitutive',
					desc: 'Atrophy compounds',
					traits: ['Black box', 'Consumes output', 'Skill decays']
				}
			}
		},
		{
			id: 'choice',
			chapter: 3,
			content: {
				conclusion: 'The correlation isn\'t a one-time effect. It\'s a trajectory.',
				cta: 'These extensions are designed for the upper path.'
			}
		}
	];

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(container, (ctx) => {
			// Overall progress for the progress bar
			gsap.to({}, {
				scrollTrigger: {
					trigger: container,
					start: 'top top',
					end: 'bottom bottom',
					scrub: true,
					onUpdate: (self) => {
						scrollProgress = Math.round(self.progress * 100);
					}
				}
			});

			// Step triggers
			const stepElements = container.querySelectorAll('.step');
			stepElements.forEach((step, index) => {
				gsap.to({}, {
					scrollTrigger: {
						trigger: step,
						start: 'top center',
						end: 'bottom center',
						onEnter: () => { currentStep = index; },
						onEnterBack: () => { currentStep = index; }
					}
				});
			});

			// Animate content reveals
			gsap.utils.toArray('.step-content').forEach((el) => {
				gsap.fromTo(
					el as Element,
					{ opacity: 0, y: 40 },
					{
						opacity: 1,
						y: 0,
						duration: 0.8,
						ease: 'power2.out',
						scrollTrigger: {
							trigger: el as Element,
							start: 'top 75%',
							toggleActions: 'play none none reverse'
						}
					}
				);
			});
		});

		return () => cleanup?.();
	});

	// Derived state for visual
	const pathProgress = $derived(
		currentStep >= 3 ? 1 : currentStep >= 2 ? 0.5 : currentStep >= 1 ? 0.25 : 0
	);
	const showComplementary = $derived(currentStep >= 3);
	const showSubstitutive = $derived(currentStep >= 3);
</script>

<div bind:this={container} class="scrollytelling">
	<!-- Progress indicator -->
	<aside class="progress-indicator" aria-hidden="true">
		<div class="progress-bar" style="height: {scrollProgress}%"></div>
		<div class="progress-chapters">
			<span class="chapter-dot" class:active={currentStep < 2}>1</span>
			<span class="chapter-dot" class:active={currentStep >= 2 && currentStep < 3}>2</span>
			<span class="chapter-dot" class:active={currentStep >= 3}>3</span>
		</div>
	</aside>

	<!-- Sticky visual: Diverging paths -->
	<div class="sticky-visual">
		<svg viewBox="0 0 400 200" class="diverging-svg" aria-label="Diverging paths visualization" style="opacity: {currentStep >= 3 ? 1 : 0.15}">
			<!-- Origin point -->
			<circle cx="40" cy="100" r="5" fill="var(--color-text-muted)" />

			<!-- Upper path - complementary -->
			<path
				class="path-upper"
				d="M 40 100 Q 120 100, 160 70 Q 200 40, 280 30 Q 340 20, 380 15"
				fill="none"
				stroke="var(--color-accent-positive)"
				stroke-width="3"
				stroke-linecap="round"
				stroke-dasharray="300"
				stroke-dashoffset={300 - (pathProgress * 300)}
				opacity={showComplementary ? 1 : 0.3}
			/>

			<!-- Lower path - substitutive -->
			<path
				class="path-lower"
				d="M 40 100 Q 120 100, 160 130 Q 200 160, 280 170 Q 340 180, 380 185"
				fill="none"
				stroke="var(--color-accent-negative)"
				stroke-width="3"
				stroke-linecap="round"
				stroke-dasharray="300"
				stroke-dashoffset={300 - (pathProgress * 300)}
				opacity={showSubstitutive ? 1 : 0.3}
			/>

			<!-- Labels -->
			{#if showComplementary}
				<text x="360" y="15" class="path-label upper" fill="var(--color-accent-positive)">
					Complementary
				</text>
			{/if}
			{#if showSubstitutive}
				<text x="360" y="195" class="path-label lower" fill="var(--color-accent-negative)">
					Substitutive
				</text>
			{/if}

			<!-- Center line / origin label -->
			<text x="40" y="120" class="origin-label" fill="var(--color-text-muted)">now</text>
		</svg>
	</div>

	<!-- Scrolling steps -->
	<div class="steps">
		<!-- Chapter 1: The Gap -->
		<section class="step" data-chapter="1">
			<div class="step-content">
				<div class="chapter-label">Chapter 1</div>
				<h2 class="step-title">The Perception Gap</h2>

				<div class="stat-display">
					<p class="stat-line">
						Developers using AI felt <span class="stat positive">24% faster</span>
					</p>
					<p class="stat-line">
						They were <span class="stat negative">19% slower</span>
					</p>
				</div>

				<div class="gap-badge">
					<span class="gap-number">43</span>
					<span class="gap-label">point gap</span>
				</div>

				<p class="source">METR 2025 — n=16 experienced developers, mature codebases</p>
				<p class="insight">AI shifts work from generation to verification. Writing feels easier. Catching errors in mostly-correct code takes longer.</p>
			</div>
		</section>

		<section class="step" data-chapter="1">
			<div class="step-content">
				<h3 class="evidence-title">The pattern is consistent</h3>

				<div class="evidence-grid">
					<div class="evidence-card">
						<span class="evidence-stat">r = −0.75</span>
						<span class="evidence-label">AI use vs critical thinking</span>
						<span class="evidence-source">Gerlich 2025</span>
					</div>
					<div class="evidence-card">
						<span class="evidence-stat">20%</span>
						<span class="evidence-label">skill decay in 3 months</span>
						<span class="evidence-source">Budzyń 2025, Lancet</span>
					</div>
					<div class="evidence-card">
						<span class="evidence-stat">83%</span>
						<span class="evidence-label">couldn't recall AI-assisted writing</span>
						<span class="evidence-source">Kosmyna, MIT 2025</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Chapter 2: The Frame -->
		<section class="step" data-chapter="2">
			<div class="step-content">
				<div class="chapter-label">Chapter 2</div>
				<h2 class="step-title">What determines the outcome?</h2>

				<div class="factors-list">
					<div class="factor">
						<span class="factor-name">Transparency</span>
						<span class="factor-effect">β = 0.415</span>
						<span class="factor-desc">User sees reasoning</span>
					</div>
					<div class="factor highlight">
						<span class="factor-name">Process Control</span>
						<span class="factor-effect">β = 0.507</span>
						<span class="factor-desc">User shapes how — strongest effect</span>
					</div>
					<div class="factor">
						<span class="factor-name">Outcome Control</span>
						<span class="factor-effect">β = 0.486</span>
						<span class="factor-desc">User shapes what</span>
					</div>
				</div>

				<p class="source">Blaurock et al. 2024, Journal of Service Research — meta-analysis of 106 studies</p>
			</div>
		</section>

		<!-- Chapter 3: The Path -->
		<section class="step" data-chapter="3">
			<div class="step-content">
				<div class="chapter-label">Chapter 3</div>
				<h2 class="step-title">Foundations compound</h2>

				<div class="paths-comparison">
					<div class="path-card complementary">
						<h4>Complementary</h4>
						<p class="path-outcome">Capability compounds</p>
						<ul class="path-traits">
							<li>Sees reasoning, learns patterns</li>
							<li>Guides direction, shapes outcomes</li>
							<li>Grows more capable over time</li>
						</ul>
					</div>
					<div class="path-card substitutive">
						<h4>Substitutive</h4>
						<p class="path-outcome">Atrophy compounds</p>
						<ul class="path-traits">
							<li>Black box, just consumes output</li>
							<li>No control, passive acceptance</li>
							<li>Skills decay without use</li>
						</ul>
					</div>
				</div>
			</div>
		</section>

		<section class="step" data-chapter="3">
			<div class="step-content final">
				<p class="conclusion">The β = −0.69 correlation isn't a one-time effect.</p>
				<p class="conclusion-emphasis">It's a trajectory.</p>

				<p class="final-statement">These extensions are designed for the upper path.</p>

				<div class="cta-group">
					<a href="{base}/catalog/" class="cta primary">
						Browse Extensions
						<span class="arrow">→</span>
					</a>
					<a href="{base}/library/" class="cta secondary">
						View Research
					</a>
				</div>
			</div>
		</section>
	</div>
</div>

<style>
	.scrollytelling {
		position: relative;
		min-height: 400vh; /* 5 steps */
	}

	/* Progress indicator */
	.progress-indicator {
		position: fixed;
		left: var(--space-4);
		top: 50%;
		transform: translateY(-50%);
		height: 200px;
		width: 4px;
		background: var(--color-border);
		border-radius: var(--radius-full);
		z-index: 50;
	}

	.progress-bar {
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
		background: var(--color-accent);
		border-radius: var(--radius-full);
		transition: height 0.1s ease-out;
	}

	.progress-chapters {
		position: absolute;
		left: calc(100% + var(--space-2));
		top: 0;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.chapter-dot {
		width: 20px;
		height: 20px;
		border-radius: 50%;
		background: var(--color-bg-surface);
		border: 2px solid var(--color-border);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: var(--text-xs);
		font-family: var(--font-mono);
		color: var(--color-text-muted);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.chapter-dot.active {
		background: var(--color-accent);
		border-color: var(--color-accent);
		color: var(--color-bg-deep);
	}

	/* Sticky visual */
	.sticky-visual {
		position: sticky;
		top: 100px;
		height: calc(100vh - 200px);
		display: flex;
		align-items: center;
		justify-content: center;
		pointer-events: none;
		z-index: 1;
	}

	.diverging-svg {
		width: 100%;
		max-width: 500px;
		height: auto;
		opacity: 0.15;
		transition: opacity var(--duration-slow) var(--ease-out);
	}

	/* Full opacity when in chapter 3 - controlled via JS pathProgress */

	.path-upper, .path-lower {
		transition: stroke-dashoffset 0.8s ease-out, opacity 0.4s ease-out;
	}

	.path-label {
		font-family: var(--font-mono);
		font-size: 11px;
		text-anchor: end;
	}

	.origin-label {
		font-family: var(--font-mono);
		font-size: 10px;
		text-anchor: middle;
	}

	/* Steps */
	.steps {
		position: relative;
		z-index: 10;
	}

	.step {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--space-16) var(--space-6);
	}

	.step-content {
		max-width: 600px;
		background: var(--color-bg);
		padding: var(--space-8);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-lg);
	}

	.chapter-label {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-accent);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		margin-bottom: var(--space-2);
	}

	.step-title {
		font-size: var(--text-2xl);
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
	}

	/* Hook section styles */
	.stat-display {
		margin-bottom: var(--space-6);
	}

	.stat-line {
		font-size: var(--text-xl);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-2);
	}

	.stat {
		font-family: var(--font-mono);
		font-weight: var(--font-bold);
	}

	.stat.positive {
		color: var(--color-accent-positive);
	}

	.stat.negative {
		color: var(--color-accent-negative);
	}

	.gap-badge {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		background: var(--color-bg-elevated);
		padding: var(--space-3) var(--space-5);
		border-radius: var(--radius-md);
		border: 1px solid var(--color-border);
		margin-bottom: var(--space-6);
	}

	.gap-number {
		font-family: var(--font-mono);
		font-size: var(--text-3xl);
		font-weight: var(--font-bold);
		color: var(--color-text-primary);
		line-height: 1;
	}

	.gap-label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	.source {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-4);
	}

	.insight {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Evidence section */
	.evidence-title {
		font-size: var(--text-lg);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
	}

	.evidence-grid {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.evidence-card {
		display: flex;
		flex-direction: column;
		padding: var(--space-4);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
		border-left: 3px solid var(--color-accent-negative);
	}

	.evidence-stat {
		font-family: var(--font-mono);
		font-size: var(--text-xl);
		font-weight: var(--font-bold);
		color: var(--color-accent-negative);
	}

	.evidence-label {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin: var(--space-1) 0;
	}

	.evidence-source {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	/* Factors section */
	.factors-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
		margin-bottom: var(--space-6);
	}

	.factor {
		display: grid;
		grid-template-columns: 1fr auto;
		grid-template-rows: auto auto;
		gap: var(--space-1) var(--space-4);
		padding: var(--space-3);
		background: var(--color-bg-surface);
		border-radius: var(--radius-md);
	}

	.factor.highlight {
		background: var(--color-accent-subtle);
		border: 1px solid var(--color-accent);
	}

	.factor-name {
		font-weight: var(--font-semibold);
		color: var(--color-text-primary);
	}

	.factor-effect {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent-positive);
		text-align: right;
	}

	.factor-desc {
		grid-column: span 2;
		font-size: var(--text-sm);
		color: var(--color-text-tertiary);
	}

	/* Paths comparison */
	.paths-comparison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-4);
	}

	.path-card {
		padding: var(--space-4);
		border-radius: var(--radius-md);
	}

	.path-card.complementary {
		background: oklch(96% 0.03 145);
		border: 1px solid var(--color-accent-positive);
	}

	.path-card.substitutive {
		background: oklch(96% 0.03 25);
		border: 1px solid var(--color-accent-negative);
	}

	.path-card h4 {
		font-size: var(--text-base);
		font-weight: var(--font-semibold);
		margin-bottom: var(--space-1);
	}

	.path-card.complementary h4 {
		color: var(--color-accent-positive);
	}

	.path-card.substitutive h4 {
		color: var(--color-accent-negative);
	}

	.path-outcome {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-3);
	}

	.path-traits {
		list-style: none;
		padding: 0;
		margin: 0;
		font-size: var(--text-sm);
		color: var(--color-text-tertiary);
	}

	.path-traits li {
		margin-bottom: var(--space-1);
		padding-left: var(--space-3);
		position: relative;
	}

	.path-traits li::before {
		content: '·';
		position: absolute;
		left: 0;
	}

	/* Final section */
	.step-content.final {
		text-align: center;
	}

	.conclusion {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-2);
	}

	.conclusion-emphasis {
		font-size: var(--text-2xl);
		font-weight: var(--font-bold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-8);
	}

	.final-statement {
		font-size: var(--text-xl);
		color: var(--color-accent-positive);
		font-weight: var(--font-medium);
		margin-bottom: var(--space-8);
	}

	.cta-group {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-3);
	}

	.cta {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-6);
		border-radius: var(--radius-md);
		font-weight: var(--font-medium);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.cta.primary {
		background: var(--color-accent);
		color: var(--color-bg-deep);
	}

	.cta.primary:hover {
		background: var(--color-accent-hover);
		transform: translateY(-2px);
	}

	.cta.secondary {
		color: var(--color-text-muted);
		font-size: var(--text-sm);
	}

	.cta.secondary:hover {
		color: var(--color-accent);
	}

	.cta .arrow {
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.cta:hover .arrow {
		transform: translateX(4px);
	}

	/* Mobile */
	@media (max-width: 768px) {
		.progress-indicator {
			left: var(--space-2);
			height: 150px;
		}

		.progress-chapters {
			display: none;
		}

		.sticky-visual {
			top: 80px;
			height: 200px;
		}

		.diverging-svg {
			max-width: 300px;
		}

		.step-content {
			padding: var(--space-5);
		}

		.paths-comparison {
			grid-template-columns: 1fr;
		}
	}

	/* Hide progress on very small screens */
	@media (max-width: 480px) {
		.progress-indicator {
			display: none;
		}
	}
</style>
