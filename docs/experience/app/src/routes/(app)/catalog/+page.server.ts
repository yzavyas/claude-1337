import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

const PLUGINS_ROOT = join(process.cwd(), '../../../plugins');
const MARKETPLACE_PATH = join(process.cwd(), '../../../.claude-plugin/marketplace.json');
const GITHUB_BASE = 'https://github.com/yzavyas/claude-1337/tree/main/plugins';

interface PluginInfo {
	name: string;
	displayName: string;
	description: string;
	category: string;
	sourceUrl: string;
}

// Pre-render all plugins at build time
export async function entries() {
	return [{}]; // Single catalog page
}

function parseReadme(content: string): { displayName: string; description: string } {
	const lines = content.split('\n');

	// First line is title: # plugin-name or # Display Name
	const titleLine = lines.find(l => l.startsWith('# '));
	const rawTitle = titleLine?.replace(/^#\s*/, '').trim() || 'Unknown';

	// Convert slug-case to Title Case for display
	const displayName = rawTitle
		.replace(/-1337$/, '') // Remove -1337 suffix
		.replace(/-/g, ' ')
		.replace(/\b\w/g, l => l.toUpperCase());

	// First paragraph after title is the description
	let description = '';
	let foundTitle = false;
	for (const line of lines) {
		if (line.startsWith('# ')) {
			foundTitle = true;
			continue;
		}
		if (foundTitle && line.trim() && !line.startsWith('#')) {
			description = line.trim();
			break;
		}
	}

	return { displayName, description: description || 'No description available' };
}

function inferCategory(name: string, readme: string): string {
	const lowerReadme = readme.toLowerCase();

	// Name-based checks first (most specific)
	if (name.includes('rust')) return 'language';
	if (name.includes('kotlin')) return 'language';
	if (name.includes('jvm')) return 'tooling';
	if (name.includes('terminal')) return 'tooling';
	if (name.includes('eval')) return 'testing';
	if (name.includes('visuals')) return 'visuals';
	if (name.includes('sensei')) return 'documentation';
	if (name.includes('experience')) return 'frontend';
	if (name.includes('extension-builder') || name.includes('builder')) return 'meta';
	if (name.includes('arch-guild')) return 'meta';
	if (name.includes('core')) return 'foundation';

	// Content-based fallbacks
	if (lowerReadme.includes('image generation') || lowerReadme.includes('video generation')) return 'visuals';
	if (lowerReadme.includes('documentation') || lowerReadme.includes('tutorial')) return 'documentation';
	if (lowerReadme.includes('frontend') || lowerReadme.includes('animation')) return 'frontend';

	return 'other';
}

export async function load(): Promise<{ plugins: PluginInfo[] }> {
	const plugins: PluginInfo[] = [];

	try {
		// Read marketplace for plugin registry
		const marketplaceContent = await readFile(MARKETPLACE_PATH, 'utf-8');
		const marketplace = JSON.parse(marketplaceContent);
		const registeredPlugins = new Map(
			marketplace.plugins.map((p: { name: string; description?: string }) => [p.name, p])
		);

		// Read plugin directories
		const dirs = await readdir(PLUGINS_ROOT, { withFileTypes: true });

		for (const dir of dirs) {
			if (!dir.isDirectory()) continue;

			const pluginName = dir.name;
			const readmePath = join(PLUGINS_ROOT, pluginName, 'README.md');

			try {
				const readme = await readFile(readmePath, 'utf-8');
				const { displayName, description } = parseReadme(readme);
				const category = inferCategory(pluginName, readme);

				// Only include plugins registered in marketplace
				if (registeredPlugins.has(pluginName)) {
					plugins.push({
						name: pluginName,
						displayName,
						description,
						category,
						sourceUrl: `${GITHUB_BASE}/${pluginName}`
					});
				}
			} catch {
				// No README, use marketplace info if available
				const registered = registeredPlugins.get(pluginName);
				if (registered) {
					plugins.push({
						name: pluginName,
						displayName: pluginName.replace(/-1337$/, '').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
						description: (registered as { description?: string }).description || 'No description available',
						category: inferCategory(pluginName, ''),
						sourceUrl: `${GITHUB_BASE}/${pluginName}`
					});
				}
			}
		}

		// Sort by category then name
		plugins.sort((a, b) => {
			if (a.category !== b.category) return a.category.localeCompare(b.category);
			return a.name.localeCompare(b.name);
		});

	} catch (e) {
		console.error('Failed to load plugins:', e);
	}

	return { plugins };
}
