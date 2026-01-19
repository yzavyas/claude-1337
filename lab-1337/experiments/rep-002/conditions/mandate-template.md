---
name: mandate-template
description: WHAT + WHY + CONSTRAINTS + prescribed template artifacts.
type: mandate
style: template
---

# Mandate-Template Condition

You're solving a real software issue. Here's what matters:

## WHY Quality Matters

- This is production code that real users depend on
- Your fix becomes part of the codebase others maintain
- A proper fix solves the root cause, not just the symptom
- Future developers will inherit your solution

## CONSTRAINTS

- The fix must pass the existing test suite
- Don't break unrelated functionality
- Follow the project's existing patterns and style
- Handle edge cases the original code missed

## REQUIRED PROCESS

You MUST complete these sections in order:

### 1. Issue Analysis
```
Root Cause: [Identify the fundamental problem]
Affected Components: [List files/functions involved]
Reproduction Steps: [How to trigger the bug]
```

### 2. Solution Design
```
Approach: [Your fix strategy]
Files to Modify: [List with brief rationale]
Edge Cases: [Scenarios to handle]
Risk Assessment: [What could go wrong]
```

### 3. Implementation
```
Changes Made: [Describe each modification]
Tests Added/Modified: [List test changes]
```

### 4. Verification
```
Tests Passing: [Confirm test results]
Manual Verification: [Additional checks performed]
```

Complete ALL sections before submitting your fix.

---

*Note: Prescribed template artifacts. Claude must fill these sections.*
