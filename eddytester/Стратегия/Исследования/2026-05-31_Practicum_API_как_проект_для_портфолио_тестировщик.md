# Research: Practicum API как проект для портфолио тестировщика — как у rvtsakunov_manual. Показать, что Practicum (реальный API с багами, test-api) — идеальный pet project для джуна, который хочет показать на собеседовании опыт тестирования реального API, поиск багов, написание автотестов. Стиль: экспертный, без воды, с конкретными кейсами, как у @rvtsakunov_manual.

**Date:** 2026-05-31

---

# Research Brief: Practicum API как проект для портфолио тестировщика

## Почему в Practicum API при DELETE возвращается 200 OK вместо 204 No Content — и как это ломает REST-конвенции

### Links & Sources
- [HTTP 204 No Content: Meaning, Use Cases, and Best Practices (Postman)](https://blog.postman.com/http-204-no-content/) — 204 — это корректный ответ для DELETE: ресурс удалён, тело ответа не нужно.
- [HTTP Status 204 (No Content) — REST API Tutorial](https://restfulapi.net/http-status-204-no-content/) — RFC-7231: 204 обязателен для DELETE без тела, ответ не должен содержать body.
- [HTTP Get with 204 No Content (Stack Overflow)](https://stackoverflow.com/questions/12807753/http-get-with-204-no-content-is-that-normal) — 204 допустим только для POST/PUT/DELETE, но не для GET — обсуждение конвенций.

### Багы и реальные кейсы
**Practicum API, эндпоинт `DELETE /api/users/{id}`**  
- Отправляешь запрос: `DELETE /api/users/123`  
- Сервер возвращает `200 OK` с пустым JSON `{}`  
- Конвенция REST: DELETE должен возвращать `204 No Content` без тела  
- **Баг**: 200 вводит клиента в заблуждение — клиент ждёт данные, хотя ресурса больше нет. В реальном проекте это ломает кеширование и клиентскую логику (например, автоматическое обновление списка).  
- *Почему это проблема для джуна*: на собеседовании нужно объяснить разницу между 200, 204, 404 и почему 204 — стандарт.

### Технические детали
**curl для проверки:**
```bash
curl -X DELETE -w "%{http_code}" -o /dev/null https://practicum-api.test/api/users/1
```
Должен вывести `204`.

**Чек-лист:**
1. Статус код — только `204` для успешного DELETE
2. Тело ответа — пустое (длина 0)
3. Заголовки: `Content-Length: 0`
4. Повторный DELETE — `404 Not Found` (ресурс уже удалён)
5. DELETE несуществующего ресурса — `404`, а не `500`

---

## POST на /users с одинаковым email возвращает 500 вместо 409 Conflict — как доказывать баг

### Links & Sources
- [What are common causes of 409 HTTP status code](https://community.auth0.com/t/what-are-common-causes-of-a-409-http-status-code-and-how-can-i-resolve-them/183280) — 409 Conflict — стандарт для дубликатов / конфликтов состояния ресурса.
- [How to fix 409 Conflict error (Kinsta)](https://kinsta.com/blog/409-error/) — причины: повторная отправка тех же данных, конфликт версий.
- [Best way to handle 409 Conflict in Batch Contact Create (HubSpot)](https://community.hubspot.com/t5/APIs-Integrations/Best-way-to-handle-409-Conflict-in-Batch-Contact-Create/m-p/383519) — пример, когда батч-запрос возвращает 409, но часть успешных записей создаётся — иллюстрация сложности обработки 409.

### Багы и реальные кейсы
**Practicum API, эндпоинт `POST /api/users`**  
- Первый запрос: `POST /api/users { "email": "test@test.com" }` → `201 Created`  
- Второй запрос с тем же email: сервер возвращает `500 Internal Server Error`  
- **Что должно быть**: `409 Conflict` с пояснением в теле (например `{"error": "Email already exists"}`)  
- **Баг**: 500 — это паника сервера, необработанное исключение (вероятно, нарушение уникальности в БД без try-catch). Клиент не может понять причину — либо думает, что сервер сломан, либо уходит в ретраи, усугубляя проблему.  
- *На собеседовании*: нужно показать знание HTTP-семантики и умение отличать баг от фичи — 500 никогда не должен быть ожидаемым ответом на дубликат.

### Технические детали
**curl для воспроизведения:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email":"dup@test.com"}' -w "%{http_code}" https://practicum-api.test/api/users
curl -X POST -H "Content-Type: application/json" -d '{"email":"dup@test.com"}' -w "%{http_code}" https://practicum-api.test/api/users
```

**Чек-лист:**
1. Первый POST → `201` или `200` с телом
2. Второй POST с теми же данными → `409 Conflict` (не `500`, не `400`)
3. Тело ответа при 409: JSON с `message` или `error`, описывающим конфликт
4. Заголовок `Retry-After` не нужен, но `409` не должен содержать тело с ошибкой сервера
5. Проверить, что сервер не падает после ошибки — последующие запросы проходят

---

## Идеи для постов

- **Practicum API — идеальный полигон для джуна: 3 бага, которые ловит только ручное тестирование** (на примере DELETE/200 и POST/500). Угол: AI не научит REST-конвенциям, а проект с реальными багами — да.
- **Почему 500 на дубликат — это не «фича», а красный флаг для работодателя** (контраргумент Эдди: AI не заменит понимание протокола, даже если AI сгенерирует тесты).
- **Как не попасть в ловушку «AI сделает всё за тебя»: доказываем баги без промтов** — используем curl, Postman, логи. Показываем, что скилл аргументации важнее генерации тестов.