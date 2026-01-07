# Cognitive Design

Psychological foundations for interactive experiences. Evidence-based patterns for attention, perception, and engagement.

## Cognitive Load

### Miller's Magic Number

**George Miller (1956)**: Working memory holds ~7 chunks (±2). The key: **chunks, not bits**.

| finding | implication |
|---------|-------------|
| 7±2 chunks | Group related items |
| Chunks depend on expertise | Experts chunk more efficiently |
| Capacity affected by load | Reduce extraneous processing |

### Sweller's Load Types

**John Sweller (1988)**:

| load type | definition | design response |
|-----------|------------|-----------------|
| **Intrinsic** | Inherent task complexity | Can't reduce, can sequence |
| **Extraneous** | Poor design impositions | Minimize ruthlessly |
| **Germane** | Learning and schema building | This is the goal |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| "Limit navigation to 7 items" | 7±2 is about recall, not visible options |
| "Users can only process 7 things" | Chunking matters more than raw count |
| Applying 7±2 everywhere | Rule applies to recall, not recognition |

**Recognition vs recall:** Visible menus don't require memory. The 7±2 applies when users must hold information without visual support.

## Attention Patterns

### F-Pattern (NNg 2006, 2017)

Eye-tracking across thousands of users. **The F-pattern is a failure mode** — it means users are skimming because content doesn't reward reading.

| component | what happens |
|-----------|-------------|
| First horizontal | Top of page, reads headline |
| Second horizontal | Shorter, slightly down |
| Vertical | Left side scan, looking for keywords |

### Other Patterns

| pattern | when it occurs | implication |
|---------|----------------|-------------|
| **Layer-cake** | Headings stand out | Invest in heading quality |
| **Spotted** | Links, bold, bullets | Strategic emphasis works |
| **Z-pattern** | Visual-heavy marketing | For image-driven pages |

### Line Length Research

**Baymard, Bringhurst, WCAG:**

| range | context |
|-------|---------|
| 45-75 characters | Extended reading |
| 66 characters | The "ideal" (Bringhurst) |
| 80 characters max | WCAG 2.2 accessibility |
| 30-50 characters | Mobile |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| "Users read in F-patterns" | F-pattern is a symptom of poor content |
| "Design for Z-pattern" | Only for specific page types |
| One pattern universally | Depends on content and intent |

## Animation Psychology

### Nielsen's Response Thresholds

**Miller (1968), Nielsen (1993)** — unchanged for 55 years:

| threshold | effect |
|-----------|--------|
| **0.1s (100ms)** | Feels instantaneous |
| **1.0s** | Flow maintained |
| **10s** | Attention lost, progress needed |

### Duration Ranges

| element type | duration | source |
|-------------|----------|--------|
| Micro-interactions | 100-200ms | NNg, Material Design |
| Small components | 200-300ms | Industry consensus |
| Page transitions | 300-500ms | Material Design |

### Asymmetric Timing

**Enter should be slower than exit:**

| transition | enter | exit |
|------------|-------|------|
| Popup | 300ms | 200-250ms |
| Menu | 250ms | 200ms |
| Modal | 350ms | 250ms |

Users need time to perceive what's appearing. Removal can be faster.

### Easing

| easing | use case | why |
|--------|----------|-----|
| `ease-out` | Elements entering | Deceleration feels natural |
| `ease-in` | Elements exiting | Acceleration feels natural |
| `ease-in-out` | Position changes | Balanced |
| `linear` | Progress indicators | Matches actual time |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| 300ms for everything | Different elements need different durations |
| Symmetric enter/exit | Entering should be slower |
| Linear easing for UI | Linear feels mechanical |
| Forgetting reduced-motion | 70M+ people with vestibular disorders |

## Emotional Design

### Don Norman's Three Levels (2004)

| level | processing | design target |
|-------|------------|---------------|
| **Visceral** | Automatic, sensory | Look and feel |
| **Behavioral** | Subconscious, use | Usability and function |
| **Reflective** | Conscious, meaning | Identity and memory |

All three combine. Beautiful but unusable fails at behavioral. Usable but ugly fails at visceral.

### Aesthetic-Usability Effect

**Kurosu & Kashimura (1995), Tractinsky (1997)**:

| finding | correlation |
|---------|-------------|
| Beauty → perceived ease of use | r = 0.589 |
| Cross-cultural validation | Tractinsky replication |
| Users forgive minor issues | When aesthetically pleased |
| **Can mask problems** | Test ugly versions too |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| Aesthetics as optional | Visceral shapes all subsequent perception |
| "Make it pretty later" | Aesthetic choices should be early |
| Ignoring behavioral | Beautiful but unusable fails |

## Audience Targeting

### Age-Related Design

**NNg research**: Usability declines 0.8% per year between ages 25-60.

| factor | compensation |
|--------|--------------|
| Vision decline | Larger fonts, high contrast |
| Motor precision | 48px+ touch targets |
| Working memory | Reduce information density |
| Attention | Minimize visual noise |

**Key insight:** Tailored interfaces improve usability by 30% for older adults.

### Expertise Levels

| user type | priority | approach |
|-----------|----------|----------|
| **Novice** | Learnability | Clear guidance, fewer options |
| **Intermediate** | Efficiency | Common case optimization |
| **Expert** | Power | Shortcuts, density, customization |

**Jakob's Law:** Users spend most time on *other* sites. Optimize for intermediates.

### Cultural Factors

**Hofstede's dimensions:**

| dimension | design implication |
|-----------|-------------------|
| Power distance | Authority vs. egalitarian |
| Individualism | Personal vs. group framing |
| Uncertainty avoidance | Structure vs. exploration |

### Color Across Cultures

| color | Western | China |
|-------|---------|-------|
| **Red** | Danger | Good fortune |
| **White** | Purity | Death, mourning |
| **Blue** | Calm, trust | Immortality |

**Critical:** White can signal death/mourning in Chinese markets.

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| Designing for 25-35 only | Real users include older adults |
| "Everyone is a beginner" | Many are intermediates wanting efficiency |
| Western color meanings | Red = danger is cultural, not universal |

## Serial Position Effect

**Ebbinghaus (1885), Murdock (1962)**:

| effect | mechanism | application |
|--------|-----------|-------------|
| **Primacy** | Transfer to long-term memory | First items get attention |
| **Recency** | Still in working memory | Last items remembered |
| **Middle** | Neither advantage | Most forgotten |

### Production Applications

| element | application |
|---------|-------------|
| Navigation | Important items first AND last |
| Carousels | Priority items at ends |
| CTAs | End of content blocks |
| Lists | Never bury key info in middle |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| "Put important things first" | First AND last are privileged |
| Ignoring middle problem | Actively surface middle content |

## Engagement Research

### Scroll Depth

**Baymard, Contentsquare:**

| metric | context |
|--------|---------|
| 50-60% average | General web pages |
| 60-80% good | Indicates engagement |
| Below 40% | Warning signal |

**Context matters:** 25% scroll + low bounce on landing page = success. 25% on article = failure.

### The Pudding Methodology

| technique | effect |
|-----------|--------|
| Scrollytelling | 400% higher engagement |
| Sticky/stepper layout | Visual pinned, text scrolls |
| Step-by-step reveal | Each scroll updates state |

### What Claude Gets Wrong

| mistake | correction |
|---------|-----------|
| "Above fold is all that matters" | Users scroll — design for journey |
| Treating all pages same | Different patterns for different pages |

## Quick Reference

| question | evidence-based answer |
|----------|----------------------|
| How many nav items? | Recognition task — test comprehension, not count |
| Animation duration? | 100-200ms micro, 200-300ms components, 300-500ms pages |
| Which easing? | ease-out enter, ease-in exit |
| Text width? | 45-75 chars, 66 ideal |
| Where for CTAs? | Start or end — never middle |
| Scroll target? | 60-80% for engagement content |
| Cross-cultural color? | Research target market — never assume |

## Sources

- [Miller's Law](https://lawsofux.com/millers-law/)
- [F-Pattern - NNg](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/)
- [Animation Duration - NNg](https://www.nngroup.com/articles/animation-duration/)
- [Norman's Three Levels - IxDF](https://www.interaction-design.org/literature/article/norman-s-three-levels-of-design)
- [Aesthetic-Usability Effect](https://lawsofux.com/aesthetic-usability-effect/)
- [Serial Position Effect](https://lawsofux.com/serial-position-effect/)
- [Usability for Seniors - NNg](https://www.nngroup.com/articles/usability-for-senior-citizens/)
- [Hofstede Dimensions](https://geerthofstede.com/culture-geert-hofstede-gert-jan-hofstede/6d-model-of-national-culture/)
- [The Pudding Methodology](https://pudding.cool/process/how-to-make-dope-shit-part-3/)
