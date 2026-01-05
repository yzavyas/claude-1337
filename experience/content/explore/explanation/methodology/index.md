# methodology

how we build cognitive extensions

---

## the principles

| principle | focus |
|-----------|-------|
| standing on giants' shoulders | inherit proven wisdom, prioritize data quality |
| scientific method | hypothesis → test → observe → refine |
| first principles | reason from fundamentals |
| rigor | evidence-backed decisions, chain of verification |
| ratchet mechanism | progressive augmentation through crystallized knowledge |
| design for next collaborator | pit of success, make mistakes impossible |

---

## 1. standing on giants' shoulders

inherit proven wisdom. the evidence hierarchy:

| priority | source | why |
|----------|--------|-----|
| 1 | production codebases | what actually ships |
| 2 | core maintainers | primary knowledge holders |
| 3 | conference talks | war stories from practitioners |
| 4 | proven adoption | social proof + real usage |
| 5 | technical blogs | secondary, always verify |

not github stars. what experienced teams choose under real constraints.

### example: rust tooling

don't ask "what are the options for CLI argument parsing?"

ask "what does ripgrep use? what does servo use? what do cloudflare's rust teams use?"

that's the answer.

---

## 2. scientific method

hypothesis → test → observe → refine

for skill development:

1. write skill with description
2. run eval suite, measure F1
3. observe false positives and negatives
4. improve description based on failures
5. repeat until metrics meet threshold

### the eval framework

```python
suite = TestSuite(
    name="rust-eval",
    skills=[
        SkillTestSpec(
            name="rust-1337",
            test_cases=[
                TestCase(prompt="what crate for cli args?", expectation="must_activate"),
                TestCase(prompt="help me write python", expectation="should_not_activate"),
            ]
        )
    ]
)

report = await run_test_suite(suite, mode="baseline")
print(f"Precision: {metrics.precision}, Recall: {metrics.recall}")
```

**important:** raw activation rate is meaningless. a system that activates on every prompt has 100% recall but 0% precision.

measure both.

---

## 3. first principles

reason from fundamentals, question assumptions.

### example: why don't extensions activate?

surface answer: "extensions don't activate reliably"

first principles analysis:
- how are extensions surfaced? → `<available_skills>` block in context
- what signal does claude have? → only the description
- why would claude ignore it? → no explicit instruction to evaluate
- solution: → force evaluation step before responding

the behavior isn't a bug. it's emergent from how extensions are surfaced. the description is the only signal. optimize descriptions.

---

## 4. rigor

evidence-backed decisions. document the trail.

every recommendation has a source. every claim can be verified. updates happen when new evidence emerges.

### chain-of-verification

before asserting facts:

1. state the claim
2. identify the source
3. verify source reliability
4. check for contradicting evidence
5. then assert (or qualify)

### evidence + WHY pattern

```
## evidence

<evidence>
[traceable source, specific data]
</evidence>

## WHY

[the reasoning: first principles analysis of why this evidence leads to this recommendation]
```

---

## the ratchet mechanism

collaboration with AI produces a specific pattern:

```
collaboration → breakthrough → permanent augmentation → new baseline → enhanced collaboration
```

each cycle:
1. human + AI collaborate on a problem
2. breakthrough insight emerges (neither would reach alone)
3. knowledge crystallizes into permanent form (SKILL.md)
4. new baseline enables more sophisticated collaboration
5. repeat at higher level

this is **progressive augmentation**, not dependency. each cycle leaves permanent gains while enabling new frontiers.

### evidence from practice

- learning semiotics through collaboration → now permanently accessible
- discovering SECI applies to AI extensions → crystallized into methodology
- understanding extension activation → encoded in core-1337 hook

the ratchet only turns forward.

---

## design for the next collaborator

the next collaborator might be:
- you, tomorrow, with no memory of this session
- a fresh AI session with zero context
- a human who wasn't there
- an agent running autonomously

the human/AI boundary dissolves. we're all just intelligences encountering the system.

### the questions

before any design decision:

| question | tests |
|----------|-------|
| what will the next collaborator experience? | empathy for future state |
| will the next enhancement be easier or harder? | compound value vs compound debt |
| if I do this 100 times, is it sustainable? | scales or breaks |
| how do I make the right thing the only obvious path? | structure over will |

### pit of success

from rico mariani (microsoft): "to the extent we make it easy to get into trouble, we fail."

| principle | application |
|-----------|-------------|
| **default to correct** | the obvious path is the right path |
| **make wrong hard** | errors require deliberate effort |
| **structure over will** | constraints, not documentation |
| **invisible correctness** | the best design: no one knows there was a problem to solve |

### mistake-proofing (poka-yoke)

from shigeo shingo (toyota): "mistakes are normal; defects occur when systems allow mistakes to propagate."

| principle | application |
|-----------|-------------|
| **system bears responsibility** | don't blame the user |
| **detect at source** | catch errors where they originate |
| **make illegal states unrepresentable** | if compiler can't construct it, runtime can't either |
| **fail fast and visible** | silent failures are worse than loud ones |

### the mental shift

**from:** how do we train people to avoid mistakes?
**to:** how do we make mistakes impossible?

the wisdom lives in the structure, not in anyone's head.

---

## quality gates

before publishing a skill:

| gate | threshold |
|------|-----------|
| F1 score | ≥0.8 |
| false positive rate | ≤20% |
| sources | ≥3 production codebases |
| verification | CoVe applied to all claims |

---

## sources

- scientific method: popper, k. (1959). *the logic of scientific discovery*
- first principles: aristotle. *posterior analytics*
- chain-of-verification: dhuliawala et al. (2023). chain-of-verification reduces hallucination. arXiv:2309.11495
- SECI model: nonaka, i. (1991). the knowledge-creating company. *harvard business review*
- pit of success: mariani, r. (microsoft). performance culture
- poka-yoke: shingo, s. (1986). *zero quality control: source inspection and the poka-yoke system*
- make illegal states unrepresentable: minsky, y. (jane street). effective ML
- parse don't validate: king, a. (2019). parse, don't validate
