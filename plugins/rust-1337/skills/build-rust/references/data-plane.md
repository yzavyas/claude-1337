# Proxies & Data Plane

Building proxies, API gateways, service mesh components, traffic routing infrastructure.

## Proxy Frameworks

| Framework | Best For | Unique Value |
|-----------|----------|--------------|
| **Pingora** | CDN/edge at massive scale | Shared connection pools, 1T req/day @ Cloudflare |
| **Rama** | Flexible network tooling | Fingerprint emulation (JA3/JA4), MITM, scraping |
| **Sōzu** | Hot-reconfigurable routing | Runtime config via unix socket, zero-downtime |
| **Quilkin** | UDP game servers | Agones integration, DDoS mitigation |

### Pingora

THE choice for high-performance HTTP reverse proxy at scale.

```rust
use pingora::prelude::*;

pub struct MyProxy;

#[async_trait]
impl ProxyHttp for MyProxy {
    async fn upstream_peer(&self, _session: &mut Session, _ctx: &mut ())
        -> Result<Box<HttpPeer>>
    {
        let peer = HttpPeer::new(("1.1.1.1", 443), true, "one.one.one.one".into());
        Ok(Box::new(peer))
    }
}
```

**Performance vs Nginx**: 70% less CPU, 67% less memory, 80ms TTFB reduction.

**Gotcha**: `pingora_cache` is EXPERIMENTAL - API volatile.

**Load balancing**: `pingora_load_balancing` crate (Round Robin, Least Connections, IP Hash)

### Rama

Flexible framework for proxies, MITM, scrapers, API gateways.

**Unique features**:
- TLS fingerprint emulation (JA3, JA4, Akamai H2)
- MITM and distortion proxies
- HAR export, curl conversion diagnostics
- User-Agent emulation

**Status**: "Experimental" but used in production for network security, data extraction.

**Use when**: Building scrapers, security tools, anything needing fingerprint control.

### Sōzu

Hot-reconfigurable reverse proxy - config changes without restart.

**Unique**: Runtime configuration via secure unix sockets, zero-downtime upgrades.

**Use when**: PaaS routing layers, environments with constant config changes.

**Who uses it**: Clever Cloud (built it for their PaaS).

### Quilkin

UDP proxy for multiplayer game servers.

**Features**: Agones integration, xDS discovery, DDoS mitigation, packet inspection.

**Use when**: Game servers on Kubernetes with Agones. Niche but best-in-class for it.

## Service Mesh Sidecars

If you're in a service mesh, the proxy choice is made for you:

| Mesh | Proxy | Notes |
|------|-------|-------|
| **Linkerd** | linkerd2-proxy | <1ms p99, <10MB RAM |
| **Istio ambient** | ztunnel | L4-only, 90% less memory than Envoy |

Don't build custom service mesh proxies. Use the mesh's native proxy.

## xDS

Envoy's dynamic configuration protocol: LDS (Listeners), EDS (Endpoints), RDS (Routes), CDS (Clusters), SDS (Secrets).

### xDS Client

**Use**: `xds-api` crate - Tonic bindings for xDS v3.

```rust
use xds_api::envoy::service::discovery::v3::{
    DiscoveryRequest, DiscoveryResponse,
    aggregated_discovery_service_client::AggregatedDiscoveryServiceClient,
};

async fn connect_xds(addr: &str) -> Result<(), Error> {
    let channel = tonic::transport::Channel::from_shared(addr)?
        .connect().await?;
    let mut client = AggregatedDiscoveryServiceClient::new(channel);
    // Stream discovery requests/responses
}
```

### xDS Control Plane

**Use go-control-plane**. Rust options (rust-control-plane, envoy-control-plane) not production-ready.

## proxy-wasm (Envoy Extensions)

Write Envoy filters in Rust, compile to WASM.

```rust
use proxy_wasm::traits::*;
use proxy_wasm::types::*;

impl HttpContext for MyFilter {
    fn on_http_request_headers(&mut self, _: usize, _: bool) -> Action {
        self.add_http_request_header("x-custom", "value");
        Action::Continue
    }
}
```

**Performance**: ~50% of native. Trade-off: easier than custom Envoy builds.

## Traffic Management Patterns

### Load Balancing

- **Pingora**: `pingora_load_balancing` (Round Robin, Least Connections, IP Hash)
- **Tower**: `tower::balance` for service-level balancing

### Health Checking

```rust
// Tower-style with load shedding
let service = ServiceBuilder::new()
    .load_shed()
    .concurrency_limit(100)
    .service(my_service);
```

### Circuit Breakers

States: Closed (normal) → Open (failing) → Half-Open (testing)

**Gotcha**: Don't retry into overload - combine with backoff.

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Pingora cache volatile | Build custom cache |
| xDS control plane | Use Go, not Rust |
| proxy-wasm 50% native perf | Acceptable trade-off for ease |
| ztunnel L4-only | Need waypoint proxy for L7 |
| Quilkin UDP-only | Not for HTTP/TCP |
