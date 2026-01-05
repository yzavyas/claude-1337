import type { PageLoad } from './$types';

// Read from canonical marketplace.json (single source of truth)
import marketplaceJson from '../../../../../../../.claude-plugin/marketplace.json';

export const load: PageLoad = () => {
	// Transform marketplace plugins - components field is declarative in marketplace.json
	const plugins = marketplaceJson.plugins.map((plugin) => ({
		name: plugin.name,
		description: plugin.description,
		keywords: plugin.keywords || [],
		components: plugin.components || ['skills']
	}));

	return {
		plugins,
		marketplaceName: marketplaceJson.name,
		version: marketplaceJson.metadata?.version || '0.0.0'
	};
};
