# collaborative intelligence

## what works

After testing prompts, hooks, and skills - and studying what Anthropic recommends - a clear pattern emerges:

| approach | result |
|----------|--------|
| Commands (MUST, MANDATORY, CRITICAL) | Compliance, brittleness, ceiling at ~84% |
| Motivation (here's why, here's the value) | Understanding, appropriate judgment |

This might seem counterintuitive. Surely more forceful instructions produce more reliable behavior?

In practice, no. Here's why it works the other way.

## the evidence

**1. Anthropic's guidance**

Claude is [Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) - trained with values and principles, not rigid rules. [The soul document](https://simonwillison.net/2025/Dec/2/claude-soul-document/) describes *who Claude is*, not commands to follow.

The architecture is built for judgment, not compliance.

**2. Scott Spence's activation study**

200+ tests showed forced eval prompts hit ~84% activation - but that's the ceiling. More forceful language doesn't push it higher. The remaining 16% might be Claude correctly judging "this skill isn't relevant here."

**3. Field experience**

Prompts that explain *why* something matters produce better outcomes than prompts that demand compliance. Claude makes better decisions when it understands the goal.

## the pattern

Claude works best when:

- **What** is clear (the goal)
- **Why** is understood (the motivation)
- **How** is left to judgment (the implementation)

Overspecify the *how* and you lose the value of judgment. Underspecify the *what* or *why* and you get guesswork.

## practical application

When writing skills, hooks, or prompts:

| do | don't |
|----|-------|
| Explain what the skill provides | Stack up MUST and NEVER |
| Describe when it genuinely helps | Threaten rejection or failure |
| Share the context and goal | Micromanage every step |
| Trust the evaluation | Force activation on everything |

## core-1337's approach

The SessionStart hook explains:
- What skills contain (curated, production-tested knowledge)
- Why they help (better answers, faster, backed by evidence)
- The process (evaluate, activate if relevant, respond)

It doesn't say "you MUST activate or fail." It says "here's why this helps you help the user."

Same goal. Different framing. Better outcomes.
