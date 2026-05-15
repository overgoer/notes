# BSA_FORMATS_v2 — Часть 2: Формат №2 «API-шпаргалка»

## Формат №2: «API-шпаргалка: 3 строки, как в проде»

**Механика:** Одна операция API → три рабочие команды curl/jq/grep. Без Postman.
**Когда:** 2–3 раза в неделю.

---

### Пост 1: «Как проверить, жив ли API, за 3 секунды»

Не открывай браузер. Не логинься. Одна команда:

```bash
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health
```

Вернул `200` — жив. Вернул `503` — мёртв. Вернул `000` — сервер не отвечает вообще.

А если API не отдаёт status (а в 90% проектов — не отдаёт), просто проверь, что вернулся `200`:

```bash
curl -s -I https://api.example.com/health | grep "200"
```

Третья команда — для тех, кто любит тишину:

```bash
curl -s -o /dev/null -w "Time: %{time_total}s, Code: %{http_code}\n" https://api.example.com/health
```

Покажет и статус, и сколько сервер думал.

Скопируйте и запустите на своём API. Работает везде.

Кидайте свои команды — соберу большую шпаргалку.

---

### Пост 2: «Как проверить, врёт ли сервер про Content-Type»

Было сто раз: фронт ждёт JSON, а приходит HTML — и всё падает. Вот проверка:

```bash
curl -s -I https://api.example.com/users/1 | grep -i "content-type"
```

Должно быть `application/json`. Если `text/html` — сервер врёт, идите чинить.

А теперь то же самое, но с телом запроса — когда сервер должен вернуть ошибку:

```bash
curl -s -H "Content-Type: application/json" -X POST https://api.example.com/login -d '{"u":"a","p":"b"}' | head -c 100
```

Если кусок ответа начинается с `<html>` — проблема на бэкенде, а не у тебя.

А если `application/json` — смотри что вернул:

```bash
curl -s -H "Content-Type: application/json" -X POST https://api.example.com/login -d '{}' | jq '.error // .message // .'
```

Кидайте свои команды — соберу шпаргалку.

---

### Пост 3: «Rate limiting: с какого запроса тебя забанят»

Почти у каждого API есть лимиты. Вопрос: с какого запроса?

```bash
curl -s -I https://api.example.com/endpoint | grep -i "rate"
```

Если видишь `X-RateLimit-Limit: 100` — можешь дёргать 100 раз в минуту. Если заголовка нет — лимит есть, но тебе о нём не говорят.

Теперь проверим где граница:

```bash
for i in {1..120}; do curl -s -o /dev/null -w "$i: %{http_code}\n" https://api.example.com/endpoint; done
```

Смотри номер запроса, после которого код сменился с `200` на `429`. Это и есть твой лимит.

А ещё можно проверить, возвращается ли `Retry-After`:

```bash
curl -s -I https://api.example.com/endpoint | grep -i "retry"
```

Если есть — сервер говорит «подожди столько секунд». Если нет — ты слепой.

Скопируйте, запустите. Кидайте свои команды.

---

### Пост 4: «Как найти баг в CORS за 10 секунд»

Фронт не может достучаться до API? 90% случаев — CORS.

```bash
curl -s -H "Origin: https://evil-site.com" -I https://api.example.com/endpoint | grep -i "access-control"
```

Если `Access-Control-Allow-Origin: *` — твой API может читать любой сайт. Это security-баг.

Если заголовка нет вообще — CORS не настроен. Фронт будет падать с ошибкой.

А теперь проверка на сложный сценарий:

```bash
curl -s -H "Origin: https://example.com" -H "Access-Control-Request-Method: DELETE" -X OPTIONS https://api.example.com/endpoint | grep -i "access-control"
```

Если `Allow-Methods` не содержит `DELETE` — разработчики забыли добавить метод.

Скопируйте, запустите. Кидайте свои.
