# REST Assured — тестирование REST API на Java

## Вопрос
> Что такое REST Assured? Как ты используешь его для тестирования API? Приведи пример теста с проверкой статус-кода, тела и заголовков.

## Ожидаемый ответ

### 1. Что это?
- **REST Assured** — библиотека для тестирования REST API на Java, основанная на **DSL** (domain-specific language), похожем на BDD.
- Позволяет писать **читаемые, лаконичные тесты** без boilerplate-кода (`HttpURLConnection`, `JsonPath` ручного парсинга).
- Интегрируется с JUnit/TestNG, Allure, TestContainers, CI/CD.

### 2. Основные компоненты

| Компонент | Назначение | Пример |
|----------|-------------|--------|
| `given()` | Настройка запроса (заголовки, auth, body) | `.auth().oauth2(token)` |
| `when()` | Выполнение HTTP-запроса | `.get("/api/v1/users/1")` |
| `then()` | Проверка ответа (статус, тело, заголовки) | `.statusCode(200).body("name", equalTo("Ed"))` |
| `JsonPath` | Парсинг JSON-тела | `response.jsonPath().getString("email")` |

### 3. Пример теста

```java
@Test
void getUser_returns200_andValidUser() {
    // given
    String token = getValidOAuth2Token();

    // when
    Response response = given()
        .auth().oauth2(token)
        .header("X-Request-ID", UUID.randomUUID().toString())
        .when()
        .get("/api/v1/users/1");

    // then
    response
        .then()
        .statusCode(200)
        .header("Content-Type", "application/json; charset=UTF-8")
        .body("id", equalTo(1))
        .body("name", notNullValue())
        .body("email", containsString("@"));
}
```

**Пояснение:**
- В `given()` — настроено аутентификация и заголовок `X-Request-ID`.
- В `when()` — выполнен `GET`.
- В `then()` — проверены статус, заголовок `Content-Type`, тело (`id`, `name`, `email`).

### 4. Частые ошибки кандидатов

1. **Игнорирование `JsonPath`** — пытаются парсить JSON через `response.asString().contains("name")`. Это хрупко и ненадёжно. Правильно — `response.jsonPath().getString("name")`.
2. **Забыть `.contentType(JSON)`** в `given()` при `POST/PATCH`, что приводит к `415 Unsupported Media Type`.
3. **Тесты, зависящие от случайных данных** — например, `given().body(new User(UUID.randomUUID(), "Ed")).when().post("/users")`. Непредсказуемо. Лучше — `User user = new User(1, "Ed")` и `body(user)`.
4. **Слишком широкие `body()`-проверки**, вроде `.body("", notNullValue())` — они маскируют реальную семантику. Лучше — точечные проверки полей.

### 5. Best Practices
- **Делай `given()` максимально детерминированным**: хардкод `userId = 1`, а не `userId = getUserById("admin").getId()`.
- **Используй `@BeforeEach` для получения токена**, а не дублируй логику в каждом тесте.
- **Пиши тесты в `given/when/then`-стиле**: это повышает читаемость как для QA, так и для разработчиков.
- **Интегрируй с Allure**: через `Allure.step()`, чтобы в отчёте была полная цепочка запроса/ответа.

## Оценка

- **Junior:** Знает, что это библиотека для API-тестов, может написать простой `GET` с `statusCode`.
- **Middle:** Использует `body()`, `header()`, `JsonPath`, объясняет `given/when/then`.
- **Senior:** Пишет параметризованные тесты (`@ParameterizedTest`), интегрирует с `TestContainers`, `Allure`, `JUnit Platform`, объясняет как оценивать покрытие API-тестами.

## Ссылки

- [REST Assured Official Docs](https://rest-assured.io/)
- [REST Assured + Allure](https://docs.qameta.io/allure/#_rest_assured)
- [REST Assured Cookbook](https://github.com/rest-assured/rest-assured/wiki/Usage#example-9)

---

**Следующий вопрос:** [`Selenide_Basics.md`](Selenide_Basics.md)