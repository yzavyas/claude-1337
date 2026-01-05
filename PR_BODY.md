## Summary

This PR includes two major updates:

### 1. Messaging Updates: Yo Dawg Meme + Best-in-Class Terminology

**Yo dawg, I heard you like 1337 skills, so we put 1337 skills in your 1337 coding agent so you can 1337 while Claude Code 1337s.**

Replaced "pick winners" terminology with "best-in-class" and "THE answer" throughout:
- README.md: Yo dawg tagline, best-in-class philosophy
- marketplace.json: Updated metadata description
- CLAUDE.md: Consistent terminology
- 1337-extension-builder SKILL.md: "THE answer not catalogs"
- docs/: All pages updated (index, how-to, preview pages, Base layout)

### 2. Curator-1337: Evolutionary Skill Updater

Implemented **curator-1337**, an Agent SDK app that automatically monitors and updates skills with evidence-based recommendations.

#### Architecture

```
Agent SDK Python App
        ↓
GitHub Actions (monthly + manual)
        ↓
Claude analyzes skills via structured prompts
        ↓
Creates PR with findings + evidence
        ↓
Human review required
```

#### Features

- **Monthly automatic runs** (1st of month, 2am UTC)
- **Manual triggers** with options (rust/terminal/all, dry-run)
- **Evidence-based updates** (production usage > GitHub stars)
- **Checks for**:
  - Deprecations (crates, tools)
  - New best-in-class options
  - Security advisories
  - Breaking changes

#### Components Added

```
.github/workflows/
  └── curator-1337.yml          # GHA workflow with scheduling

scripts/curator-1337/
  ├── curator.py                # Main Agent SDK app (7.9K)
  ├── requirements.txt          # anthropic>=0.40.0, requests
  ├── README.md                 # Complete documentation
  └── prompts/
      ├── detect-rust-updates.md    # Rust crate checks
      └── detect-tool-updates.md    # CLI tool checks
```

#### How It Works

1. **Agent Analysis**: Claude uses structured prompts to analyze each skill
2. **Evidence Collection**: Requires production usage, maintainer quotes, or security advisories
3. **PR Creation**: Generates PR with structured findings and citations
4. **Human Review**: All updates require maintainer approval (never auto-merge)

#### Required Secrets

- `ANTHROPIC_API_KEY` - Claude API access
- `GITHUB_TOKEN` - Auto-provided by GHA

#### Usage

**Automatic**: Runs monthly on schedule

**Manual**:
```bash
# Via GitHub Actions
Actions → Curator-1337 → Run workflow
  Options: rust/terminal/all, dry-run

# Local testing
cd scripts/curator-1337
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python curator.py --check all --dry-run
```

#### Philosophy

Curator follows the same principles as the skills it maintains:
- **Best-in-class only** - THE answer, not catalogs
- **Evidence over opinion** - Production usage > stars
- **High confidence** - Require multiple sources
- **Conservative** - Only suggest changes with clear evidence

#### Meta Commentary

*Yo dawg, we put an AI curator in your AI coding assistant marketplace so it can keep your best-in-class recommendations best-in-class while you use best-in-class tools.*

This is the natural evolution of the 1337 philosophy: not just opinionated content, but automated mechanisms to keep that content current and best-in-class.

## Testing

- ✅ Python syntax validation
- ✅ YAML workflow validation
- ✅ File permissions (curator.py executable)
- ✅ Documentation complete
- ✅ All files staged and committed

## Changes

**Modified**:
- CLAUDE.md (documented curator architecture)
- README.md (yo dawg tagline)
- marketplace.json (updated description)
- plugins/1337-extension-builder/SKILL.md (terminology updates)
- docs/ (5 files: index, how-to, preview pages, Base layout)

**Added**:
- .github/workflows/curator-1337.yml
- scripts/curator-1337/ (complete implementation)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
