<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import CodeBlock from '$lib/components/CodeBlock.svelte';
	import { getContent } from '$lib/content';

	const content = getContent('explore/explanation/ethos');
</script>

<article class="markdown-content">
	{#if content}
		<SvelteMarkdown source={content} renderers={{ code: CodeBlock }} />
	{:else}
		<p>Loading...</p>
	{/if}
</article>
