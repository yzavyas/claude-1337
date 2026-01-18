<script lang="ts">
	/**
	 * Main Navigation Component
	 *
	 * Four pillars architecture:
	 * - Marketplace (/catalog)
	 * - Lab (/lab)
	 * - Library (/library)
	 * - Forum (external → GitHub Discussions)
	 */
	import { page } from '$app/stores';
	import { base } from '$app/paths';

	type Pillar =
		| { href: string; label: string; external?: false }
		| { href: string; label: string; external: true };

	const pillars: Pillar[] = [
		{ href: '/catalog', label: 'Catalog' },
		{ href: '/lab', label: 'Lab' },
		{ href: '/explore', label: 'Library' },
		{ href: '/ethos', label: 'Ethos' },
		{ href: 'https://github.com/yzavyas/claude-1337/discussions', label: 'Forum', external: true }
	];

	function isActive(href: string): boolean {
		return $page.url.pathname.startsWith(`${base}${href}`);
	}
</script>

<nav class="nav" aria-label="Main navigation">
	<a href="{base}/" class="nav-brand">
		claude-1337
	</a>

	<div class="nav-links">
		{#each pillars as pillar}
			{#if pillar.external}
				<a
					href={pillar.href}
					class="nav-link"
					target="_blank"
					rel="noopener noreferrer"
				>
					{pillar.label}
					<span class="external-icon" aria-hidden="true">↗</span>
				</a>
			{:else}
				<a
					href="{base}{pillar.href}"
					class="nav-link"
					class:active={isActive(pillar.href)}
					aria-current={isActive(pillar.href) ? 'page' : undefined}
				>
					{pillar.label}
				</a>
			{/if}
		{/each}
	</div>
</nav>

<style>
	.nav {
		position: fixed;
		top: 36px; /* Below banner */
		left: 0;
		right: 0;
		z-index: 99;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-3) var(--space-6);
		background: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
	}

	.nav-brand {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-semibold);
		color: var(--color-text);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.nav-brand:hover {
		color: var(--color-accent);
	}

	.nav-links {
		display: flex;
		gap: var(--space-6);
	}

	.nav-link {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.nav-link:hover {
		color: var(--color-link-hover);
	}

	.nav-link.active {
		color: var(--color-text);
		font-weight: var(--font-medium);
	}

	.external-icon {
		display: inline-block;
		margin-left: 2px;
		font-size: 0.75em;
		opacity: 0.6;
	}

	/* Mobile adjustments */
	@media (max-width: 640px) {
		.nav {
			top: 28px; /* Smaller banner on mobile */
			padding: var(--space-2) var(--space-4);
		}

		.nav-links {
			gap: var(--space-4);
		}

		.nav-link,
		.nav-brand {
			font-size: var(--text-xs);
		}
	}
</style>
