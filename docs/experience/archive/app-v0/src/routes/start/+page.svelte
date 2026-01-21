<script lang="ts">
	import SvelteMarkdown from '@humanspeak/svelte-markdown';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<article class="markdown-content">
	<SvelteMarkdown source={data.content} />
</article>
