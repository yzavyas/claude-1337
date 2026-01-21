<script lang="ts">
	/**
	 * Font Toggle Component
	 *
	 * Allows switching between sans-serif and serif fonts for reading.
	 * Uses Bits UI Toggle primitive for accessibility.
	 * Consumes context from Article component.
	 */
	import { getContext } from 'svelte';
	import { Toggle } from 'bits-ui';

	// Get article context (provided by Article component)
	const article = getContext<{
		fontFamily: 'sans' | 'serif';
		toggleFont: () => void;
	}>('article');

	// Fallback for standalone use
	let localFontFamily = $state<'sans' | 'serif'>('sans');

	const fontFamily = $derived(article?.fontFamily ?? localFontFamily);
	const toggleFont = article?.toggleFont ?? (() => {
		localFontFamily = localFontFamily === 'sans' ? 'serif' : 'sans';
	});
</script>

<div class="font-toggle-container">
	<span class="font-toggle-label" id="font-toggle-label">Font</span>
	<Toggle.Root
		pressed={fontFamily === 'serif'}
		onPressedChange={toggleFont}
		class="font-toggle"
		aria-labelledby="font-toggle-label"
		aria-describedby="font-toggle-desc"
	>
		<span class="font-option sans" class:active={fontFamily === 'sans'} aria-hidden="true">
			Aa
		</span>
		<span class="font-option serif" class:active={fontFamily === 'serif'} aria-hidden="true">
			Aa
		</span>
	</Toggle.Root>
	<span class="sr-only" id="font-toggle-desc">
		Currently using {fontFamily === 'sans' ? 'sans-serif' : 'serif'} font
	</span>
</div>

<style>
	.font-toggle-container {
		display: flex;
		align-items: center;
		gap: var(--space-2);
	}

	.font-toggle-label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	:global(.font-toggle) {
		display: flex;
		gap: var(--space-1);
		padding: var(--space-1);
		background: var(--color-bg-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	:global(.font-toggle:hover) {
		border-color: var(--color-border-strong);
	}

	:global(.font-toggle:focus-visible) {
		outline: var(--focus-ring-width) solid var(--focus-ring-color);
		outline-offset: var(--focus-ring-offset);
	}

	.font-option {
		padding: var(--space-1) var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		border-radius: var(--radius-sm);
		transition:
			background-color var(--duration-fast) var(--ease-out),
			color var(--duration-fast) var(--ease-out);
	}

	.font-option.active {
		background: var(--color-bg-elevated);
		color: var(--color-text);
	}

	.font-option.sans {
		font-family: var(--font-body);
	}

	.font-option.serif {
		font-family: var(--font-reading);
		font-style: italic;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}
</style>
