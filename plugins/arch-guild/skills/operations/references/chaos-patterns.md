# Chaos Engineering Patterns

Systematic failure injection to build confidence in system resilience.

## Core Principles

From Principles of Chaos Engineering:

1. **Build a hypothesis around steady state behavior**
2. **Vary real-world events** (failures, traffic spikes, etc.)
3. **Run experiments in production** (or prod-like)
4. **Automate experiments to run continuously**
5. **Minimize blast radius**

## Steady State Hypothesis

Before breaking things, define "normal":

```yaml
steady_state:
  metrics:
    - name: error_rate
      threshold: "< 1%"
    - name: p99_latency
      threshold: "< 500ms"
    - name: availability
      threshold: "> 99.9%"

  assertions:
    - "Users can complete checkout"
    - "Search returns results within 2s"
    - "Orders are processed within 5m"
```

**The experiment:** Inject failure → measure → compare to steady state.

## Failure Injection Types

### Network Failures

| Failure | What It Tests | Tool |
|---------|---------------|------|
| Latency injection | Timeout handling | tc, toxiproxy |
| Packet loss | Retry logic | tc |
| DNS failure | Fallback behavior | iptables |
| Partition | Split-brain handling | iptables |

**Example: 500ms latency injection**
```bash
tc qdisc add dev eth0 root netem delay 500ms
```

### Process Failures

| Failure | What It Tests | Tool |
|---------|---------------|------|
| Process kill | Restart behavior | kill -9 |
| OOM | Memory handling | stress-ng |
| CPU saturation | Throttling | stress-ng |
| Disk full | Error handling | fallocate |

**Example: Kill random container**
```bash
docker kill $(docker ps -q | shuf -n 1)
```

### Resource Exhaustion

| Failure | What It Tests | Tool |
|---------|---------------|------|
| Connection pool exhaustion | Pool sizing | siege |
| File descriptor exhaustion | Limit handling | ulimit |
| Thread pool saturation | Backpressure | load generator |

### Dependency Failures

| Failure | What It Tests | Tool |
|---------|---------------|------|
| Database unavailable | Fallback/cache | toxiproxy |
| External API timeout | Circuit breaker | toxiproxy |
| Message queue down | Retry/dead letter | iptables |

## GameDay Planning

### Pre-GameDay

1. **Define scope**: What systems? What failures?
2. **Set success criteria**: What's acceptable degradation?
3. **Prepare rollback**: How to stop the experiment fast?
4. **Notify stakeholders**: Who needs to know?
5. **Schedule**: Off-peak, with full team available

### GameDay Checklist

```
Before:
□ Rollback procedure documented and tested
□ Monitoring dashboards open
□ Team in war room (or Slack channel)
□ Customer support notified
□ No other changes scheduled

During:
□ Start small, escalate gradually
□ Monitor metrics continuously
□ Document observations real-time
□ Stop immediately if unexpected

After:
□ Return to steady state
□ Document findings
□ Create action items
□ Update runbooks
□ Share learnings
```

### GameDay Template

```markdown
# GameDay: [Service] [Date]

## Hypothesis
If [failure], then [service] will [expected behavior].

## Scope
- Services: [list]
- Failure type: [type]
- Duration: [time]
- Blast radius: [affected scope]

## Success Criteria
- Error rate < [X]%
- Latency p99 < [Y]ms
- No customer impact

## Rollback
1. [Step to stop failure injection]
2. [Step to restore normal operation]
3. [Verification step]

## Results
[Documented after GameDay]

## Action Items
- [ ] [Finding → action]
```

## Chaos Monkey Principles

Netflix's original chaos:

1. **Random instance termination**: Any instance can die
2. **During business hours**: When team can respond
3. **Automated**: Runs continuously
4. **Opt-out available**: New services can exclude temporarily

### Simian Army (Expanded)

| Monkey | Purpose |
|--------|---------|
| Chaos Monkey | Random instance termination |
| Latency Monkey | Artificial delays |
| Conformity Monkey | Find non-compliant instances |
| Doctor Monkey | Health checks |
| Janitor Monkey | Cleanup unused resources |
| Security Monkey | Find security issues |
| Chaos Gorilla | Kill entire availability zone |
| Chaos Kong | Kill entire region |

## Blast Radius Containment

### Start Small

```
Level 1: Single instance, non-critical path
Level 2: Single instance, critical path
Level 3: Multiple instances, single AZ
Level 4: Entire AZ
Level 5: Cross-region (with extreme caution)
```

### Abort Conditions

Automatic experiment termination if:
- Error rate exceeds threshold
- Customer impact detected
- On-call paged
- Monitoring system itself fails

```python
class ChaosExperiment:
    def should_abort(self, metrics):
        if metrics.error_rate > 0.05:  # 5%
            return True
        if metrics.pager_duty_incidents > 0:
            return True
        if not metrics.monitoring_healthy:
            return True
        return False
```

## Production vs Staging

| Aspect | Production | Staging |
|--------|------------|---------|
| Realism | High | Lower |
| Risk | Higher | Lower |
| Findings validity | Definitive | May not apply |
| Blast radius | Real customers | Test data |

**Recommendation:** Start in staging, graduate to production with safeguards.

## Common Experiments

### Circuit Breaker Validation

```yaml
experiment:
  name: "Validate payment service circuit breaker"
  hypothesis: "When payment service fails, checkout degrades gracefully"

  steady_state:
    - "Checkout success rate > 99%"
    - "Payment errors are retried 3 times"

  method:
    - action: "Block payment service endpoint"
      duration: "5 minutes"

  expected:
    - "Circuit breaker opens after 5 failures"
    - "Fallback message shown to users"
    - "Recovery within 30s of restoration"
```

### Timeout Validation

```yaml
experiment:
  name: "Validate search timeout handling"

  method:
    - action: "Add 10s latency to search service"

  expected:
    - "Requests timeout after 5s"
    - "Error page shows within 6s"
    - "No connection pool exhaustion"
```

### Data Corruption Handling

```yaml
experiment:
  name: "Handle corrupted cache data"

  method:
    - action: "Inject malformed JSON into cache"

  expected:
    - "Application falls back to database"
    - "Error logged with correlation ID"
    - "Cache entry invalidated"
```

## Tools

| Tool | Type | Use Case |
|------|------|----------|
| **Chaos Monkey** | Instance | Random termination |
| **Gremlin** | Platform | Comprehensive chaos |
| **LitmusChaos** | Kubernetes | K8s-native chaos |
| **Toxiproxy** | Network | Proxy-based failures |
| **tc/netem** | Network | Linux traffic control |
| **Pumba** | Docker | Container chaos |
| **PowerfulSeal** | Kubernetes | K8s chaos |
| **Chaos Toolkit** | Framework | Experiment orchestration |

## Guild Members for Chaos

| Agent | Focus |
|-------|-------|
| **Taleb** | Overall resilience, Black Swan scenarios |
| **Erlang** | Saturation, backpressure behavior |
| **Vector** | Security implications of failures |
| **Ixian** | Metrics, validation criteria |
