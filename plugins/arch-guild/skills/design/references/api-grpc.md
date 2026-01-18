# gRPC Gotchas

Production lessons for gRPC API design.

## Streaming Patterns

### Unary (Request-Response)

```protobuf
service UserService {
  rpc GetUser(GetUserRequest) returns (User);
}
```

Simple, like REST. Use for most operations.

### Server Streaming

```protobuf
service EventService {
  rpc Subscribe(SubscribeRequest) returns (stream Event);
}
```

**Use cases:**
- Real-time feeds
- Large dataset download
- Server push notifications

**Gotcha:** Client must handle stream end and errors.

```go
stream, err := client.Subscribe(ctx, req)
for {
    event, err := stream.Recv()
    if err == io.EOF {
        break // Stream ended normally
    }
    if err != nil {
        // Handle error (connection lost, etc.)
        return err
    }
    process(event)
}
```

### Client Streaming

```protobuf
service UploadService {
  rpc Upload(stream Chunk) returns (UploadResult);
}
```

**Use cases:**
- File uploads
- Batch operations
- Aggregating client data

### Bidirectional Streaming

```protobuf
service ChatService {
  rpc Chat(stream Message) returns (stream Message);
}
```

**Use cases:**
- Real-time chat
- Game state sync
- Collaborative editing

**Gotcha:** Complex error handling, both sides can fail independently.

## Versioning Protobuf

### Safe Changes (Backward Compatible)

- Adding new fields (with new field numbers)
- Adding new services or methods
- Adding new enum values
- Changing field from singular to repeated (if wire type matches)
- Deprecating fields

### Breaking Changes (Avoid)

- Removing fields
- Changing field numbers
- Changing field types
- Renaming fields (binary safe, but breaks generated code)
- Changing `optional` to `required`

### Versioning Strategy

**Package versioning:**
```protobuf
package myservice.v1;

service UserService { ... }
```

```protobuf
package myservice.v2;

service UserService { ... }
```

**Reserved fields:**
```protobuf
message User {
  reserved 2, 15, 9 to 11;
  reserved "old_field", "deprecated_field";

  string id = 1;
  string name = 3;
}
```

Prevents accidental reuse of removed field numbers.

## Error Handling

### gRPC Status Codes

| Code | Use For |
|------|---------|
| OK (0) | Success |
| CANCELLED (1) | Client cancelled |
| UNKNOWN (2) | Unknown error |
| INVALID_ARGUMENT (3) | Bad input |
| NOT_FOUND (5) | Resource not found |
| ALREADY_EXISTS (6) | Duplicate |
| PERMISSION_DENIED (7) | Auth failure |
| RESOURCE_EXHAUSTED (8) | Rate limited |
| FAILED_PRECONDITION (9) | Wrong state for operation |
| ABORTED (10) | Conflict (retry may succeed) |
| UNIMPLEMENTED (12) | Not implemented |
| INTERNAL (13) | Server bug |
| UNAVAILABLE (14) | Transient failure (retry) |
| UNAUTHENTICATED (16) | No auth |

### Rich Error Details

```go
import "google.golang.org/genproto/googleapis/rpc/errdetails"

st := status.New(codes.InvalidArgument, "Invalid request")
st, _ = st.WithDetails(&errdetails.BadRequest{
    FieldViolations: []*errdetails.BadRequest_FieldViolation{
        {Field: "email", Description: "Invalid format"},
    },
})
return st.Err()
```

### Common Mistakes

```go
// Wrong: Generic error
return status.Error(codes.Internal, "something went wrong")

// Right: Specific code with details
return status.Error(codes.InvalidArgument, "email must be valid")

// Wrong: Using HTTP-style thinking
return status.Error(codes.NotFound, "404 not found")

// Right: gRPC semantics
return status.Error(codes.NotFound, "user abc123 not found")
```

## Interceptors

gRPC middleware pattern.

### Unary Interceptor

```go
func loggingInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    log.Printf("method=%s duration=%v error=%v",
        info.FullMethod, time.Since(start), err)
    return resp, err
}

server := grpc.NewServer(
    grpc.UnaryInterceptor(loggingInterceptor),
)
```

### Chaining Interceptors

```go
import "google.golang.org/grpc/middleware"

server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(
        loggingInterceptor,
        authInterceptor,
        metricsInterceptor,
    ),
)
```

### Stream Interceptors

Different signature, wraps the stream:

```go
func streamLoggingInterceptor(
    srv interface{},
    ss grpc.ServerStream,
    info *grpc.StreamServerInfo,
    handler grpc.StreamHandler,
) error {
    start := time.Now()
    err := handler(srv, ss)
    log.Printf("stream=%s duration=%v error=%v",
        info.FullMethod, time.Since(start), err)
    return err
}
```

## Deadlines and Timeouts

### Client-Side Deadline

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

resp, err := client.GetUser(ctx, req)
if err != nil {
    if status.Code(err) == codes.DeadlineExceeded {
        // Timeout
    }
}
```

### Server-Side Checking

```go
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    // Check if already past deadline
    if ctx.Err() == context.DeadlineExceeded {
        return nil, status.Error(codes.DeadlineExceeded, "deadline exceeded")
    }

    // Check before expensive operation
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    return s.db.GetUser(ctx, req.Id)
}
```

### Deadline Propagation

Deadlines automatically propagate through gRPC calls. A client deadline of 5s on call A means call A's downstream call B inherits remaining time.

## Load Balancing

### Client-Side LB (Default)

```go
conn, err := grpc.Dial(
    "dns:///myservice.example.com",
    grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`),
)
```

**Policies:**
- `pick_first` (default): Use first healthy server
- `round_robin`: Rotate through servers

### Server-Side LB (Proxy)

Use Envoy, Linkerd, or similar. Better for:
- Weighted routing
- Circuit breaking
- Advanced health checking

## Connection Management

### Connection Reuse

gRPC maintains persistent connections. Don't create new connections per request:

```go
// Wrong: Connection per request
func getUser(id string) (*User, error) {
    conn, _ := grpc.Dial(...)
    defer conn.Close()
    client := pb.NewUserServiceClient(conn)
    return client.GetUser(...)
}

// Right: Shared connection
var conn *grpc.ClientConn

func init() {
    conn, _ = grpc.Dial(...)
}

func getUser(id string) (*User, error) {
    client := pb.NewUserServiceClient(conn)
    return client.GetUser(...)
}
```

### Keep-Alive

```go
conn, err := grpc.Dial(target,
    grpc.WithKeepaliveParams(keepalive.ClientParameters{
        Time:                10 * time.Second,
        Timeout:             3 * time.Second,
        PermitWithoutStream: true,
    }),
)
```

## Guild Members for gRPC

| Agent | Focus |
|-------|-------|
| **Lamport** | Streaming, deadline propagation |
| **Erlang** | Backpressure, connection management |
| **Vector** | mTLS, auth interceptors |
| **Burner** | Service boundaries, proto organization |
