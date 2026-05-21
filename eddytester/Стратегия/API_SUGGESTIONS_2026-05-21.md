# 🏗 API Improvement Suggestions — 2026-05-21

**Сгенерировано:** 2026-05-21 22:00
**Источник:** BSA API Bridge

---

## 1. File upload endpoint with Zip Slip vulnerability

**Репозиторий:** free-trial-api
**Сложность:** P1

**Триггер:** 2026-05-17: Testing file uploads: multipart forms, validation, size limits, security (Zip Slip)

**Описание:** Add POST /free/api/upload endpoint that accepts multipart file uploads (zip archives) with a known Zip Slip path traversal bug. The endpoint extracts files without sanitizing paths, allowing writing outside the target directory. Rate-limited per trial key.

**Стратегическая связь:** Learning: students can discover and fix a real security bug. Content: spawns posts on file upload testing, Zip Slip exploit, and security fixes. Popularization: high engagement via 'find the bug' format.

**Контент-угол:** We added a file upload endpoint with a dangerous Zip Slip vulnerability. Can you exploit it? Find the bug and submit a fix to earn credits.

**Бриф для content_manager:**
> Заголовок: 'Мы специально сломали загрузку файлов. Найди уязвимость Zip Slip за 5 минут'. Угол: интерактивное обучение безопасности API. Ключевые точки: описание Zip Slip, как воспроизвести, как исправить, призыв прислать решение.

---

## 2. Mock payment endpoint for testing payment flows

**Репозиторий:** free-trial-api
**Сложность:** P1

**Триггер:** Backlog B-002: Платёжка (любая работающая) – monetization need and content about payment testing

**Описание:** Add POST /free/api/payment endpoint that simulates a payment gateway. Accepts card number, amount, currency. Returns success for test card '4242 4242 4242 4242' and failure for others. Includes intentional bugs: wrong HTTP status code on success (201 instead of 200), missing idempotency key handling, and no validation for negative amount.

**Стратегическая связь:** Monetization: prepares infrastructure for real payments. Learning: teaches payment API testing, idempotency, and validation. Content: posts about mocking payments, testing strategies, and finding bugs in payment logic.

**Контент-угол:** New mock payment endpoint – try to break it! We've hidden bugs in the simulation. Test your payment integration skills and report issues.

**Бриф для content_manager:**
> Заголовок: 'Тестируем платежи: как не потерять деньги из-за бага в API'. Угол: практическое тестирование платежного шлюза. Ключевые точки: создание мока, тест-кейсы (успех, отказ, невалидные суммы), обнаруженные баги (статус, идемпотентность).

---

## 3. Rate limit test endpoint with configurable limits

**Репозиторий:** free-trial-api
**Сложность:** P2

**Триггер:** General need for API testing content; existing rate limiting in free-trial-api can be demonstrated via a dedicated endpoint

**Описание:** Add GET /free/api/rate-limit-test that returns 200 OK for first 3 requests per trial key, then 429 Too Many Requests for subsequent requests within a 1-minute window. The limit and window can be overridden via query parameters (e.g., ?limit=1&window=5) for advanced testing.

**Стратегическая связь:** Learning: hands-on experience with rate limiting headers (Retry-After), handling 429s, and designing retry logic. Content: posts on rate limiting best practices, testing strategies, and how to avoid being blocked.

**Контент-угол:** Test your rate limiting handling with our dedicated endpoint – try different limits and windows to see how APIs protect themselves.

**Бриф для content_manager:**
> Заголовок: 'Как тестировать rate limiting: практическое руководство с нашим API'. Угол: обучение обработке 429 ошибок. Ключевые точки: настройка параметров, чтение Retry-After, реализация exponential backoff, тестирование с разными сценариями.

---

> Статус: предложено → принято/отклонено → сделано → опубликовано
> Отмечай статус в API_IMPROVEMENT_TRACKER.md