# TestContainers — интеграционные тесты с Docker

## Вопрос
> Что такое TestContainers? Зачем он нужен? Приведи пример теста с PostgreSQL.

## Ожидаемый ответ

### 1. Что это?
- **TestContainers** — библиотека для запуска реальных (не моковых) зависимостей в Docker-контейнерах **во время тестов**.
- Позволяет писать **интеграционные тесты**, а не unit-тесты с моками, что снижает риск «тесты проходят, а в prod падает».
- Поддерживает: PostgreSQL, MySQL, Redis, Kafka, Elasticsearch, Selenium и др.

### 2. Зачем нужен?
| Сценарий | Без TestContainers | С TestContainers |
|----------|----------------------|-------------------|
| Тест с БД | Мок `JDBC` → не проверяет SQL |
| Тест с БД | `H2 in-memory` → не проверяет особенности PostgreSQL |
| Тест с БД | ✅ Реальный PostgreSQL → гарантирует работоспособность SQL, индексов, транзакций |

**Ключевое преимущество:** Тесты работают в **точно таком же окружении**, как и в продакшене.

### 3. Пример теста с PostgreSQL

```java
@SpringBootTest
@Testcontainers
class UserRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb")
        .withUsername("testuser")
        .withPassword("testpass");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void findByEmail_returnsUser() {
        // given
        User user = new User("ed@domain.com", "Ed");
        userRepository.save(user);

        // when
        User found = userRepository.findByEmail("ed@domain.com");

        // then
        assertNotNull(found);
        assertEquals("Ed", found.getName());
    }
}
```

**Объяснение:**
- `@Container` → запускает PostgreSQL в Docker при старте теста.
- `@DynamicPropertySource` → подставляет его параметры в `application.yml`.
- Тест работает с реальной БД — и проверяет SQL, DDL, `@Transactional`.

### 4. Частые ошибки кандидатов

1. **«Я использовал H2 вместо TestContainers»** — это не ошибка, но это не интеграционный тест, а unit-тест с моком. Запросы могут работать в H2, но падать в PostgreSQL.
2. **Забыть `@Testcontainers`** — без этой аннотации контейнеры не запустятся.
3. **Не использовать `@DynamicPropertySource`** — тогда `spring.datasource` останется от `application.yml`, а не от контейнера.
4. **Пытаться запустить Selenium и PostgreSQL в одном тесте** — это плохо по архитектуре. Один тест — одна зависимость.

### 5. Best Practices
- Используй `@Container static` — контейнер запускается **один раз** на весь класс.
- Для тестов, где нужна чистая БД для каждого теста, используй `@BeforeEach` + `@Transactional` или `Flyway clean`.
- Не запускай TestContainers в CI без Docker — это упадёт. Просто пропускай такие тесты через профиль (`-Dtestcontainers.enabled=false`).

## Оценка

- **Junior:** Знает, что TestContainers — это для Docker и тестов с БД.
- **Middle:** Пишет базовый тест с `@Container`, объясняет разницу с `H2`.
- **Senior:** Говорит про `DynamicPropertySource`, `@Nested` контейнеры, интеграцию с `Allure`, CI-настройку, откат на моки в CI.

## Ссылки

- [TestContainers Official Docs](https://www.testcontainers.org/)
- [Spring Boot + TestContainers](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing.testcontainers)
- [Stack Overflow: best practices](https://stackoverflow.com/questions/tagged/testcontainers)

---

**Следующий вопрос:** [`REST_Assured_Basics.md`](REST_Assured_Basics.md)