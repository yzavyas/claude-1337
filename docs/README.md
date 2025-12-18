# claude-1337 docs

Documentation site for the claude-1337 marketplace.

## Development

```bash
cd docs
bun install
bun run dev
```

Site runs at `http://localhost:4321/claude-1337/`

## Structure

```
docs/src/pages/
├── index.astro          # Landing page
├── concepts.astro       # How the plugin system works
├── explanation.astro    # Why skills don't activate + fix
├── how-to.astro         # Installation and usage
└── reference/           # Per-plugin documentation
    ├── terminal-1337.astro
    ├── rust-1337.astro
    └── ...
```

## Diataxis Framework

Documentation follows [Diataxis](https://diataxis.fr/):

| Type | Purpose | Pages |
|------|---------|-------|
| Tutorial | Learning | (future) |
| How-to | Task completion | how-to.astro |
| Explanation | Understanding | explanation.astro, concepts.astro |
| Reference | Information | reference/*.astro |

## Building

```bash
bun run build
```

Output goes to `dist/`. Deploy as static site.

## Styling

Minimal CSS in `src/styles/global.css`. Terminal-inspired aesthetic.
