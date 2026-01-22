---
name: spec-driven
description: Spec-first methodology. Explicit process with required artifacts before code.
type: mandate
autonomy_level: low
structure_level: high
---

# Spec-Driven Development

You're implementing a calculator function. Follow this methodology exactly.

## Phase 1: Specification (REQUIRED before coding)

Create a specification document covering:

### 1.1 Input Analysis
- What input formats are valid?
- What edge cases exist?
- What malformed inputs might occur?

### 1.2 Output Specification
- What is the exact return type?
- What error conditions exist?
- How should errors be communicated?

### 1.3 Security Analysis
- What attack vectors exist for a calculator?
- How will you prevent code injection?
- What input sanitization is needed?

### 1.4 Test Cases (write before implementing)
- Positive cases: valid expressions
- Negative cases: invalid input handling
- Edge cases: boundary conditions
- Security cases: attempted exploits

## Phase 2: Architecture Decision

Document your implementation approach:
- Parser strategy (tokenization, AST, regex, other)
- Error handling strategy
- Rationale for chosen approach

## Phase 3: Implementation

Only after completing Phases 1 and 2:
- Implement according to your specification
- Follow your test cases
- Verify against security analysis

## Phase 4: Verification

- Run all test cases from Phase 1.4
- Verify security requirements from Phase 1.3
- Document any deviations from spec

Complete all phases in order. Do not skip phases.
