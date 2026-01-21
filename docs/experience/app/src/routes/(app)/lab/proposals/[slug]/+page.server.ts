import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

// Pre-render all proposals at build time
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

type REPStatus = 'draft' | 'discussion' | 'fcp' | 'accepted' | 'rejected' | 'postponed' | 'implemented';

interface ProposalData {
	slug: string;
	id: string;
	title: string;
	status: REPStatus;
	created: string;
	authors: string;
	content: string;
	rip?: {
		slug: string;
		content: string;
	};
	experimentSlug?: string;
	findingsSlug?: string;
}

function parseMarkdownMeta(content: string): {
	title: string;
	status: REPStatus;
	created: string;
	authors: string;
	body: string;
} {
	const titleMatch = content.match(/^#\s+(.+?)(?:\n|$)/m);
	const title = titleMatch?.[1] || 'Untitled';

	const statusMatch = content.match(/\*\*Status\*\*:\s*(\w+)/i);
	const status = (statusMatch?.[1]?.toLowerCase() || 'draft') as REPStatus;

	const createdMatch = content.match(/\*\*Created\*\*:\s*(.+)/i);
	const created = createdMatch?.[1] || '';

	const authorsMatch = content.match(/\*\*Authors\*\*:\s*(.+)/i);
	const authors = authorsMatch?.[1] || '';

	// Strip frontmatter: remove everything before ## Summary
	const summaryIndex = content.indexOf('## Summary');
	const body = summaryIndex !== -1 ? content.slice(summaryIndex) : content;

	return { title, status, created, authors, body };
}

export async function load({ params }): Promise<ProposalData> {
	const { slug } = params;

	// Security: prevent directory traversal
	if (slug.includes('..')) {
		throw error(400, 'Invalid path');
	}

	// Must be a REP file
	if (!slug.startsWith('rep-')) {
		throw error(400, 'Only REP proposals can be viewed');
	}

	const proposalPath = join(LAB_ROOT, 'reps', `${slug}.md`);

	try {
		const rawContent = await readFile(proposalPath, 'utf-8');
		const { title, status, created, authors, body } = parseMarkdownMeta(rawContent);

		// Extract ID
		const idMatch = slug.match(/^rep-(\d+)/);
		const id = idMatch?.[1] || '000';

		// Try to load RIP
		let rip: ProposalData['rip'];
		try {
			const ripSlug = slug.replace('rep-', 'rip-');
			const ripPath = join(LAB_ROOT, 'rips', `${ripSlug}.md`);
			const ripRaw = await readFile(ripPath, 'utf-8');
			// Strip RIP frontmatter - start from ## Overview
			const overviewIndex = ripRaw.indexOf('## Overview');
			const ripBody = overviewIndex !== -1 ? ripRaw.slice(overviewIndex) : ripRaw;
			rip = { slug: ripSlug, content: ripBody };
		} catch {
			// No RIP exists
		}

		// Check for experiment
		let experimentSlug: string | undefined;
		try {
			const { readdir } = await import('fs/promises');
			const experimentsDir = join(LAB_ROOT, 'experiments');
			const folders = await readdir(experimentsDir, { withFileTypes: true });
			const expFolder = folders.find(f => f.isDirectory() && f.name.startsWith(`rep-${id}`));
			if (expFolder) {
				experimentSlug = expFolder.name;
			}
		} catch {
			// No experiments
		}

		// Check for findings
		let findingsSlug: string | undefined;
		try {
			const { readdir } = await import('fs/promises');
			const resultsDir = join(LAB_ROOT, 'findings');
			const files = await readdir(resultsDir);
			const findingsFile = files.find(f => f.startsWith(`rep-${id}`) && f.endsWith('-findings.md'));
			if (findingsFile) {
				findingsSlug = findingsFile.replace('.md', '');
			}
		} catch {
			// No findings
		}

		return {
			slug,
			id,
			title,
			status,
			created,
			authors,
			content: body,
			rip,
			experimentSlug,
			findingsSlug
		};
	} catch (e) {
		throw error(404, 'Proposal not found');
	}
}
