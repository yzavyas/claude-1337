import { readdir, readFile, stat } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

const LAB_ROOT = join(process.cwd(), '../../../lab-1337');

// Pre-render all experiments at build time
export async function entries() {
	try {
		const expDir = join(LAB_ROOT, 'experiments');
		const items = await readdir(expDir, { withFileTypes: true });
		return items
			.filter(d => d.isDirectory())
			.map(d => ({ slug: d.name }));
	} catch {
		return [];
	}
}

interface ExperimentResult {
	name: string;
	model: string;
	timestamp: string;
	summary: {
		singleShot: { total: number; passed: number; passRate: number; avgTokens: number };
		ralphStyle: { total: number; passed: number; passRate: number; avgTokens: number };
	};
	hasAnalysis: boolean;
	analysisPath?: string;
}

interface ExperimentData {
	slug: string;
	name: string;
	repId?: string;
	readme?: string;
	results: ExperimentResult[];
}

export async function load({ params }): Promise<ExperimentData> {
	const { slug } = params;

	// Security
	if (slug.includes('..')) {
		throw error(400, 'Invalid path');
	}

	const expPath = join(LAB_ROOT, 'experiments', slug);

	try {
		// Check if directory exists
		const stats = await stat(expPath);
		if (!stats.isDirectory()) {
			throw error(404, 'Experiment not found');
		}

		// Check for REP linkage
		const repMatch = slug.match(/^rep-(\d+)/);
		const repId = repMatch?.[1];

		// Try to read README
		let readme: string | undefined;
		try {
			readme = await readFile(join(expPath, 'README.md'), 'utf-8');
		} catch {
			// No README
		}

		// Load results
		const files = await readdir(expPath);
		const resultFiles = files.filter(f => f.startsWith('results-') && f.endsWith('.json'));
		const results: ExperimentResult[] = [];

		for (const resultFile of resultFiles) {
			try {
				const content = await readFile(join(expPath, resultFile), 'utf-8');
				const data = JSON.parse(content);

				const analysisFile = resultFile.replace('.json', '-analysis.md');
				const hasAnalysis = files.includes(analysisFile);

				results.push({
					name: resultFile.replace('.json', ''),
					model: data.model || 'unknown',
					timestamp: data.timestamp || '',
					summary: {
						singleShot: {
							total: data.summary?.['single-shot']?.total || 0,
							passed: data.summary?.['single-shot']?.passed || 0,
							passRate: data.summary?.['single-shot']?.pass_rate || 0,
							avgTokens: data.summary?.['single-shot']?.avg_tokens || 0
						},
						ralphStyle: {
							total: data.summary?.['ralph-style']?.total || 0,
							passed: data.summary?.['ralph-style']?.passed || 0,
							passRate: data.summary?.['ralph-style']?.pass_rate || 0,
							avgTokens: data.summary?.['ralph-style']?.avg_tokens || 0
						}
					},
					hasAnalysis,
					analysisPath: hasAnalysis ? `/lab/experiments/${slug}/${analysisFile}` : undefined
				});
			} catch {
				// Skip invalid JSON
			}
		}

		// Sort by timestamp descending
		results.sort((a, b) => b.timestamp.localeCompare(a.timestamp));

		return {
			slug,
			name: slug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
			repId,
			readme,
			results
		};
	} catch (e) {
		if ((e as { status?: number }).status) throw e;
		throw error(404, 'Experiment not found');
	}
}
