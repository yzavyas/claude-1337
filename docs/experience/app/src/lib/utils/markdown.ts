/**
 * Markdown Rendering with Shiki Syntax Highlighting
 *
 * VS Code-quality code highlighting for dynamic markdown content.
 * Shiki is lazily loaded to avoid bundle bloat.
 */
import { marked } from 'marked';
import type { Highlighter } from 'shiki';

let highlighter: Highlighter | null = null;

/**
 * Get or create the Shiki highlighter instance
 * Lazy-loaded to defer the ~40KB cost
 */
async function getHighlighter(): Promise<Highlighter> {
	if (!highlighter) {
		const { createHighlighter } = await import('shiki');
		highlighter = await createHighlighter({
			themes: ['github-light', 'github-dark'],
			langs: [
				'javascript',
				'typescript',
				'svelte',
				'python',
				'bash',
				'json',
				'yaml',
				'markdown',
				'rust',
				'go',
				'css',
				'html'
			]
		});
	}
	return highlighter;
}

/**
 * Render markdown content with syntax highlighting
 *
 * @param content - Raw markdown string
 * @param theme - Shiki theme to use (default: github-light for craft aesthetic)
 * @returns HTML string
 */
export async function renderMarkdown(content: string, theme = 'github-light'): Promise<string> {
	const hl = await getHighlighter();

	const renderer = new marked.Renderer();

	renderer.code = ({ text, lang }) => {
		const language = lang || 'text';
		try {
			return hl.codeToHtml(text, {
				lang: language,
				theme: theme
			});
		} catch {
			// Fallback for unsupported languages
			return `<pre><code class="language-${language}">${escapeHtml(text)}</code></pre>`;
		}
	};

	marked.use({ renderer });

	return marked(content) as string;
}

/**
 * Render markdown without syntax highlighting (faster, smaller)
 * Use for content that doesn't have code blocks
 */
export function renderMarkdownSimple(content: string): string {
	return marked(content) as string;
}

/**
 * Escape HTML entities
 */
function escapeHtml(text: string): string {
	return text
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#39;');
}

/**
 * Load and render a markdown file from a URL
 *
 * @param fetch - Fetch function (from +page.ts load)
 * @param path - Path to markdown file
 * @returns Rendered HTML string
 */
export async function loadMarkdown(
	fetch: typeof globalThis.fetch,
	path: string
): Promise<string> {
	const res = await fetch(path);
	if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
	const content = await res.text();
	return renderMarkdown(content);
}
