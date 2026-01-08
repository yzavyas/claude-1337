<script lang="ts">
	import HookSection from '$lib/components/ethos/HookSection.svelte';
	import EvidenceSection from '$lib/components/ethos/EvidenceSection.svelte';
	import ExtendedMindSection from '$lib/components/ethos/ExtendedMindSection.svelte';
	import FrameworkSection from '$lib/components/ethos/FrameworkSection.svelte';
	import LensSection from '$lib/components/ethos/LensSection.svelte';
	import PrinciplesSection from '$lib/components/ethos/PrinciplesSection.svelte';
	import ChoiceSection from '$lib/components/ethos/ChoiceSection.svelte';
</script>

<svelte:head>
	<title>Why This Approach — claude-1337</title>
	<meta name="description" content="Research-backed rationale for cognitive extensions that make engineers better, not more dependent." />
</svelte:head>

<main class="ethos-page">
	<HookSection />

	<EvidenceSection />

	<ExtendedMindSection />

	<FrameworkSection />

	<LensSection />

	<PrinciplesSection />

	<ChoiceSection />
</main>

<style>
	.ethos-page {
		min-height: 100vh;
		padding-top: 84px;
	}
</style>
