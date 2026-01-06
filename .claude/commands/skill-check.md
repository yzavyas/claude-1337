Diagnose skill health and triggering issues.

## Check Available Skills

1. How many skills are in your `<available_skills>` block?
2. List each skill's name and the first 50 chars of its description
3. Are any descriptions truncated or showing ">-" instead of content?

## Validate Skills in This Repo

For each SKILL.md in `plugins/*/`:

1. **Frontmatter check**:
   - Has `name` field (max 50 chars)?
   - Has `description` field (max 600 chars)?
   - Using quoted strings (not `>-` or `|`)?

2. **Size check**:
   - SKILL.md line count (max: 500)
   - Description char count (must be <600)

3. **Reference check**:
   - All files in references/ exist?
   - Links in SKILL.md point to valid files?

## Report Format

```
=== Skill Health Report ===

Available in <available_skills>: X skills
Truncation detected: Yes/No

rust-1337:
  - Description: XXX chars (OK/OVER)
  - SKILL.md: XXX lines (OK/OVER)
  - References: X files, all valid
  - Status: OK / ISSUES FOUND

terminal-1337:
  - Description: XXX chars (OK/OVER)
  - SKILL.md: XXX lines (OK/OVER)
  - References: X files, all valid
  - Status: OK / ISSUES FOUND
```

Run this check and report findings.
