# Skills

Templates, best practices, and observability for skill extensions.

---

## Structure

```
skill-name/
├── SKILL.md           (required - pragmatic, < 500 lines)
├── references/        (detailed docs, academic sources, load as needed)
├── scripts/           (executable code, deterministic operations)
└── assets/            (templates, files used in output)
```

---

## SKILL.md Template

```yaml
---
name: skill-name
description: "What it does. Use when: [trigger 1], [trigger 2]."
---

# Skill Title

One sentence: what this enables.

## Why This Approach

Practical motivation — why this matters, not research citations.

## Core Content

| situation | choice | why |
|-----------|--------|-----|
| [context] | **[winner]** | [practical reason] |

## Gotchas

| trap | fix |
|------|-----|
| [what goes wrong] | [how to avoid] |

## References

| need | load |
|------|------|
| [specific need] | [reference.md](references/reference.md) |

Research citations, detailed patterns, and examples live in references.
```

---

## What Goes Where

| SKILL.md | references/ |
|----------|-------------|
| High-level workflow | Detailed patterns |
| Decision frameworks | Full examples |
| Practical motivation | Academic/industry citations |
| "Load X when Y" navigation | Deep technical content |
| Gotchas and traps | API documentation |
| < 500 lines | No limit |

**Key insight:** SKILL.md motivates and navigates. References provide depth.

---

## Progressive Disclosure

Context is shared. Tokens are a public good.

| level | size | when loaded |
|-------|------|-------------|
| **Metadata** (name + description) | ~100 words | Always — triggers activation |
| **SKILL.md body** | < 500 lines | When skill activates |
| **References** | Unlimited | When Claude needs them |

### Referencing Patterns

**Pattern 1: Load table**
```markdown
## References

| need | load |
|------|------|
| Python patterns | [python.md](references/python.md) |
| Error handling | [errors.md](references/errors.md) |
```

**Pattern 2: Inline conditional**
```markdown
For simple edits, modify directly.

**For tracked changes**: See [redlining.md](references/redlining.md)
```

**Pattern 3: Domain routing**
```markdown
| detected | load |
|----------|------|
| AWS | [aws.md](references/aws.md) |
| GCP | [gcp.md](references/gcp.md) |
```

---

## Activation

Skills activate through LLM reasoning. The **description is the only signal**.

| good | bad |
|------|-----|
| "Use when: debugging TypeScript, need tsconfig help" | "Helps with TypeScript" |
| "Use when: creating diagrams, need Mermaid syntax" | "Diagram skill" |
| Action verbs + specific triggers | Abstract nouns |

### Character Budget

Default: 15,000 characters for all skill descriptions combined (~4000 tokens).

**Workaround**: `SLASH_COMMAND_TOOL_CHAR_BUDGET=30000`

Source: [fsck.com](https://blog.fsck.com/2025/12/17/claude-code-skills-not-triggering/)

---

## Observability

### Tracing

```python
def trace_skill_activation(prompt: str, skills: list[Skill]):
    with tracer.start_as_current_span("skill_check") as span:
        span.set_attribute("prompt", prompt[:200])
        span.set_attribute("available_skills", len(skills))

        activated = []
        for skill in skills:
            with tracer.start_as_current_span("skill_match") as skill_span:
                skill_span.set_attribute("skill_name", skill.name)
                matches = skill.matches(prompt)
                skill_span.set_attribute("activated", matches)
                if matches:
                    activated.append(skill.name)

        span.set_attribute("activated_skills", activated)
        span.set_attribute("activation_count", len(activated))
        return activated
```

### Spans

| span | attributes |
|------|------------|
| `skill_check` | prompt, available_skills, activation_count |
| `skill_match` | skill_name, activated, match_score |
| `skill_load` | skill_name, content_size, load_time_ms |
| `skill_reference` | skill_name, reference_path, load_time_ms |

### Metrics

| metric | meaning |
|--------|---------|
| Activation rate | % of prompts that trigger skill |
| False positive rate | Activated but not used |
| Content load latency | Time to load SKILL.md + references |

---

## Checklist

### Content
- [ ] Fills gaps (what Claude doesn't know)
- [ ] Decisions, not tutorials
- [ ] SKILL.md < 500 lines
- [ ] Practical motivation, not academic

### Activation
- [ ] "Use when:" in description
- [ ] Description < 600 chars
- [ ] Triggers on right prompts
- [ ] Negative test cases (shouldn't trigger on X)

### Structure
- [ ] References clearly navigated
- [ ] Academic/industry sources in references, not SKILL.md
- [ ] Scripts for deterministic operations
- [ ] Tested in real session
