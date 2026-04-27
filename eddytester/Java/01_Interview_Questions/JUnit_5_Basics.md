# `@Test`, `@BeforeEach`, `@AfterEach` — JUnit 5

## Вопрос
> Какие основные аннотации JUnit 5 ты знаешь? Когда и зачем их использовать? Приведи пример теста.

## Ожидаемый ответ

### 1. Основные аннотации

| Аннотация | Назначение | Когда использовать |
|-----------|------------|---------------------|
| `@Test` | Помечает метод как тестовый | На каждом тестовом сценарии (`positiveCase`, `negativeCase`, `edgeCase`) |
| `@BeforeEach` | Выполняется **до каждого** `@Test` | Для инициализации объектов (`new Calculator()`, `mock = Mockito.mock()`) |
| `@AfterEach` | Выполняется **после каждого** `@Test` | Для очистки состояния (закрытие `Connection`, сброс `static`-полей) |
| `@BeforeAll` | Выполняется **один раз** до всех тестов | Для тяжёлой инициализации: `DriverManager.getConnection()` |
| `@AfterAll` | Выполняется **один раз** после всех тестов | Для завершения: `connection.close()`, `driver.quit()` |

### 2. Пример теста

```java
class CalculatorTest {
    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }

    @Test
    void add_positiveNumbers_returnsSum() {
        // given
        int a = 5, b = 3;

        // when
        int result = calc.add(a, b);

        // then
        assertEquals(8, result);
    }

    @Test
    void add_negativeNumbers_returnsSum() {
        assertEquals(-2, calc.add(-5, 3));
    }
}
```

**Пояснение:**
- `@BeforeEach` гарантирует, что каждый тест получает **чистый** объект `Calculator`.
- `@Test` делает метод исполняемым как тест.
- Использование `given/when/then` — лучшая практика (человекочитаемость).

### 3. Частые ошибки кандидатов

1. **Использовать `@BeforeAll` вместо `@BeforeEach`** — приводит к `state leakage` (тесты влияют друг на друга).  
2. **Забывать `@DisplayName`** — тест без имени `add_positiveNumbers_returnsSum()` сложно читать в отчётах.  
3. **Писать `assert` в `@BeforeEach`** — это неправильно: `@BeforeEach` не для проверок, а для подготовки.  
4. **Запускать тяжёлые операции в `@BeforeEach`** — например, инициализация драйвера. Правильно — `@BeforeAll`.

### 4. Дополнительно: `@ParameterizedTest`

```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3})
void isPositive_returnsTrue(int number) {
    assertTrue(isPositive(number));
}
```

— Уменьшает дублирование тестов при одном поведении и разных входных данных.

## Оценка

- **Junior:** Называет `@Test`, `@BeforeEach`, `@AfterEach`; пишет простой тест.
- **Middle:** Объясняет разницу `@BeforeAll`/`@BeforeEach`; пишет `@ParameterizedTest`; знает, где ставить `@DisplayName`.
- **Senior:** Обсуждает `TestInstance.Lifecycle.PER_CLASS`, `@Nested` тесты, таймауты (`@Timeout(5)`), интеграцию с `TestContainers`.

## Ссылки

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Testing in Spring Boot](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
- [Effective Java, Глава 11: JUnit](https://www.informit.com/articles/article.aspx?p=2861454&seqNum=11)

---

**Следующий вопрос:** [`Mockito_Basics.md`](Mockito_Basics.md)