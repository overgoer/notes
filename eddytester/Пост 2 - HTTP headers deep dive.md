---
created: 2026-05-12
tags: http, headers, cors, caching, security, manual-testing
angle: A practical post showing how to test CORS, caching, security headers with concrete curl commands
---

# HTTP headers deep dive: как тестировать CORS, кэширование и security-заголовки

**Дата:** 2026-05-12
**GA RATING:** MUST POST

---

## GA Review

RATING: MUST POST
VERDICT: The brief delivers exactly what your audience needs — concrete, battle-tested bugs (GitHub CORS, Facebook MIME sniffing) and a step-by-step methodology for manually testing headers. No fluff, no generic theory. Perfect for manual backend testers who want to stop missing critical headers.
BEST_ANGLE: A practical post showing how to test CORS, caching, and security headers with concrete curl commands — from CORS misconfigurations to MIME sniffing and HSTS.
POST_IDEA: "HTTP headers: чек-лист из 5 проверок, которые спасут твой API"
WHY: The brief has specific, reproducible bugs for each header category. The post should be a checklist-style walkthrough.

---

## Post Draft (Channel Agent)

**Situation**
Ты настроил CORS, добавил Cache-Control, HSTS, CSP. CI зелёный. Но в проде — токены утекают, прокси кэширует приватные данные, а браузер игнорирует твои заголовки. Что пошло не так?

**Analysis**

**1. CORS: Access-Control-Allow-Origin: * + credentials**
Самый опасный баг: API отдаёт `Access-Control-Allow-Origin: *` вместе с `Access-Control-Allow-Credentials: true`. Браузер разрешит чтение ответа любому сайту. Атакующий украдёт токен через fetch с любого своего домена.
*Как проверить:*
`curl -H "Origin: https://evil.com" -v https://api.example.com/login`
Ищешь оба заголовка в ответе. Если оба есть — уязвимость.

**2. Cache-Control: no-store ≠ защита**
Прокси (Squid, Nginx) могут игнорировать `no-store`. Приватные данные (JSON с сессией) остаются в кэше.
*Как проверить:* отправить запрос дважды через корпоративный прокси. Если второй ответ приходит быстрее или содержит `Age: > 0` — кэш нарушен.
*Лечение:* отправлять тройку `Cache-Control: no-cache, no-store, must-revalidate`.

**3. ETag + 200 вместо 304**
Сервер возвращает 200 OK даже когда ETag совпадает. В нагрузочном тесте — лишний трафик.
*Как проверить:* получить ETag первого ответа, отправить `If-None-Match: <etag>`. Ожидаешь 304, получаешь 200 — баг.
`curl -H "If-None-Match: \"abc123\"" -v https://api.example.com/data`

**4. X-Content-Type-Options: nosniff**
Без этого заголовка браузер может выполнить JavaScript внутри JSON-ответа (MIME sniffing). Реальный инцидент: Facebook позволял запускать JS в JSON — XSS через MIME-атаку.
*Как проверить:* `curl -v https://api.example.com/data | grep -i "x-content-type-options"`. Если отсутствует — добавить.

**5. HSTS misconfig**
`max-age` слишком мал или отсутствует preload — downgrade-атака возможна.
*Как проверить:* `curl -s -D- https://example.com | grep -i strict-transport-security`
Правильно: `Strict-Ttansport-Security: max-age=63072000; includeSubDomains; preload`

**6. Preflight (OPTIONS) не кэшируется**
По умолчанию Access-Control-Max-Age = 5 секунд. Каждый запрос — лишний OPTIONS.
*Как проверить:* `curl -X OPTIONS -v https://api.example.com/resource | grep -i access-control-max-age`
Оптимально: 86400 (24 часа). Больше — опасно, меньше — тормозит.

**Verdict**
Не настройка заголовков — **баг**. Если хотя бы один из этих заголовков отсутствует или настроен неверно — API уязвим или неоптимален.

**Takeaway**
Заголовки — не магия, а контракт. Тестируй их так же тщательно, как бизнес-логику. Чек-лист из 6 пунктов выше — готовый сценарий для регресса.

**Реалы**
- CORS с `*` и credentials — классическая ошибка даже в крупных API.
- MIME sniffing в JSON — многие тестировщики даже не слышали про `X-Content-Type-Options`.
- HSTS с `max-age=31536000` — часто копипастят, не понимая, что 1 год мало для preload-списка.

**Полезно:**
[MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
[MDN: Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
[HTTP Toolkit: Cache your CORS](https://httptoolkit.com/blog/cache-your-cors/)

---

## Post Draft (Style Adapter)

Ты настроил CORS, добавил Cache-Control, HSTS, CSP. CI зелёный. Но в проде — токены утекают, прокси кэширует приватные данные, а браузер игнорирует заголовки. Вот 6 проверок, которые спасут твой API.

CORS. Самая опасная комбинация: `Access-Control-Allow-Origin: *` вместе с `Access-Control-Allow-Credentials: true`. Любой сайт может прочитать ответ твоего API и украсть токен. Проверка: `curl -H "Origin: https://evil.com" -v https://api.example.com/login`. Если оба заголовка в ответе — уязвимость.

Cache-Control. `no-store` не гарантирует защиту. Прокси вроде Squid или Nginx могут его игнорировать и кэшировать приватные JSON-ответы. Лечение: отправляй тройку `no-cache, no-store, must-revalidate`. Проверка: два запроса через корпоративный прокси — если второй быстрее или с `Age: > 0`, кэш нарушен.

ETag. Сервер возвращает 200 OK даже когда ETag совпадает. В нагрузочном тесте — лишний трафик и время. Проверка: `curl -H "If-None-Match: \"abc123\"" -v https://api.example.com/data`. Ожидаешь 304 — получаешь 200. Баг.

X-Content-Type-Options. Без этого заголовка браузер может выполнить JavaScript внутри JSON-ответа (MIME sniffing). Реальный кейс: Facebook позволял запускать JS в JSON — XSS-атака через определение типа контента браузером. Проверка: `curl -v https://api.example.com/data | grep -i x-content-type-options`. Если нет — ставь `nosniff`.

HSTS. `max-age` меньше 2 лет и без `preload` — downgrade-атака возможна. Правильно: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`.

Preflight (OPTIONS). По умолчанию Access-Control-Max-Age = 5 секунд. Каждый запрос — лишний OPTIONS. Оптимально: 86400 (24 часа). Больше — опасно, меньше — тормозит.

**Что делать:** сделай этот чек-лист частью регресса. Заголовки — не магия, а контракт. Тестируй их как бизнес-логику.

**Полезно:** [MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control), [HTTP Toolkit: Cache your CORS](https://httptoolkit.com/blog/cache-your-cors/)

---

## Research Brief

Тема: HTTP headers deep dive: how to test CORS, caching, security headers in practice

Ключевые находки:
- GitHub API CORS misconfiguration
- Cache-Control no-store не спасает от прокси (Squid, Nginx)
- ETag + 200 вместо 304 — нагрузочные тесты покажут лишний трафик
- Facebook MIME sniffing инцидент (XSS через JSON)
- HSTS max-age: preload-список требует > 2 лет
- OPTIONS preflight: по умолчанию 5 сек кэша
- CSP unsafe-inline = нет защиты от XSS
