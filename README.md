# claude-1337

**Yo dawg, I heard you like Claude Code, so we put 1337 skills in your Claude Code so you can 1337 while you code.**

Best-in-class tooling, practices, and learnings from industry leaders and master craftsmen. Not catalogs of options — THE answer for each use case.

## Get Started

```bash
/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337
```

_Install core-1337 first — it activates 1337 mode (forced skill checking, decisions over catalogs)_

## Why claude-1337

- **84% activation rate** vs 20% baseline — forced skill evaluation before every response
- **Production-proven** decisions — what ripgrep, servo, cloudflare actually use (not GitHub stars)
- **Decision frameworks** — "use tokio" not "options include tokio, async-std, smol"

## Plugins

| Plugin | Description | Components |
|--------|-------------|------------|
| [core-1337](plugins/core-1337/) | The foundation (install first) | hooks |
| [terminal-1337](plugins/terminal-1337/) | Modern CLI tools (rg, fd, bat, eza, fzf, xh, jq, atuin) | skills, hooks |
| [rust-1337](plugins/rust-1337/) | Rust development decisions across 12 domains | skills |
| [1337-skill-creator](plugins/1337-skill-creator/) | Skill authoring methodology | skills |
| [sensei-1337](plugins/sensei-1337/) | Teaching methodology (Feynman + Diataxis) | skills, agents |

**[Browse the interactive catalog →](https://yzavyas.github.io/claude-1337/reference/catalog/)**

## How these were built

1. **Learn** from domain experts, core maintainers, and reputable technical blogs
2. **Validate** against production codebases — what actually ships, not just what's popular
3. **Distill** — cut what Claude already knows, keep non-obvious decisions and gotchas
4. **Format** as decision tables, not prose explanations

**Philosophy**: Best-in-class only. Not catalogs of options — THE answer for each use case.

The methodology is documented in [1337-skill-creator](plugins/1337-skill-creator/).

## The Research

Skills fail 80% of the time due to three problems:

1. **Activation crisis** — skills activate ~20% of the time by default
2. **Decision paralysis** — catalogs of options instead of THE answer
3. **Knowledge gap** — generic training data instead of production evidence

**[Read why skills fail and how we fixed it →](https://yzavyas.github.io/claude-1337/explanation/)** — research from Scott Spence's 200+ test study and the claude-1337 validation framework.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
