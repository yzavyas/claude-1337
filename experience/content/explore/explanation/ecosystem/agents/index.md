[&larr; explanation](../)

# agents

<p class="dimmed-intro">understanding how autonomous agents work in claude code</p>

## what is an agent?

an agent is claude with a specific job and the tools to do it autonomously. think of it like this:

- **regular claude** - asks you for confirmation before every action. "should i edit this file?" "should i run this command?"
- **agent** - given a goal, figures out the steps and executes them without asking. "explore the codebase and find X" → does it.

agents are claude instances with:

1. **a specific goal** - "find all files that import X"
2. **access to tools** - Read, Grep, Glob, Bash, etc.
3. **autonomous execution** - makes decisions and calls tools without user input
4. **context awareness** - knows what it already tried, what worked, what failed

## how agents work

when you use the Task tool to spawn an agent, here's what happens:

```
1. User: "find all rust async functions"
2. Claude spawns Explore agent with that goal
3. Agent thinks: "I need to search for 'async fn' in .rs files"
4. Agent calls Grep tool: pattern="async fn", glob="*.rs"
5. Agent gets results, analyzes them
6. Agent calls Read tool on interesting files
7. Agent compiles findings
8. Agent returns report to main Claude
9. Main Claude shows you the results
```

key insight: agents run in the background. main claude doesn't wait - it can keep working or spawn more agents in parallel.

## agent types in claude code

| agent type | purpose | tools available |
|------------|---------|-----------------|
| general-purpose | complex multi-step tasks, research | all tools (Read, Edit, Grep, Bash, etc.) |
| Explore | fast codebase exploration | Read, Grep, Glob |
| Plan | implementation planning | Read, Grep, Glob (read-only) |
| custom agents | specialized tasks (e.g., sensei-1337's feynman agent) | whatever tools you give them |

## agents vs regular claude

| aspect | regular claude | agent |
|--------|----------------|-------|
| user input | asks for confirmation | autonomous (no asking) |
| tool access | all tools | subset of tools |
| context | full conversation history | task-specific context only |
| execution | synchronous (you wait) | can run in background |
| output | direct to user | returns to parent claude |

## when to use agents

use agents for tasks that are:

- **exploratory** - "find all places where X is used"
- **multi-step** - "search, analyze, compile report"
- **parallelizable** - "check these 5 directories simultaneously"
- **well-defined** - clear goal, measurable success

don't use agents for:

- **ambiguous tasks** - "make the code better" (what does better mean?)
- **single tool calls** - just use the tool directly
- **user interaction** - agents can't ask you questions mid-task

## agent lifecycle

```
┌─────────────┐
│ spawn agent │ ← Task tool called
└──────┬──────┘
       │
┌──────▼────────┐
│ agent running │ → calls tools autonomously
└──────┬────────┘
       │
┌──────▼──────┐
│ agent done  │ → returns results
└──────┬──────┘
       │
┌──────▼────────┐
│ claude uses   │ → incorporates findings
│ results       │
└───────────────┘
```

## building custom agents

you can build custom agents using the claude agent sdk. an agent is basically:

```python
# pseudo-code
agent = {
  name: "my-agent",
  description: "what it does",
  tools: [tool1, tool2, tool3],
  system_prompt: "instructions for the agent",
}
```

see [extensibility](../extensibility/) for how to build and integrate custom agents.

## agent communication

agents communicate with the parent claude through structured outputs:

- **findings** - results of exploration or analysis
- **errors** - what went wrong (if anything)
- **metadata** - files checked, tools used, time taken

the parent claude decides what to do with this information. maybe it spawns more agents, maybe it shows results to you, maybe it uses the findings to complete your task.

## parallel vs sequential agents

claude can spawn multiple agents:

- **parallel** - multiple agents running simultaneously (faster, but uses more resources)
- **sequential** - one agent after another (when later agents need earlier results)

```
# parallel (simultaneous)
Task: "search frontend"  ┐
Task: "search backend"   ├─ all run at once
Task: "search tests"     ┘

# sequential (one by one)
Task: "find entry points"      ← runs first
  → results feed into
Task: "trace dependencies"     ← runs second using first results
```

## agent context limits

agents have their own context windows separate from main claude. this means:

- agent doesn't see your full conversation history
- agent only knows what's in its task prompt
- agent results are summarized when returned to main claude

think of it like delegating to a colleague - you give them the relevant context, not your entire work history.
