# activation

Skill activation and validation research.

---

## the activation problem

Claude Code skills have ~20% baseline activation rate. You install a skill, ask a relevant question, and Claude ignores it 80% of the time.

---

## root cause

From Lee Han Chung's analysis:

- **No algorithmic routing** — no regex, embeddings, or classifiers
- **Pure LLM reasoning** — Claude reads descriptions and decides
- **Description is everything** — the only signal for matching

---

## the forced evaluation study

**Scott Spence (2024).** 200+ test validation study.

| approach | activation rate |
|----------|-----------------|
| No intervention (baseline) | ~20% |
| Simple instruction | ~20% |
| LLM eval hook | 80% |
| Forced eval hook | **84%** |

---

## the fix

Explicit evaluation prompts that force skill checking before responding:

```
Before responding:
1. Check if any skills in <available_skills> are relevant
2. If relevant, invoke the Skill tool
3. Then respond using that knowledge
```

---

## what makes skills activate

| pattern | why it works |
|---------|--------------|
| "use when:" clause | Explicit trigger conditions |
| Specific terms | "axum, tonic, sqlx" not "backend" |
| Action verbs | "building", "debugging", "configuring" |
| Front-loaded keywords | Claude matches against description start |

---

## validation methodology

Tests send prompts through Claude Agent SDK and monitor for `ToolUseBlock` with `name == "Skill"`. This is ground truth — did Claude actually invoke the skill?

| activation rate | meaning |
|-----------------|---------|
| 80%+ | Description working well |
| 50-79% | Description needs improvement |
| <50% | Likely missing "use when:" or too vague |

---

## sources

- [Anthropic: Equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Scott Spence: Skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably)
- [Lee Han Chung: Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
