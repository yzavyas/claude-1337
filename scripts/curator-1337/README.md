# curator-1337

Evolutionary skill curator for claude-1337. Monitors for deprecations, finds new best-in-class options, and creates PRs with evidence-based updates.

## Architecture

**curator-1337** is an Agent SDK application invoked by GitHub Actions:

- **Agent SDK Python App**: Uses Claude to analyze skills for updates
- **GitHub Actions**: Runs monthly or on-demand
- **Automated PRs**: Creates pull requests with evidence-based findings

## How It Works

1. **Monthly Check** (1st of month, 2am UTC)
   - GHA workflow triggers curator agent
   - Agent analyzes each skill using Claude
   - Identifies deprecations, new best-in-class options
   - Creates PR with findings and evidence

2. **Manual Trigger**
   - Actions tab → "Curator-1337" → Run workflow
   - Choose check type: rust, terminal, or all
   - Option for dry-run (no PR created)

3. **Evidence-Based Updates**
   - Production usage > GitHub stars
   - Maintainer announcements
   - Security advisories
   - Major project adoption

## Usage

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Run checks
python curator.py --check all

# Dry run (no PR)
python curator.py --check rust --dry-run
```

### GitHub Actions

The workflow runs automatically monthly, or manually via:

1. Go to Actions tab
2. Select "Curator-1337"
3. Click "Run workflow"
4. Choose options:
   - Check type: all/rust/terminal
   - Dry run: yes/no

## What It Checks

### rust-1337
- Crate deprecations (archived, unmaintained)
- Better alternatives with production adoption
- Security advisories
- Major version updates with breaking changes

### terminal-1337
- Tool deprecations (archived repos)
- Successor tools announced by authors
- Installation issues on major platforms
- Breaking changes in recent releases

## Prompts

The agent uses structured prompts in `prompts/`:

- `detect-rust-updates.md` - Rust ecosystem checks
- `detect-tool-updates.md` - CLI tool checks

Each prompt includes:
- Analysis criteria
- Evidence standards (production usage, maintainer quotes)
- Output format for structured findings

## Output

When updates are found, curator creates:

1. **Branch**: `curator/updates-YYYYMMDD`
2. **PR**: With findings document
3. **Evidence**: Citations for each recommendation

Example finding:
```markdown
## FINDING: async-std
TYPE: better-alternative
DESCRIPTION: async-std development slowed; smol emerged as lightweight alternative
EVIDENCE: https://github.com/smol-rs/smol - active maintenance, used in iroh
RECOMMENDED_ACTION: Update obsolete patterns: "async-std → smol (or tokio)"
```

## Configuration

### Required Secrets

Set in repository settings → Secrets:

- `ANTHROPIC_API_KEY` - Claude API access
- `GITHUB_TOKEN` - Automatically provided by GHA

### Workflow Schedule

Edit `.github/workflows/curator-1337.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 1 * *'  # Monthly, 1st at 2am UTC
```

## Philosophy

Curator follows the same principles as the skills it maintains:

- **Best-in-class only** - Not catalogs, THE answer
- **Evidence over opinion** - Production usage > stars
- **High confidence** - Require multiple sources
- **Conservative** - Only suggest changes with clear evidence

## Development

### Adding New Check Types

1. Create prompt template in `prompts/`
2. Add check method to `CuratorAgent` class
3. Update CLI arguments
4. Update GHA workflow options

### Testing Prompts

Test prompts before committing:

```bash
# Dry run to test prompt logic
python curator.py --check rust --dry-run

# Review output without creating PR
```

## Maintenance

### False Positives

If curator suggests incorrect updates:
1. Review evidence standards in prompts
2. Strengthen "high-confidence" criteria
3. Add counterexamples to prompts

### Adding Skills

When new skills are added to claude-1337:
1. Add check method to `curator.py`
2. Create prompt template
3. Update `--check` options
4. Document in this README

## Credits

Inspired by:
- Dependabot (automated dependency updates)
- Renovate (smart update PRs)
- The "yo dawg" philosophy of 1337 skills curating 1337 skills
