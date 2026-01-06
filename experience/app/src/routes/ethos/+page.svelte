<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import { getContent } from '$lib/content';

	const content = getContent('ethos');
</script>

<article class="markdown-content">
	{#if content}
		<SvelteMarkdown source={content} />
	{:else}
		<p>Loading...</p>
	{/if}
</article>
