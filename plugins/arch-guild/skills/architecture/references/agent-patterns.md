# Multi-Agent Coordination Patterns

Patterns for orchestrating multiple agents.

## Pattern Selection

| Pattern | Use When | Coordination |
|---------|----------|--------------|
| **Parallel Specialists** | Independent perspectives needed | None (merge results) |
| **Evaluator-Optimizer** | Iterative refinement | Sequential loop |
| **Debate** | Consensus required | Adversarial rounds |
| **Plan-Execute** | Complex multi-step task | Hierarchical |
| **Reflection** | Self-improvement | Self-loop |

## Selection Flowchart

```
Is consensus required?
├─ Yes → Adversarial pressure needed?
│        ├─ Yes → DEBATE
│        └─ No  → EVALUATOR-OPTIMIZER
└─ No  → Perspectives independent?
         ├─ Yes → PARALLEL SPECIALISTS
         └─ No  → Multi-step?
                  ├─ Yes → PLAN-EXECUTE
                  └─ No  → REFLECTION
```

## Pattern Details

### Parallel Specialists

The Guild uses this pattern. Independent agents evaluate simultaneously.

```
     ┌─────────────────────┐
     │   Shared Context    │  (Read-only)
     └──────────┬──────────┘
    ┌───────────┼───────────┐
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│Agent A│  │Agent B│  │Agent C│
└───┬───┘  └───┬───┘  └───┬───┘
    └───────────┼───────────┘
                ▼
         Merged Results
```

**Characteristics:**
- No cross-agent communication during evaluation
- Each agent sees same input
- Results merged at end
- Orthogonality locks prevent overlap

**Trade-offs:**
| Pro | Con |
|-----|-----|
| Simple to implement | No cross-agent synthesis |
| Parallelizable | May miss emergent concerns |
| Fault tolerant | Requires human to reconcile conflicts |

**Implementation:**
```typescript
async function parallelDeliberation(context: Context): Promise<Deliberation> {
  const agents = [k, karman, burner, lamport, erlang, vector, ace];

  // Run all agents in parallel
  const verdicts = await Promise.all(
    agents.map(agent => agent.evaluate(context))
  );

  // Merge results
  return {
    masters: verdicts,
    consensus: deriveConsensus(verdicts),
    blocking: verdicts.filter(v => v.verdict === 'BLOCK'),
  };
}
```

### Evaluator-Optimizer Loop

Iterative refinement through feedback cycles.

```
┌───────────┐     ┌───────────┐
│ Generator │────▶│ Evaluator │
└───────────┘     └─────┬─────┘
      ▲                 │
      └─── feedback ────┘
```

**Process:**
1. Generate initial output
2. Evaluate against criteria (0.0-1.0)
3. Provide specific feedback
4. Refine based on feedback
5. Loop until score ≥ threshold

**Implementation:**
```typescript
async function evaluatorOptimizer(
  task: Task,
  threshold: number = 0.9,
  maxIterations: number = 5
): Promise<Output> {
  let output = await generator.generate(task);

  for (let i = 0; i < maxIterations; i++) {
    const evaluation = await evaluator.evaluate(output, task.criteria);

    if (evaluation.score >= threshold) {
      return output;
    }

    output = await generator.refine(output, evaluation.feedback);
  }

  return output; // Best effort after max iterations
}
```

**When to use:**
- Code generation with quality requirements
- Document drafting with style guides
- Test generation with coverage targets

### Debate Pattern

Adversarial refinement through structured disagreement.

```
┌──────────┐         ┌──────────┐
│ Proposer │◀───────▶│  Critic  │
└──────────┘  rounds └──────────┘
                │
                ▼
          ┌──────────┐
          │  Judge   │
          └──────────┘
```

**Process:**
1. Proposer presents position
2. Critic challenges weaknesses
3. Proposer defends/refines
4. Repeat for N rounds
5. Judge synthesizes final position

**Implementation:**
```typescript
async function debate(
  topic: string,
  rounds: number = 3
): Promise<Synthesis> {
  let position = await proposer.initialPosition(topic);

  for (let i = 0; i < rounds; i++) {
    const critique = await critic.challenge(position);
    position = await proposer.defend(position, critique);
  }

  return await judge.synthesize(topic, position, allCritiques);
}
```

**When to use:**
- High-stakes decisions
- When devil's advocate perspective valuable
- Exploring solution space thoroughly

### Plan-Execute

Hierarchical decomposition with execution tracking.

```
        ┌──────────┐
        │ Planner  │
        └────┬─────┘
             │ plan
    ┌────────┼────────┐
    ▼        ▼        ▼
┌───────┐┌───────┐┌───────┐
│Step 1 ││Step 2 ││Step 3 │
└───┬───┘└───┬───┘└───┬───┘
    │        │        │
    └────────┴────────┘
             │
             ▼
      ┌──────────┐
      │ Verifier │
      └──────────┘
```

**Process:**
1. Planner decomposes task into steps
2. Execute steps (possibly in parallel if independent)
3. Track success/failure of each step
4. Re-plan if step fails
5. Verify final result

**Implementation:**
```typescript
async function planExecute(task: Task): Promise<Result> {
  const plan = await planner.decompose(task);

  for (const step of plan.steps) {
    try {
      const result = await executor.execute(step);
      step.status = 'completed';
      step.result = result;
    } catch (error) {
      step.status = 'failed';
      // Re-plan from current state
      plan = await planner.replan(task, plan, step, error);
    }
  }

  return await verifier.verify(task, plan);
}
```

**When to use:**
- Complex multi-step tasks
- When intermediate verification needed
- Tasks requiring rollback capability

### Reflection

Self-improvement through introspection.

```
┌──────────┐
│  Agent   │
└────┬─────┘
     │ output
     ▼
┌──────────┐
│ Reflect  │
└────┬─────┘
     │ insights
     ▼
┌──────────┐
│  Agent   │ (refined)
└──────────┘
```

**Process:**
1. Generate initial output
2. Reflect on output quality, mistakes, improvements
3. Generate refined output incorporating insights
4. Optionally repeat

**Implementation:**
```typescript
async function reflectiveGeneration(task: Task): Promise<Output> {
  const initial = await agent.generate(task);

  const reflection = await agent.reflect(initial, {
    questions: [
      'What did I do well?',
      'What could be improved?',
      'What did I miss?',
      'How would an expert critique this?'
    ]
  });

  return await agent.refine(initial, reflection);
}
```

**When to use:**
- Single-agent quality improvement
- When external evaluator unavailable
- Learning/calibration tasks

## The Guild's Approach

The Guild primarily uses **Parallel Specialists** with optional **Debate** escalation:

1. **Default**: Parallel evaluation by Masters
2. **Conflict**: If agents disagree, Lotfi scores trade-offs
3. **Deadlock**: Human decides with full context
4. **Closure**: Ixian always provides validation criteria

This balances thoroughness with practical efficiency.
