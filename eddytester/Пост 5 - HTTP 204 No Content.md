---
created: 2026-05-13
tags: http, 204, content-length, curl, fetch, manual-testing
angle: Show how the same 204+Content-Length:0 response causes cURL to hang indefinitely but passes fetch and Postman silently — a CI/CD time bomb
---

# HTTP 204 No Content: почему cURL зависает, а fetch — нет

**Дата:** 2026-05-13
**GA RATING:** MUST POST

---

## GA Review

RATING: MUST POST
VERDICT: The topic hits the channel's sweet spot — a real, non-obvious backend testing trap where basic tools behave differently, and the cost is a broken CI/CD pipeline.
BEST_ANGLE: Show how the same 204+Content-Length:0 response causes cURL to hang indefinitely but passes fetch and Postman silently — a CI/CD time bomb.
POST_IDEA: "HTTP 204 No Content: почему твой CI/CD падает из-за одного заголовка (и как это тестировать)"
WHY: The bug is tool-specific (cURL hangs, fetch passes) — a perfect cautionary tale about testing with only one tool.

---

## Post Draft (Style Adapter)

Представь: ты удаляешь объект через API, сервер возвращает 204 No Content — всё чисто, запрос прошёл. В Postman зелёная галочка. В браузере fetch отработал как надо. А cURL в CI/CD пайплайне висит 5 минут и падает по таймауту. Почему?

Всё дело в Content-Length.

RFC 7230 говорит: сервер НЕ должен отправлять Content-Length в ответе с кодом 204. Но многие фреймворки (и разработчики) ставят `Content-Length: 0`. Для fetch это валидный ответ — он видит 204, игнорирует тело, закрывает соединение. Для cURL это сигнал: "жди 0 байт". И curl ждёт. И ждёт. Пока не упадёт по таймауту.

Та же история с Postman — он обрабатывает 404 и 500, а 204 с Content-Length может подвиснуть. Разница в том, как каждый клиент интерпретирует заголовок.

Самый жесть — HTTP/2. Там `Content-Length` на 204 — фатальная ошибка стрима. Safari и curl рвут соединение. CORS-зависимые клиенты просто падают.

**Как тестировать:**
```bash
curl -v -X DELETE https://api.example.com/resource/123
```
Если видишь `Content-Length: 0` на 204 — это баг. Сервер должен опустить заголовок.

Пробей эндпоинт минимум тремя инструментами: curl, fetch (или Postman) и wget. Если хотя бы один ведёт себя иначе — копай.

**Чек-лист:**
1. 204 No Content — Content-Length должен отсутствовать
2. Если есть — cURL зависнет, fetch пройдёт, Postman может зависнуть
3. HTTP/2 + Content-Length на 204 = фатальная ошибка стрима
4. Тестируй endpoint в трёх клиентах: различия в поведении = баг

**Полезно:**
[MDN: 204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/204)
[Bun issue: Content-Length with 204](https://github.com/oven-sh/bun/issues/20676)
[Postman issue: 204 non-zero Content-Length](https://github.com/postmanlabs/postman-app-support/issues/5818)

---

## Post Draft (Channel Agent — старая версия)

**Situation**
Твой CI/CD пайплайн делает DELETE запрос и ждёт ответ. cURL зависает на 5 минут. Postman показывает успех. Кто врёт?

**Analysis**
HTTP 204 No Content означает "запрос выполнен, тела нет". Проблема: некоторые серверы добавляют `Content-Length: 0`. По RFC — нельзя, но фреймворки делают.
- **cURL**: видит Content-Length: 0 → ждёт 0 байт → не может закрыть соединение → таймаут через 2-5 минут.
- **fetch (браузер)**: игнорирует Content-Length на 204 → успех.
- **Postman**: обрабатывает как успех, но с нюансами.
- **HTTP/2**: Content-Length на 204 = fatal stream error.

**Verdict**
Это **баг**. Если сервер возвращает Content-Length на 204 — он нарушает RFC и ломает часть клиентов.

**Takeaway**
Никогда не тестируй эндпоинт только одним инструментом. Разные клиенты = разное поведение. 204 + Content-Length:0 — классический "тихий" баг.

**Реалы**
- Баг живёт годами. Nginx, Tornado, Bun — все через это проходили.
- В HTTP/2 такой ответ просто рвёт соединение. Safari падает молча.
- cURL — единственный, кто честно ждёт. И падает.

**Полезно:**
[MDN: 204 No Content](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/204)
[curl issue: 204 with Transfer-Encoding chunked](https://github.com/curl/curl/issues/3968)

---

## Research Brief

Тема: HTTP 204 No Content with Content-Length: 0 — fetch API treats it as success, but cURL hangs

Ключевые находки:
- GitHub API 204 + Content-Length: 0 — CI/CD пайплайны падают
- curl зависает, fetch проходит — разная интерпретация заголовков
- RFC: сервер не должен отправлять Content-Length на 204
- Node.js/Postman: по-разному обрабатывают
- Bun: Content-Length на 204 — фатальная ошибка (HTTP/2)
- Тестовый чек-лист: curl, wget, Postman, node-fetch
- Tornado issue #1736: обсуждают как фиксить
