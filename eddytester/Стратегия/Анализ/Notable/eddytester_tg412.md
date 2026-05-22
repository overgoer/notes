---
channel: @eddytester
tg_post_id: 412
posted_at: 2026-05-17T09:57:01+00:00
views: 321
forwards: 5
replies: 11
category: api/bugs
---

## Post

**Час прошёл. Поехали.**

Правильный ответ:
А) Бэкенда.

Почему? По шагам. С доказательствами.

Шаг 1. Воспроизвожу

Запрос №1 - пустое тело:

```curl -v -X POST https://api.practicum.com/users \
  -H "Content-Type: application/json" \
  -d ''```

Ответ:
HTTP/1.1 500 Internal Server Error

Запрос №2 - пустой JSON:

```curl -v -X POST https://api.practicum.com/users \
  -H "Content-Type: application/json" \
  -d '{}'```

Ответ:
HTTP/1.1 500 Internal Server Error

Шаг 2. Смотрю в логи сервера

ERR

## Analysis

Пост содержит практический разбор кейса с запросами к API, анализом логов и ссылкой на RFC. Четкая структура и доказательства делают материал полезным для QA-специалистов.

## Why Works

Пост залетел из-за конкретного примера, который легко применить на практике, и наглядного объяснения разницы между 400 и 500 ошибками.
