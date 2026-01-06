# cognitive extensions for effective collaborative intelligence

claude-1337 is a marketplace of cognitive extensions — skills, hooks, agents, commands, and MCP servers that make collaboration actually work. Not just smarter AI. Smarter *together*.

*Plugins are the mechanism. Extensions are what they provide.*

---

## the problem

Human-AI collaboration fails by default.

[Vaccaro et al. (2024)](https://www.nature.com/articles/s41562-024-02024-1) meta-analyzed 106 studies. Human-AI combos perform **worse** than the best performer alone (g = -0.23). Content creation is the exception; decision-making reliably gets worse.

[METR (2025)](https://arxiv.org/abs/2507.09089) ran an RCT with 16 experienced developers. They were **19% slower** with AI tools. They perceived themselves **20% faster**.

[Gerlich (2025)](https://www.mdpi.com/2075-4698/15/1/6) found r = -0.75 between AI use and critical thinking. The correlation is strong and negative.

**The mechanism:**

| what happens | why it's bad |
|--------------|--------------|
| opaque abstractions | you consume output without understanding |
| cognitive offloading | you stop thinking through problems |
| capability atrophy | skills you don't use decline |
| miscalibrated confidence | you can't tell it's happening |

The default trajectory: offload more, think less, can't tell the difference.

---

## the method

Enhanced collaborative intelligence requires **bidirectional learning** — both human and AI develop capability through the collaboration.

| participant | what they learn | how |
|-------------|-----------------|-----|
| **human** | reasoning, evidence, tradeoffs | transparent abstractions, visible rationale |
| **claude** | corrections, context, domain specifics | feedback during session |
| **system** | crystallized knowledge | extensions persist, baseline improves |

The principles and ethos that go into extensions built for this marketplace are documented in [ethos](/ethos) and [craftsmanship](/explore/explanation/craftsmanship/).

---

## kaizen

```
collaboration → breakthrough → crystallization → improved baseline
```

When you figure something out with Claude, write it down. The file persists. Next session starts from that baseline. Corrections flow through too — the system gets more accurate, not just bigger.

The codebase gets smarter. Whether you do depends on whether you **engage** with the knowledge or just consume the output.

This is the design choice: extensions are readable. You can see how they work, learn from them, fork them, validate claims before trusting them. Kaizen — continuous improvement through small, iterative cycles.

---

## get started

```
/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337
```

[browse the catalog](/explore/reference/catalog)

---

## learn more

- [ethos](/ethos) — why this approach
- [explore](/explore/) — documentation, tutorials, reference
