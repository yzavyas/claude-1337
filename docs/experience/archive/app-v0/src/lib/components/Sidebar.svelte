<script lang="ts">
	import { page } from '$app/stores';

	interface Props {
		section: string;
		items: Array<{ href: string; label: string }>;
	}

	let { section, items }: Props = $props();
</script>

<aside class="sidebar">
	<nav class="sidebar-nav">
		<div class="section-title">
			<span class="prompt">$</span>
			<span class="section-name">{section}/</span>
		</div>
		<ul>
			{#each items as item, i}
				<li style="--delay: {i * 30}ms">
					<a
						href={item.href}
						class="nav-link"
						class:active={$page.url.pathname === item.href ||
							$page.url.pathname === item.href.replace(/\/$/, '')}
					>
						<span class="link-indicator"></span>
						{item.label}
					</a>
				</li>
			{/each}
		</ul>
	</nav>
</aside>

<style>
	.sidebar {
		position: sticky;
		top: var(--space-xl);
		align-self: start;
	}

	.sidebar-nav {
		padding: var(--space-md);
		background: var(--bg-surface);
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-md);
	}

	.section-title {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		font-family: var(--font-mono);
		font-size: 0.85rem;
		font-weight: 500;
		margin-bottom: var(--space-md);
		padding-bottom: var(--space-sm);
		border-bottom: 1px solid var(--border-subtle);
	}

	.prompt {
		color: var(--accent);
		font-weight: 500;
	}

	.section-name {
		color: var(--text-primary);
	}

	ul {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	li {
		animation: slideIn 200ms ease forwards;
		animation-delay: var(--delay);
		opacity: 0;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-8px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.nav-link {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-sm);
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--text-secondary);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: all var(--transition-fast);
	}

	.nav-link:hover {
		color: var(--text-primary);
		background: var(--bg-elevated);
	}

	.link-indicator {
		width: 4px;
		height: 4px;
		border-radius: 50%;
		background: var(--border-default);
		transition: all var(--transition-fast);
	}

	.nav-link:hover .link-indicator {
		background: var(--text-muted);
	}

	.nav-link.active {
		color: var(--text-primary);
		background: var(--accent-muted);
	}

	.nav-link.active .link-indicator {
		background: var(--accent);
		box-shadow: 0 0 6px var(--accent);
	}

	/* Mobile: horizontal scrollable nav */
	@media (max-width: 768px) {
		.sidebar {
			position: relative;
			top: 0;
			margin-bottom: var(--space-lg);
		}

		.sidebar-nav {
			padding: var(--space-sm) var(--space-md);
		}

		.section-title {
			margin-bottom: var(--space-sm);
			padding-bottom: var(--space-xs);
		}

		ul {
			flex-direction: row;
			gap: var(--space-sm);
			overflow-x: auto;
			padding-bottom: var(--space-xs);
			-webkit-overflow-scrolling: touch;
			scrollbar-width: none;
		}

		ul::-webkit-scrollbar {
			display: none;
		}

		li {
			flex-shrink: 0;
		}

		.nav-link {
			white-space: nowrap;
			padding: var(--space-xs) var(--space-sm);
		}

		.link-indicator {
			display: none;
		}
	}
</style>
