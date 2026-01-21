<script lang="ts">
	interface Props {
		term: string;
		definition: string;
	}

	let { term, definition }: Props = $props();
	let expanded = $state(false);

	function toggle() {
		expanded = !expanded;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			toggle();
		}
	}
</script>

<span
	class="expand-term"
	class:expanded
	role="button"
	tabindex="0"
	onclick={toggle}
	onkeydown={handleKeydown}
>
	<span class="term-text">{term}</span>
	<span class="definition-text">{definition}</span>
</span>

<style>
	.expand-term {
		position: relative;
		display: inline-block;
		cursor: pointer;
		border-bottom: 1px dotted var(--color-accent);
		transition: border-color var(--duration-normal) var(--ease-out);
	}

	.expand-term:hover {
		border-color: var(--color-text-primary);
	}

	.expand-term:focus-visible {
		outline: 2px solid var(--color-accent);
		outline-offset: 2px;
		border-radius: 2px;
	}

	.term-text {
		display: inline;
		transition: opacity var(--duration-normal) var(--ease-out);
	}

	.definition-text {
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		white-space: nowrap;
		opacity: 0;
		font-size: 0.65em;
		font-weight: var(--font-normal);
		letter-spacing: normal;
		color: var(--color-accent);
		transition: opacity var(--duration-normal) var(--ease-out);
		pointer-events: none;
	}

	.expanded .term-text {
		opacity: 0.3;
	}

	.expanded .definition-text {
		opacity: 1;
	}

	.expanded {
		border-color: transparent;
	}
</style>
