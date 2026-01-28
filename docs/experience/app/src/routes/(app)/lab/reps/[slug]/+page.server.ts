import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

// Pre-render all REPs at build time
export async function entries() {
	try {
		const repsDir = join(LAB_ROOT, 'reps');
		const files = await readdir(repsDir);
		return files
			.filter(f => f.startsWith('rep-') && f.endsWith('.md'))
			.map(f => ({ slug: f.replace('.md', '') }));
	} catch {
		return [];
	}
}

interface REPPageData {
	slug: string;
	markdown: string;
	experimentSlug?: string;
}

export async function load({ params }): Promise<REPPageData> {
	const { slug } = params;

	// Security: prevent directory traversal
	if (slug.includes('..')) {
		throw error(400, 'Invalid path');
	}

	// Must be a REP file
	if (!slug.startsWith('rep-')) {
		throw error(400, 'Invalid REP');
	}

	const repPath = join(LAB_ROOT, 'reps', `${slug}.md`);

	try {
		const markdown = await readFile(repPath, 'utf-8');

		// Extract REP ID for experiment lookup
		const idMatch = slug.match(/^rep-(\d+)/);
		const id = idMatch?.[1] || '000';

		// Check for linked experiment
		let experimentSlug: string | undefined;
		try {
			const experimentsDir = join(LAB_ROOT, 'experiments');
			const folders = await readdir(experimentsDir, { withFileTypes: true });
			const expFolder = folders.find(f => f.isDirectory() && f.name.startsWith(`rep-${id}`));
			if (expFolder) {
				experimentSlug = expFolder.name;
			}
		} catch {
			// No experiments
		}

		return {
			slug,
			markdown,
			experimentSlug
		};
	} catch (e) {
		throw error(404, 'REP not found');
	}
}
