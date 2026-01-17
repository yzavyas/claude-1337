---
name: ralph-iteration
description: Same prompt repeated (Ralph style) - no feedback, just retry
system_prompt: |
  You are a Python expert. Provide clean, correct code with no explanation.
  Output ONLY the function implementation in a Python code block.
iteration:
  strategy: ralph
  max_iterations: 3
---
