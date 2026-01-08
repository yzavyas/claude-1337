<script lang="ts">
	import Mermaid from './Mermaid.svelte';
	import VisualRenderer from './VisualRenderer.svelte';

	interface Props {
		lang?: string;
		text: string;
	}

	const { lang, text }: Props = $props();
</script>

{#if lang === 'mermaid'}
	<Mermaid code={text} />
{:else if lang === 'visual'}
	<VisualRenderer name={text} />
{:else}
	<pre><code class={lang ? `language-${lang}` : ''}>{text}</code></pre>
{/if}
