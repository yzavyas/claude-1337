import marketplace from '../../../../../../.claude-plugin/marketplace.json';
import metadata from '../../../../../../.claude-plugin/metadata.json';

const GITHUB_BASE = 'https://github.com/yzavyas/claude-1337/tree/main';

export function load() {
	const plugins = marketplace.plugins.map(p => ({
		name: p.name,
		description: p.description,
		displayName: metadata[p.name as keyof typeof metadata]?.displayName ?? p.name,
		category: metadata[p.name as keyof typeof metadata]?.category ?? 'other',
		sourceUrl: `${GITHUB_BASE}/${p.source.replace('./', '')}`
	}));

	return { plugins };
}
