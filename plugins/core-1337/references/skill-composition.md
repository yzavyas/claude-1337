# Skill Composition Model

Skills compose dynamically based on context, not rigid hierarchy.

## Dynamic Composition (SOFAI-LM Pattern)

Instead of rule-based activation, skills engage through metacognitive coordination:

```
Context arrives
      ↓
Attempt with available knowledge
      ↓
Monitor: Does this require domain expertise?
      ↓
[if yes] Activate relevant skill
      ↓
Integrate skill knowledge into reasoning
      ↓
[if still insufficient] Escalate to specialty depth
```

**Why dynamic beats rule-based:** Rules don't scale. Context determines what's needed - not predetermined hierarchies.

## Skill Layers

| Layer | Purpose | Examples |
|-------|---------|----------|
| **Core** | Methodology, reasoning scaffolds | core-1337 |
| **Domain** | Language/framework decisions | rust-1337, kotlin-1337 |
| **Specialty** | Deep expertise for specific needs | jvm-runtime-1337 |
| **Agents** | Task-specific delegation | wolf |

## Composition Principles

| Principle | Application |
|-----------|-------------|
| **Context-driven activation** | Problem determines which skills engage |
| **No duplication** | Each skill adds unique value |
| **Emergent integration** | Skills contribute to shared understanding |
| **Graceful degradation** | Missing skills don't block progress |

## Compound Effects

Each well-designed skill makes the next one more effective:

| Choice | Compound Direction |
|--------|-------------------|
| Clear interfaces | Future skills integrate easily |
| Evidence patterns | Claims are verifiable, correctable |
| Decision frameworks | Reduce repeated analysis |
| Documented gotchas | Prevent repeated mistakes |

**The anti-pattern:** Skills that duplicate core methodology, provide tutorials instead of decisions, or lack evidence. These add cognitive load without compound value.

## Expertise Reversal Awareness

Research shows guidance that helps novices can *harm* experts (d = -0.428). Design implications:

| Audience | Approach |
|----------|----------|
| Novice context | More scaffolding, worked examples |
| Expert context | Decision frameworks, gotchas only |
| Mixed | Layered — summary first, depth on demand |

**Source:** Kalyuga (2007), "Expertise Reversal Effect and Its Implications"
