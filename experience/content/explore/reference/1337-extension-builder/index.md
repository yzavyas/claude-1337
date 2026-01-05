# 1337-extension-builder

Build Claude extensions - skills, hooks, agents, commands, MCP servers.

---

## install

```
/plugin install 1337-extension-builder@claude-1337
```

## what it provides

**Methodology** for building high-quality extensions:
- Evidence-based research workflow
- Content triage framework
- Quality gates (sources, evidence tier, CoVe)
- First principles thinking

**Executable prompts** that guide extension creation step-by-step.

## usage

After installation, ask Claude to help build an extension:

```
"Help me build a skill for Kubernetes deployments"
```

The extension-builder skill activates and guides you through:
1. Research phase (gathering sources)
2. Content triage (what to include)
3. Skill authoring (format, description, activation)
4. Validation (testing activation rates)

## quality gates

| gate | principle |
|------|-----------|
| sources | Multiple independent sources — if limited, acknowledge explicitly |
| evidence | Use highest quality available — production > maintainer > blog |
| claims | Each claim traceable to source (author, year, context) |

## reference docs

The plugin includes detailed reference material:
- `references/research-workflow.md` - full research process
- `references/content-triage.md` - what to include/exclude
- `references/skill-process.md` - authoring best practices

## see also

- [tutorials: build a custom plugin](/explore/tutorials/custom-plugin/)
- [explanation: extensibility](/explore/explanation/ecosystem/extensibility/)
- [explanation: activation](/explore/explanation/ecosystem/activation/)
