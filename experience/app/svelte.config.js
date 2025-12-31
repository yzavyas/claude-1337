import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte'],

	preprocess: [vitePreprocess()],

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: false
		}),
		paths: {
			base: process.env.NODE_ENV === 'production' ? '/claude-1337' : ''
		},
		prerender: {
			handleMissingId: 'warn',
			handleHttpError: 'warn',
			handleUnseenRoutes: 'warn',
			entries: ['*']
		}
	}
};

export default config;
