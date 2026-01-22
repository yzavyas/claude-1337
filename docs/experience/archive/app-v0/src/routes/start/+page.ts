import { getContent } from '$lib/content';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = () => {
	const content = getContent('start');

	if (!content) {
		throw error(404, 'Start page not found');
	}

	return { content };
};
