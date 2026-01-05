<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import { getContent } from '$lib/content';

	const content = getContent('start');
</script>

<article class="markdown-content">
	{#if content}
		<SvelteMarkdown source={content} />
	{:else}
		<h1>claude-1337</h1>
		<p>cognitive extensions for claude code</p>
	{/if}
</article>
