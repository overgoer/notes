---
created: 2026-05-18
type: post
format: "№10 Баг-репорт"
status: готов к публикации
calendar_date: 2026-05-21 Чт 11:30
topic: "Content-Type text/plain на JSON-эндпоинте"
tags: post, обучение, bug-report
---

# Content-Type text/plain на JSON-эндпоинте

**Ситуация:** Отправляю POST на эндпоинт создания пользователя. Content-Type: text/plain. Тело — валидный JSON.

Сервер: `HTTP/1.1 200 OK` — пользователь создан.

**Странно.** Почему text/plain пропустили, а JSON ожидали?

**Разбор:** Некоторые фреймворки (Express, Flask, Spring) по умолчанию не проверяют Content-Type, если тело — строка. JSON парсится даже с text/plain, потому что парсер смотрит на содержимое, а не на заголовок.

**Проблема:** Если атакующий может подменить Content-Type, он может обойти:
- Валидацию схемы (которая привязана к application/json)
- Rate limiting по типу контента
- Логирование (в логах text/plain, хотя тело — JSON)

**Как проверить:**
```bash
curl -X POST /api/users \
  -H "Content-Type: text/plain" \
  -d '{"name": "test", "email": "test@test.com"}'
```

Если 200 — баг. Сервер **должен** проверять Content-Type на прикладном уровне.

**Чек-лист:**
- [ ] POST с Content-Type: text/plain — что возвращает?
- [ ] POST с Content-Type: application/xml — что возвращает?
- [ ] POST без Content-Type — что возвращает?
- [ ] PATCH/PUT с неверным Content-Type — что возвращает?

➡️ Находили такое на проде? 👇
