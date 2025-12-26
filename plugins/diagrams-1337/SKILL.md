---
name: diagrams-1337
description: "Proactive diagram generation for documentation. Use when: writing docs, explaining architecture, documenting APIs, showing workflows, git branching, state machines, data models. Covers: Mermaid (sequenceDiagram, stateDiagram, erDiagram, gitGraph, flowchart, C4, timeline), D2 for complex architecture, decision frameworks."
---

# Diagrams-1337: Elite Diagram-as-Code

Proactive, evidence-based diagram generation. Default to Mermaid, upgrade to D2 only when necessary.

## Tool Selection (THE Answer)

| Scenario | Tool | Why |
|----------|------|-----|
| **Documentation in GitHub/GitLab** | **Mermaid** | Zero build step, native rendering, instant sync with code |
| **Complex cloud architecture** | **D2** | Superior layouts, precise control (accept build step trade-off) |
| **C4 model with sprites** | **C4-PlantUML** | Production-proven, standardized notation (rare, <1%) |
| **95% of all cases** | **Mermaid** | Zero friction beats polish |

**Evidence**: Kubernetes, GitLab, Azure DevOps, Terraform tooling all default to Mermaid for documentation.

## Decision Framework: Context → Diagram Type

### Proactive Offering

When explaining these concepts, **offer diagrams automatically**:

| Context | Diagram Type | Example |
|---------|-------------|---------|
| API interactions, service calls | `sequenceDiagram` | kubectl → API server → scheduler |
| Process with decisions/branches | `flowchart` | Deployment pipeline with approval gates |
| Database schema, data model | `erDiagram` | Users, Posts, Comments relationships |
| State-based behavior | `stateDiagram-v2` | Order lifecycle: pending → paid → shipped |
| Class structure, OOP design | `classDiagram` | Interface implementations, inheritance |
| Git workflow, branching | `gitGraph` | Feature branches, releases, hotfixes |
| Cloud/service architecture | `architecture-beta` or D2 | Microservices, load balancers, databases |
| Project timeline, roadmap | `gantt` | Milestones, dependencies, durations |
| Hierarchical concepts | `mindmap` | System components, knowledge organization |
| Chronological events | `timeline` | Product history, migration phases |
| Priority/effort matrix | `quadrantChart` | Feature prioritization (impact/effort) |
| Flow quantities | `sankey` | Traffic sources, resource allocation |
| Workflow states | `kanban` | Todo, doing, done columns |

### Don't Default to Flowcharts

**Trap**: Claude defaults to flowcharts for everything.

**Fix**: Choose by information type:
- **Temporal** (interactions over time) → `sequenceDiagram`
- **State-based** (distinct modes) → `stateDiagram-v2`
- **Structural** (relationships) → `classDiagram` or `erDiagram`
- **Process** (algorithm, decisions) → `flowchart` (only then!)

## Cognitive Principles (When Diagrams Work)

**Grounded in cognitive science**: Cognitive Load Theory (Sweller), Dual Coding (Paivio), Cognitive Fit (Vessey)

### Use Diagrams When

| Condition | Why | Research |
|-----------|-----|----------|
| **Spatial/relational information** | Architecture, dependencies, hierarchies | Cognitive Fit Theory - spatial tasks → diagrams |
| **Pattern recognition > precision** | Relationships matter more than exact values | Vessey (1991) - graphs for spatial tasks |
| **Reader has prior knowledge** | Can interpret domain notation (UML, C4) | Diagrams ineffective without prerequisites |
| **Complexity manageable (5-10 elements)** | Avoids "hairball" visualizations | Cognitive Load research |

### Use Tables/Text When

| Condition | Why |
|-----------|-----|
| **Precision > patterns** | Exact values, configuration specs |
| **Sequential processing** | Step-by-step procedures, algorithms |
| **Abstract concepts** | No spatial/visual properties |
| **Reader lacks background** | Diagrams increase confusion |

### Design Principles

**Spatial Contiguity** (Mayer): Embed labels in diagrams, not in separate legends
**Coherence** (Mayer): Remove decorative elements. Instructive > pretty.
**Dual Coding** (Paivio): Provide diagram + text description (visual + verbal channels)
**Complexity Limit**: 5-10 elements per diagram. Split complex systems into multiple views.

**Research**: UML diagrams reduce maintenance time 22-60% (Sharif & Maletic). Effect size 0.82 when constructing diagrams (Nesbit & Adesope, 2006).

## Production Gotchas

| Trap | Fix |
|------|-----|
| Using newest Mermaid features | GitHub uses ~10.0.2, GitLab 10.6.0. Test on target platform. Avoid `architecture-beta`, `timeline`, `mindmap` for GitHub deployment. |
| Flowcharts for everything | Pick appropriate type: sequence for API calls, state for lifecycles, ER for data models |
| Assuming GitHub Pages works | Jekyll blocks Mermaid. Need manual plugin config or pre-render. |
| Ignoring mobile | iOS GitHub app shows raw code, not diagrams. Test on mobile if that's your audience. |
| Silent syntax failures | Validate with Mermaid Live Editor (mermaid.live) before commit. Bad parameters fail silently. |
| Overly complex diagrams | Keep focused. One diagram per concept. Split mega-diagrams into multiple views. |
| Using D2 unnecessarily | Build step adds friction. Only use when Mermaid's layout is genuinely poor. |
| Trusting AI-generated syntax | Always validate. Claude makes arrow syntax errors, typos, unsupported features. |
| User-generated Mermaid in production | Security risk. HTML characters bypass sanitization. Use dedicated Mermaid sanitizer. |

## Platform Compatibility

| Platform | Mermaid Version | Notes |
|----------|----------------|-------|
| GitHub | ~10.0.2 (2024) | Lags official. Newer types may not render. |
| GitLab | 10.6.0 (Oct 2023) | Brief flicker on load (client-side render). |
| GitHub Pages | Doesn't work | Jekyll safe mode blocks. Need plugin. |
| Azure DevOps | Native support | Wikis render Mermaid. |
| Official | 11.x+ | Cutting edge features unavailable on platforms. |

**Test diagrams on target platform before production.**

## Diagram Type Quick Reference

### Temporal/Sequential
- `sequenceDiagram` - Object interactions over time
- `timeline` - Chronological events
- `gantt` - Project schedule with dependencies
- `gitGraph` - Version control branching

### Structural/Static
- `classDiagram` - Code structure (OOP)
- `erDiagram` - Data structure (databases)
- `architecture-beta` - System structure (cloud/services)
- `c4Context` / `c4Container` - C4 model levels

### Behavioral/Dynamic
- `stateDiagram-v2` - State transitions
- `flowchart` - Process flow (algorithm)
- `journey` - User experience flow

### Analytical/Comparative
- `quadrantChart` - 2D comparison (prioritization)
- `pie` - Proportions
- `sankey` - Flow analysis with quantities
- `kanban` - Workflow visualization

## When to Upgrade from Mermaid to D2

**Only when**:
- Complex architecture (50+ nodes) where Mermaid's auto-layout is poor
- Precise positioning required for clarity
- Team willing to accept build step for better aesthetics
- Producing final diagrams for product documentation

**Not when**:
- Quick documentation (Mermaid's instant rendering wins)
- Team collaboration (Mermaid's zero setup wins)
- Need Gantt, timeline, or mindmap (D2 doesn't support)

## Syntax Validation Checklist

Before committing diagrams:
- [ ] Tested in Mermaid Live Editor (mermaid.live)
- [ ] Verified diagram type supported on target platform (GitHub/GitLab version)
- [ ] Used correct arrow syntax for diagram type (varies by type)
- [ ] Added descriptive labels and titles
- [ ] Checked diagram renders on mobile (if relevant)
- [ ] Kept diagram focused (one concept, not mega-diagram)
- [ ] Validated security if accepting user input

## Layout Optimization

| Issue | Fix |
|-------|-----|
| Wide diagram cut off | Use `LR` (left-right) instead of `TB` (top-bottom) |
| Too many nodes cluttered | Split into multiple diagrams or use subgraphs |
| Hard to follow flow | Add descriptive labels, use consistent naming |
| Poor automatic layout | Try D2 (accept build step) or manual grouping |

## Domain Routing

For deep dives, load references:

| Detected | Load |
|----------|------|
| Mermaid syntax, diagram types | [mermaid-types.md](references/mermaid-types.md) |
| D2 usage, when to switch | [d2.md](references/d2.md) |
| Architecture diagrams, C4 model | [c4-architecture.md](references/c4-architecture.md) |
| Platform issues, debugging | [gotchas.md](references/gotchas.md) |

---

**Evidence sources**: Kubernetes diagram guide, GitLab handbook, Mermaid official docs, D2 official docs, C4 model docs, production codebases (Terramaid, K8s-docs-mermaid), community research (Mermaid vs D2 comparisons).
