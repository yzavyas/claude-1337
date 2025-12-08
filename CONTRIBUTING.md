# Contributing to claude-1337

Thanks for your interest in contributing! This marketplace aims to teach Claude Code elite terminal tools and developer workflows.

## Getting Started

1. **Read CLAUDE.md** - Project steward file with architecture and conventions
2. **Check existing issues** - See if your idea is already being discussed
3. **Open an issue first** - Discuss significant changes before implementing

## What We're Looking For

### New Skills
- Language-specific tooling (Python, Rust, Go, TypeScript, etc.)
- Development workflows (testing, debugging, profiling)
- Elite tools that significantly improve over standard utilities

### Slash Commands
- Quick-access patterns for common operations
- Tool-specific shortcuts
- Workflow automation

### Specialized Agents
- Task-specific automation (e.g., terminal-optimizer)
- Tool recommendation systems
- Configuration management

### Not Interested In
- Human-facing tools (Claude doesn't need TUI interfaces)
- Duplicate functionality of existing plugins
- Tools without clear Claude Code use cases
- Marketing or promotional content

## Standards

This is a **serious community contribution**. We maintain high standards:

- ✅ Production-ready code
- ✅ Comprehensive documentation
- ✅ Clear, professional writing
- ✅ Tested on target platforms
- ❌ No marketing speak
- ❌ No placeholder content
- ❌ No cringe or memes (except the Xzibit quote, that stays)

## Development Process

### 1. Fork and Branch

```bash
git clone https://github.com/yzavyas/claude-1337.git
cd claude-1337
git checkout -b feat/your-feature-name
```

### 2. Make Changes

Follow the established patterns:

**Adding a new skill:**
```
plugins/plugin-name/skills/skill-name/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── references/       # Optional: Comprehensive docs
├── scripts/          # Optional: Install/setup scripts
└── assets/           # Optional: Config snippets
```

**Update marketplace.json:**
```json
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Brief description",
      "version": "0.1.0",
      "author": {
        "name": "your-name",
        "email": "your-email"
      },
      "keywords": ["relevant", "tags"],
      "category": "development",
      "strict": false,
      "skills": ["./skills/skill-name"]
    }
  ]
}
```

### 3. Test Your Changes

- [ ] SKILL.md has valid YAML frontmatter
- [ ] All referenced files exist
- [ ] Scripts are executable (`chmod +x`)
- [ ] Scripts work on macOS and Linux
- [ ] No TODO or placeholder content
- [ ] Documentation is clear and complete

### 4. Commit

Use descriptive commit messages:

```
Add skill-name for [purpose]

- What the skill does
- Why it's useful for Claude Code
- Any important implementation notes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 5. Push and Open PR

```bash
git push origin feat/your-feature-name
```

Open a PR with:
- Clear description of what you're adding
- Why it's valuable for Claude Code users
- Any testing you've done
- Screenshots/examples if applicable

## Code Style

### Documentation
- Clear, concise, professional
- Explain WHY not just WHAT
- Examples for complex concepts
- No marketing language

### Scripts
- OS detection (macOS/Linux)
- Package manager detection
- Error handling with `set -e`
- Verification after installation
- Clear success/failure messages

### SKILL.md Structure
```markdown
---
name: skill-name
description: Brief description (max 1024 chars) explaining when Claude should use this
---

# Skill Name

## Purpose
[What this skill does]

## When to Use
[Situations where Claude should activate this skill]

## Available Tools
[List of tools this skill teaches]

## Tool Detection
[How to check if tools are installed]

## Installation
[How to install missing tools]

## Usage Patterns
[Common usage examples]

## References
[Point to comprehensive docs in references/]
```

## Review Process

1. Maintainer reviews PR for:
   - Adherence to standards
   - Code quality
   - Documentation completeness
   - Test coverage

2. Feedback and iteration
3. Approval and merge

## Questions?

- Open an issue for discussion
- Check CLAUDE.md for architecture details
- Review existing plugins for patterns

## License

By contributing, you agree your contributions will be licensed under MIT.
