/**
 * Scroll-triggered Reveal Action
 *
 * Uses CSS scroll-timeline for modern browsers (Chrome 115+),
 * falls back to Intersection Observer for others.
 *
 * Usage:
 *   <div use:reveal={{ y: 30, delay: 100 }}>Content</div>
 */
import { browser } from '$app/environment';

export interface RevealOptions {
	/** Vertical offset in pixels (default: 30) */
	y?: number;
	/** Delay in milliseconds (default: 0) */
	delay?: number;
	/** Duration in milliseconds (default: 600) */
	duration?: number;
}

export function reveal(node: HTMLElement, options: RevealOptions = {}) {
	if (!browser) return;

	const { y = 30, delay = 0, duration = 600 } = options;

	// Check for reduced motion preference
	if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
		node.style.opacity = '1';
		return;
	}

	// Check if CSS scroll-timeline is supported
	const supportsScrollTimeline = CSS.supports('animation-timeline', 'view()');

	if (supportsScrollTimeline) {
		// Use native CSS scroll-driven animation
		node.style.setProperty('--reveal-y', `${y}px`);
		node.style.setProperty('--reveal-delay', `${delay}ms`);
		node.style.setProperty('--reveal-duration', `${duration}ms`);
		node.classList.add('reveal-css');
		return;
	}

	// Fallback: Intersection Observer
	const observer = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					// Add delay then reveal
					setTimeout(() => {
						node.classList.add('revealed');
					}, delay);
					observer.unobserve(node);
				}
			});
		},
		{ threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
	);

	node.style.setProperty('--reveal-y', `${y}px`);
	node.style.setProperty('--reveal-duration', `${duration}ms`);
	node.classList.add('reveal-fallback');
	observer.observe(node);

	return {
		destroy() {
			observer.disconnect();
		}
	};
}
