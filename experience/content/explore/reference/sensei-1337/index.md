<p class="dimmed-intro">the feynman technique meets diataxis</p>

## what this is

sensei-1337 provides teaching methodology for documentation. it answers: how do you explain complex things clearly?

two components:

| component | what it does |
|-----------|-------------|
| **skill** | teaching principles - diataxis framework, feynman technique, anti-patterns |
| **agent: feynman** | autonomous documentation workflow - understand, simplify, teach, refine |

## the feynman technique

richard feynman's method for truly understanding anything:

1. **choose the concept** - be specific, not vague
2. **teach it to a child** - simple words, no jargon
3. **identify gaps** - where did you struggle? research more
4. **simplify** - shorter sentences, better analogies

if you can't explain it simply, you don't understand it well enough.

## diataxis framework

four documentation types for four user needs:

| type | user says | form |
|------|-----------|------|
| tutorial | "teach me" | guided lesson |
| how-to | "help me do X" | focused recipe |
| explanation | "help me understand" | context discussion |
| reference | "what exactly is X?" | precise spec |

mixing types creates confusion. a tutorial that stops to explain theory loses momentum. a reference with narrative is hard to scan.

## anti-patterns

| trap | why it fails | fix |
|------|-------------|-----|
| wall of text | reader bounces | headers every 3-5 paragraphs |
| theory first | boring, loses people | hook with problem |
| "obviously" / "simply" | makes reader feel dumb | delete the word |
| explaining everything | buries the point | link for depth |
| no examples | can't apply knowledge | code within 30 seconds |

## the feynman agent

invoke the agent for autonomous documentation:

```
Task(
  subagent_type="sensei-1337:feynman",
  prompt="Write concept docs for the authentication system"
)
```

the agent executes four phases:

| phase | what happens |
|-------|-------------|
| UNDERSTAND | read domain, identify audience, list concepts, find sources |
| SIMPLIFY | structure with one concept per section, plan examples |
| TEACH | write with example first, no jargon, max 5 lines per paragraph |
| REFINE | read aloud, cut ruthlessly, link for depth |

## simplicity checks

quantifiable targets for clear writing:

| metric | target |
|--------|--------|
| sentence length | &lt; 25 words |
| paragraph length | &lt; 5 lines |
| time to first example | &lt; 30 seconds |
| unexplained jargon | 0 |
| concepts per section | 1 |

## when to use

- writing concept explanations
- creating tutorials or how-tos
- drafting READMEs
- building learning materials

## structure

```
plugins/sensei-1337/
├── .claude-plugin/plugin.json
├── SKILL.md              # teaching methodology
├── agents/
│   └── feynman.md        # documentation workflow
├── hooks/
│   └── skill-eval.sh     # SessionStart activation
└── references/
    ├── diataxis.md       # doc type decisions
    └── feynman-technique.md
```

## sources

- [diataxis.fr](https://diataxis.fr) - daniele procida's framework
- [feynman technique](https://fs.blog/feynman-technique/) - learning method
- [stripe docs](https://docs.stripe.com) - exemplar technical writing
