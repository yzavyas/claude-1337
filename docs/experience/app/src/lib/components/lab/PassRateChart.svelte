<script lang="ts">
	interface Props {
		data?: {
			strategy: string;
			passRate: number;
			tokens: number;
		}[];
	}

	let { data = [
		{ strategy: 'Single-shot', passRate: 86.6, tokens: 232 },
		{ strategy: 'Ralph-style', passRate: 98.8, tokens: 2264 }
	] }: Props = $props();

	// Chart dimensions
	const width = 400;
	const height = 200;
	const padding = { top: 24, right: 20, bottom: 40, left: 48 };
	const chartWidth = width - padding.left - padding.right;
	const chartHeight = height - padding.top - padding.bottom;

	// Calculate bar positions
	const barWidth = chartWidth / data.length - 40;
	const maxValue = 100;
</script>

<div class="chart-container">
	<h4 class="chart-title">Pass Rate Comparison</h4>
	<div class="chart-wrapper">
		<svg viewBox="0 0 {width} {height}" class="chart-svg">
			<!-- Y-axis -->
			<g class="axis y-axis">
				{#each [0, 25, 50, 75, 100] as tick}
					{@const y = padding.top + chartHeight - (tick / maxValue * chartHeight)}
					<line x1={padding.left} x2={width - padding.right} y1={y} y2={y} class="grid-line" />
					<text x={padding.left - 8} y={y} class="tick-label" text-anchor="end" dominant-baseline="middle">
						{tick}%
					</text>
				{/each}
			</g>

			<!-- Bars -->
			{#each data as item, i}
				{@const barHeight = (item.passRate / maxValue) * chartHeight}
				{@const x = padding.left + (i * (chartWidth / data.length)) + 20}
				{@const y = padding.top + chartHeight - barHeight}

				<!-- Bar -->
				<rect
					x={x}
					y={y}
					width={barWidth}
					height={barHeight}
					rx="4"
					class="bar"
				/>

				<!-- Value label -->
				<text
					x={x + barWidth / 2}
					y={y - 8}
					class="value-label"
					text-anchor="middle"
				>
					{item.passRate}%
				</text>

				<!-- X-axis label -->
				<text
					x={x + barWidth / 2}
					y={height - 12}
					class="axis-label"
					text-anchor="middle"
				>
					{item.strategy}
				</text>
			{/each}
		</svg>
	</div>
	<p class="chart-caption">
		Iteration improves pass rate by 12.2 percentage points at ~10x token cost
	</p>
</div>

<style>
	.chart-container {
		margin: var(--space-6) 0;
	}

	.chart-title {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: 500;
		color: var(--color-text-secondary);
		margin-bottom: var(--space-3);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.chart-wrapper {
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: var(--space-4);
	}

	.chart-svg {
		width: 100%;
		max-width: 400px;
		height: auto;
		display: block;
		margin: 0 auto;
	}

	.grid-line {
		stroke: var(--color-border-subtle);
		stroke-width: 1;
	}

	.tick-label {
		font-family: var(--font-mono);
		font-size: 10px;
		fill: var(--color-text-muted);
	}

	.bar {
		fill: #3b82f6;
		transition: fill 0.2s ease;
	}

	.bar:hover {
		fill: #2563eb;
	}

	.value-label {
		font-family: var(--font-mono);
		font-size: 12px;
		font-weight: 600;
		fill: var(--color-text-primary);
	}

	.axis-label {
		font-family: var(--font-mono);
		font-size: 11px;
		fill: var(--color-text-secondary);
	}

	.chart-caption {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-top: var(--space-3);
		text-align: center;
	}
</style>
