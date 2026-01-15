<script lang="ts">
	import { base } from '$app/paths';
	import { onMount } from 'svelte';
	import gsap from 'gsap';

	// Act 1: Signal — The Formation
	// Tree grows from seed. Text types. Principles land.

	let line1El: HTMLElement;
	let line2El: HTMLElement;
	let videoEl: HTMLVideoElement;
	let principlesEl: HTMLElement;
	let ctaEl: HTMLElement;
	let principleEls: HTMLElement[] = [];

	let activePrinciple = $state<number | null>(null);
	let sequenceComplete = $state(false);

	const line1Text = 'Cognitive Extensions for';
	const line2Text = 'Effective Collaborative Intelligence';

	const principles = [
		{
			word: 'transparency',
			definition: 'You see the reasoning. No black boxes.'
		},
		{
			word: 'trust',
			definition: 'Mutual and earned. Both agents reliable.'
		},
		{
			word: 'control',
			definition: 'You guide the direction. You shape the outcome.'
		},
		{
			word: 'agency',
			definition: 'You grow through it. Not dependent on it.'
		}
	];

	function typeText(element: HTMLElement, text: string, duration: number): gsap.core.Timeline {
		const tl = gsap.timeline();
		element.textContent = '';
		element.style.visibility = 'visible';

		const chars = text.split('');
		chars.forEach((char) => {
			const span = document.createElement('span');
			span.textContent = char === ' ' ? '\u00A0' : char;
			span.style.opacity = '0';
			element.appendChild(span);
		});

		const charSpans = element.querySelectorAll('span');
		const charDelay = duration / chars.length;

		tl.to(charSpans, {
			opacity: 1,
			duration: 0.03,
			stagger: charDelay,
			ease: 'none'
		});

		return tl;
	}

	onMount(() => {
		const tl = gsap.timeline({
			onComplete: () => {
				sequenceComplete = true;
			}
		});

		// Initial states
		line1El.style.visibility = 'hidden';
		line2El.style.visibility = 'hidden';
		gsap.set(videoEl, { opacity: 0 });
		gsap.set(principlesEl, { opacity: 0, y: 20 });
		gsap.set(ctaEl, { opacity: 0, y: 15 });

		// Sequence
		tl.to({}, { duration: 0.3 });

		// Type first line
		tl.add(typeText(line1El, line1Text, 1.0));

		tl.to({}, { duration: 0.2 });

		// Type headline
		tl.add(typeText(line2El, line2Text, 1.5));

		// Start video as headline completes
		tl.to(videoEl, {
			opacity: 1,
			duration: 0.5,
			onStart: () => {
				videoEl.play();
			}
		}, '-=0.5');

		// Wait for tree to grow (video is ~5 seconds)
		tl.to({}, { duration: 4.5 });

		// Principles fade in
		tl.to(principlesEl, {
			opacity: 1,
			y: 0,
			duration: 0.8,
			ease: 'power2.out'
		});

		// Stagger principles
		tl.fromTo(
			principleEls,
			{ opacity: 0, y: 10 },
			{
				opacity: 1,
				y: 0,
				duration: 0.5,
				stagger: 0.1,
				ease: 'power2.out'
			},
			'-=0.4'
		);

		tl.to({}, { duration: 0.3 });

		// CTA
		tl.to(ctaEl, {
			opacity: 1,
			y: 0,
			duration: 0.6,
			ease: 'power2.out'
		});

		return () => tl.kill();
	});

	function handlePrincipleEnter(index: number) {
		if (!sequenceComplete) return;
		activePrinciple = index;
	}

	function handlePrincipleLeave() {
		activePrinciple = null;
	}

	function togglePrinciple(index: number) {
		if (!sequenceComplete) return;
		activePrinciple = activePrinciple === index ? null : index;
	}
</script>

<section class="formation">
	<div class="signal">
		<p class="line-context" bind:this={line1El}></p>
		<h1 class="headline" bind:this={line2El}></h1>

		<div class="tree-container">
			<video
				bind:this={videoEl}
				src="{base}/glyphs/formation-tree.mp4"
				muted
				playsinline
				preload="auto"
				class="tree-video"
			></video>
		</div>

		<div class="principles" bind:this={principlesEl}>
			{#each principles as { word }, i}
				<button
					class="principle"
					class:active={activePrinciple === i}
					bind:this={principleEls[i]}
					onclick={() => togglePrinciple(i)}
					onmouseenter={() => handlePrincipleEnter(i)}
					onmouseleave={handlePrincipleLeave}
				>
					{word}
				</button>
				{#if i < principles.length - 1}
					<span class="separator">·</span>
				{/if}
			{/each}
		</div>

		{#if activePrinciple !== null}
			<div class="definition" role="tooltip">
				<span class="def-word">{principles[activePrinciple].word}</span>
				<span class="def-text">{principles[activePrinciple].definition}</span>
			</div>
		{/if}
	</div>

	<div class="threshold" bind:this={ctaEl}>
		<a href="{base}/explore/" class="enter">
			<span>Explore extensions</span>
			<span class="arrow">→</span>
		</a>
	</div>
</section>

<style>
	.formation {
		min-height: 100dvh;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: var(--space-6);
		text-align: center;
		background: var(--craft-paper);
	}

	.signal {
		position: relative;
		max-width: 800px;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.line-context {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: 400;
		letter-spacing: var(--tracking-wide);
		color: var(--craft-text-tertiary);
		margin-bottom: var(--space-2);
		min-height: 1.5em;
	}

	.headline {
		font-size: clamp(1.75rem, 5vw, 3rem);
		font-weight: 500;
		letter-spacing: -0.02em;
		line-height: 1.2;
		margin: 0;
		color: var(--craft-text-primary);
		min-height: 1.2em;
	}

	.tree-container {
		margin: var(--space-8) 0;
		width: min(320px, 70vw);
		aspect-ratio: 1;
	}

	.tree-video {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}

	.principles {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-3);
		flex-wrap: wrap;
	}

	.principle {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: 500;
		letter-spacing: var(--tracking-wide);
		color: var(--craft-text-tertiary);
		background: none;
		border: none;
		padding: var(--space-1) var(--space-2);
		cursor: pointer;
		transition: color var(--duration-normal) var(--ease-out);
	}

	.principle:hover,
	.principle.active {
		color: var(--gold);
	}

	.separator {
		color: var(--craft-text-tertiary);
		opacity: 0.5;
		user-select: none;
	}

	.definition {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		top: calc(100% + var(--space-4));
		width: min(360px, calc(100vw - var(--space-8)));
		padding: var(--space-4) var(--space-5);
		background: var(--craft-text-primary);
		color: var(--craft-paper);
		border-radius: var(--radius-md);
		box-shadow: var(--shadow-lg);
		text-align: left;
		z-index: 10;
		animation: defReveal 0.3s var(--ease-out) forwards;
	}

	@keyframes defReveal {
		from {
			opacity: 0;
			transform: translateX(-50%) translateY(6px);
		}
		to {
			opacity: 1;
			transform: translateX(-50%) translateY(0);
		}
	}

	.def-word {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: 600;
		letter-spacing: var(--tracking-wide);
		opacity: 0.6;
		margin-bottom: var(--space-1);
	}

	.def-text {
		display: block;
		font-size: var(--text-sm);
		line-height: var(--leading-normal);
	}

	.threshold {
		margin-top: var(--space-10);
	}

	.enter {
		display: inline-flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-4) var(--space-6);
		font-size: var(--text-base);
		font-weight: 500;
		letter-spacing: var(--tracking-wide);
		color: var(--craft-paper);
		background: var(--gold);
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition:
			background var(--duration-normal) var(--ease-out),
			transform var(--duration-normal) var(--ease-spring);
	}

	.enter:hover {
		background: var(--gold-hover);
	}

	.enter:active {
		transform: scale(0.98);
	}

	.arrow {
		display: inline-block;
		transition: transform var(--duration-normal) var(--ease-spring);
	}

	.enter:hover .arrow {
		transform: translateX(4px);
	}

	@media (max-width: 640px) {
		.formation {
			padding: var(--space-4);
		}

		.line-context {
			font-size: var(--text-xs);
		}

		.headline {
			font-size: clamp(1.5rem, 7vw, 2rem);
		}

		.tree-container {
			width: min(260px, 65vw);
			margin: var(--space-6) 0;
		}

		.principles {
			gap: var(--space-2);
		}

		.principle {
			font-size: var(--text-xs);
		}

		.definition {
			position: fixed;
			bottom: var(--space-4);
			top: auto;
			left: var(--space-4);
			right: var(--space-4);
			transform: none;
			width: auto;
		}

		@keyframes defReveal {
			from {
				opacity: 0;
				transform: translateY(12px);
			}
			to {
				opacity: 1;
				transform: translateY(0);
			}
		}

		.threshold {
			margin-top: var(--space-8);
		}

		.enter {
			font-size: var(--text-sm);
			padding: var(--space-3) var(--space-5);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.definition {
			animation: none;
			opacity: 1;
		}
	}
</style>
