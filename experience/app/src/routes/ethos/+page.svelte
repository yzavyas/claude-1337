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
		text-align: center;
		animation: fadeIn 500ms ease;
	}

	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	.pixel-art {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		line-height: 1.2;
		color: var(--accent);
		background: var(--bg-surface);
		border: 1px solid var(--border-subtle);
		border-radius: var(--radius-md);
		padding: var(--space-lg);
		margin-bottom: var(--space-xl);
		white-space: pre;
	}

	.message {
		margin-bottom: var(--space-lg);
	}

	.tagline {
		font-family: var(--font-mono);
		font-size: 1.1rem;
		color: var(--text-primary);
		margin-bottom: var(--space-xs);
	}

	.sub {
		font-family: var(--font-mono);
		font-size: 0.85rem;
		color: var(--text-muted);
	}

	.dots {
		display: flex;
		gap: var(--space-sm);
	}

	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--border-default);
		transition: all var(--transition-fast);
	}

	.dot.active {
		background: var(--accent);
		box-shadow: 0 0 8px var(--accent);
	}

	@media (max-width: 640px) {
		.pixel-art {
			font-size: 0.6rem;
			padding: var(--space-md);
		}
	}
</style>
