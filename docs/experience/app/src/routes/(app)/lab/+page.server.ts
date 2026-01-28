import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

interface ResearchPaper {
	id: string;
	slug: string;
	title: string;
	summary: string;  // Hypothesis from ## Summary
	keywords: string[];
	date: string;
	status: 'published' | 'in-progress' | 'draft';
	hypothesis?: string;  // The research question
	findingsHtml?: string;  // Rendered findings section for dialog
	findingsRaw?: string;   // Raw markdown of findings section
	links: {
		rep: string;  // Single source of truth - the REP
		experiment?: string;
	};
}

interface Frontmatter {
	tags?: string[];
	keywords?: string[];
}

function parseFrontmatter(content: string): { frontmatter: Frontmatter; body: string } {
	const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
	if (!match) {
		return { frontmatter: {}, body: content };
	}

	const yamlStr = match[1];
	const body = match[2];
	const frontmatter: Frontmatter = {};

	for (const line of yamlStr.split('\n')) {
		const colonIdx = line.indexOf(':');
		if (colonIdx === -1) continue;

		const key = line.slice(0, colonIdx).trim();
		let value = line.slice(colonIdx + 1).trim();

		if (key === 'tags' || key === 'keywords') {
			value = value.replace(/^\[|\]$/g, '');
			frontmatter[key] = value.split(',').map(t => t.trim()).filter(Boolean);
		}
	}

	return { frontmatter, body };
}

function extractSection(content: string, sectionName: string): string | undefined {
	// Match ## Section Name followed by content until next ## or ---
	const regex = new RegExp(`## ${sectionName}[^\\n]*\\n\\n([\\s\\S]*?)(?=\\n---\\n|\\n## |$)`, 'i');
	const match = content.match(regex);
	return match?.[1]?.trim();
}

function extractKeywords(content: string): string[] {
	const { frontmatter } = parseFrontmatter(content);
	return frontmatter.tags || frontmatter.keywords || [];
}

async function loadREPs(): Promise<ResearchPaper[]> {
	const papers: ResearchPaper[] = [];

	try {
		const repsDir = join(LAB_ROOT, 'reps');
		const files = await readdir(repsDir);
		const repFiles = files.filter(f => f.startsWith('rep-') && f.endsWith('.md'));

		for (const file of repFiles) {
			const content = await readFile(join(repsDir, file), 'utf-8');
			const { body } = parseFrontmatter(content);

			const idMatch = file.match(/^rep-(\d+)/);
			const id = idMatch?.[1] || '000';

			// Extract title
			const titleMatch = body.match(/^#\s+(.+?)(?:\n|$)/m);
			const title = titleMatch?.[1]?.replace(/^REP-\d+:?\s*/i, '') || 'Untitled';

			// Extract status
			const statusMatch = body.match(/\*\*Status\*\*:\s*(\w+)/i);
			const rawStatus = statusMatch?.[1]?.toLowerCase() || 'draft';

			// Map status to our categories
			let status: ResearchPaper['status'];
			if (['implemented', 'interim'].includes(rawStatus)) {
				status = 'published';
			} else if (['discussion', 'fcp', 'accepted'].includes(rawStatus)) {
				status = 'in-progress';
			} else {
				status = 'draft';
			}

			// Skip rejected/postponed
			if (['rejected', 'postponed'].includes(rawStatus)) continue;

			// Extract dates
			const createdMatch = body.match(/\*\*Created\*\*:\s*(.+)/i);
			const updatedMatch = body.match(/\*\*Updated\*\*:\s*(.+)/i);
			const publishedMatch = body.match(/\*\*Published\*\*:\s*(.+)/i);
			const date = updatedMatch?.[1] || publishedMatch?.[1] || createdMatch?.[1] || '';

			// Extract summary (hypothesis)
			const summary = extractSection(body, 'Summary') || '';

			// Extract findings section if it exists
			const findingsRaw = extractSection(body, 'Findings(?:\\s*\\(Interim\\))?');

			// Extract the research question/hypothesis
			const questionSection = extractSection(body, 'The Question');
			const hypothesis = questionSection?.match(/>\s*(.+)/)?.[1] || summary.split('.')[0];

			papers.push({
				id,
				slug: file.replace('.md', ''),
				title,
				summary: summary.split('\n')[0] || '', // First paragraph
				keywords: extractKeywords(content),
				date,
				status,
				hypothesis,
				findingsRaw,
				links: {
					rep: `/lab/reps/${file.replace('.md', '')}`,
					experiment: `/lab/experiments/rep-${id}`
				}
			});
		}
	} catch (e) {
		console.error('Failed to load REPs:', e);
	}

	return papers;
}

export async function load() {
	const papers = await loadREPs();

	// Sort: published first, then by date
	papers.sort((a, b) => {
		if (a.status === 'published' && b.status !== 'published') return -1;
		if (b.status === 'published' && a.status !== 'published') return 1;
		return b.date.localeCompare(a.date);
	});

	// Extract all unique keywords for filtering
	const allKeywords = [...new Set(papers.flatMap(p => p.keywords))].sort();

	return { papers, allKeywords };
}
