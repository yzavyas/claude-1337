/**
 * Scroll Infrastructure
 * Lenis smooth scroll + GSAP ScrollTrigger integration
 *
 * Usage: Initialize once at app root, use ScrollTrigger in components
 */

import { browser } from '$app/environment';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register GSAP plugins
if (browser) {
	gsap.registerPlugin(ScrollTrigger);
}

let lenis: Lenis | null = null;

/**
 * Initialize scroll infrastructure
 * Lenis disabled by default - native scroll is better for reading-focused sites
 * Call once in root layout
 */
export function initSmoothScroll(options?: { enableLenis?: boolean }): Lenis | null {
	if (!browser) return null;

	// Set ScrollTrigger defaults for animations
	ScrollTrigger.defaults({
		toggleActions: 'play none none reverse'
	});

	// Lenis disabled by default - causes laggy feel on content sites
	// Enable only for pages with scroll-driven animations
	if (!options?.enableLenis) {
		return null;
	}

	// Check for reduced motion preference
	const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	if (prefersReducedMotion) {
		return null;
	}

	// Create Lenis instance with snappier settings if enabled
	lenis = new Lenis({
		lerp: 0.15, // Snappier than 0.1
		smoothWheel: true,
		wheelMultiplier: 1
	});

	// Sync Lenis with GSAP ScrollTrigger
	lenis.on('scroll', ScrollTrigger.update);

	// Use GSAP ticker for smooth animation frame sync
	gsap.ticker.add((time) => {
		lenis?.raf(time * 1000);
	});

	// Disable GSAP's native lag smoothing to let Lenis handle it
	gsap.ticker.lagSmoothing(0);

	return lenis;
}

/**
 * Destroy smooth scroll instance
 * Call in root layout cleanup
 */
export function destroySmoothScroll(): void {
	if (lenis) {
		lenis.destroy();
		lenis = null;
	}
	if (browser) {
		ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
	}
}

/**
 * Get current Lenis instance
 */
export function getLenis(): Lenis | null {
	return lenis;
}

/**
 * Scroll to element or position
 */
export function scrollTo(
	target: string | number | HTMLElement,
	options?: { offset?: number; duration?: number; immediate?: boolean }
): void {
	if (!browser) return;

	if (lenis) {
		lenis.scrollTo(target, {
			offset: options?.offset ?? 0,
			duration: options?.duration ?? 1.2,
			immediate: options?.immediate ?? false
		});
	} else {
		// Fallback for reduced motion
		if (typeof target === 'string') {
			const element = document.querySelector(target);
			element?.scrollIntoView({ behavior: 'auto' });
		} else if (typeof target === 'number') {
			window.scrollTo({ top: target, behavior: 'auto' });
		} else {
			target.scrollIntoView({ behavior: 'auto' });
		}
	}
}

/**
 * Create a scroll-triggered animation context
 * Returns cleanup function
 */
export function createScrollContext(
	element: HTMLElement,
	callback: (ctx: gsap.Context) => void
): () => void {
	if (!browser) return () => {};

	const ctx = gsap.context(callback, element);

	return () => {
		ctx.revert();
	};
}

// Export GSAP and ScrollTrigger for direct use
export { gsap, ScrollTrigger };
