<script lang="ts">
	/**
	 * App layout - includes Shell with Banner, Nav, Footer
	 */
	import { Shell } from '$lib/components/layout';

	let { children } = $props();
</script>

<Shell>
	{@render children()}
</Shell>
