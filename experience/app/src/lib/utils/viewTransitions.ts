/**
 * View Transitions Hook
 *
 * Provides smooth page transitions using the View Transitions API.
 * Chromium 96%+ support, graceful degradation elsewhere.
 *
 * Usage: Call setupViewTransitions() once in root layout
 */
import { onNavigate } from '$app/navigation';

/**
 * Set up View Transitions for SvelteKit navigation
 * Falls back to instant navigation if API not supported
 */
export function setupViewTransitions(): void {
	onNavigate((navigation) => {
		// Skip if View Transitions API not supported
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
}
