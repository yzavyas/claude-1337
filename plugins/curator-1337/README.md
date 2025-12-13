# curator-1337

Evolutionary curator for claude-1337 skills. Monitors for deprecations, finds new best-in-class options, validates recommendations with evidence.

## What It Does

Curator-1337 keeps your skills best-in-class by:
- Detecting deprecated crates and tools
- Finding new best-in-class alternatives
- Validating recommendations with production evidence
- Checking for security advisories
- Monitoring major version updates

## As a Plugin

Install and use directly:

```
/plugin install curator-1337@claude-1337
```

Then invoke the curator agent:

```
Can you check the rust-1337 skill for any outdated recommendations?
```

The curator agent will activate automatically when you're:
- Updating skills
- Checking for deprecated crates/tools
- Validating tooling choices
- Looking for better alternatives

## As GitHub Actions

Curator also runs automatically monthly via GitHub Actions to keep claude-1337 itself up-to-date.

See `.github/workflows/curator-1337.yml`

## Components

### Agent: curator

The curator agent (`agents/curator.md`) analyzes skills using:
- **Evidence-based validation** (production usage > stars)
- **Multi-source requirements** (2+ sources for changes)
- **Conservative approach** (only high-confidence findings)

Invoke directly:
```
Task(subagent_type="curator-1337:curator",
     prompt="Analyze this skill for deprecated recommendations: [skill content]")
```

### References

- `rust-checks.md` - Rust crate validation process
- `tool-checks.md` - CLI tool validation process

## Philosophy

**Best-in-class only** - THE answer, not catalogs
**Evidence over opinion** - Production usage > GitHub stars
**High confidence** - Require multiple sources
**Conservative** - Only suggest changes with clear justification

## Evidence Standards

### What Counts as Evidence

✅ **Strong evidence:**
- Production usage at major companies (blogs, talks, code)
- Maintainer announcements (deprecation, archival, successor)
- Security advisories (CVEs, RustSec)
- Major project migrations (Servo, Tokio, Cloudflare, etc.)

❌ **Not sufficient alone:**
- GitHub stars
- Reddit opinions
- Single blog post
- Personal preferences

### Confidence Levels

**High**: 2+ strong evidence sources, clear action
**Medium**: 1 strong source, needs monitoring
**Low**: Signals only, needs investigation

Only high-confidence findings result in recommendations.

## Example Usage

### Check a Skill

```
Check rust-1337 for any deprecated crates or better alternatives.
```

Output:
```markdown
# Curator Analysis: rust-1337

**Findings**: 1

## FINDING: async-std

**Type**: better-alternative
**Description**: async-std development slowed; smol emerged as lightweight alternative

**Evidence**:
1. https://github.com/smol-rs/smol - active, used in iroh (n0 production)
2. async-std last release 18+ months, maintainers suggest smol
3. Production adoption: iroh, dioxus, bevy (via smol)

**Recommended Action**: Update obsolete patterns: "async-std → smol (or tokio)"
**Confidence**: high
```

### Validate Your Own Skill

```
I created a new skill recommending crate X for use case Y.
Can you validate this is still the best-in-class choice?
```

The curator will:
1. Check maintenance status
2. Look for production usage
3. Search for better alternatives
4. Report findings with evidence

## Integration with claude-1337

Curator-1337 automatically maintains claude-1337 itself:
- Runs monthly (1st of month, 2am UTC)
- Creates PRs with findings
- Requires human review (never auto-merge)

This keeps all 1337 skills actually best-in-class.

## Meta

*Yo dawg, we put a curator agent in your skills marketplace so it can keep your best-in-class recommendations best-in-class while you code with best-in-class tools.*

The curator is itself a skill that can be curated. Recursive excellence.
