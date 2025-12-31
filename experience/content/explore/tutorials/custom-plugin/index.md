# build a custom plugin

Create a minimal plugin from scratch to understand the structure.

## goal

Build **python-1337** - a skill with production Python patterns.

## prerequisites

- Claude Code with claude-1337 marketplace
- Text editor
- Basic familiarity with [architecture](../../explanation/architecture/)

## step 1: create plugin structure

```bash
mkdir -p python-1337/.claude-plugin
mkdir -p python-1337/skills
```

## step 2: plugin metadata

Create `python-1337/.claude-plugin/plugin.json`:

```json
{
  "name": "python-1337",
  "version": "0.1.0",
  "description": "Production Python patterns - typing, async, packaging",
  "author": {
    "name": "your-name",
    "email": "you@example.com"
  },
  "license": "MIT"
}
```

## step 3: skill content

Create `python-1337/skills/SKILL.md`:

```yaml
---
name: python-1337
description: "Production Python patterns. Use when: type hints, async/await, packaging, virtual envs. Covers: mypy, ruff, uv, pyproject.toml."
---

# Python Production Patterns

## Type Hints

| Pattern | Use | Don't |
|---------|-----|-------|
| Function args | `def foo(x: int) -> str:` | `def foo(x):` |
| Optional | `x: int \| None` | `x: Optional[int]` (3.10+) |
| Generics | `list[str]`, `dict[str, int]` | `List[str]`, `Dict` |

## Async

**Runtime:** use asyncio (stdlib)

**Patterns:**
- `async def` for I/O-bound operations
- `await` for other async functions
- `asyncio.gather()` for parallel tasks
- Avoid `asyncio.run()` in libraries (let caller control event loop)

## Packaging

**Tool:** use `uv` (rust-based, 10x faster than pip/poetry)

```bash
uv init              # create pyproject.toml
uv add requests      # add dependency
uv sync              # install lockfile
uv run pytest        # run in venv
```

**pyproject.toml:**
```toml
[project]
name = "mylib"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.31.0"]
```

## Linting

**Use ruff** (rust-based, replaces black + flake8 + isort):

```bash
ruff check .         # lint
ruff format .        # format
```

## Type Checking

**Use mypy:**

```bash
mypy --strict mylib/
```

**Config:**
```toml
[tool.mypy]
strict = true
warn_return_any = true
```
```

## step 4: test locally

Load the plugin in Claude Code:

```bash
# From your plugin directory
claude code --plugin ./python-1337
```

Ask: "What's the modern way to manage Python dependencies?"

Expected: Claude activates python-1337, recommends `uv`.

## step 5: improve description

If activation is low (&lt;80%), revise the description:

**Bad:** "Helps with Python development"
**Good:** "Production Python patterns. Use when: type hints, async/await, packaging. Covers: mypy, ruff, uv."

**Why good:**
- "Use when:" clause with explicit activation triggers
- Specific tools mentioned (mypy, ruff, uv)
- Front-loaded keywords (Python, type hints, async)

## step 6: validate activation

Use the eval framework:

```bash
cd /path/to/claude-1337/evals
uv run skill-test test "how do i add type hints?" -s python-1337 -n 5
```

Target: 80%+ activation rate

## what you learned

- **Plugin structure** - `.claude-plugin/plugin.json` + `skills/SKILL.md`
- **Skill format** - YAML skill description (frontmatter) + markdown content
- **Description is critical** - determines activation
- **Content structure** - tables > prose, decision frameworks > reference docs

## next steps

- [Test systematically](../../how-to/#test-skill-activation) - run eval suites
- [Study 1337-skill-creator](../../reference/1337-skill-creator/) - full methodology
- [Understand activation](../../explanation/activation/) - why 84% vs 20%
- [Contribute](../../reference/catalog/) - submit to claude-1337 marketplace

## advanced topics

**Add commands:**
```bash
mkdir python-1337/commands
echo "Run mypy strict type checking on project" > python-1337/commands/typecheck.md
```

**Add hooks:**
```bash
mkdir python-1337/hooks
# Create SessionStart hook with Python best practices reminder
```

**Add agents:**
```bash
mkdir python-1337/agents
# Create specialized agent for refactoring to type hints
```

See [extensibility](../../explanation/extensibility/) for details.
