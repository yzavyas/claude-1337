# visuals-1337

AI image and video generation guidance.

## What This Is

Decision frameworks for Midjourney, image generation models, and video generation models. Not tutorials — corrections, gotchas, and "which tool for which job."

## When It Activates

- Creating artwork, images, illustrations, visual assets
- Producing animations or videos with AI
- Aesthetic direction and style guidance
- Choosing between image/video generation models
- Troubleshooting AI art issues (symmetry, shape preservation, etc.)
- Reference type selection (--sref vs --cref vs --oref)

## Key Content

### Midjourney Gotchas
- V7 breaking changes (multi-prompt `::` behavior changed, `--cref` deprecated)
- Reference type decision tree
- Parameter version compatibility
- Common failures and fixes

### Model Selection
- Image models: Midjourney, DALL-E 3, Flux, Stable Diffusion, Ideogram, Leonardo.ai
- Video models: Runway, Kling, Luma, Sora, Hailuo, Stable Video

## Structure

```
skills/visual-creation/
├── SKILL.md                    # Decision frameworks (< 200 lines)
└── references/
    ├── midjourney/
    │   ├── reference-types.md  # --sref vs --cref vs --oref
    │   ├── v7-guide.md         # What changed in V7
    │   ├── parameters.md       # Version compatibility
    │   └── animation.md        # Video/animation features
    ├── image-models.md         # Model comparison matrix
    └── video-models.md         # Model comparison matrix
```

## Sources

All Midjourney references cite official documentation (docs.midjourney.com, updates.midjourney.com). Model comparisons based on 2025-2026 benchmarks and pricing.
