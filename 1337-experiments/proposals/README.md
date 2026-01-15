# Lab Enhancement Proposals (LEPs)

Rust RFC-style proposals for experiments and lab improvements.

## Lifecycle

```
Draft → Discussion → FCP → Accepted/Rejected/Postponed → Implemented
```

| Status | Meaning |
|--------|---------|
| `draft` | Initial writing, not ready for review |
| `discussion` | Open for feedback and iteration |
| `fcp` | Final Comment Period - last call before decision |
| `accepted` | Approved for implementation |
| `rejected` | Not accepted (with rationale) |
| `postponed` | Good idea, not the right time |
| `implemented` | Done - links to results |

## Commands

```bash
# Create new proposal
lab-1337 proposal new "Title of proposal"

# List all proposals
lab-1337 proposal list

# Show specific proposal
lab-1337 proposal show 001

# Update status
lab-1337 proposal status 001 discussion

# Move to FCP (Final Comment Period)
lab-1337 proposal fcp 001

# Accept proposal
lab-1337 proposal accept 001

# Mark as implemented
lab-1337 proposal implemented 001 --tracking "experiments/my-experiment"
```

## Numbering

LEPs are numbered sequentially: `lep-001`, `lep-002`, etc.

The CLI handles numbering automatically when creating new proposals.

## Format

See [TEMPLATE.md](TEMPLATE.md) for the standard format (Rust RFC style).
