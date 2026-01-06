# design principles

What makes extensions enhance capability rather than create dependency.

---

## the distinction

Most AI tools are just tools. You use them, put them down, and you're no different.

Cognitive extensions are different. They become part of how you think. Done right, you're more capable even when the extension isn't available.

The goal: engineering excellence through effective collaborative intelligence.

---

## extended mind thesis

Extensions expand cognitive capability — they become part of how the human-AI system thinks together.

When you can't remember phone numbers because your phone does, that's cognitive extension. The boundary between "you" and "your capabilities" has blurred. The same principle applies here: skills, agents, and hooks become part of how the composite system reasons.

**The parity principle**: If a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's still cognition — just extended.

**Source**: [Clark & Chalmers (1998). The Extended Mind.](https://www.philosophy.ed.ac.uk/pages/people/andy-clark/extended-mind.pdf)

---

## collaborative agency

Both human and AI retain agency in the collaboration. Understanding why, not just following commands.

| approach | result |
|----------|--------|
| commands (MUST, MANDATORY) | compliance, brittleness |
| motivation (here's why) | understanding, judgment |

Claude is [constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) — trained with values, not rigid rules. Extensions that try to force behavior through aggressive prompting work against this architecture.

**Evidence**: [Scott Spence (2024)](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) — 200+ tests showed forced evaluation prompts improved activation, but more forceful language didn't push higher. Claude exercises judgment.

---

## bidirectional learning

Both human and AI develop capability through collaboration.

| participant | learns | how |
|-------------|--------|-----|
| **human** | reasoning, tradeoffs | visible rationale, approval gates |
| **claude** | corrections, context | feedback, refinement |
| **system** | crystallized knowledge | extensions persist |

**The risk**: Human offloads → AI produces → human consumes → capability atrophies.

**Evidence**:
- [Gerlich (2025)](https://www.mdpi.com/2075-4698/15/1/6): r = -0.75 correlation between AI use and critical thinking
- [Lee et al. (2025)](https://dl.acm.org/doi/10.1145/3613904.3642902): confidence in AI → reduced critical thinking (β = -0.69)

---

## transparent abstractions

If you can't see how it works, you can't learn from it.

| property | meaning |
|----------|---------|
| **readable** | plaintext markdown, no magic |
| **forkable** | copy, modify, make your own |
| **verifiable** | claims have sources |
| **observable** | see what Claude does with them |

---

## composable architecture

Extensions build on each other. Compound improvements, not reinvention.

| modality | extends |
|----------|---------|
| **skills** | knowledge — decision frameworks, expertise |
| **agents** | reasoning — specialized problem-solving |
| **hooks** | context — session behavior, environment |
| **commands** | efficiency — workflow shortcuts |
| **mcp** | reach — external data, systems |

Together: human + extensions + AI = emergent capability neither produces alone.

---

## for builders

| principle | implication |
|-----------|-------------|
| extend cognition | design for integration, not one-off use |
| collaborative agency | explain why, don't command |
| bidirectional learning | make reasoning visible |
| transparent abstractions | plaintext, sources cited |
| composable architecture | build on what exists |

---

## related

- [collaborative-intelligence](/explore/explanation/collaborative-intelligence/) — extended mind research
- [craftsmanship](/explore/explanation/craftsmanship/) — evidence hierarchy, first principles, the guild path
