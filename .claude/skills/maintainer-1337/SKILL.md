---
name: maintainer-1337
description: "Maintain the claude-1337 marketplace. Use when: updating skills, checking skill health, validating marketplace.json, adding new plugins, or running periodic updates on this repository."
---

# claude-1337 Maintainer

Maintain and update the claude-1337 marketplace.

**Composes with**:
- `example-skills:skill-creator` - skill fundamentals, anatomy, packaging
- `1337-skill-creator` - opinionated content layer (picks winners, evidence-based)

## Repository Structure

```
claude-1337/
├── .claude-plugin/
│   └── marketplace.json     # Plugin registry
├── .claude/
│   ├── commands/            # Repo-local commands
│   │   ├── skill-check.md
│   │   └── skill-update.md
│   └── skills/              # Repo-local skills
│       └── maintainer-1337/ # This skill
├── plugins/                 # Public plugins
│   ├── terminal-1337/
│   ├── rust-1337/
│   └── 1337-skill-creator/
└── .github/workflows/
    └── update-skills.yml    # Weekly auto-update
```

## Skill Health Check

Run `/skill-check` or manually verify:

1. **Check `<available_skills>`**:
   - "How many skills in your `<available_skills>` block?"
   - Any truncated or showing ">-"?

2. **Validate SKILL.md files**:
   - `name` < 50 chars
   - `description` < 600 chars, quoted string
   - Line count ~100-200 (max 350)

3. **Check references**:
   - All linked files exist
   - No broken links

## Skill Update Workflow

Run `/skill-update` or manually:

1. **Research**: Web search for deprecations, new releases, production usage
2. **Validate**: Is "best-in-class" still best? Any new contenders?
3. **Update**: Only with evidence (production usage > GitHub stars)
4. **Commit**:
   ```
   Update [skill]: [brief description]

   [Evidence]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

## Adding a New Plugin

1. **Load skills**: `example-skills:skill-creator` then `1337-skill-creator`
2. Create `plugins/new-plugin/SKILL.md` following skill-creator guidelines
3. Add to `marketplace.json`:
   ```json
   {
     "name": "new-plugin",
     "source": "./plugins/new-plugin",
     "description": "Brief description with triggers",
     "version": "0.1.0",
     "skills": ["./"]
   }
   ```
4. Run `/skill-check` to validate

## Quality Standards

- **Best-in-class only** - THE answer, not catalogs
- **Evidence over opinion** - Production usage matters
- **Concise** - Decision trees + gotchas, not tutorials
- **Description < 600 chars** with "Use when:" triggers
- **SKILL.md 100-200 lines** (max 350)
- **Quoted strings** in YAML (not `>-`)

## Update Schedule

- **rust-1337**: Check quarterly (Rust moves fast)
- **terminal-1337**: Check semi-annually
- **GitHub Action**: Runs monthly (1st at 2am UTC)
