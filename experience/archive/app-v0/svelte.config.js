import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.md', '.svx'],
	preprocess: [
		vitePreprocess(),
		mdsvex({
			extensions: ['.md', '.svx'],
			// Layout for markdown files (optional, can add later)
			// layout: './src/lib/layouts/MdLayout.svelte'
		})
	],

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
