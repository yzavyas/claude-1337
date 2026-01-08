<script lang="ts">
	import { browser } from '$app/environment';

	interface Props {
		command: string;
	}

	let { command }: Props = $props();
	let copied = $state(false);
	let timeout: ReturnType<typeof setTimeout>;

	async function copy() {
		if (!browser) return;

		try {
			await navigator.clipboard.writeText(command);
			copied = true;
			clearTimeout(timeout);
			timeout = setTimeout(() => {
				copied = false;
			}, 2000);
		} catch (err) {
			console.error('Failed to copy:', err);
		}
	}
</script>

<button class="copy-cmd" class:copied onclick={copy}>
	<span class="cmd-text">{command}</span>
	<span class="copy-hint">{copied ? '✓' : 'copy'}</span>
</button>

<style>
	.copy-cmd {
		position: relative;
		display: block;
		padding: var(--space-3) var(--space-4);
		background: var(--color-bg-elevated);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-md);
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		text-align: left;
		width: 100%;
		cursor: pointer;
		transition:
			border-color var(--duration-fast) var(--ease-out),
			background var(--duration-fast) var(--ease-out),
			transform var(--duration-fast) var(--ease-out);
	}

	.copy-cmd:hover {
		border-color: var(--color-accent);
		background: var(--color-bg-surface);
	}

	.copy-cmd:active {
		transform: scale(0.98);
	}

	.copy-cmd.copied {
		border-color: var(--color-accent-positive);
	}

	.cmd-text {
		display: block;
		color: var(--color-text-secondary);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		padding-right: var(--space-16);
	}

	.copy-hint {
		position: absolute;
		right: var(--space-4);
		top: 50%;
		transform: translateY(-50%);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		opacity: 0;
		transition: opacity var(--duration-fast) var(--ease-out);
		pointer-events: none;
		background: var(--color-bg-elevated);
		padding-left: var(--space-2);
	}

	.copy-cmd:hover .copy-hint {
		opacity: 1;
	}

	.copy-cmd.copied .copy-hint {
		opacity: 1;
		color: var(--color-accent-positive);
	}
</style>
