# Midjourney Reference Types: Decision Framework

## Quick Reference

| Reference | Preserves | Changes | Parameter | Range |
|-----------|-----------|---------|-----------|-------|
| **Image Prompt** | Composition, layout, general aesthetic | Details, colors, style via text | `--iw` | 0-3 |
| **Style Ref (--sref)** | Color palette, mood, rendering technique | Subject, composition | `--sw` | 0-1000 |
| **Character Ref (--cref)** | Face, hair, body shape | Clothing, pose, setting | `--cw` | 0-100 |
| **Omni Ref (--oref)** | Exact object/character appearance | Everything else | `--ow` | 1-1000 |

---

## 1. Image Prompt (--iw)

**Use when:** You want composition inspiration + text control together.

**Mental model:** Addition (image + text = result)

| --iw Value | Behavior |
|------------|----------|
| 0 | Ignores reference, text-only |
| 0.5 | Text prioritized, loose inspiration |
| 1 (default) | Balanced |
| 1.5-2 | Reference dominates |
| 3 | Maximum adherence |

**Best for:** Exploration, variation, using existing images as starting point.

---

## 2. Style Reference (--sref)

**Use when:** Apply consistent aesthetic to different subjects.

**Mental model:** Multiplication (style × subject = result)

| --sw Value | Behavior |
|------------|----------|
| 0-100 | Subtle hints |
| 100-300 | Clear, balanced style (start here) |
| 300-500 | Strong style dominance |
| 700-1000 | Maximum style adherence |

**SREF Codes:** Predefined numeric identifiers for styles.
- `--sref random` = Midjourney selects random preset
- V7 updated codes; old ones need `--sv 4` or use V6

**Can combine:** Multiple style references (space-separated URLs).

---

## 3. Character Reference (--cref)

**Use when:** Same character across multiple scenes/outfits/poses.

**CRITICAL:** Works best with Midjourney-generated images, NOT real photos.

| --cw Value | Preserves |
|------------|-----------|
| 0 | Face only (max outfit flexibility) |
| 25 | Face + hair |
| 50 | Face + hair + partial clothing |
| 100 (default) | Everything |

**Cannot preserve:** Specific freckles, small logos, fine tattoo details, intricate accessories.

**Best for:** Character consistency, comics, storytelling.

---

## 4. Omni Reference (--oref) — V7 ONLY

**Use when:** "Put THIS specific object in my image" with exact details.

| --ow Value | Behavior | Use Case |
|------------|----------|----------|
| 25-50 | Subtle, style transformation | Photo → anime |
| 100 (default) | Balanced | General use |
| 200-400 | Strong influence | Preserve details |
| 400+ | Maximum (needs high --stylize) | Exact replication |

**Key rule:** Keep below 400 unless using very high stylize values.

**Competing parameters:** --stylize and --exp compete with --oref.
- High stylize + low --ow = stylization wins
- Need higher --ow to counterbalance high stylize

**Limitations:**
- 2x GPU cost
- Only ONE omni reference (no multiples)
- NOT compatible with inpainting/outpainting
- NOT compatible with Draft Mode

---

## Decision Flowchart

```
What's your main goal?

├─ "Visual style consistency across images"
│  └─ --sref (Style Reference)
│     └─ --sw 100-300
│
├─ "Same character, new outfit/pose"
│  └─ --cref (Character Reference)
│     ├─ Want outfit change? → --cw 0-50
│     └─ Keep everything? → --cw 100
│
├─ "Exact object/character preservation"
│  └─ --oref (Omni Reference, V7 only)
│     └─ --ow 100-400
│
├─ "Composition + text together"
│  └─ Image Prompt
│     └─ --iw 1-2
│
└─ "Character + specific art style"
   └─ Combine: --cref + --sref
      └─ --cw + --sw (independent control)
```

---

## Combination Guide

| Combination | Use Case |
|-------------|----------|
| --cref + --sref | Character in consistent style (comic panels) |
| --oref + --sref | Object in consistent style |
| Image prompt + --sref | Composition + aesthetic |
| Image prompt + --cref | Multi-character scene |

**Cannot combine:**
- --oref + inpainting/outpainting
- --oref + draft mode
- Multiple --oref references

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using real photo with --cref | Use Midjourney-generated source |
| --cw 100 when wanting outfit change | Lower --cw to 0-50 |
| High --stylize with low --ow | Increase --ow to 300+ |
| Multiple --oref references | Use only 1 |
| --oref with inpainting | Use --cref instead |
| No text prompt with reference | Always include subject description |

---

## Cost Comparison

| Reference Type | GPU Cost |
|----------------|----------|
| Image prompt | 1x |
| --sref | 1x |
| --cref | 1x |
| **--oref** | **2x** |

---

## Sources
- [Style Reference – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Character Reference – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
- [Omni Reference – Midjourney](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Image Prompts – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts)
