# Commands

Templates, best practices, and observability for command extensions.

---

## Template

```yaml
---
name: command-name
description: "What it does"
arguments:
  - name: target
    description: "What to operate on"
    required: true
  - name: options
    description: "Additional options"
    required: false
---

# Command: /command-name

You are executing the /command-name command.

## Arguments

$ARGUMENTS

## Process

1. [Step 1 with $ARGUMENTS.target]
2. [Step 2]
3. [Step 3]

## Output

[Expected format]
```

---

## Argument Schema

```yaml
arguments:
  - name: file
    description: "File to process"
    required: true
  - name: format
    description: "Output format (json, yaml, text)"
    required: false
    default: "json"
  - name: verbose
    description: "Enable verbose output"
    required: false
    type: boolean
```

### Accessing Arguments

In the command body, use `$ARGUMENTS`:
- `$ARGUMENTS.file` — single argument
- `$ARGUMENTS` — all arguments as object

---

## Command Patterns

| pattern | example | use case |
|---------|---------|----------|
| **commit workflow** | `/commit` | staged changes + message |
| **code review** | `/review-pr 123` | fetch and analyze |
| **diagnostics** | `/debug` | collect context |
| **generation** | `/scaffold component` | create from template |
| **query** | `/explain function` | answer questions |

---

## Best Practices

| practice | why |
|----------|-----|
| Predictable behavior | Same input → same process |
| Composable | Can chain with other commands |
| Documented arguments | Self-describing |
| Helpful errors | Guide user on failure |
| Idempotent where possible | Safe to retry |
| Clear output format | Consistent results |
| Validate early | Fail fast with clear message |

### Error Handling

```yaml
## Error Handling

If arguments are invalid:
- Report which argument failed
- Show expected format
- Suggest fix

If process fails:
- Report which step failed
- Preserve partial progress
- Suggest recovery
```

---

## Observability

### Tracing

```python
def execute_command(command: str, args: dict):
    with tracer.start_as_current_span("command") as span:
        span.set_attribute("command_name", command)
        span.set_attribute("arg_count", len(args))

        with tracer.start_as_current_span("command_parse") as parse_span:
            parsed = parse_args(args)
            parse_span.set_attribute("valid", parsed.valid)
            if not parsed.valid:
                parse_span.set_attribute("error", parsed.error)

        if parsed.valid:
            with tracer.start_as_current_span("command_execute") as exec_span:
                result = run_command(command, parsed)
                exec_span.set_attribute("success", result.success)
                exec_span.set_attribute("output_size", len(result.output))

        span.set_attribute("duration_ms", elapsed_ms())
        span.set_attribute("success", result.success if parsed.valid else False)
        return result
```

### Spans

| span | attributes |
|------|------------|
| `command` | command_name, arg_count, duration_ms, success |
| `command_parse` | valid, error |
| `command_execute` | success, output_size |

### Metrics

| metric | meaning |
|--------|---------|
| Invocation rate | Usage frequency |
| Success rate | % completed successfully |
| Argument errors | Common mistakes |
| Execution time | Performance |

---

## Quality Checklist

- [ ] Predictable behavior
- [ ] Arguments documented
- [ ] Required vs optional clear
- [ ] Helpful error messages
- [ ] Composable with other commands
- [ ] Clear output format
- [ ] Tested with edge cases
