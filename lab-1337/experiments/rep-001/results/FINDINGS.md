# LEP-001 Experiment Findings

## Summary

**Primary hypothesis**: Does iteration improve outcomes?

**Finding**: It depends. Iteration can hurt when initial code is correct.

## Critical Clarification: Two Different Iteration Types

This experiment tested **API-level multi-turn iteration** (conversation history persists).

The official **Ralph Loop plugin** uses a fundamentally different approach:
- Same prompt repeated (no conversation history)
- Iteration happens via file persistence (git history, modified files)
- Claude reads its own previous work from files, not context

| What We Tested | Official Ralph Loop |
|----------------|---------------------|
| Multi-turn API conversation | Stop hook loops same prompt |
| Test feedback in context | File persistence only |
| Model sees conversation history | Model sees files/git changes |
| Isolated code generation | Full Claude Code session |

**These are different hypotheses**. Results here apply to API-level iteration, not the Ralph methodology.

## Results

### Ralph-Style Iteration (text-justify, Haiku)

| Strategy | Success | Avg Tests Passed | Avg Tokens | Avg Cost |
|----------|---------|------------------|------------|----------|
| single-shot | 0/3 | 12/20 | 707 | $0.05 |
| ralph-iteration | 0/3 | 12/20 | 1,558 | $0.02 |

**Finding**: Ralph-style "same prompt repeated with no feedback" provides no benefit. Same success rate, 2x token usage.

### Interval Merging (Easy Task)

| Agent | Success Rate | Notes |
|-------|-------------|-------|
| single-shot (Haiku) | 100% (3/3) | Perfect baseline |
| test-feedback (Haiku) | 67% (2/3) | Iteration HURT |

**Key observation**: test-feedback run 2 went from correct (22/22) to broken (0/22) after iterations.

### Text Justify (Harder Task)

| Agent | Success Rate | Notes |
|-------|-------------|-------|
| single-shot (Haiku) | 0% (0/3) | Consistent 12/20 partial success |
| test-feedback (Haiku) | 0% (0/3) | Dropped to 0/20 |

**Key observation**: Iteration made things worse, not better.

## Analysis

### When Iteration Hurts

1. **Correct code gets "fixed"**: If initial code passes all tests, mid-evaluation exits early. But if iteration happens anyway, the model may introduce bugs.

2. **Over-correction**: The model doesn't have good judgment about when code is "good enough." It keeps trying to improve even when improvement isn't needed.

3. **Harder tasks don't benefit**: For text-justify where single-shot gets ~60%, iteration didn't help - it made things worse.

### Why Test-Feedback Fails

The test-feedback strategy shows actual failures, but:
- The model may focus on "fixing" the wrong things
- Responses don't always include complete, working code
- Multiple iterations compound errors

### Implications for Ralph

The original "Ralph" iteration hypothesis assumed iteration would help. This data suggests:

1. **Iteration is not universally beneficial**
2. **Task difficulty matters**: Too easy = iteration hurts. Too hard = iteration doesn't help.
3. **Model capability matters**: Haiku may not have the capability to iterate effectively.

## Next Steps

### For API-Level Iteration (Current Approach)
1. **Try with Sonnet**: Does a more capable model iterate better?
2. **Better exit criteria**: Don't iterate if initial code is correct
3. **Different iteration strategies**: Maybe self-review works better than test-feedback for some tasks
4. **Find the sweet spot**: Tasks where single-shot is ~60-80% might benefit from iteration

### To Test Official Ralph Methodology
Testing the official Ralph Loop plugin requires a different experiment design:

1. **File-based tasks**: Tasks that produce/modify files, not just return values
2. **Full Claude Code session**: Can't use isolated Agent SDK calls
3. **Measurement via hooks**: Track iterations, file changes, git history
4. **Different success criteria**: "Did files converge to correct state?"

This would be a separate experiment (LEP-001b or new LEP) because it tests a different hypothesis:
- Current: "Does conversation context help iteration?"
- Ralph: "Does file persistence + same prompt help iteration?"

## Architecture

The experiment now uses hexagonal architecture:
- **Agents**: Defined in `agents/*.md` with system prompts and iteration config
- **Tasks**: Defined in `tasks/*.yaml` with prompts and test cases
- **Harness**: Generic runner that loads configs and executes

This makes it easy to test new iteration strategies by adding new agent definitions.
