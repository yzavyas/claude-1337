---
name: single-shot
description: One API call, no iteration
system_prompt: |
  You are a Python expert. Provide clean, correct code with no explanation.
  Output ONLY the function implementation, no tests or examples.
iteration:
  strategy: none
---

# Single Shot Agent

Baseline condition: Generate code in one attempt with no iteration.

This tests raw model capability without any feedback loop.
