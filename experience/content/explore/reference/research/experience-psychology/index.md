# experience psychology

Cognitive and psychological foundations for interactive experience design. Evidence-based patterns for attention, perception, and engagement.

---

## cognitive load

### Miller's magic number

**George Miller (1956)**: "The Magical Number Seven, Plus or Minus Two"

Working memory holds approximately 7 chunks (plus or minus 2). The key insight: memory span is limited to **chunks, not bits**.

| finding | source | implication |
|---------|--------|-------------|
| 7 plus or minus 2 chunks | Miller 1956 | Group related items |
| Chunks depend on prior knowledge | Miller 1956 | Experts can chunk more |
| Capacity affected by cognitive load | Sweller 1988 | Reduce extraneous processing |
| Age and expertise affect capacity | Multiple | Design for your actual users |

**Chunking is the strategy.** Seven words (containing many letters) take the same capacity as seven single digits. The chunk is the unit.

### Sweller's cognitive load theory

**John Sweller (late 1980s)**: Extension of Miller's work.

| load type | definition | design response |
|-----------|------------|-----------------|
| **Intrinsic** | Inherent task complexity | Can't reduce, can sequence |
| **Extraneous** | Poor design impositions | Minimize ruthlessly |
| **Germane** | Learning and schema building | This is the goal |

**The design target:** Minimize extraneous load to maximize germane load.

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| "Limit navigation to 7 items" | 7 plus or minus 2 is about memory recall, not visible options |
| "Users can only process 7 things" | Chunking matters more than raw count |
| "Apply 7 plus or minus 2 everywhere" | Rule applies to recall, not recognition |
| Treating all users the same | Experts chunk more efficiently than novices |

**Recognition vs recall distinction:** Visible menus don't require memory - they're recognition tasks. The 7 plus or minus 2 applies when users must hold information in mind without visual support.

---

## attention patterns

### F-pattern (Nielsen Norman Group 2006, 2017)

Eye-tracking research across thousands of users. The F-pattern emerges when:
- Users face text-heavy pages
- Content is not web-optimized
- Users are scanning, not reading

| component | what happens |
|-----------|-------------|
| First horizontal movement | Top of page, reads headline |
| Second horizontal movement | Shorter, slightly down the page |
| Vertical movement | Left side scan, looking for keywords |

**The F-pattern is a failure mode.** It means users are skimming because the content doesn't reward reading.

### other patterns (NNg research)

| pattern | when it occurs | design implication |
|---------|----------------|-------------------|
| **Layer-cake** | Headings stand out | Invest in heading quality |
| **Spotted** | Links, bold, bullets | Strategic emphasis works |
| **Commitment** | User highly motivated | Long-form can work if relevant |
| **Exhaustive** | Mission-critical task | Users will read everything |

### Z-pattern

Applies to visual-heavy, marketing-oriented pages with less text.

| step | location | purpose |
|------|----------|---------|
| 1 | Top-left | Brand/logo recognition |
| 2 | Top-right | Primary CTA scan |
| 3 | Diagonal | Visual hierarchy descent |
| 4 | Bottom-right | Call to action |

### line length research

**Baymard Institute, Bringhurst, WCAG:**

| range | source | context |
|-------|--------|---------|
| 45-75 characters | Typography consensus | Print and extended reading |
| 66 characters | The "ideal" | Bringhurst, Ruder |
| 80 characters max | WCAG 2.2 | Accessibility standard |
| 30-50 characters | Mobile recommendation | Small screens |

**Why it matters:** Saccades (eye jumps) average 20-50ms. The return sweep (line end to next line start) is the hardest part. Optimal line length reduces missed returns.

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| "Users read in F-patterns" | F-pattern is a symptom of poor content design |
| "Design for Z-pattern" | Only applies to specific page types |
| Applying one pattern universally | Pattern depends on content type and user intent |
| Ignoring cultural variation | Right-to-left readers have mirrored patterns |

---

## animation timing

### Nielsen's response time thresholds

**Robert B. Miller (1968), popularized by Jakob Nielsen (1993):**

| threshold | effect | requirement |
|-----------|--------|-------------|
| **0.1s (100ms)** | Feels instantaneous | Direct manipulation illusion |
| **1.0s** | Flow maintained | User still feels in control |
| **10s** | Attention lost | Progress indicator required |

These haven't changed in 55 years of research.

### animation duration ranges

| element type | duration | source |
|-------------|----------|--------|
| Micro-interactions | 100-200ms | NNg, Material Design |
| Small components | 200-300ms | Industry consensus |
| Page transitions | 300-500ms | Material Design |
| Complex sequences | 500-700ms total | Production experience |

**Key insight:** Human visual perception averages 230ms (Model Human Processor). Animations under 100ms register as "not animated" by 80% of users.

### asymmetric timing

**Appearance should be slower than disappearance:**

| transition | enter | exit |
|------------|-------|------|
| Popup window | 300ms | 200-250ms |
| Menu expansion | 250ms | 200ms |
| Modal | 350ms | 250ms |

Users need time to perceive what's appearing. Removal can be faster because they already know what was there.

### convex effect on perceived wait time

**Journal of Consumer Research (2024):**

Animation speed has a **convex** (U-shaped) relationship with perceived waiting time:
- Too slow: feels sluggish
- Too fast: feels jarring
- Moderate speed: shortest perceived wait

### easing and natural motion

| easing | use case | why |
|--------|----------|-----|
| `ease-out` | Elements entering | Deceleration feels natural (arrival) |
| `ease-in` | Elements exiting | Acceleration feels natural (departure) |
| `ease-in-out` | Position changes | Balanced for sustained motion |
| `linear` | Progress indicators | Matches actual time passage |

**Physics basis:** Physical objects have mass. They can't start or stop instantaneously. Abrupt changes feel unnatural.

**Spring physics:** Stiffness, damping, and mass create interruptible, natural-feeling animations that cubic-bezier can't match.

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| Using 300ms for everything | Different elements need different durations |
| Symmetric enter/exit timing | Entering should be slightly slower |
| Linear easing for UI elements | Linear feels mechanical, not natural |
| Over-animating | 500ms+ feels sluggish for small elements |
| Forgetting `prefers-reduced-motion` | 70+ million people affected by vestibular disorders |

---

## emotional design

### Don Norman's three levels (2004)

**Emotional Design: Why We Love (or Hate) Everyday Things**

| level | processing | speed | design target |
|-------|------------|-------|---------------|
| **Visceral** | Automatic, sensory | Immediate | Look and feel |
| **Behavioral** | Subconscious, use | During use | Usability and function |
| **Reflective** | Conscious, meaning | After use | Identity and memory |

**Key insight:** All three combine for the total experience. A beautifully designed product that's unusable fails at behavioral. A usable product that's ugly fails at visceral.

### the aesthetic-usability effect

**Kurosu and Kashimura (1995)**, replicated cross-culturally by **Tractinsky (1997)**:

| finding | correlation | implication |
|---------|-------------|-------------|
| Beauty correlates with perceived ease of use | r = 0.589 | Aesthetics affect usability perception |
| Effect holds across cultures | Tractinsky replication | Not culturally specific |
| Users forgive minor usability issues | When aesthetically pleased | But not major issues |
| Can mask problems in testing | Aesthetic bias | Test ugly versions too |

**The danger:** Beautiful interfaces can hide real usability problems because users are more tolerant. Test with lo-fi prototypes to find actual issues.

### visceral level gotchas

| element | visceral response |
|---------|-------------------|
| Color | Immediate emotional association |
| Typography | Trust, professionalism signals |
| Spacing | Calm (more) vs. urgency (less) |
| Imagery | Emotional priming |
| Sound | Attention, mood setting |

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| Treating aesthetics as optional | Visceral response shapes all subsequent perception |
| "Make it pretty later" | Aesthetic choices should be early, not polish |
| Ignoring behavioral during visual design | Beautiful but unusable fails |
| Forgetting reflective | What does this say about the user's identity? |

---

## audience considerations

### age-related design

**NNg research, systematic reviews (PMC 2024):**

Usability declines 0.8% per year between ages 25 and 60.

| factor | effect | compensation |
|--------|--------|--------------|
| Vision decline | 1 in 6 over 70 impaired | Larger fonts, high contrast |
| Motor precision | Touch target difficulty | 48px+ touch targets |
| Working memory | Processing slows | Reduce information density |
| Attention | More distractible | Minimize visual noise |

**27 design guidelines** from systematic review, organized into:
- Help and training
- Navigation (linear, simple)
- Visual design (contrast, size)
- Cognitive load (chunking, progressive disclosure)
- Interaction (error tolerance, clear feedback)

**Key insight:** Tailored interfaces enhance usability by 30% for older adults.

### expertise levels

**NNg research on novice vs expert users:**

| user type | priority | design approach |
|-----------|----------|-----------------|
| **Novice** | Learnability | Clear guidance, fewer options |
| **Intermediate** | Efficiency | Most common case optimization |
| **Expert** | Power | Shortcuts, density, customization |

**Jakob's Law:** Users spend most time on *other* sites. They rarely become true experts on yours.

| expert trait | novice trait |
|--------------|--------------|
| Values speed | Values clarity |
| Appreciates density | Sees clutter |
| Knows terminology | Needs plain language |
| Wants shortcuts | Needs guidance |

**Production approach:** Optimize for intermediates, provide progressive disclosure for novices, offer shortcuts for experts.

### cultural factors

**Hofstede's cultural dimensions applied to design:**

| dimension | design implication |
|-----------|-------------------|
| **Power distance** | Authority emphasis vs. egalitarian interfaces |
| **Individualism** | Personal benefit vs. group/community framing |
| **Uncertainty avoidance** | Clear structure vs. exploration freedom |
| **Long-term orientation** | Immediate vs. future benefit messaging |

### color across cultures

| color | Western | China | Japan |
|-------|---------|-------|-------|
| **Red** | Danger, passion | Good fortune, happiness | Authority, joy |
| **White** | Purity, weddings | Death, mourning | Purity, also mourning |
| **Blue** | Calm, trust | Immortality, calm | Calmness, security |
| **Black** | Death, elegance | Neutral | Formal, mystery |

**Critical mistake:** White packaging, backgrounds, or themes can signal death/mourning in Chinese markets.

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| Designing for 25-35 year olds only | Real user bases include older adults |
| "Everyone is a beginner" | Many users are intermediates who want efficiency |
| Assuming Western color meanings | Red = danger is cultural, not universal |
| Hofstede as rigid rules | Use as flexible guide, not rulebook |

---

## serial position effect

### Ebbinghaus (1885), Murdock (1962), Glanzer & Cunitz (1966)

Items at the beginning and end of sequences are recalled better than items in the middle.

| effect | mechanism | design application |
|--------|-----------|-------------------|
| **Primacy** | Transfer to long-term memory | First items get most attention |
| **Recency** | Still in working memory | Last items freshly remembered |
| **Middle** | Neither advantage | Most forgotten |

**Working memory capacity:** 3-4 chunks (Glanzer & Cunitz finding).

### production applications

| element | application |
|---------|-------------|
| Navigation | Important items first and last |
| Product carousels | First and last positions for priority items |
| Forms | Critical fields at start |
| CTAs | End of content blocks |
| Lists | Don't bury key information in middle |

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| "Put important things first" | First AND last - both positions are privileged |
| Ignoring middle problem | Actively work to surface middle content |
| Applying to recognition tasks | Serial position mainly affects recall |

---

## engagement and scroll behavior

### scroll depth research

**Industry analytics (Baymard, Contentsquare, multiple):**

| metric | value | context |
|--------|-------|---------|
| Average scroll depth | 50-60% | General web pages |
| "Good" scroll depth | 60-80% | Indicates engagement |
| Long-form target | 75%+ | Article/blog content |
| Warning signal | Below 40% | Content or design problems |

**Context matters:**
- Homepage with above-fold CTA: 25% scroll + low bounce = success
- Long-form article: 25% scroll = failure

### The Pudding methodology

Award-winning data journalism approach:

| technique | implementation |
|-----------|---------------|
| **Scrollytelling** | Scroll triggers visualization changes |
| **Sticky/stepper layout** | Visual pinned, text scrolls alongside |
| **Step-by-step reveal** | Each scroll step updates visual state |
| **Exploration layer** | Let users explore after guided narrative |

**Research claim:** Scroll-driven stories can achieve 400% higher engagement than static content.

### dwell time considerations

| threshold | implication |
|-----------|-------------|
| 0-10 seconds | Bounce/mismatch |
| 10-30 seconds | Scanning |
| 30-60 seconds | Light reading |
| 60+ seconds | Engaged reading |

**Note:** Dwell time without scroll depth is misleading - user may have left tab open.

### what Claude gets wrong

| mistake | correction |
|---------|-----------|
| "Above the fold is all that matters" | Users scroll - design for the journey |
| Assuming linear scroll | Users jump, skim, and revisit |
| Treating all pages the same | Homepage vs. article vs. product have different patterns |
| Ignoring scroll depth in testing | Essential metric for content effectiveness |

---

## synthesis: what Claude typically misses

### the big gaps

1. **Recognition vs recall distinction** - 7 plus or minus 2 applies to recall tasks, not visible menus.

2. **F-pattern is a failure mode** - It indicates poor content design, not natural reading behavior.

3. **Asymmetric animation timing** - Enter should be slower than exit.

4. **Aesthetic-usability masking** - Beautiful designs can hide real usability problems in testing.

5. **Age-related decline is measurable** - 0.8% per year usability decline; 30% improvement with tailored interfaces.

6. **Cultural color inversion** - White means death in China; red means luck.

7. **Primacy AND recency** - Both ends of lists are privileged, not just the beginning.

8. **Context-dependent scroll depth** - 25% is success for landing pages, failure for articles.

### decision framework

| question | evidence-based answer |
|----------|----------------------|
| How many nav items? | Recognition task, not memory - test actual comprehension |
| What animation duration? | 100-200ms micro, 200-300ms components, 300-500ms pages |
| Which easing? | ease-out for enter, ease-in for exit |
| How wide should text be? | 45-75 characters, 66 ideal |
| Where to put CTAs? | Start or end of sequences - never middle |
| How much to scroll? | Target 60-80% for engagement content |
| How to handle older users? | Larger targets, simpler navigation, less density |
| Cross-cultural color? | Research target market - never assume |

---

## sources

- [Miller's Law - Laws of UX](https://lawsofux.com/millers-law/)
- [F-Shaped Pattern - Nielsen Norman Group](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/)
- [Animation Duration - Nielsen Norman Group](https://www.nngroup.com/articles/animation-duration/)
- [Response Times - Nielsen Norman Group](https://www.nngroup.com/articles/response-times-3-important-limits/)
- [Norman's Three Levels - IxDF](https://www.interaction-design.org/literature/article/norman-s-three-levels-of-design)
- [Aesthetic-Usability Effect - Laws of UX](https://lawsofux.com/aesthetic-usability-effect/)
- [Serial Position Effect - Laws of UX](https://lawsofux.com/serial-position-effect/)
- [Usability for Seniors - Nielsen Norman Group](https://www.nngroup.com/articles/usability-for-senior-citizens/)
- [Hofstede Cultural Dimensions](https://geerthofstede.com/culture-geert-hofstede-gert-jan-hofstede/6d-model-of-national-culture/)
- [Color in Chinese Culture - Wikipedia](https://en.wikipedia.org/wiki/Color_in_Chinese_culture)
- [Line Length Readability - Baymard](https://baymard.com/blog/line-length-readability)
- [The Pudding Methodology](https://pudding.cool/process/how-to-make-dope-shit-part-3/)
- [Easing Functions Cheat Sheet](https://easings.net/)
