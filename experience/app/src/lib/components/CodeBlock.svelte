<script lang="ts">
	import Mermaid from './Mermaid.svelte';

	interface Props {
		lang?: string;
		text: string;
	}

	const { lang, text }: Props = $props();

	const isMermaid = lang === 'mermaid';
</script>

{#if isMermaid}
	<Mermaid code={text} />
{:else}
	<pre><code class={lang ? `language-${lang}` : ''}>{text}</code></pre>
{/if}
