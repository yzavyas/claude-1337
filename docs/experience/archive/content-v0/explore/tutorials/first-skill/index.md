# your first skill activation

Hands-on walkthrough: activate terminal-1337 and observe what happens.

## goal

Understand skill activation by watching it happen in real-time.

## prerequisites

- Claude Code installed
- claude-1337 marketplace added
- core-1337 and terminal-1337 installed

(If not, run [quick start](/start/) first)

## step 1: fresh session

Restart Claude Code to activate the SessionStart hook:

```bash
# Exit Claude Code completely, then restart
```

You should see output from core-1337's hook (might be subtle - just a context injection).

## step 2: activate terminal-1337

Ask a question that should activate the skill:

```
"What's the fastest way to search for function definitions in my Rust project?"
```

## step 3: observe activation

Watch Claude's response. It should:

1. **Mention checking skills** (if verbose) or just activate silently
2. **Invoke terminal-1337**
3. **Recommend `rg "fn \w+"`** (ripgrep pattern)
4. **Explain why rg > grep** (10x faster, respects .gitignore)

## step 4: verify tool knowledge

The skill loaded reference docs for 8 tools. Test knowledge:

```
"What's the modern alternative to find for searching files by name?"
```

Expected: Claude recommends `fd`, explains simpler syntax and speed.

## step 5: fallback behavior

Ask about a tool terminal-1337 doesn't cover:

```
"What's a good terminal file manager?"
```

Expected: Claude responds from base knowledge, doesn't mention terminal-1337.

## what you learned

- **Skill descriptions are activation triggers** - "search files", "grep patterns" matched terminal-1337
- **Skills load on-demand** - SKILL.md only loaded when activated
- **Activation is selective** - irrelevant questions don't activate
- **Core-1337 matters** - without it, extensions activate unreliably

## troubleshooting

**Claude didn't activate terminal-1337?**

Check if it's loaded:
```
"List all skills in your <available_skills> block with their descriptions."
```

If terminal-1337 is missing → truncation problem. See [explanation/activation](../../explanation/ecosystem/activation/).

If present but didn't activate → description needs work or core-1337 not installed.

**Want to test systematically?**

See [how-to: test skill activation](../../how-to/#test-skill-activation) for eval framework usage.

## next steps

- [Understand activation](../../explanation/ecosystem/activation/) - research on extension activation
- [Browse other plugins](../../reference/catalog/) - rust-1337, sensei-1337, etc
- [Build your own plugin](../custom-plugin/) - step-by-step guide
