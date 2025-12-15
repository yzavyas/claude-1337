// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

// https://astro.build/config
export default defineConfig({
  site: 'https://yzavyas.github.io',
  base: '/claude-1337',
  output: 'static',
  integrations: [svelte()],
});
