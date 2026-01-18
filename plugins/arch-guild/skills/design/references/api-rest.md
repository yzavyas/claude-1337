# REST API Gotchas

Production lessons for REST API design.

## Pagination

### Offset Pagination Problems

```
GET /users?offset=1000&limit=20
```

**Gotchas:**
- Performance degrades with large offsets (`OFFSET 1000000` is slow)
- Inconsistent results if data changes between pages
- Client can request offset beyond data size

### Cursor Pagination (Preferred)

```
GET /users?cursor=abc123&limit=20

Response:
{
  "data": [...],
  "cursors": {
    "next": "def456",
    "previous": "xyz789"
  }
}
```

**Benefits:**
- Consistent performance regardless of position
- Stable results even with data changes
- Natural fit for infinite scroll

**Implementation:**
```typescript
// Cursor is encoded (id, timestamp) tuple
const cursor = Buffer.from(JSON.stringify({
  id: lastItem.id,
  createdAt: lastItem.createdAt
})).toString('base64');

// Query uses cursor for WHERE clause
const items = await db.query(`
  SELECT * FROM users
  WHERE (created_at, id) > ($1, $2)
  ORDER BY created_at, id
  LIMIT $3
`, [cursor.createdAt, cursor.id, limit]);
```

## Versioning

### URL Versioning

```
/api/v1/users
/api/v2/users
```

**Pros:** Clear, easy to route, cache-friendly
**Cons:** URL pollution, client must change URLs

### Header Versioning

```
GET /api/users
Accept: application/vnd.api+json; version=2
```

**Pros:** Clean URLs, same resource different representations
**Cons:** Harder to test in browser, less discoverable

### Recommendation

Use URL versioning for major breaking changes, header versioning for minor variations.

**Breaking changes (new URL):**
- Removing fields
- Changing field types
- Changing response structure

**Non-breaking (same URL):**
- Adding optional fields
- Adding new endpoints
- Adding new optional parameters

## Error Handling

### Consistent Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req_abc123"
  }
}
```

### HTTP Status Code Mapping

| Status | Use For |
|--------|---------|
| 200 | Success with body |
| 201 | Created (POST) |
| 204 | Success, no body (DELETE) |
| 400 | Client error (validation, bad format) |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Semantically invalid (valid format, wrong data) |
| 429 | Rate limited |
| 500 | Server error |

### Common Mistakes

**Wrong:**
```json
// Using 200 for errors
{ "status": 200, "error": "User not found" }

// Generic 500 for client errors
500 Internal Server Error

// No error details
{ "error": "Something went wrong" }
```

## Rate Limiting

### Headers to Include

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
Retry-After: 60
```

### Implementation Patterns

**Fixed Window:**
```
100 requests per minute
Reset at minute boundary
```
- Simple but allows bursts at window edges

**Sliding Window:**
```
100 requests per rolling 60 seconds
```
- Smoother but more complex to implement

**Token Bucket:**
```
100 tokens, refill 1.67/second
Each request costs 1 token
```
- Allows controlled bursts, smooths traffic

### Per-Resource Limits

```
Global: 1000/hour
/search: 100/hour (expensive)
/users: 500/hour (moderate)
/health: unlimited
```

## Idempotency

### The Problem

```
POST /orders
{ "items": [...] }

# Network timeout, client retries
# Did the order get created or not?
```

### Solution: Idempotency Keys

```
POST /orders
Idempotency-Key: abc-123-def-456
{ "items": [...] }
```

**Server behavior:**
1. Check if key exists in store
2. If exists, return cached response
3. If not, process request, store response with key
4. Return response

**Implementation:**
```typescript
async function handleRequest(req: Request) {
  const key = req.headers['idempotency-key'];

  if (key) {
    const cached = await idempotencyStore.get(key);
    if (cached) {
      return cached.response;
    }
  }

  const response = await processRequest(req);

  if (key) {
    await idempotencyStore.set(key, { response }, { ttl: '24h' });
  }

  return response;
}
```

## HATEOAS (When Worth It)

Hypermedia as the Engine of Application State.

```json
{
  "id": "order_123",
  "status": "pending",
  "_links": {
    "self": { "href": "/orders/order_123" },
    "cancel": { "href": "/orders/order_123/cancel", "method": "POST" },
    "pay": { "href": "/orders/order_123/pay", "method": "POST" }
  }
}
```

**Worth it when:**
- Discoverable API is important
- State machine drives available actions
- Multiple clients need guidance

**Skip when:**
- Internal service-to-service
- Simple CRUD
- Clients are tightly coupled anyway

## Caching

### Cache Headers

```
Cache-Control: public, max-age=3600
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```

### Conditional Requests

```
GET /users/123
If-None-Match: "abc123"

Response: 304 Not Modified (if unchanged)
```

### Cache Invalidation

The hard problem. Options:
- Short TTLs with conditional requests
- Event-driven invalidation
- Cache tags for group invalidation

## Guild Members for REST

| Agent | Focus |
|-------|-------|
| **Ace** | DX, error messages, discoverability |
| **Vector** | Auth, rate limiting, input validation |
| **Karman** | Resource naming, URL structure |
| **Lamport** | Idempotency, consistency |
