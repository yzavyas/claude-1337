# Networking

HTTP clients, protocol crates, servers, middleware - building apps that talk to things.

## HTTP Client

**Use**: `reqwest` for most cases, `hyper` if you need low-level control.

```rust
// reqwest - batteries included
let client = reqwest::Client::new();
let resp = client.get("https://api.example.com")
    .bearer_auth(token)
    .send()
    .await?;

// Connection pooling is automatic
```

**Gotcha**: Don't create a new `Client` per request - reuse it for connection pooling.

## Protocol Crates

| Protocol | Crate | Notes |
|----------|-------|-------|
| gRPC | **tonic** | Only serious option |
| QUIC | **quinn** | Pure Rust, mature |
| WebSocket | **tokio-tungstenite** | Tokio ecosystem |
| Kafka | **rdkafka** | librdkafka bindings, battle-tested |
| Redis | **fred** | Full cluster support, maintained |
| NATS | **async-nats** | Official client |
| DNS | **hickory-resolver** | Async DNS (std DNS is blocking!) |

## gRPC with Tonic

```rust
// Client
let mut client = MyServiceClient::connect("http://[::1]:50051").await?;
let response = client.my_method(Request::new(MyRequest { ... })).await?;

// Server
Server::builder()
    .add_service(MyServiceServer::new(my_impl))
    .serve(addr)
    .await?;
```

**Gotcha**: Default 4MB message limit. Configure `max_decoding_message_size()` for large payloads.

## WebSocket

```rust
use tokio_tungstenite::connect_async;

let (ws_stream, _) = connect_async("wss://example.com/ws").await?;
let (write, read) = ws_stream.split();

// Send/receive with futures stream/sink
```

## TLS

| Choose | When |
|--------|------|
| **rustls** | Default - pure Rust, portable, fast |
| boring | FIPS compliance required |

## Middleware: Tower

THE middleware framework for async Rust services.

```rust
use tower::ServiceBuilder;

let service = ServiceBuilder::new()
    .load_shed()
    .concurrency_limit(100)
    .rate_limit(1000, Duration::from_secs(1))
    .timeout(Duration::from_secs(30))
    .service(my_service);
```

**Tower layers you'll use**:
- `timeout` - Request timeouts
- `concurrency_limit` - Max concurrent requests
- `rate_limit` - Requests per time window
- `load_shed` - Reject when overloaded
- `retry` - Retry failed requests

## Building Servers

**Use**: `axum` (built on Tower/Hyper, from Tokio team)

```rust
use axum::{routing::get, Router};

let app = Router::new()
    .route("/", get(handler))
    .layer(tower_http::trace::TraceLayer::new_for_http());

let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app).await?;
```

## Protocol Framing

For custom binary protocols:

```rust
use tokio_util::codec::{Framed, LengthDelimitedCodec};

let codec = LengthDelimitedCodec::builder()
    .length_field_type::<u16>()
    .max_frame_length(8 * 1024 * 1024)
    .new_codec();

let framed = Framed::new(socket, codec);
```

## Graceful Shutdown

```rust
use tokio_util::sync::CancellationToken;

async fn run_server(token: CancellationToken) {
    loop {
        tokio::select! {
            _ = token.cancelled() => break,
            result = listener.accept() => {
                let (socket, _) = result?;
                tokio::spawn(handle(socket, token.clone()));
            }
        }
    }
    // Drain with timeout
    tokio::time::timeout(Duration::from_secs(30), drain()).await.ok();
}
```

## Connection Pooling

Most clients (reqwest, sqlx, fred) handle this automatically. Key settings:

- **Pool size**: Start with `2 * CPU cores`
- **Idle timeout**: Match your load patterns
- **Max lifetime**: Prevent stale connections

```rust
// Example: deadpool for databases
use deadpool_postgres::{Config, Pool, Runtime};

let pool = Config {
    host: Some("localhost".into()),
    ..Default::default()
}
.create_pool(Some(Runtime::Tokio1), NoTls)?;
```

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| std DNS is blocking | Use `hickory-resolver` |
| TCP_NODELAY for RPC | Disable Nagle for low latency |
| tonic 4MB limit | Configure `max_decoding_message_size()` |
| New client per request | Reuse clients for connection pooling |
| Blocking in async | See async.md |
