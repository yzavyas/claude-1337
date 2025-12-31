# start

**yo dawg**, i heard you like claude code, so we put 1337 skills in your claude code so you can 1337 while you code.

## what is this?

claude-1337 is a marketplace of **cognitive extensions** for Claude Code — skills, hooks, agents, and commands that extend what Claude knows, how it reasons, and what it can do. best-in-class tooling from production codebases, not training data.

think of it as packages for Claude's brain.

## get started

```
/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337
```

*install core-1337 first — it activates 1337 mode (forced skill checking, decisions over catalogs)*

## why claude-1337

| baseline | with core-1337 |
|----------|----------------|
| 20% skill activation | 84% skill activation |

- **forced activation** — explicit skill evaluation before every response. no more ignored skills.
- **production-proven** — what ripgrep, servo, cloudflare actually use. not github stars.
- **decision frameworks** — "use tokio" not "options include tokio, async-std, smol"

## plugins

carefully curated plugins with production-proven knowledge — modern CLI tools, rust development decisions, skill authoring methodology, teaching frameworks.

[browse the interactive catalog](../explore/reference/catalog.md) to filter by component type (skills, hooks, agents, commands, mcp) and search by keywords.

## more plugins

```
/plugin install terminal-1337@claude-1337     # modern CLI tools
/plugin install rust-1337@claude-1337         # rust production patterns
/plugin install sensei-1337@claude-1337       # teaching methodology
/plugin install diagrams-1337@claude-1337     # diagram-as-code
/plugin install eval-1337@claude-1337         # rigorous evals
```

## methodology

1. **learn** from domain experts, core maintainers, reputable technical blogs
2. **validate** against production codebases — what actually ships
3. **distill** — cut training knowledge, keep non-obvious decisions
4. **format** as decision tables, not prose

full methodology in [1337-skill-creator](../explore/reference/1337-skill-creator.md).

## the research

skills fail 80% of the time due to three problems:

1. **activation crisis** — skills activate ~20% of the time by default
2. **decision paralysis** — catalogs of options instead of THE answer
3. **knowledge gap** — generic training data instead of production evidence

[read why skills fail and how we fixed it](../explore/explanation/) — research from scott spence's 200+ test study and the claude-1337 validation framework.

---

## trouble?

[how-to](../explore/how-to/) — includes skill debugging tips
