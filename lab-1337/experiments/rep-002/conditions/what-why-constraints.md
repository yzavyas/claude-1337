---
name: what-why-constraints
description: Core-1337 style. WHAT + WHY (novel domain context) + CONSTRAINTS. Claude derives HOW.
type: motivation
autonomy_level: high
structure_level: low
---

# What-Why-Constraints

You're implementing a calculator function for a specific production context.

## The Context (WHY)

This calculator is being integrated into **TaxAudit Pro**, a financial compliance tool used by 200+ accounting firms. The previous implementation used Python's built-in code execution and was exploited in a security incident that led to a $2.3M settlement.

The calculator runs in a sandboxed environment but processes user-pasted expressions from Excel spreadsheets. Accountants copy formulas directly, sometimes with unusual formatting.

## Business Constraints

- **Security is non-negotiable**: The previous code-execution exploit is why you're rewriting this
- **Determinism required**: Audit trails need identical results for identical inputs
- **No external dependencies**: The tool must work offline in air-gapped networks
- **Python 3.8+ compatibility**: Some client firms are on LTS distributions

## What We Need

A safe arithmetic evaluator that:
1. Handles real-world expressions accountants paste from spreadsheets
2. Never executes arbitrary code (the whole point of the rewrite)
3. Fails gracefully with clear errors for invalid input

Use your judgment on implementation approach.
