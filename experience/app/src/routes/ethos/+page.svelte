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
