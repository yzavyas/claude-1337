<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		code: string;
		lang?: 'canvas' | 'html';
	}

	const { code, lang = 'canvas' }: Props = $props();

	let iframe: HTMLIFrameElement;
	let height = $state(300);

	// Build the full HTML document
	const html = $derived(() => {
		if (lang === 'html') {
			// Raw HTML - wrap minimally
			return `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<style>
		* { margin: 0; padding: 0; box-sizing: border-box; }
		body {
			background: transparent;
			font-family: system-ui, sans-serif;
			color: #e0e0dc;
		}
	</style>
</head>
<body>
${code}
</body>
</html>`;
		}

		// Canvas/JS mode - provide canvas context
		return `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<style>
		* { margin: 0; padding: 0; box-sizing: border-box; }
		body {
			background: transparent;
			display: flex;
			justify-content: center;
			align-items: center;
			min-height: 100vh;
		}
		canvas {
			display: block;
			max-width: 100%;
		}
	</style>
</head>
<body>
	<canvas id="canvas"></canvas>
	<script>
		const canvas = document.getElementById('canvas');
		const ctx = canvas.getContext('2d');

		// Set canvas size
		canvas.width = 800;
		canvas.height = 400;

		// Expose resize helper
		function resize(w, h) {
			canvas.width = w;
			canvas.height = h;
		}

		// Animation helper
		let animationId;
		function animate(fn) {
			function loop(time) {
				fn(time);
				animationId = requestAnimationFrame(loop);
			}
			animationId = requestAnimationFrame(loop);
		}

		// User code
		${code}
	<\/script>
</body>
</html>`;
	});

	onMount(() => {
		// Listen for height messages from iframe
		const handleMessage = (e: MessageEvent) => {
			if (e.data?.type === 'resize' && e.data?.height) {
				height = e.data.height;
			}
		};
		window.addEventListener('message', handleMessage);
		return () => window.removeEventListener('message', handleMessage);
	});
</script>

<div class="script-container">
	<iframe
		bind:this={iframe}
		srcdoc={html()}
		sandbox="allow-scripts"
		title="Embedded script"
		style="height: {height}px"
	></iframe>
</div>

<style>
	.script-container {
		margin: var(--space-xl, 2rem) 0;
		border-radius: 8px;
		overflow: hidden;
		background: rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(255, 255, 255, 0.05);
	}

	iframe {
		width: 100%;
		border: none;
		background: transparent;
		display: block;
	}
</style>
