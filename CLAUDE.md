# Claude Code Marketplace: claude-1337

You are working on **claude-1337**, a community-contributed Claude Code marketplace focused on elite developer tools and best-in-class workflows.

## Project Identity

**Mission**: Provide Claude Code with opinionated, best-in-class tooling knowledge. Not catalogs of options - THE answer for each use case.

**Philosophy**: Evidence over opinion. What elite teams actually use in production. Auto-updated to stay current.

**Standards**: This is a serious community contribution. No marketing speak, no cringe content. Code and documentation must be production-ready.

## Repository Structure

```
claude-1337/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace definition (strict: false)
├── plugins/
│   ├── terminal-1337/         # Elite terminal tools
│   │   └── skills/
│   │       ├── SKILL.md
│   │       ├── references/    # 8 tools: rg, fd, bat, eza, fzf, xh, jq, atuin
│   │       └── scripts/       # Install scripts
│   └── rust-1337/             # Elite Rust development
│       ├── SKILL.md           # Core patterns, decision frameworks
│       └── references/        # 8 domains: async, networking, wasm, embedded, ffi, proc-macros, ecosystem, tooling
├── docs/
└── scripts/
```

## Architecture Principles

### Marketplace Structure
- **strict: false** - marketplace.json IS the complete plugin manifest
- **Progressive disclosure** - Metadata always loaded → SKILL.md when triggered → references/scripts/assets on-demand
- **Plugin-based organization** - Each plugin can contain commands, agents, hooks, and skills
- **source field** points to plugin directory: `./plugins/terminal-1337`
- **skills array** points to directories containing SKILL.md files

### Current Plugins

**terminal-1337**: 8 elite terminal tools (rg, fd, bat, eza, fzf, xh, jq, atuin)
- Reference docs + install scripts for each tool
- Focus: tools Claude Code can use directly

**rust-1337**: Elite Rust development patterns
- Core: Decision frameworks, production gotchas, type design
- App types: cli, backend, frontend, native
- Infrastructure: data-plane, networking, embedded
- Meta: async, ffi, proc-macros, ecosystem, tooling
- Focus: Best-in-class choices, not catalogs

### Content Philosophy

**Include**: The best tool/crate/pattern for each use case with evidence
**Exclude**:
- Catalogs of alternatives (pick THE answer)
- Not-production-ready options
- Tools Claude can't use (human-facing TUIs, AI assistants)

### Skill Authoring Rules

**From official spec + community research (see Key Documentation):**

1. **Description is THE trigger mechanism**
   - Max ~600 chars (name max ~50 chars)
   - Formula: `[What it does] + [Use when: specific triggers]`
   - Front-load keywords Claude will match against
   - Only frontmatter (~100 tokens) loaded per skill at startup

2. **SKILL.md should be lean** - 100-200 lines ideal
   - Keep decision frameworks and gotchas
   - Move deep content to references/ (loaded on-demand)

3. **`<available_skills>` budget** - ~20-22k chars total
   - 34-36 skills fit before truncation (depends on description size)
   - Truncated skills DON'T TRIGGER - Claude can't see them
   - Test: "How many skills are in your `<available_skills>` block?"

4. **YAML multiline bug** - `>-`, `|`, `|-` parse as literal ">-"
   - Use quoted strings: `description: "Your description here"`

5. **CLAUDE.md as fallback** - if skills might truncate, add pointers in CLAUDE.md

## Development Workflow

### Making Changes

1. **Branch naming**: `feat/feature-name`, `fix/issue-description`, `docs/what-changed`
2. **Commit messages**: Descriptive, explain WHY not just WHAT
3. **Always include**:
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

### Testing Skills

Before committing skill changes:
1. Validate SKILL.md structure (YAML frontmatter required)
2. Verify all referenced files exist
3. Test install scripts on target platforms
4. Confirm no TODO/placeholder content
5. Check script permissions (must be executable)

### Adding New Plugins

Future plugins should follow the pattern:
```
plugins/
└── new-plugin/
    ├── commands/          # Optional: slash commands
    ├── agents/            # Optional: specialized agents
    ├── hooks/             # Optional: event hooks
    └── skills/            # Optional: skills
        └── skill-name/
            └── SKILL.md
```

Update `marketplace.json`:
```json
{
  "plugins": [
    {
      "name": "new-plugin",
      "source": "./plugins/new-plugin",
      "description": "Brief description",
      "version": "0.1.0",
      "author": {...},
      "keywords": [...],
      "category": "development",
      "strict": false,
      "skills": ["./skills/skill-name"]
    }
  ]
}
```

## Key Documentation

**Official**:
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [Reference Implementation](https://github.com/anthropics/skills)
- [Complex Marketplace Example](https://github.com/wshobson/agents)

**Community Research** (informed our skill authoring rules):
- [Deep Dive: Anatomy of a Skill, Its Tokenomics](https://www.reddit.com/r/ClaudeAI/comments/1pha74t/deep_dive_anatomy_of_a_skill_its_tokenomics_why/) - tokenomics, `<available_skills>` budget (~20-22k chars), truncation behavior
- [CLAUDE.md and Skills Experiment](https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd_and_skills_experiment_whats_the_best_way/) - hybrid approach wins (short summaries + file pointers), embedded costs 30% more for no benefit

## Working with This Repo

### Tool Detection Pattern
```bash
if command -v toolname >/dev/null 2>&1; then
    # Tool available
else
    # Offer installation
fi
```

### Install Script Pattern
```bash
#!/bin/bash
set -e

# OS detection
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# Install based on OS
case $OS in
    macos)
        brew install toolname
        ;;
    linux)
        if command -v apt &> /dev/null; then
            sudo apt install -y toolname
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y toolname
        fi
        ;;
esac

# Verify
if command -v toolname &> /dev/null; then
    echo "✅ toolname installed successfully!"
    toolname --version
fi
```

### Progressive Disclosure in SKILL.md
- Keep SKILL.md focused on behavior and decision logic
- Reference docs contain comprehensive usage details
- Scripts are self-contained and executable
- Assets contain config snippets for user setup

## Code Style

- **No emojis** unless explicitly requested
- **Clear, concise** - avoid marketing language
- **Educational** - explain WHY when making architectural decisions
- **Professional** - this represents the community

## Current Status

**v0.1.0** - Alpha phase
- terminal-1337 skill: Complete with 8 tools
- Marketplace structure: Established and validated
- Documentation: Comprehensive
- Future expansion: Ready for commands/agents/hooks

## Future Roadmap

### Near-term
- Additional skills: 1337-python, 1337-rust (language-specific tooling)
- Slash commands: Quick access patterns (e.g., `/rg`, `/fd`)
- Testing: Validate marketplace loads correctly in Claude Code

### Long-term
- Specialized agents: terminal-optimizer, tool-recommender
- Event hooks: Auto-suggest installations, update notifications
- Community plugins: Accept external contributions

## Automated Skill Updates

Skills are auto-updated via GitHub Action (`.github/workflows/update-skills.yml`).

**Schedule**: Monthly on 1st at 2am UTC

**Manual trigger**: Actions tab → "Update Skills" → Run workflow

### What Claude Checks

| Signal | Action |
|--------|--------|
| Deprecated crate/tool | Find replacement |
| New best-in-class option | Validate production status, update if evidence |
| Major version release | Review for breaking changes |
| Security advisory | Update with mitigation |

### Update Philosophy

- Only change with clear evidence (production usage > GitHub stars)
- Cite sources when making changes
- Create PR for human review - never auto-merge

## Maintainer Notes

**Owner**: yzavyas (yza.vyas@example.com)
**License**: MIT
**Repository**: https://github.com/yzavyas/claude-1337

When working on this project:
1. Maintain high quality standards - this is a community contribution
2. Test changes thoroughly before committing
3. Update documentation when adding features
4. Follow the established patterns and conventions
5. Keep the structure clean and organized
