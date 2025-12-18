# claude-1337

**Yo dawg, I heard you like 1337 skills, so we put 1337 skills in your 1337 coding agent so you can 1337 while Claude Code 1337s.**

Best-in-class tooling, practices, and learnings from industry leaders and master craftsmen.

## Install

```
/plugin marketplace add yzavyas/claude-1337
```

## Plugins

| Plugin | What | Contains |
|--------|------|----------|
| core-1337 | The foundation | hook |
| terminal-1337 | Modern CLI tools | skill, hook |
| rust-1337 | Rust decisions | skill |
| 1337-skill-creator | Skill authoring | skill |
| sensei-1337 | Teaching methodology | skill, agent |
| diagrams-1337 | Diagram-as-code | skill, agent |

**Install core-1337 first** - it activates 1337 mode (skill checking, decisions over catalogs, production mindset).

See [docs/](docs/) for details.

## How these were built

1. **Learn** from domain experts, core maintainers, and reputable technical blogs
2. **Validate** against production codebases — what actually ships, not just what's popular
3. **Distill** — cut what Claude already knows, keep non-obvious decisions and gotchas
4. **Format** as decision tables, not prose explanations

**Philosophy**: Best-in-class only. Not catalogs of options — THE answer for each use case.

The methodology is documented in `1337-skill-creator`.

## Testing with Evals

Skills are validated using rigorous evaluation methodology:

```bash
cd evals && uv sync
uv run skill-test suite suites/rigorous-v1.json -m baseline
```

Measures **precision** (avoid false activations) and **recall** (catch valid triggers), not just raw activation rate. See [evals/](evals/) for the framework and [evals/docs/WHY_EVALS_MATTER.md](evals/docs/WHY_EVALS_MATTER.md) for the philosophy.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
