# diagrams-1337

Elite diagram-as-code for documentation and architecture visualization.

## What

Proactive diagram generation with evidence-based tool selection. Makes Claude diagram-aware and helps choose the right diagram type for each context.

## Philosophy

**Default to Mermaid** (95% of cases) - zero build step, native GitHub/GitLab rendering
**Upgrade to D2** when complex architecture needs precise layouts
**Know when to use which diagram type** - stop defaulting to flowcharts

## Contains

- **SKILL.md**: Decision frameworks for diagram types and tools
- **davinci agent**: Deep architecture diagramming specialist
- **References**: Mermaid types, D2 usage, C4 model, gotchas

## Key Decisions

| Context | Diagram Type |
|---------|-------------|
| API interactions | `sequenceDiagram` |
| State machines | `stateDiagram-v2` |
| Database schema | `erDiagram` |
| Git workflows | `gitGraph` |
| Architecture | `architecture-beta` or D2 |
| Process flow | `flowchart` (only when actually a process!) |

## Evidence

Built from production patterns used by:
- Kubernetes (official diagram guide)
- GitLab (internal handbook)
- Azure DevOps (native wiki support)
- Terraform ecosystem (Terramaid)

## Usage

The skill activates automatically when you're:
- Writing documentation
- Explaining architecture
- Documenting APIs
- Showing workflows

Claude will proactively offer appropriate diagrams.

For deep architecture work, Claude may spawn the davinci agent automatically to generate comprehensive diagram suites.

## Production Gotchas Covered

- GitHub/GitLab version lag (newer diagram types may not work)
- Platform-specific rendering issues
- Arrow syntax differences by diagram type
- When Mermaid isn't enough (complex architecture)
- Security considerations for user-generated diagrams

## License

MIT
