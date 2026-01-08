<script lang="ts">
	import Mermaid from './Mermaid.svelte';

	// Using Svelte 4 export let syntax for svelte-markdown 0.4.1 compatibility
	// TODO: Upgrade to @humanspeak/svelte-markdown when npm registry access is available
	export let lang: string | undefined = undefined;
	export let text: string = '';

	$: isMermaid = lang === 'mermaid';
</script>

{#if isMermaid}
	<Mermaid code={text} />
{:else}
	<pre><code class={lang ? `language-${lang}` : ''}>{text}</code></pre>
{/if}
