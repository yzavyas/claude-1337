import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: '404.html',
			precompress: false,
			strict: true
		}),
		paths: {
			base: process.env.NODE_ENV === 'production' ? '/claude-1337' : ''
		},
		prerender: {
			handleHttpError: ({ path, referrer }) => {
				console.warn(`[prerender] 404: ${path} (from ${referrer})`);
			}
		}
	}
};

export default config;
