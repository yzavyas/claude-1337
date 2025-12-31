<script>
	import { onMount } from 'svelte';

	let frame = $state(0);

	onMount(() => {
		const interval = setInterval(() => {
			frame = (frame + 1) % 4;
		}, 500);
		return () => clearInterval(interval);
	});

	const constructionFrames = [
		`
    ___________
   |  WORK IN  |
   | PROGRESS  |
   |___________|
      |    |
   ___||____||___
  |   \\    /   |
  |    \\  /    |
  |_____\\/_____|
        `,
		`
    ___________
   |  WORK IN  |
   | PROGRESS  |
   |___________|
      |    |
   ___||____||___
  |    \\  /    |
  |     \\/     |
  |____________|
        `,
		`
    ___________
   |  WORK IN  |
   | PROGRESS  |
   |___________|
      |    |
   ___||____||___
  |     \\/     |
  |     /\\     |
  |____/  \\____|
        `,
		`
    ___________
   |  WORK IN  |
   | PROGRESS  |
   |___________|
      |    |
   ___||____||___
  |    /  \\    |
  |   /    \\   |
  |__/______\\__|
        `
	];
</script>

<div class="wip-container">
	<pre class="pixel-art">{constructionFrames[frame]}</pre>

	<div class="message">
		<p class="tagline">something is being built here</p>
		<p class="sub">the cinematic experience is coming</p>
	</div>

	<div class="dots">
		<span class="dot" class:active={frame === 0}></span>
		<span class="dot" class:active={frame === 1}></span>
		<span class="dot" class:active={frame === 2}></span>
		<span class="dot" class:active={frame === 3}></span>
	</div>
</div>

<style>
	.wip-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 60vh;
		gap: 2rem;
	}

	.pixel-art {
		font-family: monospace;
		font-size: 0.9rem;
		line-height: 1.2;
		color: var(--yellow);
		text-shadow: 0 0 10px rgba(255, 255, 0, 0.4);
		background: none;
		border: none;
		box-shadow: none;
		margin: 0;
		padding: 0;
	}

	.pixel-art:hover {
		border: none;
		box-shadow: none;
		background: none;
	}

	.message {
		text-align: center;
	}

	.tagline {
		color: var(--fg);
		font-size: 1.1rem;
		margin-bottom: 0.5rem;
	}

	.sub {
		color: var(--fg-dim);
		font-size: 0.9rem;
	}

	.dots {
		display: flex;
		gap: 0.5rem;
	}

	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--fg-dim);
		opacity: 0.3;
		transition: all 0.3s ease;
	}

	.dot.active {
		background: var(--green);
		opacity: 1;
		box-shadow: 0 0 10px var(--glow);
	}
</style>
