# Principles and Patterns: Examples

Concrete examples of principles in action. Each example follows:

1. **Situation** - What was being designed
2. **Initial approach** - What seemed reasonable
3. **Signal** - How to recognize this in new situations
4. **Principle** - Which principle applies
5. **Why it's wrong** - The reasoning chain
6. **Better approach** - The improved design
7. **Pattern** - Generalizable takeaway

---

## Procedural Relationship Anti-Pattern

**Principle violated**: Pit of Success

### Situation

Designing CLI for enhancement lifecycle management. LEPs (proposals), IMPs (implementation plans), and experiments need to be connected.

### Initial Approach

```bash
lab-1337 proposal new "idea"      # Creates LEP-001
lab-1337 imp new "plan"           # Creates IMP-001
lab-1337 experiment new "exp"     # Creates experiment
lab-1337 link 001                 # Connect LEP-001 → IMP-001 → experiment
```

A separate `link` command to establish relationships.

### Signal

Watch for:
- "Add a command to connect X to Y"
- "User needs to link/associate/wire..."
- Separate step to establish relationship
- Artifacts that "should" be connected but aren't by default

### Principle

**Pit of Success**: Make the right thing the only obvious path. Don't rely on documentation or willpower. Structure code so mistakes are hard and correct behavior is natural.

### Why It's Wrong

```
Manual linking
    → Can be forgotten
    → Orphaned artifacts
    → Requires documentation ("remember to link!")
    → Relies on user discipline
    → Discipline fails at scale
    → Orphans accumulate
```

The pit of *failure* - the wrong thing (forgetting to link) is easy, the right thing requires extra effort.

### Better Approach

Naming convention IS the link:

```bash
lab-1337 proposal new "idea"      # Creates lep-001-idea.md
lab-1337 imp new 001              # Creates imp-001-idea.md (inherits title, number = link)
lab-1337 experiment new 001       # Creates experiments/lep-001-idea/ (number = link)
```

- `lep-001-*` → `imp-001-*` → `experiments/lep-001-*/`
- Same number = connected by convention
- CLI scaffolds with correct naming automatically
- **Cannot create orphan** because structure enforces relationship

No link command. The structure IS the linkage.

### Pattern

> When tempted to add a command that "connects", "links", "associates", or "wires" artifacts together - stop. Ask: **can the structure enforce this relationship instead of requiring a procedure?**

**Procedural**: User must do something to establish relationship
**Structural**: Relationship exists by virtue of how things are organized

Structural > Procedural. Always.

### Where Else This Applies

- **Database schemas**: Foreign keys vs. application-level "linking"
- **File organization**: Directory structure vs. metadata files listing relationships
- **API design**: Nested resources vs. separate "association" endpoints
- **Configuration**: Convention over configuration
- **Code architecture**: Composition vs. manual dependency injection

---

<!-- Add more examples as they emerge from collaborative sessions -->
