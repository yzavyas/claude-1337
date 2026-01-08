<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { gsap, createScrollContext } from '$lib/utils/scroll';

	let section: HTMLElement;
	let cleanup: (() => void) | null = null;

	onMount(() => {
		if (!browser) return;

		cleanup = createScrollContext(section, (ctx) => {
			gsap.fromTo(
				'.lens-content > *',
				{ opacity: 0, y: 30 },
				{
					opacity: 1,
					y: 0,
					duration: 0.8,
					stagger: 0.15,
					ease: 'power2.out',
					scrollTrigger: {
						trigger: section,
						start: 'top 70%'
					}
				}
			);
		});

		return () => {
			cleanup?.();
		};
	});
</script>

<section bind:this={section} class="lens-section">
	<div class="content lens-content">
		<h2>Why these factors matter</h2>

		<p class="lead">
			Theory suggests why transparency and control work.
		</p>

		<div class="finding">
			<p>
				One study found mastery-oriented users — those who approach AI as a learning scaffold
				rather than answer oracle — were <strong class="highlight">35.7 times</strong> more likely
				to maintain critical thinking.
			</p>
		</div>

		<div class="caveat">
			<p>
				The sample is from a research bank, not a top-tier venue. The effect size is extraordinary.
				The mechanism fits the validated findings.
			</p>
		</div>

		<blockquote class="insight">
			<p>How you approach AI may matter more than which AI you use.</p>
		</blockquote>

		<table class="orientation-table">
			<thead>
				<tr>
					<th>Orientation</th>
					<th>Behavior</th>
					<th>Outcome</th>
				</tr>
			</thead>
			<tbody>
				<tr class="positive-row">
					<td class="orientation">Mastery</td>
					<td>Views AI as scaffold, questions output</td>
					<td class="outcome positive">Protected</td>
				</tr>
				<tr class="negative-row">
					<td class="orientation">Performance</td>
					<td>Views AI as oracle, accepts output</td>
					<td class="outcome negative">At risk</td>
				</tr>
			</tbody>
		</table>

		<p class="source">ACU Research Bank (2025) — effect requires replication</p>
	</div>
</section>

<style>
	.lens-section {
		min-height: 80vh;
		padding: var(--space-24) var(--space-6);
		display: flex;
		align-items: center;
	}

	.content {
		max-width: var(--content-width);
		width: 100%;
		margin: 0 auto;
	}

	h2 {
		font-size: var(--text-2xl);
		margin-bottom: var(--space-6);
	}

	.lead {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-8);
	}

	.finding {
		margin: var(--space-8) 0;
	}

	.finding p {
		font-size: var(--text-lg);
		line-height: var(--leading-relaxed);
		color: var(--color-text-primary);
	}

	.highlight {
		font-family: var(--font-mono);
		color: var(--color-accent-positive);
		font-size: 1.1em;
	}

	.caveat {
		padding: var(--space-4) var(--space-5);
		background: var(--color-bg-surface);
		border-left: 2px solid var(--color-text-muted);
		border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
		margin: var(--space-6) 0;
	}

	.caveat p {
		font-size: var(--text-sm);
		color: var(--color-text-tertiary);
		font-style: italic;
		line-height: var(--leading-relaxed);
	}

	.insight {
		margin: var(--space-10) 0;
		padding: 0;
		border: none;
	}

	.insight p {
		font-size: var(--text-xl);
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
		text-align: center;
	}

	/* Table */
	.orientation-table {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-8) 0;
		font-size: var(--text-sm);
	}

	.orientation-table th {
		text-align: left;
		padding: var(--space-3) var(--space-4);
		background: var(--color-bg-surface);
		border-bottom: 1px solid var(--color-border);
		font-weight: var(--font-medium);
		color: var(--color-text-secondary);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	.orientation-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
		color: var(--color-text-secondary);
	}

	.orientation-table .orientation {
		font-weight: var(--font-medium);
		color: var(--color-text-primary);
	}

	.positive-row {
		background: oklch(16% 0.02 70 / 0.15);
	}

	.negative-row {
		background: oklch(16% 0.02 25 / 0.1);
	}

	.outcome {
		font-weight: var(--font-semibold);
	}

	.outcome.positive {
		color: var(--color-accent-positive);
	}

	.outcome.negative {
		color: var(--color-accent-negative);
	}

	.source {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-top: var(--space-6);
	}

	/* Mobile */
	@media (max-width: 640px) {
		.orientation-table {
			font-size: var(--text-xs);
		}

		.orientation-table th,
		.orientation-table td {
			padding: var(--space-2) var(--space-3);
		}
	}
</style>
