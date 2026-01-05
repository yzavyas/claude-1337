# Contributing

Curated skills for Claude Code. Production patterns, decision frameworks.

## Before You Start

1. Read **CLAUDE.md** — architecture, conventions, skill authoring rules
2. Load the extension builder skill — methodology for creating extensions
3. Check the [catalog](experience/content/explore/reference/catalog/) for existing plugins to update

## Adding a Skill

```
plugins/your-skill/
├── SKILL.md           # Required: decisions + gotchas (< 500 lines)
└── references/        # Optional: domain-specific deep dives
```

Update `marketplace.json`:
```json
{
  "name": "your-skill",
  "source": "./plugins/your-skill",
  "description": "What + Use when: triggers (max 600 chars)",
  "version": "0.1.0",
  "skills": ["./"]
}
```

## Quality Standards

| Do | Don't |
|----|-------|
| Fill gaps (what Claude doesn't know) | Teach basics |
| Cite evidence (production usage) | State opinions |
| Decision frameworks + gotchas | Complete tutorials |
| Tables and trees | Verbose prose |

## Checklist

- [ ] Description < 600 chars with "Use when:" triggers
- [ ] SKILL.md is decisions, not tutorial (< 500 lines)
- [ ] Each recommendation has evidence
- [ ] Claims traceable to source
- [ ] References linked, not embedded

## Commit Format

```
Add/Update [skill]: [brief description]

[Evidence or reasoning]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Auto-Updates

Skills auto-update monthly via GitHub Action. For manual updates:
1. Run `/skill-update` command
2. Research current state
3. Update only with evidence
4. Create PR for review

## License

MIT. By contributing, you agree your contributions will be licensed under MIT.
