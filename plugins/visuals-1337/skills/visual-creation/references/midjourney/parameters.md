# Midjourney Parameters: Version Compatibility

## Quick Reference

| Parameter | V6 | V7 | Purpose |
|-----------|----|----|---------|
| `--stylize` / `--s` | 0-1000 | 0-1000 | Artistic interpretation |
| `--chaos` / `--c` | 0-100 | 0-100 | Variation between 4 images |
| `--no` | ✅ | ✅ | Exclude elements |
| `::` weighting | ✅ | ⚠️ Changed | Multi-prompt weighting |
| `--iw` | 0-2 | 0-3 | Image prompt weight |
| `--sref` | ✅ | ✅ (improved) | Style reference |
| `--sw` | 0-1000 | 0-1000 | Style weight |
| `--cref` | ✅ | ❌ Deprecated | Character reference (V6 only) |
| `--cw` | 0-100 | N/A | Character weight (V6 only) |
| `--oref` | ❌ | ✅ | Omni reference (new) |
| `--ow` | ❌ | 1-1000 | Omni weight (new) |
| `--draft` | ❌ | ✅ | Fast mode (10x, half cost) |
| `--exp` | ❌ | ✅ | Experimental aesthetics |
| `--ar` | ✅ | ✅ | Aspect ratio |
| `--style raw` | ✅ | ✅ | Tighter prompt adherence |

---

## Stylize (--s)

Controls artistic interpretation vs prompt fidelity.

| Value | Behavior |
|-------|----------|
| 0-50 | Maximum prompt fidelity, minimal style |
| 100 (default) | Balanced |
| 100-500 | Increased artistic interpretation |
| 500-1000 | Maximum artistic freedom, may deviate |

**Trade-off:** Higher = more visual interest but less prompt adherence.

---

## Chaos (--c)

Controls variation between the 4 generated images.

| Value | Behavior |
|-------|----------|
| 0 (default) | All 4 images cluster around same concept |
| 25-50 | Moderate variation, distinct but related |
| 50-75 | High variation, visibly different |
| 100 | Maximum chaos, 4 very different interpretations |

**Use case:** High chaos for exploration, low for consistency.

---

## Image Weight (--iw)

Balance between text prompt and reference image.

| Value | Behavior |
|-------|----------|
| 0-0.5 | Text prioritized, image as subtle hint |
| 1 (default) | Balanced |
| 1.5-2 | Image dominates |
| 2.5-3 (V7) | Maximum image adherence |

---

## Style Weight (--sw)

Strength of style reference influence.

| Value | Behavior |
|-------|----------|
| 0-100 | Subtle style hints |
| 100-300 | Clear, balanced (start here) |
| 300-500 | Strong style dominance |
| 700-1000 | Maximum style adherence |

---

## Character Weight (--cw) — V6 ONLY

⚠️ **Deprecated in V7.** Use `--oref` + `--ow` instead.

What to preserve from character reference (V6 only).

| Value | Preserves |
|-------|-----------|
| 0 | Face only (max outfit flexibility) |
| 25 | Face + hair |
| 50 | Face + hair + partial clothing |
| 100 (default) | Everything |

**V7 Migration:** `--cref url --cw 50` → `--oref url --ow 100-200`

---

## Omni Weight (--ow) — V7 Only

Strength of omni reference preservation.

| Value | Behavior |
|-------|----------|
| 25-50 | Subtle, good for style transformation |
| 100 (default) | Balanced |
| 200-400 | Strong preservation |
| 400+ | Maximum (needs high --stylize to balance) |

**Key rule:** --stylize and --exp compete with --oref. Higher stylize needs higher --ow.

---

## Experimental (--exp) — V7 Only

Increases detail, dynamism, and tone-mapping.

| Value | Effect |
|-------|--------|
| 5 | Subtle enhancement |
| 10 | Light |
| 25 | Moderate |
| 50 | Strong |
| 100 | Maximum detail/dynamism |

---

## Draft Mode (--draft) — V7 Only

Fast iteration mode.

- 10x faster generation
- Half the GPU cost
- Lower quality output
- **NOT compatible with --oref**

**Workflow:** Generate in draft → select best → regenerate in quality mode.

---

## Aspect Ratio (--ar)

Common ratios:

| Ratio | Use |
|-------|-----|
| 1:1 | Square (profile pics, icons) |
| 16:9 | Widescreen, YouTube thumbnails |
| 9:16 | Vertical, mobile, TikTok |
| 2:3 | Portrait photography |
| 3:2 | Landscape photography |
| 4:5 | Instagram portrait |

**Rule:** Match input and output aspect ratios when using image references to avoid distortion.

---

## Style Raw (--style raw)

Tighter prompt adherence, less Midjourney aesthetic interpretation.

Use when:
- You need precise composition control
- Fighting against unwanted stylization
- Combining with "asymmetrical" to break symmetry

---

## Negative Prompt (--no)

Exclude elements from generation.

**Syntax:** `--no element1, element2, element3`

**Common uses:**
- `--no text, words, letters` — remove text
- `--no symmetric, mandala, radial` — break symmetry
- `--no blur, blurry` — sharpen
- `--no watermark` — clean output

**V7 note:** This is now the ONLY way to suppress elements (weighting removed).
