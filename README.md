# claude-1337

Curated skills and workflows for Claude Code. Production patterns, decision frameworks, evidence-based recommendations.

## Install

```
/plugin marketplace add yzavyas/claude-1337
```

## Plugins

**Install core-1337 first** — sets session context for skill activation and evidence-based recommendations.

```
/plugin install core-1337@claude-1337
```

Browse all plugins in the [catalog](experience/content/explore/reference/catalog/) — filter by component type (skills, hooks, agents) and search by keywords.

## How these were built

1. **Learn** from domain experts, core maintainers, and reputable technical blogs
2. **Validate** against production codebases — what actually ships, not just what's popular
3. **Distill** — cut what Claude already knows, keep non-obvious decisions and gotchas
4. **Format** as decision tables, not prose explanations

**Philosophy**: Battle-tested, best-in-class. Standing on the shoulders of giants.

The methodology is documented in the [extension builder](experience/content/explore/reference/catalog/).

## Testing with Evals

Skills are validated using rigorous evaluation methodology:

```bash
cd evals && uv sync
uv run skill-test suite suites/rigorous-v1.json -m baseline
```

Measures **precision** (avoid false activations) and **recall** (catch valid triggers), not just raw activation rate. See [evals/](evals/) for the framework and [evals/docs/why-evals-matter.md](evals/docs/why-evals-matter.md) for the philosophy.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
