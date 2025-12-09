# Backend Services

APIs, databases, gRPC. Best-in-class choices.

## Framework

**Use axum**. Tokio-native, Tower middleware, best ergonomics.

actix-web only if you've benchmarked and need that last 5% throughput.

```rust
use axum::{routing::get, Router};

let app = Router::new()
    .route("/health", get(|| async { "ok" }))
    .layer(TraceLayer::new_for_http());

let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app).await?;
```

## Database

```
Async web service?
├── YES → sqlx (compile-time verified SQL)
└── NO → diesel (sync, mature ORM)
```

**sqlx has built-in pooling** - don't add bb8/deadpool.

```rust
let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect(&database_url).await?;

// Compile-time checked query
let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
    .fetch_one(&pool).await?;
```

## gRPC

**Use tonic**. Only serious option.

```rust
// Build from proto
tonic_build::compile_protos("proto/service.proto")?;

// Server
Server::builder()
    .add_service(MyServiceServer::new(handler))
    .serve(addr).await?;

// Client
let mut client = MyServiceClient::connect("http://[::1]:50051").await?;
```

**Gotcha**: 4MB default message limit. Configure `max_decoding_message_size()`.

## API Patterns

| Need | Crate |
|------|-------|
| OpenAPI docs | **utoipa** + utoipa-swagger-ui |
| Validation | **garde** |
| Auth middleware | Tower layer with JWT |

## Axum Extractors

**Order matters**: State → Path → Query → Json (body-consuming LAST)

```rust
async fn handler(
    State(db): State<Pool>,
    Path(id): Path<u32>,
    Query(params): Query<Pagination>,
    Json(body): Json<CreateUser>,  // Must be last
) -> Result<Json<User>, AppError> {
    // ...
}
```

## Error Handling

```rust
#[derive(thiserror::Error, Debug)]
enum AppError {
    #[error("not found")]
    NotFound,
    #[error("database error")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let status = match &self {
            AppError::NotFound => StatusCode::NOT_FOUND,
            AppError::Database(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        (status, self.to_string()).into_response()
    }
}
```

## Production Stack

```rust
let app = Router::new()
    .route("/api/*", api_routes())
    .layer(TraceLayer::new_for_http())
    .layer(TimeoutLayer::new(Duration::from_secs(10)))
    .layer(CompressionLayer::new())
    .layer(CorsLayer::permissive());
```

## Graceful Shutdown

```rust
axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await?;

async fn shutdown_signal() {
    tokio::signal::ctrl_c().await.ok();
}
```

## Observability

| Need | Crate |
|------|-------|
| Logging | **tracing** + tracing-subscriber |
| Metrics | **metrics** + metrics-exporter-prometheus |
| Health check | `/health` (liveness), `/ready` (db check) |

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Extractor order | Body-consuming (Json) must be last |
| sqlx compile check | Set DATABASE_URL at build time |
| tonic message size | Configure max_decoding_message_size |
| Graceful shutdown | Handle SIGTERM for k8s |
| N+1 queries | Use sqlx::query with JOINs |
