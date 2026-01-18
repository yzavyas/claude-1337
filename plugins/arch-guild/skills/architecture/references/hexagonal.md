# Hexagonal Architecture (Ports & Adapters)

> "Allow an application to equally be driven by users, programs, automated tests, or batch scripts, and to be developed and tested in isolation from its eventual runtime devices and databases." — Alistair Cockburn

## Why Hexagonal for LLM Development

| Property | Why LLMs Love It |
|----------|------------------|
| **Explicit boundaries** | Agent knows exactly where code belongs |
| **Ports = contracts** | Interfaces explicit, no guessing intent |
| **Adapters swappable** | Change infra without touching domain |
| **Domain is pure** | Reason about logic without infra noise |
| **Dependencies inward** | Never ambiguous direction |
| **Testable by design** | Agent can verify changes work |

## Directory Structure

```
src/
├── domain/                 ← The Hexagon (pure, no external deps)
│   ├── models/             ← Entities, Value Objects, Aggregates
│   ├── services/           ← Domain logic
│   └── ports/              ← Interfaces
│       ├── driven/         ← "I need X" (repos, clients)
│       └── driving/        ← "X triggers me" (use cases)
│
├── adapters/               ← Outside the Hexagon
│   ├── driven/             ← Implements ports/driven/
│   │   ├── persistence/    ← Database
│   │   ├── messaging/      ← Queues
│   │   └── external/       ← Third-party APIs
│   └── driving/            ← Calls ports/driving/
│       ├── http/           ← REST controllers
│       ├── cli/            ← CLI handlers
│       └── events/         ← Event consumers
│
└── config/                 ← Wiring (DI, bootstrap)
```

## The Four Rules

### Rule 1: Domain Imports Nothing External

```typescript
// WRONG — domain depends on infrastructure
import { PrismaClient } from '@prisma/client';
import { Entity } from 'typeorm';

// RIGHT — domain defines what it needs
export interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  save(user: User): Promise<void>;
}
```

### Rule 2: Ports Define Contracts

```typescript
// ports/driven/UserRepository.ts
export interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  save(user: User): Promise<void>;
}

// ports/driven/EmailService.ts
export interface EmailService {
  send(to: Email, subject: string, body: string): Promise<void>;
}

// ports/driving/RegisterUser.ts (use case)
export interface RegisterUser {
  execute(command: RegisterUserCommand): Promise<UserId>;
}
```

### Rule 3: Adapters Implement Ports

```typescript
// adapters/driven/persistence/PrismaUserRepository.ts
import { UserRepository } from '@/domain/ports/driven/UserRepository';
import { PrismaClient } from '@prisma/client';

export class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: UserId): Promise<User | null> {
    const record = await this.prisma.user.findUnique({ where: { id: id.value } });
    return record ? this.toDomain(record) : null;
  }

  async save(user: User): Promise<void> {
    await this.prisma.user.upsert({
      where: { id: user.id.value },
      create: this.toPersistence(user),
      update: this.toPersistence(user),
    });
  }

  private toDomain(record: PrismaUser): User { /* mapping */ }
  private toPersistence(user: User): PrismaUser { /* mapping */ }
}
```

### Rule 4: Wiring at the Edge

```typescript
// config/container.ts
import { PrismaClient } from '@prisma/client';
import { PrismaUserRepository } from '@/adapters/driven/persistence/PrismaUserRepository';
import { SendGridEmailService } from '@/adapters/driven/external/SendGridEmailService';
import { RegisterUserService } from '@/domain/services/RegisterUserService';

export function createContainer() {
  const prisma = new PrismaClient();
  const userRepository = new PrismaUserRepository(prisma);
  const emailService = new SendGridEmailService(process.env.SENDGRID_KEY);
  const registerUser = new RegisterUserService(userRepository, emailService);

  return { registerUser, userRepository };
}
```

## Common Violations

| Violation | Symptom | Fix |
|-----------|---------|-----|
| Domain imports ORM | `import { Entity }` in domain | Pure models, map at adapter boundary |
| Controller has logic | Business rules in HTTP handler | Extract to domain service |
| No port interface | Adapter used directly in domain | Define interface in ports/ |
| Circular dependency | Domain ↔ Adapter imports | Invert with port interface |
| Adapter in domain folder | Infrastructure code in wrong place | Move to adapters/ |
| Port returns infra types | `Promise<PrismaUser>` in port | Return domain types only |

## LLM Implementation Order

When scaffolding a new service:

1. **Port first** — Define the contract (what the domain needs)
2. **Domain second** — Implement pure business logic
3. **Adapter third** — Connect to actual infrastructure
4. **Wire in config** — Dependency injection at entry point

This order ensures domain stays pure and testable.

## Language-Specific Examples

### Python

```python
# domain/ports/user_repository.py
from abc import ABC, abstractmethod
from domain.models import User, UserId

class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: UserId) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...

# adapters/driven/sqlalchemy_user_repository.py
from domain.ports.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, id: UserId) -> User | None:
        # implementation
```

### Go

```go
// domain/ports/user_repository.go
type UserRepository interface {
    FindByID(ctx context.Context, id UserID) (*User, error)
    Save(ctx context.Context, user *User) error
}

// adapters/driven/postgres_user_repository.go
type PostgresUserRepository struct {
    db *sql.DB
}

func (r *PostgresUserRepository) FindByID(ctx context.Context, id UserID) (*User, error) {
    // implementation
}
```

### Kotlin

```kotlin
// domain/ports/UserRepository.kt
interface UserRepository {
    suspend fun findById(id: UserId): User?
    suspend fun save(user: User)
}

// adapters/driven/ExposedUserRepository.kt
class ExposedUserRepository(private val database: Database) : UserRepository {
    override suspend fun findById(id: UserId): User? = newSuspendedTransaction(db = database) {
        // implementation
    }
}
```

## Testing Strategy

Hexagonal makes testing straightforward:

```typescript
// Unit test with fake adapter
describe('RegisterUserService', () => {
  it('creates user and sends welcome email', async () => {
    const fakeRepo = new InMemoryUserRepository();
    const fakeEmail = new FakeEmailService();
    const service = new RegisterUserService(fakeRepo, fakeEmail);

    const userId = await service.execute({ email: 'test@example.com' });

    expect(fakeRepo.users.has(userId)).toBe(true);
    expect(fakeEmail.sentEmails).toHaveLength(1);
  });
});
```

The domain doesn't know or care if it's talking to Postgres, MongoDB, or an in-memory fake.
