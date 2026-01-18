---
name: design
description: This skill should be used when the user asks to "review code design", "check API design", "evaluate abstractions", "review naming", "check SOLID compliance", "design an API", "choose between REST and GraphQL", or discusses code quality, interface design, API contracts, or developer experience.
---

# Design

Code, component, and API design evaluation.

## Abstraction Quality

### Naming

- Does `processData()` actually process data?
- Do names reveal intent?
- Consistent vocabulary (don't mix "user" and "account" for same concept)?

**Red flags:**
- `Manager`, `Handler`, `Processor`, `Utils` — often god classes
- Single-letter names outside tight loops
- Abbreviations that aren't universally known

### Single Responsibility

- One reason to change?
- Can you describe the class without using "and"?

**Test:** "The {ClassName} is responsible for..." — if you need "and", split it.

### Leaky Abstractions

- Does implementation leak through interface?
- Are internal data structures exposed?

**Example leak:**
```typescript
// Leaky — exposes internal Map structure
class Cache {
  getAll(): Map<string, Value> { return this.internal; }
}

// Clean — hides implementation
class Cache {
  entries(): Array<[string, Value]> { return [...this.internal]; }
}
```

### Tell, Don't Ask

- Behavior on objects vs external orchestration?
- Objects should do things, not just hold data

**Ask (bad):**
```typescript
if (order.status === 'pending' && order.items.length > 0) {
  order.status = 'confirmed';
}
```

**Tell (good):**
```typescript
order.confirm(); // Object owns its state transitions
```

## SOLID Compliance

| Principle | Question | Violation Signal |
|-----------|----------|------------------|
| **S**ingle Responsibility | One reason to change? | Class has multiple "and"s |
| **O**pen/Closed | Extend without modifying? | Switch statements on types |
| **L**iskov Substitution | Subtypes substitutable? | Instanceof checks |
| **I**nterface Segregation | Clients use what they depend on? | Empty method implementations |
| **D**ependency Inversion | Depend on abstractions? | `new ConcreteClass()` in domain |

## API Design

### Protocol Selection

| Protocol | Best For | Avoid When |
|----------|----------|------------|
| **REST** | CRUD, public APIs, caching | Real-time, complex queries |
| **GraphQL** | Flexible queries, multi-client | Simple CRUD, N+1 risk |
| **gRPC** | Internal services, performance | Browser clients |
| **WebSocket/SSE** | Real-time updates | Request-response |

### Universal Principles

1. **Contract-First**: Define API before implementation
2. **Consistency**: Same patterns everywhere
3. **Evolvability**: Version from day one
4. **DX**: Clear errors, good docs

## DX (Developer Experience)

- **Onboarding**: Can a new dev understand in 15 minutes?
- **Error Messages**: Actionable or cryptic?
- **Documentation**: Matches reality?
- **Conventions**: Consistent with ecosystem?

## Guild Members for Design

Primary: **Karman** (naming/abstractions), **Ace** (DX), **Burner** (coupling)
Secondary: **Dijkstra** (correctness), **Vector** (auth for APIs)

## Output Format

```
## Design Review: {Component}

### Abstraction Quality
- {Finding 1}
- {Finding 2}

### SOLID Violations
- {Principle}: {violation}

### API Assessment (if applicable)
- {Finding}

### DX Friction Points
- {Point 1}

### Recommendations
1. {Action}
2. {Action}
```

## Additional Resources

- **`references/solid-gotchas.md`** — Common SOLID violations with fixes
- **`references/api-rest.md`** — REST production gotchas
- **`references/api-graphql.md`** — GraphQL N+1, complexity, caching traps
- **`references/api-grpc.md`** — gRPC streaming, versioning gotchas
