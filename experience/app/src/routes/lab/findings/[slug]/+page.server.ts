import { readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../lab-1337');

interface FindingsData {
	slug: string;
	repId: string;
	title: string;
	date: string;
	status: string;
	content: string;
	proposalSlug?: string;
	experimentSlug?: string;
}

function parseMarkdownMeta(content: string): {
	title: string;
	date: string;
	status: string;
	body: string;
} {
	const titleMatch = content.match(/^#\s+(.+?)(?:\n|$)/m);
	const title = titleMatch?.[1] || 'Untitled';

	const dateMatch = content.match(/\*\*Date\*\*:\s*(.+)/i);
	const date = dateMatch?.[1] || '';

	const statusMatch = content.match(/\*\*Status\*\*:\s*(.+)/i);
	const status = statusMatch?.[1] || '';

	// Strip frontmatter: find first ## heading after metadata
	const firstSectionMatch = content.match(/\n(## \w)/);
	const body = firstSectionMatch ? content.slice(content.indexOf(firstSectionMatch[1])) : content;

	return { title, date, status, body };
}

export async function load({ params }): Promise<FindingsData> {
	const { slug } = params;

	// Security
	if (slug.includes('..')) {
		throw error(400, 'Invalid path');
	}

	// Must be a findings file
	if (!slug.startsWith('rep-') || !slug.endsWith('-findings')) {
		throw error(400, 'Invalid findings path');
	}

	const filePath = join(LAB_ROOT, 'findings', `${slug}.md`);

	try {
		const rawContent = await readFile(filePath, 'utf-8');
		const { title, date, status, body } = parseMarkdownMeta(rawContent);

		// Extract REP ID
		const idMatch = slug.match(/^rep-(\d+)/);
		const repId = idMatch?.[1] || '000';

		// Try to find linked proposal
		let proposalSlug: string | undefined;
		try {
			const { readdir } = await import('fs/promises');
			const proposalsDir = join(LAB_ROOT, 'reps');
			const files = await readdir(proposalsDir);
			const proposalFile = files.find(f => f.startsWith(`rep-${repId}`) && f.endsWith('.md'));
			if (proposalFile) {
				proposalSlug = proposalFile.replace('.md', '');
			}
		} catch {
			// No proposal found
		}

		// Try to find linked experiment
		let experimentSlug: string | undefined;
		try {
			const { readdir } = await import('fs/promises');
			const experimentsDir = join(LAB_ROOT, 'experiments');
			const folders = await readdir(experimentsDir, { withFileTypes: true });
			const expFolder = folders.find(f => f.isDirectory() && f.name.startsWith(`rep-${repId}`));
			if (expFolder) {
				experimentSlug = expFolder.name;
			}
		} catch {
			// No experiment found
		}

		return {
			slug,
			repId,
			title,
			date,
			status,
			content: body,
			proposalSlug,
			experimentSlug
		};
	} catch (e) {
		throw error(404, 'Findings not found');
	}
}
