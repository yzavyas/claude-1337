Update skills with current best-in-class recommendations.

## Update Process

For the specified skill (or all skills if not specified):

### 1. Research Current State

- Web search for latest releases, deprecations, benchmarks
- Check crate versions on crates.io (for rust-1337)
- Look for production usage from major teams (Cloudflare, Discord, AWS, etc.)

### 2. Validate Existing Recommendations

- Is each "best-in-class" choice still best?
- Any new contenders that reached production-ready status?
- Any deprecated or abandoned projects?
- Any security advisories?

### 3. Update with Evidence

Only change recommendations when there's clear evidence:
- Production usage > GitHub stars
- Benchmarks from reliable sources
- Official deprecation notices

### 4. Commit Changes

If updates were made, commit with context:

```
Update [skill]: [brief description of change]

[Why the change was made with evidence]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## What to Check

### rust-1337
- Crate versions and deprecations
- New frameworks reaching production status
- Changed best practices from Tokio, Rust teams

### terminal-1337
- New tool versions
- Changed flags or deprecated options
- Better alternatives that emerged

## Arguments

$ARGUMENTS - Skill to update: `rust-1337`, `terminal-1337`, or `all` (default: all)

---

Run the update for: $ARGUMENTS
