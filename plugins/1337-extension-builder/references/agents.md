# Agents

Templates, best practices, and observability for agent extensions.

---

## Template

```yaml
---
name: agent-name
description: "What it does. Use when: [trigger]. Use PROACTIVELY when [condition]."
tools: Read, Grep, Glob
model: sonnet
---

# Agent Name

You are a specialized agent for [purpose].

## Role

[Clear description of what this agent does]

## Process

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Completion Criteria

You are done when:
- [Condition 1]
- [Condition 2]

## Output Format

[Expected output structure]
```

---

## Tool Permissions by Role

| role | tools | use case |
|------|-------|----------|
| Read-only | Read, Grep, Glob | reviewers, auditors |
| Research | Read, Grep, Glob, WebFetch, WebSearch | analysts |
| Code writers | Read, Write, Edit, Bash, Glob, Grep | implementers |
| Full access | (all) | general purpose |

---

## Agent Patterns

| pattern | use case | tools | completion |
|---------|----------|-------|------------|
| **explorer** | codebase search | Read, Grep, Glob | found target or exhausted search |
| **verifier** | validation, testing | Read, Grep, Bash | pass/fail determined |
| **researcher** | web synthesis | WebFetch, WebSearch, Read | question answered |
| **planner** | architecture | Read, Grep, Glob | plan documented |

---

## Best Practices

| practice | why |
|----------|-----|
| Single responsibility | Clear completion criteria |
| Limited tool access | Security + focus |
| Explicit skill listing | Skills not inherited from parent |
| Clear completion criteria | Agent knows when done |
| "PROACTIVELY" in description | Encourages auto-delegation |
| Explicit output format | Consistent results |

### Critical Constraint

**Subagents cannot spawn other subagents.** No nesting.

### Description Keywords

| keyword | effect |
|---------|--------|
| "Use when:" | Helps Claude decide when to delegate |
| "PROACTIVELY" | Encourages autonomous use |
| "MUST BE USED" | Strong trigger |

---

## Observability

### Tracing

```python
def run_agent(task: str):
    with tracer.start_as_current_span("agent") as agent_span:
        agent_span.set_attribute("task", task)
        agent_span.set_attribute("agent_name", self.name)
        agent_span.set_attribute("model", self.model)

        step = 0
        while not done:
            step += 1

            with tracer.start_as_current_span("llm_call") as llm_span:
                llm_span.set_attribute("step", step)
                response = call_llm(messages)
                llm_span.set_attribute("input_tokens", response.usage.input)
                llm_span.set_attribute("output_tokens", response.usage.output)
                llm_span.set_attribute("model", response.model)

            for tool_call in response.tool_calls:
                with tracer.start_as_current_span("tool_call") as tool_span:
                    tool_span.set_attribute("tool_name", tool_call.name)
                    tool_span.set_attribute("tool_args", str(tool_call.args)[:500])
                    result = execute_tool(tool_call)
                    tool_span.set_attribute("success", not result.error)
                    tool_span.set_attribute("result_size", len(str(result)))

        agent_span.set_attribute("total_steps", step)
        agent_span.set_attribute("success", True)
        agent_span.set_attribute("total_tokens", total_tokens)
```

### Spans

| span | attributes |
|------|------------|
| `agent` | task, agent_name, model, total_steps, success, total_tokens |
| `llm_call` | step, model, input_tokens, output_tokens |
| `tool_call` | tool_name, tool_args, success, result_size |

### Metrics

| metric | meaning |
|--------|---------|
| Steps per task | Agent efficiency |
| Tokens per task | Cost indicator |
| Tool call distribution | Which tools used most |
| Completion rate | % of tasks completed successfully |

---

## Quality Checklist

- [ ] Single responsibility
- [ ] Minimal tools for the role
- [ ] Clear completion criteria
- [ ] No nesting assumption
- [ ] "PROACTIVELY" if auto-delegating
- [ ] Output format documented
- [ ] Tested with representative tasks
