# GraphQL Gotchas

Production lessons for GraphQL API design.

## The N+1 Problem

### The Problem

```graphql
query {
  posts {
    title
    author {
      name
    }
  }
}
```

Without optimization:
```
1 query: SELECT * FROM posts
N queries: SELECT * FROM users WHERE id = ? (for each post)
```

### Solution: DataLoader

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (userIds: string[]) => {
  const users = await db.users.findMany({
    where: { id: { in: userIds } }
  });

  // Must return in same order as input
  const userMap = new Map(users.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id));
});

// In resolver
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId)
  }
};
```

**Key points:**
- DataLoader batches within single tick
- Must return results in same order as keys
- Create new loader per request (not global)

## Query Complexity

### The Problem

```graphql
query {
  users {
    posts {
      comments {
        author {
          posts {
            comments {
              # ... infinite nesting
            }
          }
        }
      }
    }
  }
}
```

### Solution: Complexity Analysis

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const complexityLimit = createComplexityLimitRule(1000, {
  scalarCost: 1,
  objectCost: 10,
  listFactor: 10,
});

// Apply as validation rule
const server = new ApolloServer({
  validationRules: [complexityLimit],
});
```

### Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  validationRules: [depthLimit(5)],
});
```

## Caching Challenges

### The Problem

REST: `GET /users/123` → easy to cache
GraphQL: `POST /graphql` → same endpoint, different queries

### Solutions

**Persisted Queries:**
```
# Instead of sending full query
POST /graphql
{ "query": "{ user(id: 123) { name } }" }

# Send hash
POST /graphql
{ "extensions": { "persistedQuery": { "sha256Hash": "abc..." } } }
```

**Response Caching:**
```typescript
const server = new ApolloServer({
  plugins: [
    responseCachePlugin({
      sessionId: (ctx) => ctx.request.http.headers.get('authorization'),
    }),
  ],
});

// In schema
type User @cacheControl(maxAge: 60) {
  id: ID!
  name: String!
  email: String! @cacheControl(maxAge: 0)  # Never cache
}
```

**CDN/Edge Caching:**
- Use GET for queries (with query param)
- Hash-based URLs for persisted queries

## Schema Evolution

### Breaking vs Non-Breaking

**Non-breaking (safe):**
- Adding new types
- Adding optional fields
- Adding optional arguments
- Deprecating fields

**Breaking (dangerous):**
- Removing fields
- Making nullable field non-null
- Changing field types
- Removing enum values

### Deprecation Pattern

```graphql
type User {
  id: ID!
  name: String! @deprecated(reason: "Use fullName instead")
  fullName: String!
}
```

### Versioning Strategies

**Field-level (preferred):**
```graphql
type User {
  address: String @deprecated(reason: "Use addressV2")
  addressV2: Address
}
```

**Type-level:**
```graphql
type UserV1 { ... }
type UserV2 { ... }
```

**Avoid:** New endpoints (`/graphql/v2`)

## Error Handling

### GraphQL Error Format

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND",
        "field": "id"
      }
    }
  ]
}
```

### Partial Success

GraphQL can return partial data with errors:

```json
{
  "data": {
    "user": {
      "name": "Alice",
      "posts": null
    }
  },
  "errors": [
    {
      "message": "Failed to fetch posts",
      "path": ["user", "posts"]
    }
  ]
}
```

### Union Error Types

```graphql
union CreateUserResult = User | ValidationError | DuplicateEmailError

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

Client handles each case explicitly.

## Authorization

### Field-Level Auth

```typescript
const resolvers = {
  User: {
    email: (user, args, context) => {
      if (context.user.id !== user.id && !context.user.isAdmin) {
        throw new ForbiddenError('Cannot view other users\' emails');
      }
      return user.email;
    }
  }
};
```

### Directive-Based Auth

```graphql
directive @auth(requires: Role!) on FIELD_DEFINITION

type Query {
  users: [User!]! @auth(requires: ADMIN)
  me: User @auth(requires: USER)
}
```

```typescript
class AuthDirective extends SchemaDirectiveVisitor {
  visitFieldDefinition(field) {
    const requiredRole = this.args.requires;
    const originalResolve = field.resolve;

    field.resolve = async function(source, args, context, info) {
      if (!context.user || !context.user.roles.includes(requiredRole)) {
        throw new ForbiddenError('Insufficient permissions');
      }
      return originalResolve.call(this, source, args, context, info);
    };
  }
}
```

## Performance Gotchas

### Over-Fetching at Resolver Level

**Problem:**
```typescript
// Always fetches all fields from DB
Post: {
  author: async (post) => {
    return await db.users.findUnique({ where: { id: post.authorId } });
  }
}
```

**Solution: Check requested fields:**
```typescript
import { parseResolveInfo } from 'graphql-parse-resolve-info';

Post: {
  author: async (post, args, context, info) => {
    const fields = parseResolveInfo(info);
    return await db.users.findUnique({
      where: { id: post.authorId },
      select: Object.keys(fields.fieldsByTypeName.User)
    });
  }
}
```

### Circular References

Watch out for circular types causing infinite loops in schema generation or serialization.

## Guild Members for GraphQL

| Agent | Focus |
|-------|-------|
| **Knuth** | N+1, query complexity |
| **Vector** | Authorization, injection |
| **Ace** | Schema design, error messages |
| **Lamport** | Caching consistency |
