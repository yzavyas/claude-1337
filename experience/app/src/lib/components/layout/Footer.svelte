<script lang="ts">
	/**
	 * Site Footer Component
	 *
	 * Minimal footer with essential links and attribution.
	 */
	import { base } from '$app/paths';

	const year = new Date().getFullYear();
</script>

<footer class="footer">
	<div class="footer-content content-width-wide">
		<div class="footer-section">
			<p class="footer-brand">claude-1337</p>
			<p class="footer-tagline">Cognitive extensions for effective collaborative intelligence.</p>
		</div>

		<nav class="footer-nav" aria-label="Footer navigation">
			<div class="footer-column">
				<h4 class="footer-heading">Explore</h4>
				<a href="{base}/catalog">Marketplace</a>
				<a href="{base}/lab">Lab</a>
				<a href="{base}/library">Library</a>
			</div>

			<div class="footer-column">
				<h4 class="footer-heading">Community</h4>
				<a href="https://github.com/yzavyas/claude-1337" target="_blank" rel="noopener">GitHub</a>
				<a href="https://github.com/yzavyas/claude-1337/discussions" target="_blank" rel="noopener">Forum</a>
			</div>

			<div class="footer-column">
				<h4 class="footer-heading">About</h4>
				<a href="{base}/ethos">Ethos</a>
				<a href="{base}/library/research">Research</a>
			</div>
		</nav>
	</div>

	<div class="footer-bottom content-width-wide">
		<p class="footer-copyright">
			© {year} claude-1337 project. Open source under MIT.
		</p>
	</div>
</footer>

<style>
	.footer {
		margin-top: var(--space-16);
		padding: var(--space-12) 0 var(--space-8);
		background: var(--color-bg-surface);
		border-top: 1px solid var(--color-border);
	}

	.footer-content {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: var(--space-12);
	}

	.footer-section {
		max-width: 280px;
	}

	.footer-brand {
		font-family: var(--font-mono);
		font-weight: var(--font-semibold);
		color: var(--color-text);
		margin-bottom: var(--space-2);
	}

	.footer-tagline {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		line-height: var(--leading-relaxed);
	}

	.footer-nav {
		display: flex;
		gap: var(--space-12);
	}

	.footer-column {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.footer-heading {
		font-size: var(--text-xs);
		font-weight: var(--font-semibold);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--color-text-muted);
		margin-bottom: var(--space-1);
	}

	.footer-column a {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.footer-column a:hover {
		color: var(--color-link-hover);
	}

	.footer-bottom {
		margin-top: var(--space-8);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border);
	}

	.footer-copyright {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	/* Mobile */
	@media (max-width: 768px) {
		.footer-content {
			grid-template-columns: 1fr;
			gap: var(--space-8);
		}

		.footer-nav {
			flex-wrap: wrap;
			gap: var(--space-8);
		}

		.footer-column {
			min-width: 120px;
		}
	}
</style>
