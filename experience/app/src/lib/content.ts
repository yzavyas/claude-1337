// Content loader for experience/content/ markdown files
// Single source of truth - all content lives in experience/content/

// Import all markdown files as raw strings
// Path: src/lib/ -> ../../ -> app/ -> ../ -> experience/ -> content/
const modules = import.meta.glob('../../../content/**/*.md', {
  eager: true,
  query: '?raw',
  import: 'default'
}) as Record<string, string>;

/**
 * Get content by slug
 * @param slug - Path relative to content/, e.g. 'explore/reference/core-1337'
 * @returns Raw markdown string or undefined
 */
export function getContent(slug: string): string | undefined {
  // Normalize slug (remove leading/trailing slashes)
  const normalizedSlug = slug.replace(/^\/+|\/+$/g, '');

  // Try index.md first (for directories), then direct .md
  const indexPath = `../../../content/${normalizedSlug}/index.md`;
  const directPath = `../../../content/${normalizedSlug}.md`;

  return modules[indexPath] || modules[directPath];
}

/**
 * Get all content with slugs
 * @returns Array of { slug, content } objects
 */
export function getAllContent(): Array<{ slug: string; content: string }> {
  return Object.entries(modules).map(([path, content]) => {
    // Convert path to slug
    // ../../../content/explore/reference/core-1337/index.md -> explore/reference/core-1337
    const slug = path
      .replace('../../../content/', '')
      .replace('/index.md', '')
      .replace('.md', '');

    return { slug, content };
  });
}

/**
 * Get content tree for navigation
 * @param basePath - Base path to filter, e.g. 'explore/reference'
 * @returns Filtered content entries
 */
export function getContentTree(basePath: string): Array<{ slug: string; content: string }> {
  return getAllContent().filter(({ slug }) => slug.startsWith(basePath));
}

export interface NavItem {
  href: string;
  label: string;
  slug: string;
}

/**
 * Build navigation items from content tree
 * @param section - Section path, e.g. 'explore/reference'
 * @param baseUrl - Base URL for links, e.g. '/explore/reference'
 * @returns Array of nav items for direct children (not nested)
 */
export function buildNavItems(section: string, baseUrl: string): NavItem[] {
  const tree = getContentTree(section);
  const items: NavItem[] = [];
  const seen = new Set<string>();

  for (const { slug } of tree) {
    // Get the path relative to section
    // e.g., 'explore/reference/core-1337' -> 'core-1337'
    const relativePath = slug.replace(`${section}/`, '');

    // Get first segment (direct child only)
    const firstSegment = relativePath.split('/')[0];

    // Skip if we've seen this, or if it's the section index itself
    if (!firstSegment || seen.has(firstSegment)) continue;
    seen.add(firstSegment);

    items.push({
      href: `${baseUrl}/${firstSegment}/`,
      label: firstSegment,
      slug: `${section}/${firstSegment}`
    });
  }

  // Sort alphabetically, but put 'index' first if present
  return items.sort((a, b) => {
    if (a.label === 'index') return -1;
    if (b.label === 'index') return 1;
    return a.label.localeCompare(b.label);
  });
}
