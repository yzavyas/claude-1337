---
name: self-review
description: Iterate with self-review (no external feedback)
system_prompt: |
  You are a Python expert. Provide clean, correct code.
  When asked to review, be thorough and check edge cases.
  Always output the COMPLETE function when providing corrections.
iteration:
  strategy: self-review
  max_iterations: 3
  review_template: |
    Review your implementation carefully. Consider:
    - Edge cases (empty input, single element, negative numbers)
    - Off-by-one errors
    - Type handling
    - Algorithm correctness

    If you find issues, provide a COMPLETE corrected implementation.
    If correct, respond with "IMPLEMENTATION VERIFIED" and the code.
---

# Self Review Agent

Iterates by asking the model to review its own work without external feedback.

This tests whether self-reflection alone improves outcomes.

## Limitations

Self-review doesn't provide actual signal about what's wrong.
The model must guess which parts might have issues.
Often leads to "fixing" things that weren't broken.
