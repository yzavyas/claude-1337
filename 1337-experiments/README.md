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
├── proposals/          # LEPs - Lab Enhancement Proposals (Rust RFC style)
├── experiments/        # Each experiment is its own package
├── results/            # Published findings
└── src/lab_1337/       # CLI and shared infrastructure
```

## Usage

```bash
# Install
uv sync

# List experiments
lab-1337 experiments

# Run an experiment
lab-1337 run ralph-iteration-effect

# View results
lab-1337 results ralph-iteration-effect
```

## Proposals

Lab Enhancement Proposals (LEPs) follow [Rust RFC format](https://rust-lang.github.io/rfcs/).

```bash
# Create new proposal
lab-1337 proposal new "My experiment idea"

# List all proposals
lab-1337 proposal list

# Show specific proposal
lab-1337 proposal show 001

# Update status (draft → discussion → fcp → accepted)
lab-1337 proposal status 001 discussion
lab-1337 proposal fcp 001
lab-1337 proposal accept 001

# Mark as implemented
lab-1337 proposal implemented 001 --tracking "experiments/my-experiment"
```

Current proposals:

- [LEP-001: Rigor is What You Want](proposals/lep-001-rigor-is-what-you-want.md)

## License

MIT
