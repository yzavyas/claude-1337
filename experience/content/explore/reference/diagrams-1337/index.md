<p style="color: var(--fg-dim);">proactive diagram generation with evidence-based tool selection</p>

## what this is

diagrams-1337 makes claude diagram-aware. it answers: what diagram type should i use? when should i use mermaid vs d2?

two components:

| component | what it does |
|-----------|--------------|
| **skill** | decision frameworks - diagram type selection, tool choice, platform gotchas |
| **agent: davinci** | deep architecture diagramming - generates comprehensive diagram suites |

## the answer

**default to mermaid** (95% of cases). zero build step, native github/gitlab rendering.

| scenario | tool | why |
|----------|------|-----|
| documentation in github/gitlab | mermaid | native rendering, instant sync with code |
| complex cloud architecture (50+ nodes) | d2 | superior layouts, precise control |
| c4 model with sprites | c4-plantuml | production-proven, standardized (rare, &lt;1%) |

## diagram type selection

stop defaulting to flowcharts. choose by context:

| context | diagram type |
|---------|--------------|
| api interactions, service calls | `sequenceDiagram` |
| database schema, data model | `erDiagram` |
| state-based behavior | `stateDiagram-v2` |
| git workflow, branching | `gitGraph` |
| cloud/service architecture | `architecture-beta` or d2 |
| process with decisions | `flowchart` (only then!) |
| priority matrix | `quadrantChart` |
| hierarchical concepts | `mindmap` |

## production gotchas

| trap | fix |
|------|-----|
| using newest mermaid features | github uses ~10.0.2, gitlab 10.6.0. test on target platform. |
| flowcharts for everything | sequence for api calls, state for lifecycles, er for data |
| assuming github pages works | jekyll blocks mermaid. need plugin config or pre-render. |
| ignoring mobile | ios github app shows raw code. test if mobile matters. |
| silent syntax failures | validate with mermaid live editor (mermaid.live) |

## the davinci agent

invoke for deep architecture work:

```
Task(
  subagent_type="diagrams-1337:davinci",
  prompt="Generate architecture diagrams for the e-commerce platform"
)
```

the agent generates comprehensive diagram suites:

- **context** - system boundary, external dependencies
- **container** - services, databases, communication
- **sequence** - critical api flows
- **state** - entity lifecycles
- **data model** - entity relationships (if applicable)

## decision framework

choose by information type:

| type | diagram |
|------|---------|
| temporal/sequential | sequence, timeline, gantt, gitgraph |
| structural/static | class, er, architecture |
| behavioral/dynamic | state, flowchart, journey |
| analytical/comparative | quadrant, pie, sankey |

## when to upgrade to d2

only when all of these are true:

- diagram has 50+ nodes or complex architecture
- mermaid's auto-layout produces poor results
- team can accept build step in workflow
- native github/gitlab rendering not required

otherwise, use mermaid.

## rationale: why diagrams work

this plugin is grounded in cognitive science research on diagram effectiveness:

### cognitive load theory (sweller, 1988)

properly designed diagrams reduce extraneous cognitive load by integrating information that would otherwise require split attention. embedding labels within diagrams (spatial contiguity) reduces mental integration effort.

### dual coding theory (paivio, 1971)

the mind processes information through two channels: verbal and visual. presenting information through both channels enhances encoding and recall. diagrams + text > diagrams alone or text alone.

### cognitive fit theory (vessey, 1991)

performance is superior when representation format matches task type:

| task type | best representation | why |
|-----------|---------------------|-----|
| spatial tasks (relationships, patterns) | diagrams | facilitate viewing without analytical attention |
| symbolic tasks (precise values, sequential) | tables, text | facilitate analytical processing |

### research findings

- **uml effectiveness**: reduces maintenance time by 22-60% (sharif & maletic)
- **comprehension boost**: moderate positive effect (hedges's g = 0.39) on comprehension (guo et al., 2020)
- **active construction**: effect size 0.82 when learners construct diagrams vs just studying them (nesbit & adesope, 2006)
- **split-attention effect**: integrated diagrams > separate text and images (chandler & sweller, 1992)

### when diagrams help

- showing spatial/relational information (architecture, dependencies)
- reader has adequate prior knowledge
- pattern recognition matters more than precision
- complexity is manageable (5-10 elements per diagram)

### when diagrams hurt

- visual complexity creates "hairball" visualizations
- precision matters more than patterns (use tables)
- decorative only, not instructive (sung & mayer, 2012)
- reader lacks prerequisite knowledge

## production evidence

built from production patterns with verified sources:

- **kubernetes** - [official diagram guide](https://kubernetes.io/docs/contribute/style/diagram-guide/) mandates mermaid for all contributor documentation
- **gitlab** - [internal handbook](https://handbook.gitlab.com/handbook/tools-and-tips/mermaid/) uses mermaid extensively for workflows and architecture
- **azure devops** - [native mermaid rendering](https://azuredevops.tips/wikimermaid-diagrams/) in wikis and documentation
- **terraform** - [terramaid](https://github.com/RoseSecurity/Terramaid) generates mermaid diagrams from terraform configs, 1.2k+ stars

### tool selection rationale

- **mermaid default**: zero friction (instant github/gitlab rendering) trumps polish 95% of the time
- **d2 for complexity**: superior layout engines justified only when mermaid produces poor results (50+ nodes)
- **c4-plantuml rare**: only for formal c4 models requiring standardized sprites (&lt;1% of cases)

## structure

```
plugins/diagrams-1337/
├── .claude-plugin/plugin.json
├── SKILL.md              # decision frameworks
├── agents/
│   └── davinci.md        # architecture specialist
└── references/
    ├── mermaid-types.md  # complete catalog
    ├── d2.md             # when to use d2
    ├── c4-architecture.md # c4 model patterns
    └── gotchas.md        # debugging, platforms
```

## sources

- [mermaid official docs](https://mermaid.js.org) - comprehensive syntax reference
- [d2 official docs](https://d2lang.com) - declarative diagramming
- [kubernetes diagram guide](https://kubernetes.io/docs/contribute/style/diagram-guide/) - production usage
- [c4 model](https://c4model.com) - architecture documentation standard
- [gitlab mermaid guide](https://handbook.gitlab.com/handbook/tools-and-tips/mermaid/) - production patterns
