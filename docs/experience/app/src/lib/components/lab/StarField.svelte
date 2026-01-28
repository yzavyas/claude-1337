<script lang="ts">
	/**
	 * StarField - Depth background for Observatory aesthetic
	 *
	 * Multiple star layers at different densities create depth.
	 * Static (no animation) for performance.
	 */
</script>

<div class="starfield" aria-hidden="true"></div>

<style>
	.starfield {
		position: fixed;
		inset: 0;
		z-index: -1;
		pointer-events: none;
		contain: strict;

		/* Deep space gradient - not flat black */
		background:
			radial-gradient(ellipse 120% 80% at 30% 20%, oklch(14% 0.025 250) 0%, transparent 50%),
			radial-gradient(ellipse 100% 60% at 70% 80%, oklch(12% 0.02 260) 0%, transparent 40%),
			var(--color-bg, oklch(10% 0.018 250));
	}

	/* Distant stars - many, small, dim */
	.starfield::before {
		content: '';
		position: absolute;
		inset: 0;
		background-image:
			radial-gradient(1px 1px at 10% 15%, oklch(50% 0.01 80 / 60%), transparent),
			radial-gradient(1px 1px at 25% 35%, oklch(45% 0.01 75 / 50%), transparent),
			radial-gradient(1px 1px at 40% 10%, oklch(55% 0.01 85 / 55%), transparent),
			radial-gradient(1px 1px at 55% 45%, oklch(48% 0.01 78 / 45%), transparent),
			radial-gradient(1px 1px at 70% 25%, oklch(52% 0.01 82 / 50%), transparent),
			radial-gradient(1px 1px at 85% 55%, oklch(46% 0.01 76 / 55%), transparent),
			radial-gradient(1px 1px at 15% 65%, oklch(50% 0.01 80 / 48%), transparent),
			radial-gradient(1px 1px at 30% 85%, oklch(54% 0.01 84 / 52%), transparent),
			radial-gradient(1px 1px at 60% 75%, oklch(47% 0.01 77 / 50%), transparent),
			radial-gradient(1px 1px at 80% 90%, oklch(51% 0.01 81 / 55%), transparent),
			radial-gradient(1px 1px at 95% 40%, oklch(49% 0.01 79 / 48%), transparent),
			radial-gradient(1px 1px at 5% 50%, oklch(53% 0.01 83 / 52%), transparent);
		background-size: 100% 100%;
	}

	/* Near stars - fewer, larger, brighter */
	.starfield::after {
		content: '';
		position: absolute;
		inset: 0;
		background-image:
			radial-gradient(2px 2px at 12% 22%, oklch(75% 0.02 85 / 70%), transparent),
			radial-gradient(1.5px 1.5px at 35% 68%, oklch(70% 0.015 80 / 60%), transparent),
			radial-gradient(2px 2px at 58% 18%, oklch(78% 0.02 88 / 65%), transparent),
			radial-gradient(1.5px 1.5px at 78% 52%, oklch(72% 0.018 82 / 55%), transparent),
			radial-gradient(2px 2px at 22% 88%, oklch(76% 0.02 86 / 60%), transparent),
			radial-gradient(1.5px 1.5px at 92% 72%, oklch(68% 0.015 78 / 50%), transparent);
		background-size: 100% 100%;
	}
</style>
