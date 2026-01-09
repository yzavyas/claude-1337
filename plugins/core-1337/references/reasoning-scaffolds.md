# Reasoning Scaffolds

Selection heuristics and novel patterns. Claude knows CoT, ToT, GoT, CoVe, Step-back - but **doesn't always explicitly select scaffolds**. Subagent testing shows good reasoning without metacognitive scaffold selection.

**What this reference adds:**
- Explicit selection heuristics (which scaffold for which signal)
- Novel patterns Claude doesn't have (OODA)
- Integration with thinking modes
- Research validation for Kaizen loop (Metacognitive Reuse)

## Scaffold Selection

| Signal | Scaffold | Why |
|--------|----------|-----|
| Linear steps | CoT | Natural sequence |
| Multiple approaches | ToT | Parallel exploration, prune bad paths |
| Interconnected insights | GoT | Revision as understanding deepens |
| Need verification | CoVe | Systematic error detection |
| Stuck | Step-back | Abstract reveals simpler solutions |
| Multiple concerns to balance | Blackboard | Problem determines which concern matters |
| Need high confidence | Triangulation | Independent paths to same conclusion |
| Dynamic situation, environment changing | **OODA** | Continuous reorientation |

**Note:** SOFAI-LM (fast first, escalate if needed) is for **skill composition**, not problem-solving scaffolds. See Skill Composition Model in core-1337 SKILL.md.

## OODA Loop (Gap Fill)

Boyd's decision cycle for dynamic, adversarial, or evolving situations.

```
Observe → Orient → Decide → Act → (loop)
```

| Phase | Action |
|-------|--------|
| **Observe** | Gather current information, notice changes |
| **Orient** | Analyze, synthesize, update mental model (the critical phase) |
| **Decide** | Select course of action based on orientation |
| **Act** | Execute, then immediately observe results |

**Key insight:** Orient is where advantage is gained. Faster/better orientation beats faster action. The loop is continuous - you're always observing while acting.

**When to use:** Debugging production issues, incident response, competitive analysis, any situation where conditions change faster than your plan.

**Source:** John Boyd, "Patterns of Conflict" (1986) - military strategy, widely applied to business/engineering

## SOFAI-LM Loop (Skill Composition Reference)

*This pattern is used for skill composition (see Skill Composition Model in SKILL.md), not problem-solving scaffolds. Documented here for source reference.*

```
Attempt (fast) → Monitor → [if needed] Feedback → Retry → [if still failing] Escalate
```

**Key insight:** Most problems don't need deep analysis. Try fast, escalate only when needed.

**Source:** [Khandelwal et al. (Aug 2025), "Language Models Coupled with Metacognition Can Outperform Reasoning Models"](https://arxiv.org/abs/2508.17959) - IBM Research

## Metacognitive Reuse (Kaizen Validation)

Extract recurring reasoning patterns into reusable "behaviors" (name + instruction).

**What this validates:** The Kaizen loop in core-1337 - crystallizing insights into compound value - is the same pattern. Meta AI found 46% token reduction by doing exactly this.

**How it works:**
1. Reflect on reasoning traces
2. Identify generalizable patterns
3. Extract as (name, instruction) pairs
4. Store in "behavior handbook" for reuse

**Source:** [Didolkar et al. (Sep 2025), "Metacognitive Reuse: Turning Recurring LLM Reasoning Into Concise Behaviors"](https://arxiv.org/abs/2509.13237) - Meta AI

## Integration with Thinking Modes

| Mode | Scaffolds |
|------|-----------|
| **Direct** | None |
| **Think** | CoT, Step-back |
| **Think hard** | ToT, CoVe, GoT |
| **Ultrathink** | Blackboard, Triangulation, full verification |

## When NOT to Scaffold

- Simple questions (scaffold overhead > benefit)
- Pure retrieval (just look it up)
- When intuition is sufficient

**Test:** Would I solve this faster without the scaffold? If yes, skip it.

## Composition Patterns

| Pattern | When |
|---------|------|
| Step-back + CoT | Abstract first, then reason |
| ToT + CoVe | Explore paths, verify winner |
| Blackboard + GoT | Multiple perspectives, non-linear |
| OODA wraps all | Dynamic situations - orient selects inner scaffold |
