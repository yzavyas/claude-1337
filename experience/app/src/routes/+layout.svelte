<script lang="ts">
	import { base } from '$app/paths';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>claude-1337</title>
</svelte:head>

<div class="site">
	<nav class="nav">
		<a href="{base}/" class="logo">claude-1337</a>
		<div class="links">
			<a href="{base}/explore/">explore</a>
			<a href="{base}/ethos/">ethos</a>
		</div>
	</nav>

	<main>
		{@render children()}
	</main>
</div>

<style>
	:global(*) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
		line-height: 1.6;
		color: #1a1a1a;
		background: #fafafa;
	}

	.site {
		max-width: 48rem;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}

	.nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 3rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid #e5e5e5;
	}

	.logo {
		font-weight: 600;
		font-size: 1.1rem;
		color: #1a1a1a;
		text-decoration: none;
	}

	.links {
		display: flex;
		gap: 1.5rem;
	}

	.links a {
		color: #666;
		text-decoration: none;
		font-size: 0.9rem;
	}

	.links a:hover {
		color: #1a1a1a;
	}

	main {
		min-height: 60vh;
	}

	/* Markdown content styles */
	:global(.markdown-content h1) {
		font-size: 2rem;
		font-weight: 600;
		margin-bottom: 1rem;
		line-height: 1.2;
	}

	:global(.markdown-content h2) {
		font-size: 1.4rem;
		font-weight: 600;
		margin-top: 2.5rem;
		margin-bottom: 0.75rem;
	}

	:global(.markdown-content h3) {
		font-size: 1.1rem;
		font-weight: 600;
		margin-top: 1.5rem;
		margin-bottom: 0.5rem;
	}

	:global(.markdown-content p) {
		margin-bottom: 1rem;
		color: #333;
	}

	:global(.markdown-content a) {
		color: #0066cc;
		text-decoration: none;
	}

	:global(.markdown-content a:hover) {
		text-decoration: underline;
	}

	:global(.markdown-content code) {
		font-family: 'SF Mono', Monaco, 'Courier New', monospace;
		font-size: 0.875em;
		background: #f0f0f0;
		padding: 0.15em 0.4em;
		border-radius: 3px;
	}

	:global(.markdown-content pre) {
		background: #1a1a1a;
		color: #e5e5e5;
		padding: 1rem;
		border-radius: 6px;
		overflow-x: auto;
		margin: 1rem 0;
	}

	:global(.markdown-content pre code) {
		background: none;
		padding: 0;
		font-size: 0.85rem;
	}

	:global(.markdown-content ul, .markdown-content ol) {
		margin: 1rem 0;
		padding-left: 1.5rem;
	}

	:global(.markdown-content li) {
		margin-bottom: 0.25rem;
	}

	:global(.markdown-content table) {
		width: 100%;
		border-collapse: collapse;
		margin: 1rem 0;
		font-size: 0.9rem;
	}

	:global(.markdown-content th, .markdown-content td) {
		text-align: left;
		padding: 0.5rem 0.75rem;
		border-bottom: 1px solid #e5e5e5;
	}

	:global(.markdown-content th) {
		font-weight: 600;
		background: #f5f5f5;
	}

	:global(.markdown-content hr) {
		border: none;
		border-top: 1px solid #e5e5e5;
		margin: 2rem 0;
	}

	:global(.markdown-content blockquote) {
		border-left: 3px solid #ddd;
		padding-left: 1rem;
		margin: 1rem 0;
		color: #666;
	}

	:global(.markdown-content em) {
		color: #666;
	}

	:global(.markdown-content strong) {
		font-weight: 600;
	}
</style>
