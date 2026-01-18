# core-1337

Engineering excellence methodology for builders.

## What This Is

Software craftsmanship principles and practices for disciplined, evidence-based engineering. Not tutorials — standards, decision frameworks, and the reasoning behind them.

## When It Activates

- Writing code or making technical decisions
- Refactoring and code reviews
- Debugging (especially when stuck)
- Implementation work requiring quality standards

## What You Get

### The Skill (build-core)

Engineering methodology grounded in:
- Software Craftsmanship Manifesto principles
- Evidence-based decision making
- First principles reasoning
- Scientific method for verification

### The Agent (Mr. Wolf)

**Structured problem solver.** Gets called when you're stuck, going in circles, or debugging isn't converging.

Mr. Wolf:
1. Stops what isn't working
2. Clarifies what's actually happening
3. Identifies the type of problem
4. Breaks it down systematically
5. Verifies before declaring solved

### The Hooks (Automatic Assistance)

Two hooks detect patterns that need intervention:

| Hook | Detects | Response |
|------|---------|----------|
| `detect-debugging-loop` | 3+ consecutive failures | Spawns Mr. Wolf |
| `detect-frustration` | User frustration signals | Spawns Mr. Wolf |

**To disable hooks:** Set environment variable `SKIP_MRWOLF_HOOKS=1`

```bash
SKIP_MRWOLF_HOOKS=1 claude
```

## Structure

```
core-1337/
├── skills/build-core/
│   ├── SKILL.md              # Engineering methodology
│   └── references/           # Deep dives (verification, reasoning, etc.)
├── agents/
│   └── mrwolf.md             # Structured problem solver
├── hooks/
│   ├── hooks.json            # Hook configuration
│   ├── detect-debugging-loop.sh
│   ├── detect-frustration.sh
│   └── session-start.sh      # Session transparency
└── scripts/                  # Installation helpers
```

## Philosophy

**You're not done when it works. You're done when it's right.**

Everything you create becomes part of a system others depend on. Your work is inherited. Your standards are inherited. Do the right thing because it's right.
