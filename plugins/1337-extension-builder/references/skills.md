# Skills

Templates, best practices, and observability for skill extensions.

---

## Template

```yaml
---
name: skill-name
description: "What it does. Use when: [trigger 1], [trigger 2]. Covers: [keyword1], [keyword2]."
---

# Skill Title

One sentence purpose.

## Decision Framework

| Situation | Choice | Why |
|-----------|--------|-----|
| [Use case] | **[winner]** | Evidence: [source] |

## Production Gotchas

| Trap | Fix |
|------|-----|
| [Gotcha] | [Solution] |

## Domain Routing

| Detected | Load |
|----------|------|
| [keyword] | [reference.md](references/reference.md) |
```

---

## Best Practices

| practice | why |
|----------|-----|
| "Use when:" in description | Only signal Claude uses to activate |
| Specific tools/terms | Improves activation precision |
| < 500 lines SKILL.md | Loads on every activation |
| < 600 chars description | Token budget limit (15k total) |
| References for deep content | Progressive disclosure |
| Evidence per recommendation | Verifiable, learnable |
| Decision tables over prose | Scannable, lower cognitive load |

### Activation

Skills activate through pure LLM reasoning. The description is the **only signal**.

| good description | bad description |
|------------------|-----------------|
| "Use when: debugging TypeScript errors, need tsconfig help" | "Helps with TypeScript" |
| "Covers: jest, vitest, testing patterns" | "Testing skill" |
| Action verbs + specific terms | Abstract nouns |

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

## Quality Checklist

- [ ] "Use when:" in description
- [ ] Description < 600 chars
- [ ] SKILL.md < 500 lines
- [ ] Evidence per recommendation
- [ ] Decision tables, not tutorials
- [ ] Tested activation in real session
- [ ] Negative test cases (shouldn't trigger)
