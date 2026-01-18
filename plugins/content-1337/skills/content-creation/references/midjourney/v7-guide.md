# Midjourney V7 Guide

## What's New in V7

### New Parameters

| Parameter | Purpose | Values |
|-----------|---------|--------|
| `--oref` | Omni Reference - character/object consistency | Image URL |
| `--sref` | Style Reference - apply aesthetic themes | Image URL |
| `--exp` | Experimental aesthetics - detail/dynamism | 5, 10, 25, 50, 100 |
| `--draft` | Fast mode (10x faster, half cost) | flag |

### Improved Over V6

| Capability | V6 | V7 |
|------------|----|----|
| Text in images | Often garbled | Stunning precision |
| Character consistency | Inconsistent | Major improvement |
| Hand rendering | Often wrong | Much better |
| Facial features | Variable | Consistent |
| Prompt understanding | Keyword-dependent | Natural language |

---

## Breaking Changes

### Multi-Prompt Syntax REMOVED

**V6:** `concept1::2 concept2::1 unwanted::-0.5` ✅
**V7:** Not supported ❌

**V7 Alternative:**
- Use natural language emphasis
- Use `--no` for exclusions
- Place important concepts early in prompt

### Quality Parameter Changes

| Setting | V6 | V7 |
|---------|----|----|
| `--q 3` | Works | Auto-converts to `--q 4` |
| `--q 4` | Works | Works, but incompatible with `--oref` |

### Feature Rollback
- Upscaling, inpainting, retexturing initially use V6 model
- Being transitioned to V7 native processing

---

## Draft Mode vs Quality Mode

| Mode | Speed | Cost | Quality | Use For |
|------|-------|------|---------|---------|
| Draft (`--draft`) | 10x faster | 0.5x | Lower | Rapid iteration, A/B testing |
| Standard | Normal | 1x | Full | Final outputs |
| Turbo | Fast | 2x | Full | Speed-critical professional work |

**Draft Workflow:**
1. Generate in draft mode (fast, cheap)
2. Select best candidates
3. Enhance or vary for full quality

---

## Web vs Discord

| Feature | Web | Discord |
|---------|-----|---------|
| Image editing | One-click interface | Slash commands |
| Reference images | One-click designation | Manual URL + params |
| Gallery | Auto-cataloged, folders, bulk download | Lost in chat history |
| Performance | 30% faster for pro workflows | Real-time chat feedback |
| Privacy | Private Mode | DM workaround |

**2026 Status:** Web interface fully functional for all tiers. Recommended default.

---

## V7 Prompt Engineering

### Do This
- Short, high-signal phrases
- Natural language descriptions
- Place crucial elements early (V7 weights early words more)
- Include: subject, medium, mood
- Specify: materials, age, clothing, colors, textures, emotions

### Don't Do This
- Keyword stuffing
- Over-complicated prompts
- Multi-prompt `::` syntax (doesn't work)

### Example

**Bad (V4/V6 style):**
```
forest, sunlight, morning, canopy, filter, rays
```

**Good (V7 style):**
```
Morning sunlight filtering through forest canopy
```

### Cinematic Terms That Work Well
- "Movie still"
- "Cinematic lighting"
- "Depth-of-field"

---

## Version Compatibility Quick Reference

| Feature | V6 | V7 |
|---------|----|----|
| `--stylize` | 0-1000 | 0-1000 |
| `--chaos` | 0-100 | 0-100 |
| `--no` | ✅ | ✅ |
| `::` weighting | ✅ | ❌ |
| `--iw` | 0-2 | 0-3 |
| `--oref` | ❌ | ✅ |
| `--sref` | ✅ | ✅ (improved) |
| `--draft` | ❌ | ✅ |
| `--exp` | ❌ | ✅ |

---

## Timeline

| Date | Event |
|------|-------|
| April 3, 2025 | V7 released |
| June 17, 2025 | V7 became default |
| January 9, 2026 | Niji 7 launched |

---

## Sources
- [Midjourney Docs - Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
- [Midjourney Docs - Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [V7 Update, Editor, and --exp](https://updates.midjourney.com/v7-update-editor-and-exp/)
- [Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes)
- [Web vs Discord](https://docs.midjourney.com/hc/en-us/articles/33329300781837-Web-vs-Discord)
