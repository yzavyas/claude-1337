import { getContent } from '$lib/content';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
	const slug = params.slug || '';
	const fullSlug = slug ? `explore/tutorials/${slug}` : 'explore/tutorials';
	const content = getContent(fullSlug);

	if (!content) {
		throw error(404, `Content not found: ${fullSlug}`);
	}

	return {
		content,
		slug: fullSlug
	};
};
