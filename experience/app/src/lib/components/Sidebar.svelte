<script lang="ts">
	import { page } from '$app/stores';

	interface Props {
		section: string;
		items: Array<{ href: string; label: string }>;
	}

	let { section, items }: Props = $props();
</script>

<aside class="sidebar">
	<nav class="sidebar-nav">
		<div class="section-title">
			<span class="prompt">$</span>
			{section}/
		</div>
		<ul>
			{#each items as item}
				<li>
					<a
						href={item.href}
						class="nav-link"
						class:active={$page.url.pathname === item.href ||
							$page.url.pathname === item.href.replace(/\/$/, '')}
					>
						{item.label}
					</a>
				</li>
			{/each}
		</ul>
	</nav>
</aside>
