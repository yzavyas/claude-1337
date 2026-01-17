import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.svx'],
	preprocess: [
		vitePreprocess(),
		mdsvex({
			extensions: ['.svx']
		})
	],

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		paths: {
			base: process.env.NODE_ENV === 'production' ? '/claude-1337' : ''
		},
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				// Ignore 404s for paths that aren't web routes (e.g., /plugins/)
				if (message.includes('404')) {
					console.warn(`Warning: ${path} not found (linked from ${referrer})`);
					return;
				}
				// Ignore 400s for non-HTML resources (JSON, etc.)
				if (message.includes('400') && (path.endsWith('.json') || path.endsWith('.md'))) {
					console.warn(`Warning: ${path} is not a valid route (linked from ${referrer})`);
					return;
				}
				throw new Error(message);
			}
		},
		alias: {
			$components: 'src/lib/components',
			$styles: 'src/lib/styles',
			$content: '../content'
		}
	}
};

export default config;
