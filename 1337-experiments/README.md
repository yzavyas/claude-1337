# 1337 Experiments Lab

Rigorous experiments for the agentic era.

## Mission

Decisions compound exponentially. Bad methodology choices scale with everything built on them. Good ones compound toward better outcomes.

This lab produces evidence - not opinions, not hype - that thinkers can reason from.

## Values

Core-1337 methodology applied to understanding enhanced cognition:

| Value | Source |
|-------|--------|
| **Don't fool yourself** | "The first principle is that you must not fool yourself — and you are the easiest person to fool." — Feynman |
| **Scientific method** | Hypothesize → Test → Observe → Refine. No shortcuts. |
| **Giants' shoulders** | Build on what's proven. Cite sources. Don't reinvent. |
| **Allegiance to evidence** | Data is king. Update on proof, not persuasion. |
| **Design for collaborative intelligence** | Truth accessible to any thinker. Human and AI learn together. |

## What This Is

A lab for running rigorous experiments on agentic-era questions.

- **Reproducible** - Any thinker can verify
- **Substrate-agnostic** - Evidence valid for silicon or carbon
- **Transparent** - Methodology is the product, not just results

## What This Isn't

Marketing. Hype. Framework promotion. "Top 10" lists.

## Structure

```
1337-experiments/
├── proposals/          # LEPs - Lab Enhancement Proposals
├── implementations/    # IMPs - Implementation Plans
├── experiments/        # Each experiment is its own package
├── results/            # Published findings
└── src/lab_1337/
    ├── elc/            # Enhancement Lifecycle management
    ├── core/           # Experiment infrastructure
    └── cli.py          # CLI entrypoint
```

## Enhancement Lifecycle (ELC)

Full lifecycle from idea to evidence:

```
LEP (Proposal) → IMP (Implementation Plan) → Experiment → Results
```

Naming convention enforces linkage: `lep-001-*`, `imp-001-*`, `experiments/lep-001-*` are automatically connected by number.

### Quick Start

```bash
# Install
uv sync

# Check lab status
lab-1337 status
```

### Proposals (LEPs)

[Rust RFC format](https://rust-lang.github.io/rfcs/) - what and why.

```bash
lab-1337 proposal new "My experiment idea"    # Create from template
lab-1337 proposal list                        # Show all proposals
lab-1337 proposal show 001                    # View proposal
lab-1337 proposal status 001 discussion       # Start discussion
lab-1337 proposal fcp 001                     # Final Comment Period
lab-1337 proposal accept 001                  # Accept (prompts IMP creation)
```

**Lifecycle**: draft → discussion → fcp → accepted/rejected/postponed → implemented

### Implementation Plans (IMPs)

The how - design and tasks.

```bash
lab-1337 imp new 001                          # Create IMP for LEP-001
lab-1337 imp list                             # Show all IMPs
lab-1337 imp show 001                         # View IMP
```

### Experiments

Executable packages linked to LEPs.

```bash
lab-1337 experiment new 001                   # Scaffold from LEP-001
lab-1337 experiment list                      # Show all experiments
lab-1337 run lep-001-my-experiment            # Run experiment
lab-1337 results lep-001-my-experiment        # View results
```

## Current Work

- [LEP-001: Rigor is What You Want](proposals/lep-001-rigor-is-what-you-want.md)

## License

MIT
