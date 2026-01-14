# Mermaid Diagram Types Reference

Complete catalog of Mermaid diagram types with production use cases and syntax patterns.

## Core Types (Stable, Widely Supported)

### sequenceDiagram
**Use when**: Object interactions over time, API calls, message flow

**Syntax**:
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>API: POST /orders
    API->>DB: INSERT order
    DB-->>API: order_id
    API-->>Client: 201 Created
```

**Features**: Actors, lifelines, activation boxes, loops, alternatives, notes

**Production**: Kubernetes (control plane interactions), API documentation

### flowchart / graph
**Use when**: Process flow, algorithms, decision trees

**Syntax**:
```mermaid
flowchart TD
    A[Start] --> B{Authenticated?}
    B -->|Yes| C[Show Dashboard]
    B -->|No| D[Show Login]
    C --> E[End]
    D --> E
```

**Directions**: `TD` (top-down), `LR` (left-right), `BT`, `RL`

**Shapes**: Rectangle `[]`, Diamond `{}`, Circle `(())`, Hexagon `{{}}`

**Production**: Deployment pipelines, approval workflows

### stateDiagram-v2
**Use when**: State machines, entity lifecycles, workflow states

**Syntax**:
```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Paid: payment_received
    Paid --> Shipped: ship_order
    Shipped --> Delivered: confirm_delivery
    Delivered --> [*]

    Pending --> Cancelled: timeout
    Paid --> Refunded: cancel_request
```

**Features**: States, transitions, composite states, concurrency

**Production**: Order management, deployment states, connection lifecycles

### erDiagram
**Use when**: Database schema, entity relationships, data models

**Syntax**:
```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has

    USER {
        int id PK
        string email UK
        string username
        timestamp created_at
    }
    POST {
        int id PK
        int user_id FK
        string title
        text content
    }
```

**Cardinality**: `||--o{` (one-to-many), `}o--o{` (many-to-many), `||--||` (one-to-one)

**Production**: API documentation, database design docs

### classDiagram
**Use when**: OOP structure, interfaces, inheritance

**Syntax**:
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog
```

**Relationships**: Inheritance `<|--`, Composition `*--`, Aggregation `o--`, Association `-->`

**Production**: Codebase documentation, API design

### gantt
**Use when**: Project timelines, roadmaps, milestones

**Syntax**:
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
    Requirements :done, req, 2025-01-01, 2025-01-15
    Design :active, des, 2025-01-10, 2025-01-25

    section Development
    Backend :dev1, 2025-01-20, 30d
    Frontend :dev2, after dev1, 20d
```

**Production**: Roadmaps, release planning

### pie
**Use when**: Proportional data, resource allocation

**Syntax**:
```mermaid
pie title Traffic Sources
    "Direct" : 40
    "Google" : 30
    "Social" : 20
    "Other" : 10
```

**Production**: Metrics dashboards, resource breakdown

### journey
**Use when**: User experience flows, customer journeys

**Syntax**:
```mermaid
journey
    title User Onboarding Journey
    section Sign Up
      Visit site: 5: User
      Create account: 3: User
      Verify email: 2: User
    section First Use
      Complete profile: 4: User
      First action: 5: User
```

**Production**: UX documentation, customer experience mapping

## Recent Additions (Limited Platform Support)

### gitGraph
**Use when**: Git workflows, branching strategies, release processes

**Syntax**:
```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    branch feature/auth
    checkout feature/auth
    commit
    commit
    checkout develop
    merge feature/auth
    checkout main
    merge develop
```

**Platform**: GitHub ~10.0.2 may not support. Verify on target platform.

**Production**: Git workflow documentation

### timeline
**Use when**: Chronological events, product history, migration phases

**Syntax**:
```mermaid
timeline
    title Product Evolution
    2022 : Alpha release : First 100 users
    2023 : Beta launch : 10K users : Major redesign
    2024 : v1.0 : Public launch : 100K users
```

**Platform**: GitHub may not support. Test first.

### mindmap
**Use when**: Hierarchical concepts, knowledge organization, brainstorming

**Syntax**:
```mermaid
mindmap
  root((System Architecture))
    Frontend
      React
      TypeScript
    Backend
      Node.js
      PostgreSQL
      Redis
    Infrastructure
      AWS
      Kubernetes
```

**Platform**: GitHub may not support. Test first.

### quadrantChart
**Use when**: 2D prioritization, effort/impact matrices

**Syntax**:
```mermaid
quadrantChart
    title Feature Prioritization
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Do First
    quadrant-2 Plan For
    quadrant-3 Deprioritize
    quadrant-4 Quick Wins
    Feature A: [0.3, 0.8]
    Feature B: [0.7, 0.3]
```

**Platform**: GitHub may not support. Test first.

### architecture-beta
**Use when**: Cloud/service architecture, microservices

**Syntax**:
```mermaid
architecture-beta
    service api(server)[API Gateway]
    service auth(server)[Auth Service]
    service db(database)[PostgreSQL]

    api:R --> L:auth
    auth:B --> T:db
```

**Icons**: 200K+ from iconify.design

**Platform**: GitHub may not support. Use D2 for production if unavailable.

**Warning**: Non-deterministic rendering (can vary between loads)

### sankey
**Use when**: Flow visualization, traffic sources, resource allocation

**Syntax**:
```mermaid
sankey-beta
    Website,Direct,5000
    Website,Google,3000
    Website,Social,2000
    Direct,Conversion,500
    Google,Conversion,600
    Social,Conversion,200
```

**Platform**: Very new. Test on target platform.

### kanban
**Use when**: Workflow visualization, task boards

**Syntax**:
```mermaid
kanban
    Todo
      Task 1
      Task 2
    Doing
      Task 3
    Done
      Task 4
```

**Platform**: Very new. Test on target platform.

## Syntax Patterns

### Arrow Types by Diagram

| Diagram Type | Solid | Dotted | Comment |
|--------------|-------|--------|---------|
| Flowchart | `-->` | `-.->` | Direction matters |
| Sequence | `->>` | `-->>` | Message vs return |
| Class | `--` | `..` | Association vs dependency |
| State | `-->` | N/A | Transition arrows |
| ER | `--` | N/A | Relationship lines |

### Common Modifiers

- **Labels**: `A -->|label| B`
- **Styling**: `style A fill:#f9f,stroke:#333`
- **Classes**: `class A,B important` (with `classDef important fill:#f00`)
- **Notes**: `note right of A: This is a note`
- **Subgraphs**: Group related nodes

## Version Compatibility

| Platform | Version | Core Types | New Types |
|----------|---------|------------|-----------|
| GitHub | ~10.0.2 | ✅ All | ⚠️ Limited |
| GitLab | 10.6.0 | ✅ All | ⚠️ Some |
| Official | 11.x+ | ✅ All | ✅ All |

**Test diagrams on target platform before production deployment.**

---

**Sources**: Mermaid official docs (mermaid.js.org), Kubernetes diagram guide, GitLab handbook
