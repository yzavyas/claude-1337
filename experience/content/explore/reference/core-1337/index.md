[&larr; reference](../)

# core-1337

the foundation. problem-solving methodology for coding, design, and technical work.

## install

```
/plugin install core-1337@claude-1337
```

**install this first**, then add domain skills.

## what it does

provides a structured problem-solving methodology:

| component | purpose |
|-----------|---------|
| **Evidence + WHY** | every recommendation needs reasoning and sources |
| **Scientific Method** | hypothesize → test → observe → refine |
| **Verification (CoVe)** | check your work systematically (+23% F1) |
| **Honesty** | calibrate confidence to evidence strength |

at session start, the hook injects:
- today's date (for current information lookup)
- tool reminders (WebSearch, WebFetch for current data)
- skill activation guidance

## the methodology

the full methodology is in [SKILL.md](https://github.com/yzavyas/claude-1337/blob/main/plugins/core-1337/SKILL.md) (245 lines). key elements:

### evidence + why

| component | what | why it matters |
|-----------|------|----------------|
| WHAT | the answer | without this, nothing actionable |
| WHY | the reasoning | enables validation and learning |
| EVIDENCE | the source | distinguishes knowledge from opinion |

### source hierarchy

| priority | source | why |
|----------|--------|-----|
| 1 | production codebases | what actually ships |
| 2 | core maintainers | primary knowledge holders |
| 3 | conference talks | war stories, real gotchas |
| 4 | proven adoption | social proof |
| 5 | technical blogs | secondary, verify |

### techniques

- **step-back prompting**: abstract principles before specifics (+36% vs direct)
- **chain of verification (CoVe)**: draft → question → check → refine (+23% F1)
- **quote-based grounding**: for long documents, extract quotes first

### behavioral awareness

common pitfalls the methodology addresses:
- **tests vs code**: don't modify tests to hide bugs
- **feedback incorporation**: articulate WHY the original was wrong
- **sycophancy**: agree only when you can explain why they're right
- **overconfidence**: match confidence to evidence strength

## structure

```
plugins/core-1337/
├── .claude-plugin/plugin.json
├── SKILL.md              # methodology (245 lines)
└── hooks/
    ├── hooks.json
    └── skill-eval.sh     # SessionStart context
```

## evaluation

| level | what | method |
|-------|------|--------|
| L1: Activation | does skill trigger correctly? | F1 with labeled test cases |
| L2: Behavioral | does Claude follow methodology? | LLM-as-judge rubric |

test cases in `evals/suites/rigorous-v1.json`.

## credits

- [Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - skill activation research
- [r/ClaudeAI: Anatomy of a Skill](https://www.reddit.com/r/ClaudeAI/comments/1pha74t/deep_dive_anatomy_of_a_skill_its_tokenomics_why/) - tokenomics
