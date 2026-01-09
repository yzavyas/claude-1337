# Kotlin Testing Deep Dive

Kotest, MockK, coroutine testing, and best practices.

## Kotest

### Spec Styles

```kotlin
// FunSpec — simple function-based tests
class UserServiceTest : FunSpec({
    test("creates user") {
        val user = service.create("test@example.com")
        user.email shouldBe "test@example.com"
    }
})

// BehaviorSpec — BDD style
class UserServiceTest : BehaviorSpec({
    given("a valid email") {
        `when`("creating a user") {
            then("returns the user") {
                // ...
            }
        }
    }
})

// StringSpec — minimal
class UserServiceTest : StringSpec({
    "creates user with valid email" {
        // ...
    }
})
```

### Assertions

```kotlin
// Matchers
result shouldBe expected
result shouldNotBe wrong
list shouldContain element
list shouldHaveSize 3
string shouldStartWith "Hello"
string shouldMatch Regex("\\d+")

// Exceptions
shouldThrow<IllegalArgumentException> {
    validate(invalidInput)
}

// Collections
list.shouldBeEmpty()
list.shouldContainExactly(1, 2, 3)
list.shouldContainAll(1, 2)

// Soft assertions (collect all failures)
assertSoftly {
    user.name shouldBe "John"
    user.email shouldBe "john@example.com"
    user.age shouldBe 30
}
```

### Property-Based Testing

```kotlin
class PropertyTest : FunSpec({
    test("reverse of reverse is original") {
        checkAll(Arb.string()) { s ->
            s.reversed().reversed() shouldBe s
        }
    }

    test("addition is commutative") {
        checkAll(Arb.int(), Arb.int()) { a, b ->
            a + b shouldBe b + a
        }
    }
})
```

### Data-Driven Testing

```kotlin
class DataDrivenTest : FunSpec({
    context("validation") {
        withData(
            "valid@email.com" to true,
            "invalid" to false,
            "@missing.com" to false,
        ) { (email, expected) ->
            validator.isValid(email) shouldBe expected
        }
    }
})
```

## MockK

### Creating Mocks

```kotlin
// Regular mock
val mock = mockk<UserRepository>()

// Relaxed mock (returns defaults for unstubbed calls)
val relaxedMock = mockk<UserRepository>(relaxed = true)

// Spy (partial mock)
val spy = spyk(RealUserRepository())

// Object mock
mockkObject(Singleton)
every { Singleton.method() } returns "mocked"
```

### Stubbing

```kotlin
// Return value
every { repo.findById(any()) } returns User("test")

// Return different values on consecutive calls
every { repo.findById(any()) } returnsMany listOf(user1, user2)

// Throw exception
every { repo.findById(any()) } throws NotFoundException()

// Answer with logic
every { repo.findById(id) } answers {
    if (firstArg<String>() == "123") user else null
}

// Suspending functions
coEvery { repo.fetchUser(any()) } returns user
```

### Verification

```kotlin
// Verify called
verify { repo.save(any()) }

// Verify exact count
verify(exactly = 1) { repo.save(any()) }
verify(atLeast = 2) { repo.findById(any()) }

// Verify order
verifyOrder {
    repo.findById("1")
    repo.save(any())
}

// Verify not called
verify(exactly = 0) { repo.delete(any()) }

// Suspending functions
coVerify { repo.fetchUser(any()) }
```

### Capturing Arguments

```kotlin
val slot = slot<User>()
every { repo.save(capture(slot)) } returns Unit

service.createUser("John")

slot.captured.name shouldBe "John"

// Multiple captures
val list = mutableListOf<User>()
every { repo.save(capture(list)) } returns Unit
```

### Clearing and Unmocking

```kotlin
// Clear recorded calls
clearMocks(mock)

// Clear all mocks
clearAllMocks()

// Unmock object
unmockkObject(Singleton)

// In @AfterEach
@AfterEach
fun tearDown() {
    clearAllMocks()
}
```

## Coroutine Testing

### runTest Basics

```kotlin
@Test
fun `loads data`() = runTest {
    val repo = MyRepository()
    val result = repo.loadData()
    result shouldBe expected
}
```

### TestDispatcher Types

| Dispatcher | Behavior |
|------------|----------|
| `StandardTestDispatcher` | Pauses until explicitly advanced |
| `UnconfinedTestDispatcher` | Runs immediately (eager) |

```kotlin
@Test
fun `with controlled time`() = runTest {
    val testDispatcher = StandardTestDispatcher(testScheduler)
    val viewModel = MyViewModel(testDispatcher)

    viewModel.startCountdown()

    // Time hasn't advanced yet
    viewModel.remaining.value shouldBe 10

    advanceTimeBy(5000)
    viewModel.remaining.value shouldBe 5

    advanceUntilIdle()
    viewModel.remaining.value shouldBe 0
}
```

### Testing Flow with Turbine

```kotlin
@Test
fun `emits states in order`() = runTest {
    viewModel.state.test {
        assertEquals(State.Initial, awaitItem())

        viewModel.load()

        assertEquals(State.Loading, awaitItem())
        assertEquals(State.Success(data), awaitItem())

        cancelAndIgnoreRemainingEvents()
    }
}
```

### Testing SharedFlow Events

```kotlin
@Test
fun `emits navigation event`() = runTest {
    val events = mutableListOf<Event>()
    val job = launch(UnconfinedTestDispatcher()) {
        viewModel.events.toList(events)
    }

    viewModel.onButtonClick()

    events shouldContain NavigateToDetail

    job.cancel()
}
```

## Test Patterns

### Arrange-Act-Assert

```kotlin
@Test
fun `calculates total with discount`() {
    // Arrange
    val cart = Cart()
    cart.add(Item(price = 100))
    cart.add(Item(price = 50))
    cart.applyDiscount(10)

    // Act
    val total = cart.calculateTotal()

    // Assert
    total shouldBe 135.0
}
```

### Test Fixtures

```kotlin
class UserServiceTest : FunSpec({
    lateinit var repo: UserRepository
    lateinit var service: UserService

    beforeTest {
        repo = mockk()
        service = UserService(repo)
    }

    afterTest {
        clearMocks(repo)
    }

    test("creates user") {
        every { repo.save(any()) } returns Unit
        // ...
    }
})
```

### Test Data Builders

```kotlin
fun aUser(
    id: String = "123",
    email: String = "test@example.com",
    name: String = "Test User",
    active: Boolean = true
) = User(id, email, name, active)

@Test
fun `deactivates user`() {
    val user = aUser(active = true)
    val result = service.deactivate(user)
    result.active shouldBe false
}
```

### Fakes over Mocks

```kotlin
// Fake implementation — simpler, more maintainable
class FakeUserRepository : UserRepository {
    private val users = mutableMapOf<String, User>()

    override suspend fun save(user: User) {
        users[user.id] = user
    }

    override suspend fun findById(id: String): User? = users[id]

    fun clear() = users.clear()
}

@Test
fun `saves and retrieves user`() = runTest {
    val repo = FakeUserRepository()
    val service = UserService(repo)

    service.create(aUser(id = "1"))

    repo.findById("1") shouldNotBe null
}
```

## Test Organization

### Project Structure

```
src/
├── main/kotlin/
│   └── com/example/
│       ├── domain/
│       ├── data/
│       └── presentation/
└── test/kotlin/
    └── com/example/
        ├── domain/
        │   └── UserServiceTest.kt
        ├── data/
        │   └── UserRepositoryTest.kt
        ├── fixtures/
        │   └── TestBuilders.kt
        └── fakes/
            └── FakeUserRepository.kt
```

### Naming Conventions

```kotlin
// Descriptive names with backticks
`should return user when found`
`throws exception for invalid input`
`emits loading then success then complete`

// Or use given-when-then
`given valid email when creating user then succeeds`
```

### Test Tags

```kotlin
class SlowTest : FunSpec({
    test("slow integration test").config(tags = setOf(Integration)) {
        // ...
    }
})

object Integration : Tag()

// Run: ./gradlew test -Dkotest.tags="Integration"
```
