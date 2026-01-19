# arch-guild

Architectural reasoning through 13 specialized agents with orthogonal perspectives — each locked to their domain, forcing genuine perspective diversity.

## What Problem This Solves

Architecture decisions need multiple perspectives. A caching decision involves economics (cost), consistency (distributed systems), security (DoS vectors), and capacity (memory bounds). Most reviews miss something because they come from one viewpoint.

The Guild provides structured multi-perspective evaluation. Each agent has a defined domain and **orthogonality lock** — they can only discuss their area. This prevents homogenization and forces genuine perspective diversity.

## When to Use

The Guild activates when you:

- Review architecture for a service or system
- Evaluate design decisions (caching, API protocol, boundaries)
- Check production readiness
- Make tradeoff decisions between competing concerns
- Need to understand why legacy code exists before changing it

**Example prompts:**
- "Review this architecture for a payment system"
- "Should I use Redis or in-memory HashMap for caching?"
- "Is this service ready for production?"
- "Convene the full guild on this proposal"

## The 13 Agents

Agents are named after thought leaders whose work defines their domain (Lamport for distributed systems, Dijkstra for correctness, Taleb for resilience). See `references/sources.md` for the full lineage.

### 7 Masters (Always Active)

These agents review every architectural decision.

| Agent | Domain | Core Question |
|-------|--------|---------------|
| **K** | Strategic | What forces are at play? What move creates options? |
| **Karman** | Ontological/Naming | Does code model match business reality? |
| **Burner** | Structural/Boundaries | Are dependencies clean? Do they point inward? |
| **Lamport** | Temporal/Distributed | What happens with latency, partitions, eventual consistency? |
| **Erlang** | Hydraulic/Capacity | If inflow exceeds outflow, where is the valve? |
| **Vector** | Adversarial/Security | If I control the input, how do I break this? |
| **Ace** | Psychocentric/DX | Can the next developer figure this out in 15 minutes? |

### 6 Specialists (Context-Triggered)

These agents activate when specific conditions appear.

| Agent | Domain | Trigger |
|-------|--------|---------|
| **Ixian** | Empirical/Validation | Always — mandatory post-consensus |
| **Dijkstra** | Deductive/Correctness | Critical paths: auth, payments, state machines |
| **Knuth** | Complexity/Performance | Loops, aggregations, high-cardinality data |
| **Lotfi** | Fuzzy/Tradeoffs | Agent deadlocks (K says yes, Dijkstra says no) |
| **Taleb** | Antifragile/Resilience | Production readiness, failure modes |
| **Chesterton** | Diachronic/Legacy | Removing old code, refactoring legacy systems |

## Guild Modes

| Mode | Agents | Use When |
|------|--------|----------|
| **Methodology** | Relevant subset | Default — let context determine |
| **Quick** | 7 Masters | Fast review, broad coverage |
| **Focus** | 3-4 targeted | Specific concern (security, performance) |
| **Full** | All 13 | Major decisions, comprehensive review |

## Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **APPROVE** | No concerns from this perspective | Proceed |
| **CONCERN** | Minor issues, acceptable short-term | Proceed with awareness |
| **OBJECTION** | Significant issues | Address before proceeding |
| **BLOCK** | Fundamental problem | Cannot proceed |

## The Ratchet

The Guild learns across sessions. After significant decisions, capture learnings to `.claude/guild-ratchet.md` in your project:

```markdown
## 2026-01-15: Redis vs HashMap Decision

### Blocking Agents
- Lamport: Per-instance HashMap breaks cache consistency with 4 replicas

### Principle Extracted
> "In-memory caching requires single-writer architecture or accepting stale reads."

### Future Trigger
Multi-instance deployments with shared state
```

The SessionStart hook loads this automatically. Disable with `SKIP_GUILD_RATCHET=1`.

## Structure

```
arch-guild/
├── skills/
│   ├── architecture/    # Guild methodology, hexagonal, event-driven
│   ├── design/          # SOLID, API protocols, component design
│   └── operations/      # Production readiness, chaos engineering
├── agents/              # 13 agent definitions
├── references/          # Shared methodology
├── hooks/               # SessionStart ratchet loader
└── evals/               # Activation tests
```

## Sources

The agents draw from foundational work in computer science:

| Agent | Source |
|-------|--------|
| Dijkstra | "The Humble Programmer" (1972) — correctness through proof |
| Lamport | "Time, Clocks, and the Ordering of Events" (1978) — distributed systems |
| Taleb | *Antifragile* (2012) — resilience under stress |
| Knuth | "Structured Programming with go to Statements" (1974) — complexity analysis |

Full bibliography with 24 verified sources: `references/sources.md`

## License

MIT
