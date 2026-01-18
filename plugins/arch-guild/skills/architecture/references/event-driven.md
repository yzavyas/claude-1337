# Event-Driven Architecture

Patterns for async, decoupled systems.

## When to Use

- Services need loose coupling
- Different read/write scaling requirements
- Audit trail is essential
- Async processing acceptable
- Multiple consumers for same event

## When NOT to Use

- Simple CRUD with immediate consistency needs
- Single service with no scaling requirements
- Team lacks distributed systems experience
- Latency requirements preclude async

## Core Patterns

### Event Sourcing

Store state as sequence of events, not current snapshot.

```
Traditional:     User { name: "Alice", email: "alice@example.com" }
Event-Sourced:   [UserCreated, NameChanged("Alice"), EmailChanged("alice@...")]
```

**Reconstruction:**
```typescript
function reconstruct(events: Event[]): User {
  return events.reduce((user, event) => {
    switch (event.type) {
      case 'UserCreated': return { id: event.userId };
      case 'NameChanged': return { ...user, name: event.name };
      case 'EmailChanged': return { ...user, email: event.email };
    }
  }, {} as User);
}
```

| Benefit | Cost |
|---------|------|
| Full audit trail | Increased complexity |
| Temporal queries | Eventual consistency |
| Replay capability | Storage growth |
| Debug time-travel | Learning curve |

### CQRS (Command Query Responsibility Segregation)

Separate read and write models.

```
Commands → Write Model → Events → Read Model ← Queries
              │                      ▲
              └──────────────────────┘
                    (projection)
```

**Write Model** (optimized for consistency):
```typescript
class OrderAggregate {
  private state: OrderState;

  addItem(item: Item): void {
    this.apply(new ItemAdded(this.id, item));
  }

  private apply(event: DomainEvent): void {
    this.state = this.evolve(this.state, event);
    this.uncommittedEvents.push(event);
  }
}
```

**Read Model** (optimized for queries):
```typescript
// Denormalized view, updated by projection
interface OrderView {
  orderId: string;
  customerName: string;  // denormalized from Customer
  items: ItemView[];
  totalAmount: number;   // pre-calculated
  status: string;
}
```

| Benefit | Cost |
|---------|------|
| Optimize each path independently | Eventual consistency between models |
| Scale reads/writes separately | Increased complexity |
| Simple queries (no joins) | More infrastructure |

### Saga Pattern

Coordinate distributed transactions via events.

**Choreography** (decentralized):
```
Order Service                    Payment Service                  Inventory Service
     │                                │                                │
     │ OrderCreated ─────────────────▶│                                │
     │                                │ PaymentProcessed ─────────────▶│
     │                                │                                │ InventoryReserved
     │◀─────────────────────────────────────────────────────────────────│
     │ OrderConfirmed                 │                                │
```

**Orchestration** (centralized):
```
                    ┌─────────────────┐
                    │  Order Saga     │
                    │  Orchestrator   │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Payment  │      │Inventory │      │ Shipping │
    │ Service  │      │ Service  │      │ Service  │
    └──────────┘      └──────────┘      └──────────┘
```

| Choreography | Orchestration |
|--------------|---------------|
| No SPOF | Clear flow visibility |
| Loose coupling | Easier to understand |
| Harder to debug | Orchestrator can be bottleneck |
| Services are autonomous | Central coordination logic |

### Outbox Pattern

Ensure atomic event publishing with database changes.

**Problem**: DB write succeeds, message publish fails = inconsistent state.

**Solution**:
```
Transaction:
  1. UPDATE orders SET status = 'confirmed'
  2. INSERT INTO outbox (event_type, payload) VALUES ('OrderConfirmed', {...})
COMMIT

Background worker:
  3. SELECT * FROM outbox WHERE published = false
  4. Publish to message broker
  5. UPDATE outbox SET published = true WHERE id = ?
```

```typescript
// Within same transaction
async function confirmOrder(orderId: string): Promise<void> {
  await db.transaction(async (tx) => {
    await tx.orders.update({ id: orderId }, { status: 'confirmed' });
    await tx.outbox.insert({
      eventType: 'OrderConfirmed',
      payload: JSON.stringify({ orderId }),
      published: false,
    });
  });
}

// Separate worker polls and publishes
async function publishOutbox(): Promise<void> {
  const events = await db.outbox.findMany({ where: { published: false } });
  for (const event of events) {
    await messageBroker.publish(event.eventType, event.payload);
    await db.outbox.update({ id: event.id }, { published: true });
  }
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Event as Command** | "PleaseCreateUser" couples sender to receiver | Events are facts about past, not requests |
| **Fat Events** | 50KB events with everything | Minimal events + query for details |
| **Missing Idempotency** | Duplicate events = duplicate processing | Idempotency keys, deduplication |
| **No Dead Letter Queue** | Failed messages lost forever | DLQ + alerting + retry strategy |
| **Unbounded Retry** | Poison message retries forever | Exponential backoff + max attempts |
| **Sync over Async** | Blocking wait for async response | Accept eventual consistency or use sync |

## Idempotency Implementation

```typescript
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  // Check if already processed
  const exists = await db.processedEvents.findUnique({
    where: { eventId: event.id }
  });

  if (exists) {
    logger.info('Event already processed, skipping', { eventId: event.id });
    return;
  }

  // Process event
  await processOrder(event);

  // Mark as processed
  await db.processedEvents.insert({ eventId: event.id, processedAt: new Date() });
}
```

## Guild Members for Event-Driven

| Agent | Focus |
|-------|-------|
| **Lamport** | Consistency guarantees, ordering |
| **Erlang** | Backpressure, queue saturation |
| **Burner** | Service boundaries |
| **Taleb** | Failure modes, DLQ strategy |
