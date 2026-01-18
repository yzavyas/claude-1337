# Midjourney Animation & Video Capabilities

## 1. Animate Feature - Core Capability

**How It Works:**
The Animate feature converts static images into 5-second videos using a diffusion video model. Unlike frame-by-frame rendering, the model generates all frames simultaneously, treating them as a unified volume of data.

**Workflow:**
1. Create an image in Midjourney or upload an external image
2. Click the "Animate" button
3. Choose animation mode (automatic or manual)
4. Generate 4 video variations simultaneously

**Animation Modes:**
| Mode | Control | Best For |
|------|---------|----------|
| Automatic | Default motion prompt | Quick results |
| Manual | Specific movement descriptions | Precise control |
| High Motion | Larger camera/character movements | Dynamic scenes (may glitch) |

**Output:**
- Base: 5-second videos (24 fps)
- Extendable: +4 seconds per increment
- Maximum: 21 seconds total
- Generates 4 videos per job

**Cost:** ~8x more GPU time than image generation

---

## 2. Pan & Zoom Features

**Pan:** Expands canvas in chosen direction, adds content, changes aspect ratio.

**Zoom:**
- Presets: 1.5x or 2x zoom out
- Custom: 1.0 to 2.0 range
- Keeps original centered, draws new details around it

**Infinite Zoom Workflow:**
1. Create base image
2. Repeat Zoom Out 2x (20-25 times)
3. Import sequence into video editor
4. Arrange for cinematic zoom effect
5. Export final video

---

## 3. Vary (Region) Feature

Inpainting tool for selective regeneration.

**Animation Applications:**
- Generate character/object variations for sequences
- Create iterative changes for motion
- Enable "match-cut" style transitions
- Frame-by-frame manual animation workflows

---

## 4. Video Output Options

| Format | Use Case |
|--------|----------|
| Download for Social | Optimized .mp4 for social media |
| Download Raw Video | Original .mp4 file |
| Download GIF | Animated GIF |

**Quality:**
- SD: 480p (all users)
- HD: 720p (Standard, Pro, Mega plans only)
- Frame Rate: 24 fps (fixed)
- Audio: None

**Duration:**
- Base: 5 seconds
- Extensions: +4 seconds each
- Max: 21 seconds

---

## 5. Limitations

| Limitation | Impact |
|------------|--------|
| Max 720p HD | No 1080p/4K |
| No audio | Need external tools |
| 24 fps fixed | No frame rate control |
| Max 21 seconds | Need external editing for longer |
| Quality degrades on extension | Shorter = better |
| High Motion may glitch | Use sparingly |
| 8x cost | Budget carefully |

---

## 6. When to Use Midjourney vs Dedicated Video Tools

### Use Midjourney For:
- Quick 5-21 second clips
- Social media content (Reels, TikTok)
- Animated concept art
- Cinematic zoom reveals
- Product/character variation showcases

### Use Dedicated Tools For:
- Longer narratives (>21 sec)
- Audio required
- Complex motion control
- High resolution (>720p)
- Specific frame rates
- Multi-track compositing

---

## Sources
- [Video – Midjourney](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video)
- [Introducing Our V1 Video Model](https://updates.midjourney.com/introducing-our-v1-video-model/)
- [Zoom Out – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32595476770957-Zoom-Out)
- [Pan – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan)
- [Vary Region – Midjourney](https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region)
