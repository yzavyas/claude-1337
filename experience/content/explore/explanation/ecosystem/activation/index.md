[&larr; ecosystem](../)

# activation

<p class="dimmed-intro">why skills don't activate by default and how to fix it</p>

---

## the problem

Skills have a ~20% baseline activation rate. You install a skill, ask a relevant question, Claude ignores it 80% of the time.

**Root cause**: Claude sees skills but doesn't automatically evaluate them against your request. It responds without checking if a skill would help.

---

## the solution

Explicit evaluation prompts that force Claude to check skills before responding. This is what core-1337's SessionStart hook implements.

| approach | activation rate |
|----------|-----------------|
| baseline (no intervention) | ~20% |
| forced eval hook | **84%** |

---

## how activation works

From [Lee Han Chung's deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):

- **No algorithmic routing** - no regex, no embeddings, no classifiers
- **Pure LLM reasoning** - Claude reads skill descriptions and decides
- **Description is everything** - the only signal for matching

---

## the research

[Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) ran 200+ tests on skill activation:

| approach | activation rate | notes |
|----------|-----------------|-------|
| no intervention (baseline) | ~20% | default behavior |
| simple instruction | ~20% | doesn't help |
| LLM eval hook | 80% | asks claude to evaluate |
| forced eval hook | **84%** | explicit skill checking |

**Key insight**: More forceful language ("MUST", "CRITICAL") didn't improve results. Claude exercises judgment about relevance.

---

## the fix

core-1337's SessionStart hook implements forced evaluation:

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
| "use when:" clause | explicit trigger conditions |
| specific tools/terms | "axum, tonic, sqlx" not "backend" |
| action verbs | "building", "debugging", "configuring" |
| front-loaded keywords | Claude matches against description |

---

## testing activation

The eval framework validates activation by observing actual tool invocation - not asking Claude's opinion.

### interpreting results

| activation rate | meaning |
|-----------------|---------|
| 80%+ | description is working well |
| 50-79% | description needs improvement |
| <50% | likely missing "use when:" or too vague |

### quick start

```bash
cd evals
uv sync
uv run skill-test test "how do i search for a pattern?" -s terminal-1337 -n 3
```

See [evals/ on GitHub](https://github.com/yzavyas/claude-1337/tree/main/evals) for full documentation.

---

## sources

- [Anthropic: Equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - official documentation
- [Scott Spence: Skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 200+ test validation
- [Lee Han Chung: Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - how skill routing works
