import { readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../lab-1337');

export async function load({ params }) {
	const { slug, file } = params;

	// Security: prevent directory traversal
	if (slug.includes('..') || file.includes('..')) {
		throw error(400, 'Invalid path');
	}

	// Only allow analysis markdown files
	if (!file.endsWith('-analysis.md')) {
		throw error(400, 'Only analysis files can be viewed');
	}

	const filePath = join(LAB_ROOT, 'experiments', slug, file);

	try {
		const content = await readFile(filePath, 'utf-8');

		// Parse metadata from the markdown
		const title = content.match(/^# (.+)$/m)?.[1] || file;
		const timestamp = content.match(/\*\*Generated:\*\* (.+)$/m)?.[1] || '';
		const model = content.match(/\*\*Verification Model:\*\* (.+)$/m)?.[1] || '';

		return {
			slug,
			file,
			title,
			timestamp,
			model,
			content
		};
	} catch (e) {
		throw error(404, 'Analysis not found');
	}
}
