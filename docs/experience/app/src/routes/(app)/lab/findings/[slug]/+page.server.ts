import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

// Pre-render all findings at build time
export async function entries() {
	try {
		const findingsDir = join(LAB_ROOT, 'findings');
		const files = await readdir(findingsDir);
		return files
			.filter(f => f.startsWith('rep-') && f.endsWith('-findings.md'))
			.map(f => ({ slug: f.replace('.md', '') }));
	} catch {
		return [];
	}
}

interface ChartDataPoint {
	strategy: string;
	passRate: number;
	tokens: number;
}

interface FindingsData {
	slug: string;
	repId: string;
	title: string;
	date: string;
	status: string;
	content: string;
	proposalSlug?: string;
	experimentSlug?: string;
	chartData?: ChartDataPoint[];
}

function parseMarkdownMeta(content: string): {
	title: string;
	date: string;
	status: string;
	body: string;
	chartData?: ChartDataPoint[];
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

	// Extract chart data from markdown tables (REP-001 format)
	// Looking for: | Strategy | Pass Rate | Problems | Avg Tokens |
	let chartData: ChartDataPoint[] | undefined;
	const tableMatch = content.match(/\| Strategy \| Pass Rate \| Problems \| Avg Tokens \|[\s\S]*?\n\n/);
	if (tableMatch) {
		const rows = tableMatch[0].split('\n').filter(line =>
			line.startsWith('|') && !line.includes('---') && !line.includes('Strategy')
		);
		chartData = rows.map(row => {
			const cells = row.split('|').map(c => c.trim()).filter(Boolean);
			// Parse: Single-shot | **86.6%** | 142/164 | 232
			const strategy = cells[0]?.replace(/\*\*/g, '') || '';
			const passRateStr = cells[1]?.replace(/[*%]/g, '') || '0';
			const tokensStr = cells[3]?.replace(/,/g, '') || '0';
			return {
				strategy,
				passRate: parseFloat(passRateStr),
				tokens: parseInt(tokensStr, 10)
			};
		}).filter(d => d.strategy && !isNaN(d.passRate));
	}

	return { title, date, status, body, chartData };
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
		const { title, date, status, body, chartData } = parseMarkdownMeta(rawContent);

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
			experimentSlug,
			chartData
		};
	} catch (e) {
		throw error(404, 'Findings not found');
	}
}
