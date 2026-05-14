# Промо API — Free Trial API

> План бесплатных методов для промоушена Practicum
> Связанные POST + GET с кривыми параметрами

## Цель
Дать потенциальному ученику попробовать API «на зуб» без оплаты.
Увидеть реальные баги — и захотеть купить полную версию (20 багов, V1→V2, все методы).

## Состав

### POST /free/api/users
Создание тестового пользователя.

**Параметры (body, JSON):**
| Поле | Тип | Обязательное | Описание |
|------|-----|:-----------:|----------|
| name | string | да | Имя пользователя |
| age  | integer | да | Возраст |

**Баги:**
1. Name не тримит пробелы — `"  John  "` сохраняется как есть
2. Age не проверяется на отрицательное — `-5` проходит в БД

**Rate limit:** 10 запросов в минуту

---

### GET /free/api/users
Получение списка пользователей.

**Параметры (query):**
| Параметр | Тип | Обязательное | Описание |
|----------|-----|:-----------:|----------|
| sort     | string | нет | Поле для сортировки (любое значение) |
| limit    | integer | нет | Сколько записей вернуть |
| status   | string | нет | Фильтр по статусу |

**Rate limit:** 10 запросов в минуту

**Баги:**
1. `sort` — любое значение сортирует по name по алфавиту (игнорирует переданное поле)
2. `limit` — всегда возвращает 1 запись, независимо от значения
3. `status` — регистрозависимый фильтр
4. Content-Type: text/plain вместо application/json
5. Нет заголовков безопасности (X-Content-Type-Options, X-Frame-Options)

---

## Что видит пользователь

```bash
# Создаём пользователей
curl -X POST /free/api/users \
  -H "Content-Type: application/json" \
  -H "X-Fix-Bug: free-trial" \
  -d '{"name":"  Alice  ","age":25}'
# → 201, пользователь создан с именем "  Alice  "

curl -X POST /free/api/users \
  -H "Content-Type: application/json" \
  -H "X-Fix-Bug: free-trial" \
  -d '{"name":"bob","age":30}'
# → 201

curl -X POST /free/api/users \
  -H "Content-Type: application/json" \
  -H "X-Fix-Bug: free-trial" \
  -d '{"name":"Charlie","age":-5}'
# → 201 — age = -5 прошло!

# Получаем список с sort и limit
curl "/free/api/users?sort=id&limit=10" \
  -H "X-Fix-Bug: free-trial"
# → Content-Type: text/plain
# → [{"name":"  Alice  ",...}] — всего 1 запись, сортировка по name

# Фильтр по статусу
curl "/free/api/users?status=MINOR" \
  -H "X-Fix-Bug: free-trial"
# → [] — пусто, хотя есть пользователи со статусом minor
```

Очевидно видны 5+ багов за 4 запроса.

---

## Техническая реализация

- **Таблица:** `free_users` (отдельная от основной, чтобы не пересекаться с платными пользователями)
- **API-ключ для бесплатного доступа:** статический `free-trial` (жёстко прописан в middleware)
- **Rate limit:** in-memory счётчик на IP, 10 req/min, сбрасывается каждую минуту
- **Роуты:** `/free/api/users` (GET + POST)
- **Middleware:** `validateFreeApiKey` — проверяет `x-fix-bug: free-trial`
- **Rate limit middleware:** `rateLimitFree` — 10/мин, возвращает 429 если превышен

---

## Как используем в маркетинге

1. **Пост в Telegram:** «Я открыл бесплатный API и сломал его за 30 секунд» — скриншоты curl'ов
2. **Бот Practicum Bot:** задача 0 — создай пользователя через `/free/api/users` и проверь баги
3. **Видео на YouTube:** тизер-ролик «Попробуй API бесплатно, найди баги»
4. **Pinned-пост** со ссылкой на Swagger бесплатного API

---

## Связь с платной версией

| | Free Trial | Полный Practicum |
|---|---|---|
| Методы | POST + GET (связанные) | GET /users, GET /:id, POST, PATCH, DELETE |
| Баги | 5 штук (уникальные для free) | 20 штук (все в Candidates API) |
| V1→V2 фикс | ❌ | ✅ |
| Баг-репорт | ❌ | ✅ (шаблон) |
| Доступ | По `x-fix-bug: free-trial` | По токену на почту |
| Цена | Бесплатно | 5000₽ |
