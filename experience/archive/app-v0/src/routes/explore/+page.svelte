<script>
	import { base } from '$app/paths';

	const sections = [
		{
			href: `${base}/explore/tutorials/`,
			title: 'tutorials',
			icon: '🎯',
			description: 'Learning-oriented. Build your first skill, understand the system by doing.'
		},
		{
			href: `${base}/explore/how-to/`,
			title: 'how-to',
			icon: '🔧',
			description: 'Task-oriented. Specific problems, specific solutions. You know what you need.'
		},
		{
			href: `${base}/explore/explanation/`,
			title: 'explanation',
			icon: '💡',
			description: 'Understanding-oriented. Extended mind thesis, collaborative intelligence, why this exists.'
		},
		{
			href: `${base}/explore/reference/`,
			title: 'reference',
			icon: '📚',
			description: 'Information-oriented. Plugin catalog, research citations, technical specs.'
		}
	];
</script>

<div class="page">
	<header class="page-header">
		<h1>explore</h1>
		<p class="intro">
			Documentation structured for how you actually learn.
		</p>
		<p class="intro-sub">
			Built on <a href="https://diataxis.fr" target="_blank" rel="noopener">Diátaxis</a> — a framework discovered through collaboration. The builder learned, the knowledge persisted. That's the thesis in action.
		</p>
	</header>

	<div class="sections">
		{#each sections as section, i}
			<a href={section.href} class="section-card" style="--delay: {i * 50}ms">
				<div class="card-icon">{section.icon}</div>
				<div class="card-content">
					<h3 class="card-title">
						<span class="prompt">$</span>
						{section.title}
					</h3>
					<p class="card-description">{section.description}</p>
				</div>
				<div class="card-arrow">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M5 12h14M12 5l7 7-7 7"/>
					</svg>
				</div>
			</a>
		{/each}
	</div>
</div>

<style>
	.page {
		max-width: 100%;
	}

	.page-header {
		margin-bottom: var(--space-2xl);
	}

	.page-header h1 {
		font-size: 2.5rem;
		font-weight: 600;
		color: var(--text-primary);
		letter-spacing: -0.03em;
		margin-bottom: var(--space-sm);
	}

	.intro {
		font-size: 1.1rem;
		color: var(--text-secondary);
		max-width: 500px;
		line-height: 1.5;
		margin-bottom: var(--space-xs);
	}

	.intro-sub {
		font-size: 0.9rem;
		color: var(--text-muted);
		line-height: 1.5;
	}

	.intro-sub a {
		color: var(--link);
		text-decoration: none;
	}

	.intro-sub a:hover {
		text-decoration: underline;
	}

	.sections {
		display: grid;
		gap: var(--space-md);
	}

	.section-card {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		padding: var(--space-lg);
		background: var(--bg-surface);
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--transition-fast);
		animation: fadeSlideIn 300ms ease forwards;
		animation-delay: var(--delay);
		opacity: 0;
	}

	@keyframes fadeSlideIn {
		from {
			opacity: 0;
			transform: translateY(8px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.section-card:hover {
		border-color: var(--border-default);
		background: var(--bg-elevated);
		transform: translateX(4px);
	}

	.section-card:hover .card-arrow {
		opacity: 1;
		transform: translateX(0);
	}

	.section-card:hover .card-title {
		color: var(--accent);
	}

	.card-icon {
		font-size: 1.5rem;
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--bg-elevated);
		border-radius: var(--radius-md);
		flex-shrink: 0;
	}

	.card-content {
		flex: 1;
		min-width: 0;
	}

	.card-title {
		font-family: var(--font-mono);
		font-size: 1rem;
		font-weight: 500;
		color: var(--text-primary);
		margin-bottom: var(--space-xs);
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		transition: color var(--transition-fast);
	}

	.prompt {
		color: var(--accent);
		opacity: 0.7;
	}

	.card-description {
		font-size: 0.875rem;
		color: var(--text-secondary);
		line-height: 1.5;
		margin: 0;
	}

	.card-arrow {
		color: var(--text-muted);
		opacity: 0;
		transform: translateX(-8px);
		transition: all var(--transition-fast);
		flex-shrink: 0;
	}

	/* Mobile */
	@media (max-width: 640px) {
		.page-header h1 {
			font-size: 1.8rem;
		}

		.intro {
			font-size: 1rem;
		}

		.section-card {
			padding: var(--space-md);
		}

		.card-icon {
			width: 40px;
			height: 40px;
			font-size: 1.2rem;
		}

		.card-arrow {
			display: none;
		}
	}
</style>
