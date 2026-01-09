# Kotlin Multiplatform Deep Dive

KMP architecture, expect/actual, and production patterns.

## KMP Status (2025)

Kotlin Multiplatform is **production-ready** since November 2023. Major companies using it include:
- Google Docs (iOS app)
- Netflix
- McDonald's
- Cash App

**Source:** [Guarana Technologies: KMP Production Ready 2025](https://guarana-technologies.com/blog/kotlin-multiplatform-production)

## Project Structure

```
project/
├── shared/
│   ├── src/
│   │   ├── commonMain/    # Shared Kotlin code
│   │   ├── commonTest/    # Shared tests
│   │   ├── androidMain/   # Android-specific
│   │   ├── iosMain/       # iOS-specific
│   │   └── jvmMain/       # JVM-specific (backend)
│   └── build.gradle.kts
├── androidApp/            # Android application
├── iosApp/               # iOS application (Xcode)
└── build.gradle.kts
```

### Gradle Configuration

```kotlin
// shared/build.gradle.kts
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
    id("com.android.library")
}

kotlin {
    androidTarget()

    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "shared"
            isStatic = true
        }
    }

    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
            implementation("io.ktor:ktor-client-core:2.3.12")
        }

        androidMain.dependencies {
            implementation("io.ktor:ktor-client-okhttp:2.3.12")
        }

        iosMain.dependencies {
            implementation("io.ktor:ktor-client-darwin:2.3.12")
        }
    }
}
```

## Expect/Actual Mechanism

### How It Works

`expect` declares an API in common code. `actual` provides platform implementations:

```kotlin
// commonMain
expect class Platform() {
    val name: String
}

expect fun randomUUID(): String

// androidMain
actual class Platform {
    actual val name: String = "Android ${Build.VERSION.SDK_INT}"
}

actual fun randomUUID(): String = UUID.randomUUID().toString()

// iosMain
actual class Platform {
    actual val name: String = UIDevice.currentDevice.systemName()
}

actual fun randomUUID(): String = NSUUID().UUIDString()
```

### When to Use Expect/Actual

| Scenario | Approach |
|----------|----------|
| Platform API (UUID, device info) | expect/actual |
| Networking, serialization | KMP libraries (Ktor, kotlinx.serialization) |
| Business logic | Common code |
| UI | Platform-native or Compose Multiplatform |

### Alternative: Dependency Injection

Sometimes DI is cleaner than expect/actual:

```kotlin
// commonMain
interface PlatformLogger {
    fun log(message: String)
}

class MyService(private val logger: PlatformLogger) {
    fun doWork() {
        logger.log("Working...")
    }
}

// androidMain
class AndroidLogger : PlatformLogger {
    override fun log(message: String) = Log.d("MyApp", message)
}

// iosMain
class IosLogger : PlatformLogger {
    override fun log(message: String) = NSLog(message)
}
```

## Shared Code Patterns

### Repository Pattern

```kotlin
// commonMain
interface UserRepository {
    suspend fun getUser(id: String): User?
    suspend fun saveUser(user: User)
}

class UserRepositoryImpl(
    private val api: UserApi,
    private val cache: UserCache
) : UserRepository {

    override suspend fun getUser(id: String): User? {
        return cache.get(id) ?: api.fetchUser(id)?.also {
            cache.save(it)
        }
    }

    override suspend fun saveUser(user: User) {
        api.saveUser(user)
        cache.save(user)
    }
}
```

### Network Layer with Ktor

```kotlin
// commonMain
class UserApi(private val client: HttpClient) {

    suspend fun fetchUser(id: String): User? =
        client.get("$BASE_URL/users/$id").body()

    suspend fun saveUser(user: User): User =
        client.post("$BASE_URL/users") {
            contentType(ContentType.Application.Json)
            setBody(user)
        }.body()
}

// Ktor client factory
expect fun createHttpClient(): HttpClient

// androidMain
actual fun createHttpClient(): HttpClient = HttpClient(OkHttp) {
    install(ContentNegotiation) { json() }
}

// iosMain
actual fun createHttpClient(): HttpClient = HttpClient(Darwin) {
    install(ContentNegotiation) { json() }
}
```

### Local Storage with SQLDelight

```kotlin
// commonMain (SQLDelight generates from .sq files)
interface DatabaseDriverFactory {
    fun createDriver(): SqlDriver
}

class Database(driverFactory: DatabaseDriverFactory) {
    private val driver = driverFactory.createDriver()
    private val database = AppDatabase(driver)
    private val queries = database.userQueries

    fun getUser(id: String): User? =
        queries.selectById(id).executeAsOneOrNull()?.toUser()
}

// androidMain
class AndroidDatabaseDriverFactory(private val context: Context) : DatabaseDriverFactory {
    override fun createDriver(): SqlDriver =
        AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
}

// iosMain
class IosDatabaseDriverFactory : DatabaseDriverFactory {
    override fun createDriver(): SqlDriver =
        NativeSqliteDriver(AppDatabase.Schema, "app.db")
}
```

## Compose Multiplatform

### Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("multiplatform")
    id("org.jetbrains.compose")
}

kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
        }
    }
}
```

### Shared UI

```kotlin
// commonMain
@Composable
fun UserProfile(user: User, onEdit: () -> Unit) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(
            text = user.name,
            style = MaterialTheme.typography.headlineMedium
        )
        Text(
            text = user.email,
            style = MaterialTheme.typography.bodyMedium
        )
        Button(onClick = onEdit) {
            Text("Edit Profile")
        }
    }
}
```

## Testing in KMP

### Shared Tests

```kotlin
// commonTest
class UserRepositoryTest {

    @Test
    fun `returns cached user when available`() = runTest {
        val cache = FakeUserCache()
        val api = FakeUserApi()
        val repo = UserRepositoryImpl(api, cache)

        cache.save(testUser)

        val result = repo.getUser(testUser.id)

        assertEquals(testUser, result)
        assertFalse(api.wasCalled)
    }
}
```

### Platform-Specific Tests

```kotlin
// androidTest
class AndroidSpecificTest {
    @Test
    fun `uses android-specific implementation`() {
        val platform = Platform()
        assertTrue(platform.name.startsWith("Android"))
    }
}
```

## Production Considerations

### Memory Management on iOS

The new Kotlin/Native memory model (default since 1.7.20) handles most cases, but:

- Large objects (UIImage, camera frames) should be released promptly
- Use `autoreleasepool { }` for tight loops creating many objects
- Avoid holding references to UIKit objects in shared code

### Build Performance

```kotlin
// gradle.properties
kotlin.native.cacheKind=static
kotlin.mpp.enableCInteropCommonization=true
```

### Binary Size

- Use `-Xbinary=bundleId=your.bundle.id` for proper iOS bundle
- Strip debug symbols for release: `kotlin.native.isReleaseBinaryLinked=true`
- Consider static frameworks for smaller size

### Swift Interop

```kotlin
// Expose suspend functions to Swift
class UserRepositoryWrapper(private val repo: UserRepository) {
    fun getUser(id: String, completion: (User?, Error?) -> Unit) {
        GlobalScope.launch {
            try {
                val user = repo.getUser(id)
                completion(user, null)
            } catch (e: Exception) {
                completion(null, e)
            }
        }
    }
}
```

**Note:** Swift Export (experimental) is improving direct suspend function access from Swift.

## Architecture Recommendations

### What to Share

| Share | Keep Platform-Specific |
|-------|------------------------|
| Business logic | UI (or use Compose Multiplatform) |
| Data models | Platform APIs (camera, sensors) |
| Networking | Navigation (platform conventions) |
| Caching | Notifications |
| Validation | Deep links |

### Dependency Injection

```kotlin
// commonMain
class SharedModule {
    val userApi by lazy { UserApi(createHttpClient()) }
    val userRepository by lazy { UserRepositoryImpl(userApi, userCache) }
    val userViewModel by lazy { UserViewModel(userRepository) }
}

// androidMain
class AndroidModule : SharedModule() {
    val context: Context // Injected by Android DI
}

// iosMain
class IosModule : SharedModule()
```
