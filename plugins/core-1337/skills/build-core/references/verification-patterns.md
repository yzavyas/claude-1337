# Verification Patterns

Concrete checks to verify engineering principles were applied. Run these before declaring work complete.

---

## After Any Code Change

```
[ ] No dead code left behind
    - Unused functions removed
    - Commented-out code removed (it's in git if needed)
    - Orphaned files deleted

[ ] No unused imports/dependencies
    - Every import is used
    - package.json/Cargo.toml reflects actual usage

[ ] Renames completed fully
    - Grep for old name returns nothing
    - Comments updated
    - Documentation updated

[ ] Removals completed fully
    - No orphaned references
    - No "undefined" errors waiting to happen
    - Re-exports cleaned up
```

---

## After Fixing Tests

```
[ ] Fixed the CODE, not the TEST
    - If test was modified, explain why test was wrong
    - Test still verifies the original requirement

[ ] Test integrity preserved
    - Didn't weaken assertions to make green
    - Didn't add special cases that only help this test
    - Didn't mock away the thing being tested

[ ] Bug gets a regression test
    - New test covers the bug that was fixed
    - Test would fail if bug reintroduced
```

**The key question:** Did I make the code correct, or did I make the test pass?

---

## After Refactoring

```
[ ] Refactor is complete
    - No "old way" and "new way" coexisting without migration
    - No TODO comments promising future cleanup
    - No backwards-compat shims unless explicitly needed

[ ] No orphaned abstractions
    - Every function is called
    - Every type is used
    - Every file is imported

[ ] No cruft
    - Old names gone everywhere (code, comments, docs)
    - No re-exports for "backwards compatibility" that nothing uses
    - No `_oldName` variables

[ ] Someone reading the code wouldn't know it was refactored
    - If artifacts of the old structure remain, the refactor isn't done
```

---

## Before Declaring "Done"

### The Three Checks

| Check | Question | If No |
|-------|----------|-------|
| **Task** | Does it work? | Not done |
| **Project** | Is the codebase better than before? | Not done |
| **Compound** | Is the next change easier? | Reconsider approach |

### Project Health Assessment

```
[ ] No new tech debt introduced
    - No "quick fix" that needs future cleanup
    - No special cases that complicate the general case
    - No coupling that shouldn't exist

[ ] Architecture respected
    - Change fits existing patterns
    - If pattern doesn't fit, pattern was changed (not worked around)

[ ] Future developer (including future Claude) can understand this
    - Intent is clear from code
    - Non-obvious decisions have comments explaining WHY
```

---

## Anti-Pattern Detection

### Task Over Project Health

**Symptoms:**
- "It works" but you have doubts about the approach
- Added complexity to handle one case
- Workaround instead of fix

**Check:** Would you be proud to show this code to a senior engineer?

### Test Faking

**Symptoms:**
- Changed test expectations to match current (buggy) behavior
- Added `.skip()` or `@Ignore` to make suite pass
- Mocked the thing you're supposed to be testing

**Check:** Do the tests still verify the original requirements?

### Incomplete Refactoring

**Symptoms:**
- Found yourself doing "search and replace" but stopped partway
- Left `// TODO: clean this up` comments
- Old and new patterns coexist

**Check:** Grep for the old name/pattern. Any hits = not done.

### Backwards-Compat Cruft

**Symptoms:**
- Re-exporting old names "in case something uses them"
- `_deprecated` suffixes on things nothing calls
- Migration code with no migration timeline

**Check:** Is anything actually using the compat layer? If not, delete it.

---

## The Compound Value Test

Before finishing, ask:

> If I do this same type of change 10 more times, will the 10th be easier or harder than the 1st?

- **Easier:** You're compounding value (good patterns, clean abstractions)
- **Same:** Neutral (acceptable for simple changes)
- **Harder:** You're compounding debt (stop and reconsider)

---

## When Verification Fails

If any check fails:

1. **Don't ship it** — incomplete work creates more work
2. **Fix it now** — context is fresh, cost is lowest
3. **If blocked** — surface the blocker explicitly, don't hide it

The goal isn't perfection. The goal is: **leave the codebase better than you found it.**
