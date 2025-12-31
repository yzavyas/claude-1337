[&larr; explanation](../)

# models

<p class="dimmed-intro">understanding how claude models work in claude code</p>

## what is a model?

think of a model like different versions of claude with different capabilities. it's like having a team where:

- **opus** is the senior architect - best at complex reasoning, planning, and difficult problems. slow but thorough.
- **sonnet** is the experienced developer - balanced between speed and quality. handles most tasks well.
- **haiku** is the junior developer - fast at simple, repetitive tasks. uses less resources.

each model is trained on the same data but with different "brain sizes" (parameters). larger models can hold more patterns and make more nuanced decisions.

## how claude code uses models

claude code defaults to sonnet for most work. but you can specify which model to use for specific tasks:

```bash
# use opus for complex planning
claude --model opus "design the architecture for..."

# use haiku for simple repetitive tasks
claude --model haiku "run tests"
```

### when agents spawn sub-agents

agents can spawn sub-agents with different models. think of it like delegating:

```
Main agent (sonnet):
  ├─ Complex analysis → spawn opus agent
  ├─ Simple file search → spawn haiku agent
  └─ Code review → spawn sonnet agent
```

this is what the Task tool does when you see `model: "haiku"` in tool parameters.

## model selection strategy

| task type | recommended model | why |
|-----------|------------------|-----|
| architecture design, complex planning | opus | needs deep reasoning, multi-step planning |
| code generation, refactoring, debugging | sonnet | balanced speed and quality |
| file search, simple edits, test runs | haiku | fast, cost-effective, sufficient capability |
| code review, explanation, research | sonnet or opus | needs nuance and context understanding |

## cost vs capability tradeoff

models have different costs (in both time and tokens):

- **opus** - slowest, most expensive, highest quality
- **sonnet** - balanced middle ground (default for good reason)
- **haiku** - fastest, cheapest, good for simple tasks

the key insight: don't use opus for everything just because it's "best". use the right tool for the job. a haiku agent searching files is faster and cheaper than opus doing the same task.

## how models interact with skills

all models can use skills, but they evaluate skill relevance differently:

- **opus** - better at matching vague descriptions to user intent
- **sonnet** - good skill matching with clear descriptions
- **haiku** - needs very explicit "use when:" clauses

this is why skill descriptions matter so much - they need to work across all model tiers.

## model versioning

models get updated over time. when you see `claude-sonnet-4-5-20250929`, that's:

- `claude` - the model family
- `sonnet-4-5` - the version (4.5)
- `20250929` - the release date (sept 29, 2025)

claude code automatically uses the latest stable version. you don't need to specify the date suffix.

## extending with custom model integrations

claude code is designed for anthropic models (opus, sonnet, haiku). for other model providers:

- **openai, gemini, llama** - not directly supported in claude code cli
- **custom agents** - can be built with the claude agent sdk to wrap other models
- **mcp servers** - can provide model-agnostic tool interfaces

see [extensibility](../extensibility/) for how to integrate other systems.
