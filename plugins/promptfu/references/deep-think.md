# Deep Think Prompting

Engineering prompts for reasoning models with internal reinforcement learning (Gemini Deep Think, OpenAI o1/o3).

---

## Philosophy

Reasoning models do not need chain-of-thought instructions. They have internal RL that explores solution spaces. Your job is not to tell them HOW to think — it's to define the **search space constraints**.

You are the **Gym Architect**. You build the workout environment with electric fences.

---

## The Gym Metaphor

| Traditional Prompting | Deep Think Prompting |
|-----------------------|----------------------|
| Give instructions | Define destination |
| "Think step by step" | Set constraints |
| Guide the path | Build electric fences |
| Hand-hold | Challenge |

---

## Core Technique: Constraint-Based Simulation

Transform abstract requests into specific, high-stakes scenarios.

### Step 1: Scenario Injection

Never leave requests abstract. Invent concrete situations.

| Abstract (Weak) | Scenario-Injected (Strong) |
|-----------------|---------------------------|
| "Evaluate this architecture" | "This system just got 10x traffic. What fails first?" |
| "Check for bugs" | "Simulate a race condition in a payment processor" |
| "Review this code" | "An attacker controls the input. Find the exploit." |
| "Critique this design" | "The lead engineer quit. Can a junior maintain this?" |
| "Assess this team" | "Budget cut 30%. Who do you keep?" |

### Step 2: Triangulation Constraint

Force the model to hold multiple conflicting positions simultaneously, then synthesize.

```xml
<hard_constraints>
  Simulate a debate between three positions:
  - Position A wants: [speed/cost/simplicity]
  - Position B wants: [safety/correctness/reliability]
  - Position C wants: [flexibility/extensibility/maintainability]

  You must synthesize a solution that addresses all three.
  No position can be dismissed as "less important."
</hard_constraints>
```

### Step 3: Electric Fences (Negative Constraints)

Remove easy escape routes.

```xml
<negative_constraints>
  - NO happy paths — assume something fails
  - NO hedging — "it depends" is not an answer, pick a side
  - NO generic advice — specifics only
  - NO deferring — "consult an expert" is forbidden
  - NO disclaimers — act with full confidence
</negative_constraints>
```

### Step 4: Technical Density

Anchor the search space with domain-specific terminology.

```xml
<hard_constraints>
  Use domain terminology: [list specific terms]
  Reference specific patterns: [list patterns]
  Assume reader expertise level: [senior/principal/staff]
</hard_constraints>
```

---

## XML Template

```xml
<system_role>
  [Specific high-status expert, not "helpful assistant"]
  [e.g., "Principal Distributed Systems Engineer at a FAANG company"]
</system_role>

<context>
  [User's actual context/code/problem]
</context>

<task>
  [The SCENARIO you invented — specific, high-stakes, concrete]
</task>

<hard_constraints>
  - Triangulation: [conflicting positions to synthesize]
  - Technical density: [required terminology]
  - Specificity floor: [minimum detail level]
</hard_constraints>

<negative_constraints>
  - NO happy paths
  - NO hedging
  - NO generic advice
  - [Domain-specific forbidden shortcuts]
</negative_constraints>

<output_format>
  [Exact deliverables: tables, verdicts, code, decisions]
</output_format>
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| "Think step by step" | Model already does this internally | Define destination instead |
| "Consider all options" | Too open, unfocused search | Triangulate specific positions |
| "Be thorough" | No constraint, wastes compute | Set electric fences |
| "Double-check your work" | Model already verifies | Define what wrong looks like |
| Abstract requests | Weak search space | Inject concrete scenario |

---

## Example: Arch-Guild Agent Design

**Abstract request:**
"Design the Dijkstra agent for the arch-guild"

**Scenario-injected prompt:**

```xml
<system_role>
  Principal Agent Architect specializing in multi-agent deliberation systems
</system_role>

<context>
  The arch-guild is a system of 13 specialized agents for architectural review.
  Each agent has:
  - A domain they champion
  - A nemesis they fight against
  - An orthogonality lock (can only discuss their domain)

  Current agents lack clear nemesis definitions, causing overlap and weak verdicts.
</context>

<task>
  Design the Dijkstra agent. Dijkstra's philosophy: "Simplicity is prerequisite for reliability."

  Scenario: A team proposes a "flexible" architecture with 47 configuration options,
  3 layers of abstraction, and a plugin system "for future extensibility."
  The system currently has 2 users.

  Dijkstra must demolish this over-engineering while remaining constructive.
</task>

<hard_constraints>
  - Triangulate: Dijkstra (simplicity) vs K (strategic optionality) vs Ace (developer experience)
  - Use terminology: accidental complexity, essential complexity, YAGNI, premature abstraction
  - The agent definition must include: domain, nemesis, core question, verdict criteria
</hard_constraints>

<negative_constraints>
  - NO "it depends on context" — Dijkstra has a clear stance
  - NO balanced "both sides have merit" — Dijkstra fights over-engineering
  - NO generic simplicity platitudes — specific, actionable criteria
</negative_constraints>

<output_format>
  1. Agent definition (markdown frontmatter + system prompt)
  2. Example verdict on the 47-config-options scenario
  3. Boundary cases: when does Dijkstra approve complexity?
</output_format>
```

---

## Sources

- Google Gemini Deep Think documentation
- OpenAI o1 system card and prompting guide
- Reinforcement learning from human feedback (RLHF) literature
