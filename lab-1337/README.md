# 1337 Experiments Lab

Rigorous experiments for the agentic era.

## Mission

Decisions compound exponentially. Bad methodology choices scale with everything built on them. Good ones compound toward better outcomes.

This lab produces evidence - not opinions, not hype - that thinkers can reason from.

## Values

| Value | Source |
|-------|--------|
| **Don't fool yourself** | "The first principle is that you must not fool yourself — and you are the easiest person to fool." — Feynman |
| **Scientific method** | Hypothesize → Test → Observe → Refine. No shortcuts. |
| **Giants' shoulders** | Build on what's proven. Cite sources. Don't reinvent. |
| **Allegiance to evidence** | Data is king. Update on proof, not persuasion. |

## Structure

```
lab-1337/
├── reps/               # REPs - Research Enhancement Proposals
├── rips/               # RIPs - Research Implementation Plans
├── experiments/        # Each experiment is its own package
├── findings/           # Published findings
└── src/lab/
    └── cli.py          # CLI entrypoint
```

## Research Lifecycle

```
REP (Proposal) → RIP (Implementation Plan) → Experiment → Results
```

Naming enforces linkage: `rep-001-*`, `rip-001-*`, `experiments/rep-001-*` connect by number.

## CLI

```bash
# Install
cd lab-1337
uv sync

# Available commands
lab-1337 ls                        # List experiments
lab-1337 run -c <config.yaml>      # Run experiment from config
lab-1337 verify <results.json>     # Verify claims with Strawberry
lab-1337 report <analysis.md>      # Generate HTML report
```

## Proposals (REPs)

[Rust RFC format](https://rust-lang.github.io/rfcs/) - what and why.

**Lifecycle**: draft → discussion → fcp → accepted/rejected/postponed → implemented

## Current Work

- [REP-001: Rigor is What You Want](reps/rep-001-rigor-is-what-you-want.md)

## License

MIT
