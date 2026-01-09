# Kotlin Backend Deep Dive

Ktor, Spring Boot, and server-side patterns.

## Ktor

### Project Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.0.0"
    id("io.ktor.plugin") version "2.3.12"
    kotlin("plugin.serialization") version "2.0.0"
}

dependencies {
    implementation("io.ktor:ktor-server-core-jvm")
    implementation("io.ktor:ktor-server-netty-jvm")
    implementation("io.ktor:ktor-server-content-negotiation-jvm")
    implementation("io.ktor:ktor-serialization-kotlinx-json-jvm")
}
```

### Application Structure

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module)
        .start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureRouting()
    configureDI()
}

fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            ignoreUnknownKeys = true
        })
    }
}

fun Application.configureRouting() {
    routing {
        userRoutes()
        healthRoutes()
    }
}
```

### Routing

```kotlin
fun Route.userRoutes() {
    route("/users") {
        get {
            val users = userService.findAll()
            call.respond(users)
        }

        get("/{id}") {
            val id = call.parameters["id"]
                ?: return@get call.respond(HttpStatusCode.BadRequest)
            val user = userService.findById(id)
                ?: return@get call.respond(HttpStatusCode.NotFound)
            call.respond(user)
        }

        post {
            val request = call.receive<CreateUserRequest>()
            val user = userService.create(request)
            call.respond(HttpStatusCode.Created, user)
        }
    }
}
```

### Dependency Injection with Koin

```kotlin
val appModule = module {
    single { Database.connect() }
    single { UserRepository(get()) }
    single { UserService(get()) }
}

fun Application.configureDI() {
    install(Koin) {
        modules(appModule)
    }
}

fun Route.userRoutes() {
    val userService by inject<UserService>()
    // ...
}
```

### Error Handling

```kotlin
fun Application.configureStatusPages() {
    install(StatusPages) {
        exception<NotFoundException> { call, cause ->
            call.respond(HttpStatusCode.NotFound, ErrorResponse(cause.message))
        }
        exception<ValidationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, ErrorResponse(cause.message))
        }
        exception<Throwable> { call, cause ->
            logger.error("Unhandled exception", cause)
            call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Internal error"))
        }
    }
}
```

### Authentication

```kotlin
fun Application.configureSecurity() {
    install(Authentication) {
        jwt("auth-jwt") {
            realm = "access"
            verifier(JWT.require(Algorithm.HMAC256(secret))
                .withAudience(audience)
                .withIssuer(issuer)
                .build())
            validate { credential ->
                if (credential.payload.audience.contains(audience)) {
                    JWTPrincipal(credential.payload)
                } else null
            }
        }
    }
}

fun Route.protectedRoutes() {
    authenticate("auth-jwt") {
        get("/protected") {
            val principal = call.principal<JWTPrincipal>()
            val userId = principal!!.payload.getClaim("userId").asString()
            call.respond(mapOf("userId" to userId))
        }
    }
}
```

## Spring Boot with Kotlin

### Project Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.0.0"
    kotlin("plugin.spring") version "2.0.0"
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-webflux") // For coroutines
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor")
}
```

### Controller

```kotlin
@RestController
@RequestMapping("/api/users")
class UserController(private val userService: UserService) {

    @GetMapping
    suspend fun findAll(): List<User> = userService.findAll()

    @GetMapping("/{id}")
    suspend fun findById(@PathVariable id: String): User =
        userService.findById(id) ?: throw ResponseStatusException(HttpStatusCode.NOT_FOUND)

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    suspend fun create(@RequestBody @Valid request: CreateUserRequest): User =
        userService.create(request)
}
```

### Service

```kotlin
@Service
class UserService(private val userRepository: UserRepository) {

    suspend fun findAll(): List<User> = withContext(Dispatchers.IO) {
        userRepository.findAll()
    }

    suspend fun findById(id: String): User? = withContext(Dispatchers.IO) {
        userRepository.findById(id)
    }

    @Transactional
    suspend fun create(request: CreateUserRequest): User = withContext(Dispatchers.IO) {
        val user = User(
            id = UUID.randomUUID().toString(),
            email = request.email,
            name = request.name
        )
        userRepository.save(user)
    }
}
```

### Configuration

```kotlin
@Configuration
class AppConfig {

    @Bean
    fun objectMapper(): ObjectMapper = jacksonObjectMapper().apply {
        registerKotlinModule()
        disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
    }
}
```

### Exception Handling

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException::class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    fun handleNotFound(e: NotFoundException) = ErrorResponse(e.message)

    @ExceptionHandler(MethodArgumentNotValidException::class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    fun handleValidation(e: MethodArgumentNotValidException): ErrorResponse {
        val errors = e.bindingResult.fieldErrors
            .associate { it.field to it.defaultMessage }
        return ErrorResponse("Validation failed", errors)
    }
}
```

## Database Access

### Exposed (Kotlin SQL DSL)

```kotlin
// Table definition
object Users : Table() {
    val id = varchar("id", 36)
    val email = varchar("email", 255)
    val name = varchar("name", 255)
    override val primaryKey = PrimaryKey(id)
}

// Repository
class UserRepository(private val database: Database) {

    suspend fun findById(id: String): User? = dbQuery {
        Users.select { Users.id eq id }
            .map { it.toUser() }
            .singleOrNull()
    }

    suspend fun save(user: User) = dbQuery {
        Users.insert {
            it[id] = user.id
            it[email] = user.email
            it[name] = user.name
        }
    }

    private suspend fun <T> dbQuery(block: () -> T): T =
        withContext(Dispatchers.IO) {
            transaction(database) { block() }
        }
}
```

### R2DBC (Reactive)

```kotlin
@Repository
interface UserRepository : CoroutineCrudRepository<User, String> {
    suspend fun findByEmail(email: String): User?
}

// Or with DatabaseClient
@Repository
class UserRepository(private val client: DatabaseClient) {

    suspend fun findById(id: String): User? =
        client.sql("SELECT * FROM users WHERE id = :id")
            .bind("id", id)
            .map { row -> row.toUser() }
            .awaitOneOrNull()
}
```

## Comparison

### When to Choose Ktor

- Lightweight, explicit configuration preferred
- Kotlin Multiplatform (shared networking code)
- Fast startup time critical
- Team comfortable without framework magic
- Microservices with minimal dependencies

### When to Choose Spring Boot

- Enterprise features needed (security, batch, integration)
- Team has Java/Spring background
- Rich ecosystem for specific needs (actuator, cloud)
- Convention over configuration preferred
- Extensive documentation and community support

### Key Differences

| Aspect | Ktor | Spring Boot |
|--------|------|-------------|
| Configuration | Explicit | Auto-configuration |
| Coroutine support | Native | Via WebFlux adapter |
| Startup time | ~1-2s | ~3-5s |
| Memory footprint | Lower | Higher |
| Learning curve | Steeper | Gentler (for Java devs) |
| KMP support | Yes | No |

## Production Patterns

### Health Checks

```kotlin
// Ktor
fun Route.healthRoutes() {
    get("/health") {
        call.respond(mapOf("status" to "UP"))
    }

    get("/health/ready") {
        val dbHealthy = checkDatabase()
        val status = if (dbHealthy) HttpStatusCode.OK else HttpStatusCode.ServiceUnavailable
        call.respond(status, mapOf("database" to dbHealthy))
    }
}

// Spring Boot
@RestController
class HealthController(private val healthIndicator: DatabaseHealthIndicator) {

    @GetMapping("/health/ready")
    fun ready(): Map<String, Any> {
        val health = healthIndicator.health()
        return mapOf("status" to health.status.code)
    }
}
```

### Graceful Shutdown

```kotlin
// Ktor
fun main() {
    embeddedServer(Netty, port = 8080) {
        module()
    }.apply {
        Runtime.getRuntime().addShutdownHook(Thread {
            stop(1, 5, TimeUnit.SECONDS)
        })
        start(wait = true)
    }
}

// Spring Boot (automatic with actuator)
# application.yml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

### Request Logging

```kotlin
// Ktor
fun Application.configureLogging() {
    install(CallLogging) {
        level = Level.INFO
        filter { call -> call.request.path().startsWith("/api") }
        format { call ->
            "${call.request.httpMethod.value} ${call.request.path()} - ${call.response.status()}"
        }
    }
}
```

### Rate Limiting

```kotlin
// Ktor with RateLimit plugin
fun Application.configureRateLimiting() {
    install(RateLimit) {
        register(RateLimitName("api")) {
            rateLimiter(limit = 100, refillPeriod = 1.minutes)
        }
    }
}

fun Route.limitedRoutes() {
    rateLimit(RateLimitName("api")) {
        get("/api/resource") { ... }
    }
}
```
