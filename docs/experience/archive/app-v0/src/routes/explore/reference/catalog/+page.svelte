<script lang="ts">
	import { base } from '$app/paths';
	import PluginCatalog from '$lib/components/PluginCatalog.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<article class="markdown-content">
	<h1>plugin catalog</h1>
	<p>
		all plugins in the {data.marketplaceName} marketplace. filter by component type or search by
		keywords.
	</p>

	<h2>install</h2>
	<pre><code>/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337</code></pre>

	<PluginCatalog plugins={data.plugins} format="cards" />

	<h2>component types</h2>
	<table>
		<thead>
			<tr>
				<th>type</th>
				<th>what it does</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td><strong>skill</strong></td>
				<td>injects domain knowledge and decision frameworks</td>
			</tr>
			<tr>
				<td><strong>hook</strong></td>
				<td>event-triggered behavior modification</td>
			</tr>
			<tr>
				<td><strong>agent</strong></td>
				<td>specialized subagent with focused capability</td>
			</tr>
			<tr>
				<td><strong>command</strong></td>
				<td>slash command workflow shortcuts</td>
			</tr>
			<tr>
				<td><strong>mcp</strong></td>
				<td>external system integrations</td>
			</tr>
		</tbody>
	</table>
</article>
