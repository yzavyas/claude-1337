import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

interface ResearchPaper {
	id: string;
	slug: string;
	title: string;
	subtitle?: string;
	summary: string;
	keywords: string[];
	date: string;
	status: 'published' | 'in-progress' | 'draft';
	type: 'finding' | 'proposal';
	metrics?: {
		key: string;
		value: string;
		highlight?: boolean;
	}[];
	links: {
		proposal?: string;
		experiment?: string;
		findings?: string;
	};
}

function extractKeywords(content: string): string[] {
	const keywords: string[] = [];
	const lower = content.toLowerCase();

	// Core themes
	if (lower.includes('methodology') || lower.includes('framework')) {
		keywords.push('methodology');
	}
	if (lower.includes('measure') || lower.includes('signal') || lower.includes('data')) {
		keywords.push('measurement');
	}
	if (lower.includes('evidence') || lower.includes('empirical') || lower.includes('rigorous')) {
		keywords.push('evidence');
	}

	// Methodology patterns
	if (lower.includes('iteration') || lower.includes('ralph') || lower.includes('multiple passes')) {
		keywords.push('iteration');
	}
	if (lower.includes('single-shot') || lower.includes('single shot') || lower.includes('one attempt')) {
		keywords.push('single-shot');
	}

	// Analysis concepts
	if (lower.includes('ceiling effect') || lower.includes('task difficulty') || lower.includes('harder tasks')) {
		keywords.push('task-design');
	}
	if (lower.includes('token') || lower.includes('cost') || lower.includes('resource')) {
		keywords.push('efficiency');
	}
	if (lower.includes('reproducib') || lower.includes('reliable') || lower.includes('consistent')) {
		keywords.push('reproducibility');
	}

	// Specific benchmarks/prior art
	if (lower.includes('humaneval') || lower.includes('swe-bench') || lower.includes('benchmark')) {
		keywords.push('benchmark');
	}

	return [...new Set(keywords)]; // Dedupe
}

function extractMetrics(content: string): ResearchPaper['metrics'] {
	const metrics: ResearchPaper['metrics'] = [];

	// Try to extract key findings
	const successMatch = content.match(/(\d+)%.*success/i);
	if (successMatch) {
		metrics.push({ key: 'Success Rate', value: successMatch[1] + '%', highlight: true });
	}

	const tokenMatch = content.match(/~?(\d+)x?\s*tokens/i);
	if (tokenMatch) {
		metrics.push({ key: 'Token Cost', value: tokenMatch[1] + 'x' });
	}

	return metrics;
}

async function loadPublishedFindings(): Promise<ResearchPaper[]> {
	const papers: ResearchPaper[] = [];

	try {
		const resultsDir = join(LAB_ROOT, 'findings');
		const proposalsDir = join(LAB_ROOT, 'reps');
		const files = await readdir(resultsDir);
		const findingFiles = files.filter(f => f.startsWith('rep-') && f.endsWith('-findings.md'));

		// Get proposal files for linking
		const proposalFiles = await readdir(proposalsDir).catch(() => [] as string[]);

		for (const file of findingFiles) {
			const content = await readFile(join(resultsDir, file), 'utf-8');

			// Parse metadata
			const titleMatch = content.match(/^#\s+(.+?)(?:\n|$)/m);
			const title = titleMatch?.[1]?.replace(/^LEP-\d+\s*(?:Findings)?:?\s*/i, '') || 'Untitled';

			const subtitleMatch = content.match(/^\((.+?)\)$/m);
			const subtitle = subtitleMatch?.[1];

			const dateMatch = content.match(/\*\*Date\*\*:\s*(.+)/i);
			const date = dateMatch?.[1] || '';

			const summaryMatch = content.match(/\*\*Primary finding\*\*:\s*(.+)/i);
			const summary = summaryMatch?.[1] || content.match(/##\s+Summary\n\n([^\n]+)/)?.[1] || '';

			const idMatch = file.match(/^rep-(\d+)/);
			const id = idMatch?.[1] || '000';

			// Find matching proposal file
			const proposalFile = proposalFiles.find(f => f.startsWith(`rep-${id}`) && f.endsWith('.md'));
			const proposalSlug = proposalFile ? proposalFile.replace('.md', '') : undefined;

			papers.push({
				id,
				slug: file.replace('.md', ''),
				title,
				subtitle,
				summary: summary.replace(/\*\*/g, ''),
				keywords: extractKeywords(content),
				date,
				status: 'published',
				type: 'finding',
				metrics: extractMetrics(content),
				links: {
					proposal: proposalSlug ? `/lab/proposals/${proposalSlug}` : undefined,
					findings: `/lab/findings/${file.replace('.md', '')}`
				}
			});
		}
	} catch (e) {
		console.error('Failed to load findings:', e);
	}

	return papers;
}

async function loadActiveProposals(): Promise<ResearchPaper[]> {
	const papers: ResearchPaper[] = [];

	try {
		const proposalsDir = join(LAB_ROOT, 'reps');
		const files = await readdir(proposalsDir);
		const lepFiles = files.filter(f => f.startsWith('rep-') && f.endsWith('.md'));

		// Check what findings exist (to exclude already published)
		const resultsDir = join(LAB_ROOT, 'findings');
		const resultFiles = await readdir(resultsDir).catch(() => []);
		const publishedIds = new Set(
			resultFiles
				.filter(f => f.endsWith('-findings.md'))
				.map(f => f.match(/^rep-(\d+)/)?.[1])
				.filter(Boolean)
		);

		for (const file of lepFiles) {
			const content = await readFile(join(proposalsDir, file), 'utf-8');

			const idMatch = file.match(/^rep-(\d+)/);
			const id = idMatch?.[1] || '000';

			// Skip if already has published findings
			if (publishedIds.has(id)) continue;

			const statusMatch = content.match(/\*\*Status\*\*:\s*(\w+)/i);
			const status = statusMatch?.[1]?.toLowerCase() || 'draft';

			// Only show active proposals (not implemented/rejected/postponed)
			if (['implemented', 'rejected', 'postponed'].includes(status)) continue;

			const titleMatch = content.match(/^#\s+(.+?)(?:\n|$)/m);
			const title = titleMatch?.[1]?.replace(/^LEP-\d+:?\s*/i, '') || 'Untitled';

			const summaryMatch = content.match(/##\s+Summary\n\n([^\n]+)/);
			const summary = summaryMatch?.[1] || '';

			const dateMatch = content.match(/\*\*Created\*\*:\s*(.+)/i);
			const date = dateMatch?.[1] || '';

			papers.push({
				id,
				slug: file.replace('.md', ''),
				title,
				summary,
				keywords: extractKeywords(content),
				date,
				status: status === 'fcp' ? 'in-progress' : 'draft',
				type: 'proposal',
				links: {
					proposal: `/lab/proposals/${file.replace('.md', '')}`
				}
			});
		}
	} catch (e) {
		console.error('Failed to load proposals:', e);
	}

	return papers;
}

export async function load() {
	const [findings, proposals] = await Promise.all([
		loadPublishedFindings(),
		loadActiveProposals()
	]);

	// Combine and sort - published first, then by date
	const papers = [...findings, ...proposals].sort((a, b) => {
		if (a.status === 'published' && b.status !== 'published') return -1;
		if (b.status === 'published' && a.status !== 'published') return 1;
		return b.date.localeCompare(a.date);
	});

	// Extract all unique keywords for filtering
	const allKeywords = [...new Set(papers.flatMap(p => p.keywords))].sort();

	return { papers, allKeywords };
}
