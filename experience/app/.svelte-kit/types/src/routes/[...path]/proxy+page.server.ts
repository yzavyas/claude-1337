// @ts-nocheck
import type { PageServerLoad, EntryGenerator } from './$types';
import { error } from '@sveltejs/kit';
import { readFile, readdir, stat } from 'fs/promises';
import { join } from 'path';

const CONTENT_DIR = join(process.cwd(), '..', 'content');

// Recursively find all markdown files and return their URL paths
async function findMarkdownFiles(dir: string, basePath: string = ''): Promise<string[]> {
	const dirEntries = await readdir(dir, { withFileTypes: true });
	const paths: string[] = [];

	for (const entry of dirEntries) {
		const fullPath = join(dir, entry.name);
		const relativePath = basePath ? `${basePath}/${entry.name}` : entry.name;

		if (entry.isDirectory()) {
			paths.push(...await findMarkdownFiles(fullPath, relativePath));
		} else if (entry.name.endsWith('.md')) {
			// Convert file path to URL path
			// index.md -> directory path
			// foo.md -> foo
			if (entry.name === 'index.md') {
				if (basePath) paths.push(basePath);
			} else {
				paths.push(relativePath.replace(/\.md$/, ''));
			}
		}
	}

	return paths;
}

// Extract title from markdown content (first # heading)
function extractTitle(content: string): string {
	const match = content.match(/^#\s+(.+)$/m);
	return match ? match[1] : 'Untitled';
}

export const entries: EntryGenerator = async () => {
	const paths = await findMarkdownFiles(CONTENT_DIR);
	// For [...path] rest routes, path should be the full string
	return paths.map(p => ({ path: p }));
};

export const prerender = true;

export const load = async ({ params }: Parameters<PageServerLoad>[0]) => {
	const urlPath = params.path || '';

	// Try to find the markdown file
	// First try: exact path + .md
	// Second try: path + /index.md
	const possiblePaths = [
		join(CONTENT_DIR, urlPath + '.md'),
		join(CONTENT_DIR, urlPath, 'index.md')
	];

	for (const filePath of possiblePaths) {
		try {
			const fileStat = await stat(filePath);
			if (fileStat.isFile()) {
				const content = await readFile(filePath, 'utf-8');
				const title = extractTitle(content);

				// Determine breadcrumb path
				const pathParts = urlPath.split('/').filter(Boolean);

				return {
					title,
					path: urlPath,
					pathParts,
					content
				};
			}
		} catch {
			// File doesn't exist, try next
		}
	}

	error(404, 'Page not found');
};
