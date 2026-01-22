<script lang="ts">
	interface Props {
		term: string;
		definition: string;
	}

	let { term, definition }: Props = $props();
	let flipped = $state(false);

	function toggle() {
		flipped = !flipped;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			toggle();
		}
	}
</script>

<span
	class="flip-container"
	class:flipped
	role="button"
	tabindex="0"
	onclick={toggle}
	onkeydown={handleKeydown}
>
	<span class="flip-card">
		<span class="front">{term}</span>
		<span class="back">{definition}</span>
	</span>
</span>

<style>
	.flip-container {
		display: inline-block;
		perspective: 1000px;
		cursor: pointer;
	}

	.flip-container:focus-visible {
		outline: 2px solid #3b82f6;
		outline-offset: 2px;
		border-radius: 2px;
	}

	.flip-card {
		display: inline-block;
		position: relative;
		transform-style: preserve-3d;
		transition: transform 0.5s ease;
	}

	.flipped .flip-card {
		transform: rotateX(180deg);
	}

	.front,
	.back {
		backface-visibility: hidden;
		-webkit-backface-visibility: hidden;
	}

	.front {
		display: inline-block;
		border-bottom: 1px dotted var(--color-text-muted);
		transition: border-color 0.15s ease;
	}

	.flip-container:hover .front {
		border-color: #3b82f6;
	}

	.back {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: rotateX(180deg) translate(-50%, 50%);
		white-space: nowrap;
		color: #3b82f6;
		font-family: var(--font-mono);
		font-size: 0.36em;
		font-weight: 500;
		letter-spacing: 0.01em;
	}
</style>
