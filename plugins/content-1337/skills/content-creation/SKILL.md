---
name: content-creation
description: "Visual content creation with AI. Use when: creating artwork, images, illustrations, animations, videos, visual assets, aesthetic direction, AI art generation, style guidance, choosing image or video models."
---

# Visual Content Creation

Decision frameworks for AI image and video generation. Not tutorials — corrections, gotchas, and "which tool for which job."

---

## Midjourney: Version Gotchas

### V7 Breaking Changes (Critical)

| Feature | V6 | V7 |
|---------|----|----|
| Multi-prompt `::` weighting | ✅ Works | ❌ **REMOVED** |
| Negative weights `::-0.5` | ✅ Works | ❌ **REMOVED** |
| `--no` parameter | ✅ | ✅ |
| `--iw` range | 0-2 | 0-3 |
| `--oref` (Omni Reference) | ❌ | ✅ New |
| `--draft` mode | ❌ | ✅ New (10x faster, half cost) |

**V7 workarounds for removed weighting:**
- Word order matters (early = more weight)
- Use natural language emphasis
- `--no` for exclusion
- Repetition for emphasis

**V6 prompt:** `cyberpunk::2 nature::1 dystopian::-0.5`
**V7 equivalent:** `cyberpunk city with nature elements, NOT dystopian --no dystopian, grim, dark`

---

## Midjourney: Reference Type Decision

### Quick Selector

| I want... | Use | Parameter |
|-----------|-----|-----------|
| Composition inspiration + text | Image Prompt | `--iw 1-2` |
| Same aesthetic, different subject | `--sref` | `--sw 100-300` |
| Same character, new pose/outfit | `--cref` | `--cw 0-50` |
| Same character, keep everything | `--cref` | `--cw 100` |
| Exact object/character preservation | `--oref` (V7) | `--ow 100-400` |

### Reference Type Deep Dive

**Image Prompt (--iw)**
- Mental model: Addition (image + text = result)
- Preserves: Composition, layout
- Changes: Details, style via text
- Range: 0-3 (V7), 0-2 (V6)

**Style Reference (--sref)**
- Mental model: Multiplication (style × subject = result)
- Preserves: Color palette, mood, rendering
- Changes: Subject, composition entirely
- Range: --sw 0-1000

**Character Reference (--cref)**
- **CRITICAL:** Works best with Midjourney-generated images, NOT real photos
- --cw 0 = face only (max outfit flexibility)
- --cw 100 = everything (face, hair, clothing)
- Cannot preserve: fine freckles, small logos, detailed tattoos

**Omni Reference (--oref) — V7 ONLY**
- 2x GPU cost
- Only ONE reference allowed
- NOT compatible with inpainting/outpainting or Draft mode
- Competing params: high --stylize needs higher --ow to balance

### Common Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| Reference ignored | --iw too low | Increase to 2.0+ |
| Shape lost, got mandala | Symmetry bias | Add "asymmetrical", use `--no symmetric, mandala` |
| Character looks different | Using real photo | Use Midjourney-generated source |
| Style overwhelms shape | High --sw, low --iw | Lower --sw OR increase --iw |
| --oref not working | V6 or Draft mode | Switch to V7 standard mode |

---

## Model Selection: Images

### Decision Matrix

| Need | Best Choice | Why | Backup |
|------|-------------|-----|--------|
| Photorealism | Midjourney v7 | Natural lighting, avoids plastic look | Adobe Firefly |
| Artistic/stylized | Midjourney v7 | Color harmony, aesthetic | Leonardo.ai |
| **Text in images** | Ideogram 3.0 | Best-in-class text accuracy | SD 3.5 Large |
| Character consistency | Leonardo.ai | Custom LoRA training | Flux.2 Kontext |
| Technical diagrams | SD 3.5 Large | Spatial understanding, labels | Flux |
| Speed priority | SDXL | 13 sec/image | Ideogram |
| Quality priority | Flux.1 | Best overall (2025 benchmark) | Midjourney v7 |
| Budget (API) | Flux Kontext Dev | $0.015/image | SDXL |

### Text Rendering Hierarchy

**Best → Worst:** Ideogram >> Flux >> SD 3.5 >> DALL-E 3 >> Midjourney (99% gibberish)

**Rule:** If you need readable text, don't use Midjourney. Use Ideogram or Flux.

---

## Model Selection: Video

### Decision Matrix

| Need | Best Choice | Why | Backup |
|------|-------------|-----|--------|
| Highest quality | Runway Gen-4.5 | Benchmark leader (1,247 ELO) | Veo 3.1 |
| **With audio sync** | Kling 2.6 | Only simultaneous audio-visual | — |
| Longest duration | Kling 2.6 | 3 minutes native | Runway |
| Character consistency | Kling O1 | Unified multimodal | Kling 2.6 |
| Professional color | Luma Ray3 | Only native HDR, 16-bit EXR | Runway |
| Budget | Hailuo 2.3 | Best cost-effectiveness | Kling 2.3 |
| Free/open source | HunyuanVideo | Beats Gen-3 quality | Stable Video |

### Key Insight

**Audio-visual sync is now a competitive differentiator.** Only Kling 2.6 generates video + voiceover + sound effects + ambient audio in a single pass.

---

## Troubleshooting Patterns

### "It won't preserve the shape"

1. Use Image Prompt with high --iw (2.0+)
2. Match aspect ratio (input 1:1 → output --ar 1:1)
3. Add `--style raw` for tighter adherence
4. Lower --stylize (30-50) for more literal interpretation
5. **If still failing:** Switch to Gemini/Imagen 3 — it actually understands shapes through multimodal reasoning

### "It keeps making it symmetric"

Midjourney defaults to symmetry. Fight it:
1. Add "asymmetrical" keyword explicitly
2. Use `--no symmetric, mandala, radial, mirrored, balanced, centered`
3. Add `--chaos 6-10`
4. Use directional language ("positioned to the left", "stepping diagonally")
5. Material words help ("weathered metal", "carved stone" resist perfect symmetry)

### "Style overwhelms subject"

Balance the competing forces:
- Lower --sw (style weight)
- Increase --iw (image weight) if using reference
- Use `--style raw`
- Simplify text prompt

### "Character keeps changing"

1. Use `--cref` with Midjourney-generated source (not real photos)
2. For exact preservation: `--oref` (V7 only, 2x cost)
3. For consistency across many images: Leonardo.ai with custom LoRA

---

## References

| Need | Load |
|------|------|
| Midjourney reference types detail | [midjourney/reference-types.md](references/midjourney/reference-types.md) |
| Midjourney V7 full guide | [midjourney/v7-guide.md](references/midjourney/v7-guide.md) |
| Midjourney parameters | [midjourney/parameters.md](references/midjourney/parameters.md) |
| Midjourney animation/video | [midjourney/animation.md](references/midjourney/animation.md) |
| Image model comparison | [image-models.md](references/image-models.md) |
| Video model comparison | [video-models.md](references/video-models.md) |
