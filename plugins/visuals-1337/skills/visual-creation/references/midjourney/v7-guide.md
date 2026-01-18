# Midjourney V7 Guide

**Last Updated:** January 2026
**Released:** April 3, 2025 | **Default:** June 17, 2025

---

## What's New in V7

### New Parameters

| Parameter | Purpose | Values |
|-----------|---------|--------|
| `--oref` | Omni Reference - replaces `--cref` for V7 | Image URL |
| `--ow` | Omni reference weight | 0-1000 (default: 100) |
| `--exp` | Experimental aesthetics - detail/dynamism | 0-100 (default: 0) |
| `--draft` | Fast mode (10x faster, half cost) | flag |
| `--p` | Personalization (enabled by default) | flag |

### Improved Over V6

| Capability | V6 | V7 |
|------------|----|----|
| **Text in images** | **Garbled (99%)** | **Still weak (~15% better)** |
| Character consistency | Inconsistent | Major improvement with `--oref` |
| Hand rendering | Often wrong | Fewer six-fingered hands |
| Facial features | Variable | Better coherence |
| Prompt understanding | Keyword-dependent | Natural language, literal placements |
| Beauty bias | Smoothed skin | More natural textures |

**⚠️ Text Rendering Warning:** Midjourney V7 text is still poor (~15% improvement over V6). For text in images, use **Ideogram 3.0**, **Flux 2**, or **GPT Image 1.5** instead.

---

## Breaking Changes

### Multi-Prompt Syntax CHANGED (Not Removed)

**V6:** `concept1::2 concept2::1 unwanted::-0.5` ✅
**V7:** Still functional but **behavior changed** ⚠️

**What Changed:**
- Weight ratios calculated differently
- Negative weights less predictable
- ~74% of V6 prompts required modification for V7

**V7 Workarounds:**
- Use natural language emphasis instead
- Use `--no` for exclusions (more reliable)
- Place important concepts early in prompt
- Repetition for emphasis

**Example Migration:**
```
V6: cyberpunk::2 nature::1 dystopian::-0.5
V7: cyberpunk city with nature elements, NOT dystopian --no dystopian, grim, dark
```

### Stylize Scale Changed (Critical!)

Same values produce **different results** between versions:

| V6 Value | V7 Equivalent |
|----------|---------------|
| `--s 100` | `--s 300-400` |
| `--s 250` | `--s 600-700` |
| `--s 500` | `--s 1000` |
| `--s 750` | `--s 1000` (max) |

### Character Reference (`--cref`) Deprecated

**V7 uses Omni Reference (`--oref`) instead.**

| V6 | V7 |
|----|----|
| `--cref [url] --cw 50` | `--oref [url] --ow 100-200` |

**Key differences:**
- `--oref` works for objects, characters, and vehicles
- 2x GPU cost
- Only ONE reference allowed
- NOT compatible with Draft Mode

### Style Reference Codes Changed

Old sref codes may not work in V7.

**Workarounds:**
- Add `--sv 4` to use pre-June-2025 sref model
- Or switch to V6 for legacy sref codes

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
| `--stylize` | 0-1000 | 0-1000 (different scale!) |
| `--chaos` | 0-100 | 0-100 |
| `--no` | ✅ | ✅ |
| `::` weighting | ✅ | ⚠️ Works but behavior changed |
| `--iw` | 0-2 | 0-3 |
| `--cref` | ✅ | ❌ (use `--oref`) |
| `--oref` | ❌ | ✅ (2x GPU cost) |
| `--sref` | ✅ | ✅ (use `--sv 4` for old codes) |
| `--draft` | ❌ | ✅ |
| `--exp` | ❌ | ✅ |
| `--p` | ❌ | ✅ (enabled by default) |

---

## Timeline

| Date | Event |
|------|-------|
| April 3, 2025 | V7 released |
| June 17, 2025 | V7 became default |
| January 9, 2026 | Niji 7 launched |

---

## Sources

**Official Midjourney Documentation:**
- [Version Documentation](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
- [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes)
- [Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)
- [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization)
- [GPU Speed](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo)

**Midjourney Update Announcements:**
- [V7 Alpha](https://updates.midjourney.com/v7-alpha/)
- [V7 Update, Editor, and --exp](https://updates.midjourney.com/v7-update-editor-and-exp/)
- [Style References for V7](https://updates.midjourney.com/style-references-for-v7/)
- [Omni-Reference](https://updates.midjourney.com/omni-reference-oref/)

**Third-Party Research:**
- [thecodersblog - V7 Prompt Bugs and Stylize Issues](https://thecodersblog.com/midjourney-v7-prompt-bugs-fix-stylization-issues/)
- [DataCamp - V7 Tutorial](https://www.datacamp.com/tutorial/midjourney-v7)
- [TitanXT - Character Consistency Guide](https://www.titanxt.io/post/simple-steps-for-consistent-characters-in-midjourney-v7-using-omnireference)
- [Decrypt - V7 Review](https://decrypt.co/313704/midjourney-v7-review-struggles-keep-up)
