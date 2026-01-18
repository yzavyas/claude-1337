# SOLID Gotchas

Common violations and fixes from production codebases.

## Single Responsibility Principle (SRP)

### The God Class

**Violation:**
```typescript
class UserService {
  createUser(data: UserData): User { /* ... */ }
  sendWelcomeEmail(user: User): void { /* ... */ }
  generateReport(users: User[]): Report { /* ... */ }
  validatePassword(password: string): boolean { /* ... */ }
  updateBillingInfo(user: User, billing: Billing): void { /* ... */ }
}
```

**Fix — Split by cohesion:**
```typescript
class UserRepository { /* CRUD operations */ }
class UserNotificationService { /* emails, notifications */ }
class UserReportGenerator { /* reporting */ }
class PasswordValidator { /* validation rules */ }
class BillingService { /* billing operations */ }
```

**Heuristic:** If your class has more than 5-7 public methods, it's probably doing too much.

### Mixed Abstraction Levels

**Violation:**
```typescript
class OrderProcessor {
  processOrder(order: Order) {
    // High-level orchestration
    this.validateOrder(order);
    // Low-level detail
    const connection = mysql.createConnection(config);
    connection.query('INSERT INTO orders...', [order]);
    // High-level again
    this.notifyWarehouse(order);
  }
}
```

**Fix — Consistent abstraction:**
```typescript
class OrderProcessor {
  processOrder(order: Order) {
    this.validateOrder(order);
    this.orderRepository.save(order);  // Detail hidden
    this.notifyWarehouse(order);
  }
}
```

## Open/Closed Principle (OCP)

### The Type Switch

**Violation:**
```typescript
function calculateDiscount(customer: Customer): number {
  switch (customer.type) {
    case 'regular': return 0;
    case 'premium': return 0.1;
    case 'vip': return 0.2;
    // Every new type requires modifying this function
  }
}
```

**Fix — Polymorphism:**
```typescript
interface DiscountStrategy {
  calculate(): number;
}

class RegularDiscount implements DiscountStrategy {
  calculate() { return 0; }
}

class PremiumDiscount implements DiscountStrategy {
  calculate() { return 0.1; }
}

// New types just add new classes, no modification needed
```

### When OCP Is Overkill

Not every conditional needs polymorphism. Use judgment:

**Overkill:**
```typescript
// This is fine as a simple function
function formatCurrency(amount: number, currency: 'USD' | 'EUR'): string {
  return currency === 'USD' ? `$${amount}` : `€${amount}`;
}
```

**Apply OCP when:**
- New cases are likely
- Cases have complex behavior
- Behavior varies in multiple dimensions

## Liskov Substitution Principle (LSP)

### The Square/Rectangle Problem

**Violation:**
```typescript
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  area() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Breaks Rectangle's contract!
  }
}

// Client code breaks:
function resize(rect: Rectangle) {
  rect.setWidth(5);
  rect.setHeight(10);
  assert(rect.area() === 50); // Fails for Square!
}
```

**Fix — Composition over inheritance:**
```typescript
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  area() { return this.side * this.side; }
}
```

### The instanceof Check

**Violation:**
```typescript
function process(animal: Animal) {
  if (animal instanceof Dog) {
    animal.bark();
  } else if (animal instanceof Cat) {
    animal.meow();
  }
  // LSP violation: subtypes behave differently
}
```

**Fix — Common interface:**
```typescript
interface Animal {
  makeSound(): void;
}

function process(animal: Animal) {
  animal.makeSound(); // Works for all animals
}
```

## Interface Segregation Principle (ISP)

### The Fat Interface

**Violation:**
```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots do not eat'); }  // Violation!
  sleep() { throw new Error('Robots do not sleep'); }
}
```

**Fix — Segregated interfaces:**
```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Human implements Workable, Eatable, Sleepable { /* ... */ }
class Robot implements Workable { /* ... */ }
```

### Role Interfaces

Design interfaces around client needs, not implementations:

```typescript
// Instead of one big interface
interface UserRepository {
  findById(id: string): User;
  findByEmail(email: string): User;
  findAll(): User[];
  save(user: User): void;
  delete(id: string): void;
  count(): number;
}

// Segregate by use case
interface UserReader {
  findById(id: string): User;
  findByEmail(email: string): User;
}

interface UserWriter {
  save(user: User): void;
  delete(id: string): void;
}

interface UserLister {
  findAll(): User[];
  count(): number;
}
```

## Dependency Inversion Principle (DIP)

### Hard-coded Dependencies

**Violation:**
```typescript
class OrderService {
  private emailService = new SendGridEmailService();
  private db = new PostgresDatabase();

  createOrder(order: Order) {
    this.db.save(order);
    this.emailService.send(order.customerEmail, 'Order confirmed');
  }
}
```

**Fix — Inject abstractions:**
```typescript
interface EmailService {
  send(to: string, message: string): Promise<void>;
}

interface Database {
  save(entity: unknown): Promise<void>;
}

class OrderService {
  constructor(
    private emailService: EmailService,
    private db: Database
  ) {}

  createOrder(order: Order) {
    this.db.save(order);
    this.emailService.send(order.customerEmail, 'Order confirmed');
  }
}
```

### The Service Locator Anti-Pattern

**Violation:**
```typescript
class OrderService {
  createOrder(order: Order) {
    const emailService = ServiceLocator.get<EmailService>('email');
    emailService.send(...);
  }
}
```

**Problem:** Hidden dependencies, harder to test, runtime failures.

**Fix:** Constructor injection with explicit dependencies.

## Pragmatic Exceptions

SOLID is guidance, not law. Know when to bend:

| Scenario | Pragmatic Approach |
|----------|-------------------|
| Simple CRUD | Skip full abstraction |
| Prototype/POC | Acceptable violations |
| Performance critical | May inline for speed |
| Team unfamiliar | Start simpler |

**The test:** Would a new team member understand this code faster with or without the abstraction?
