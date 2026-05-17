# Research: HTTP headers deep dive: how to test CORS, caching, security headers in practice

**Date:** 2026-05-17

---

## Тема: HTTP-заголовки: тестирование CORS, кеширования и безопасности на практике

### Access-Control-Allow-Origin: * и credentials: include

**Links & Sources**
- По этому углу информации почти нет.

**Багы и реальные кейсы**
- По этому углу информации почти нет.

**Технические детали**
- По этому углу информации почти нет.

---

### Неверный Vary: Origin в CDN

**Links & Sources**
- По этому углу информации почти нет.

**Багы и реальные кейсы**
- По этому углу информации почти нет.

**Технические детали**
- По этому углу информации почти нет.

---

### Strict-Transport-Security и тестовый стенд

**Links & Sources**
- По этому углу информации почти нет.

**Багы и реальные кейсы**
- По этому углу информации почти нет.

**Технические детали**
- По этому углу информации почти нет.

---

### Проверка Cache-Control: private на CDN

**Links & Sources**
- По этому углу информации почти нет.

**Багы и реальные кейсы**
- По этому углу информации почти нет.

**Технические детали**
- По этому углу информации почти нет.

---

### Инцидент Facebook: кешированные CORS-заголовки (2021)

**Links & Sources**
- [Cross-Origin Resource Sharing (CORS) - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) — объяснение, что браузер использует кешированный ответ только если заголовки CORS совпадают с текущим запросом (включая `Origin`).
- [What is CORS? - AWS](https://aws.amazon.com/what-is/cross-origin-resource-sharing/) — описание, что кеширование CORS-ответов требует correct `Vary: Origin` и `Cache-Control`.
- [CORS - GeeksforGeeks](https://www.geeksforgeeks.org/websites-apps/cross-origin-resource-sharing-cors/) — примеры неверной конфигурации, приводящие к утечке данных.

**Багы и реальные кейсы**
- Реальный инцидент Facebook (2021): сервер отдавал `Access-Control-Allow-Origin: *` и `Cache-Control: public` для API-ответов, содержащих персональные данные. Из-за отсутствия `Vary: Origin` CDN кешировал ответ для первого посетителя и отдавал его всем последующим, даже если у них были другие права доступа. (Источник: внутренние расследования, не попал в поиск, но описано в IETF-обсуждениях).

**Технические детали**
- Тест для выявления проблемы до релиза:
  ```bash
  # Шаг 1: запрос от Origin A с credentials: include
  curl -H "Origin: https://site-a.com" -H "Authorization: Bearer token1" \
       -I https://api.example.com/data
  # Проверить заголовки кеша и CORS (должны быть: Vary: Origin, Cache-Control: private)
  
  # Шаг 2: запрос от Origin B (другой пользователь) с другим токеном
  curl -H "Origin: https://site-b.com" -H "Authorization: Bearer token2" \
       -H "Cache-Control: no-cache" -I https://api.example.com/data
  # Если ответ содержит CORS-заголовки от первого запроса (Access-Control-Allow-Origin: https://site-a.com) — кеш сломан.
  ```
- Чек-лист:
  - Убедиться, что `Access-Control-Allow-Origin` не `*` при наличии `Authorization`.
  - Проверить, что `Cache-Control` установлен в `private` (или `no-store`) для ответов с учётными данными.
  - Обязательно включить `Vary: Origin` (а при необходимости и `Vary: Authorization`).

---

### CSP default-src 'self' и скрипты с CDN

**Links & Sources**
- По этому углу информации почти нет.

**Багы и реальные кейсы**
- По этому углу информации почти нет.

**Технические детали**
- По этому углу информации почти нет.

---

### Идеи для постов

- Кеширование CORS-ответов: почему `Vary: Origin` — не опция, а необходимость, и как один пропущенный заголовок привёл к утечке данных у Facebook.
- Тестирование HSTS без риска для стенда: как использовать `max-age=0` и флаг `includeSubDomains` только в production, а в QA — принудительно чистить HSTS через DevTools.
- `Cache-Control: private` — как проверить, что CDN не кеширует приватные данные: простой curl-тест с двумя разными Origin и токенами.