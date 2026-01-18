---
name: operations
description: This skill should be used when the user asks to "review for production", "check production readiness", "evaluate resilience", "assess observability", "review ops", "run chaos experiments", or discusses deployment, monitoring, incident response, failure modes, or chaos engineering.
---

# Operations

Production readiness evaluation focused on resilience, observability, and incident response.

## Resilience

### Failure Modes

- What can fail? List all external dependencies
- Blast radius: If X fails, what else breaks?
- Graceful degradation: Partial failure ≠ total failure?

### Patterns

| Pattern | Purpose | Check |
|---------|---------|-------|
| **Timeouts** | Prevent hung connections | Every external call has one? |
| **Circuit Breaker** | Stop cascading failures | On critical paths? |
| **Bulkhead** | Isolate failures | Separate thread pools? |
| **Retry** | Handle transient failures | With backoff? Bounded? |

## Observability

### The RED Method

| Metric | What | Why |
|--------|------|-----|
| **R**ate | Requests per second | Traffic understanding |
| **E**rrors | Failed requests | Problem detection |
| **D**uration | Latency distribution | Performance tracking |

### Logging

- Structured (JSON, not free text)
- Correlation IDs across services
- Appropriate levels (not everything is ERROR)
- PII redaction

### Tracing

- Distributed tracing enabled?
- Spans for all external calls?
- Context propagation working?

## Capacity

- **Scaling**: Horizontal preferred, auto-scaling configured?
- **Limits**: Memory, CPU, connections all bounded?
- **Backpressure**: What happens at 2x load? 10x?
- **Rate Limiting**: Per-tenant/client quotas?

## Security Posture

- **Secrets**: In vault, not env vars or code
- **Network**: Least privilege, mTLS where possible
- **Dependencies**: Vulnerability scanning in CI
- **Access**: Audit logging for sensitive operations

## Incident Readiness

- **Runbooks**: Documented recovery procedures
- **On-call**: Rotation defined, escalation clear
- **Rollback**: One-click, tested regularly
- **Communication**: Status page, stakeholder notification

## Checklist

```
□ All external calls have timeouts
□ Circuit breakers on critical paths
□ Structured logging with correlation IDs
□ RED metrics exposed
□ Alerts are actionable (not noisy)
□ Auto-scaling configured with limits
□ Graceful shutdown implemented
□ Health checks (liveness + readiness)
□ Secrets in vault
□ Runbook exists
□ Rollback tested
```

## Guild Members for Operations

Primary: **Taleb** (resilience), **Erlang** (capacity), **Vector** (security)
Secondary: **Lamport** (distributed failure), **Ixian** (metrics/validation)

## Additional Resources

- **`references/chaos-patterns.md`** — Chaos engineering patterns and failure injection
