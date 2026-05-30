# Research: баги в API тестировании — разбор бага с race condition в Postgres, конкурентные запросы и дубли

**Date:** 2026-05-30

---

### Как воспроизвести race condition при создании заказа без уникального индекса в БД

**Links & Sources**
- [Concurrent transactions result in race condition with unique constraint on insert](https://dba.stackexchange.com/questions/212580/concurrent-transactions-result-in-race-condition-with-unique-constraint-on-inser) — два транзакции одновременно вставляют строку, проверка уникальности на уровне приложения не видит друг друга, обе вставки проходят.
- [Удивительное поведение Postgres: UNIQUE индекс не всегда ловит race](https://news.ycombinator.com/item?id=40200843) — при определённом уровне изоляции (READ COMMITTED) «победившая» транзакция коммитится, «проигравшая» получает duplicate key error, но если индекс только в коде — дубль остаётся.
- [How to prevent concurrency issues in postgres with simultaneous requests for max](https://stackoverflow.com/questions/78106713/how-to-prevent-concurrency-issues-in-postgres-with-simultaneous-requests-for-max) — решение через SELECT … FOR UPDATE перед вставкой.

**Багы и реальные кейсы**
- В проекте postgraas_server при одновременных запросах на создание пользователя возникала `IntegrityError: duplicate key value violates unique constraint "pg_authid_rolname_index"`. Проблема решилась введением блокировки или семафора (issue #24).
- В production: два HTTP-запроса в одну секунду → функция создания заказа вызывает `SELECT MAX(order_number)` + 1, обе транзакции получают одинаковый номер → дубликат заказа. Уникальный индекс в БД отсутствовал.

**Технические детали**
- Воспроизведение: запустить параллельно два curl на ручку создания заказа (например, `curl … & curl …`). Если в БД нет уникального constraint на номер заказа — дубли появятся.
- Проверка: `SELECT order_number, COUNT(*) FROM orders GROUP BY order_number HAVING COUNT(*) > 1;`
- Для гарантии уникальности: создать уникальный индекс `CREATE UNIQUE INDEX CONCURRENTLY …` или использовать `INSERT … ON CONFLICT DO NOTHING`. Альтернатива — применение `pg_advisory_xact_lock` на сериализованный идентификатор заказа.

---

### Как проверить ручку создания платежа на дубли при параллельном запуске (без уникального constraint)

**Links & Sources**
- [Stripe Webhook Idempotency Race Condition](https://gembait.com/en/blog/stripe-webhook-idempotency-race-condition) — SELECT-затем-INSERT без блокировки приводит к двойному списанию; одноcтрочное решение — `INSERT INTO idempotency(key, result) VALUES ($1, $2) ON CONFLICT DO NOTHING`.
- [How Stripe Prevents Duplicate Payments Using the Idempotent API](https://medium.com/@heyambujsingh/how-stripe-prevents-duplicate-payments-using-the-idempotent-api-fe281a862b23) — идемпотентность через уникальный ключ в хранилище (Redis или БД) с атомарной операцией.
- [Idempotency is easy until the second request is different](https://news.ycombinator.com/item?id=48047930) — обсуждение: если первый запрос успешен, повтор с тем же idempotency-key должен возвращать 200, а не 409, иначе клиент не поймёт статус оригинала.

**Багы и реальные кейсы**
- Stripe в прошлом сталкивалась с дублированием платежей из-за race condition в webhook-обработчике: проверка идемпотентности через `SELECT` + `INSERT` без атомарности → при двух параллельных вызовах обе вставки успевали выполнить SELECT, видели, что ключа нет, и обе вставляли запись → два списания.
- Внутренний кейс: два параллельных запроса на создание платежа с одинаковым `Idempotency-Key` → система не успела записать ключ до прихода второго → дубль. Баг не ловился в юнит-тестах, так как они не симулировали конкурентность.

**Технические детали**
- Тест: запустить N параллельных запросов с одинаковым idempotency-key (например, с помощью `ab` или `wrk`). Проверить, что в таблице платежей только одна запись с этим ключом.
- Команда для воспроизведения:
  ```bash
  for i in {1..5}; do
    curl -X POST -H "Idempotency-Key: same-key-123" -d '...' http://api/payments &
  done
  wait
  ```
- Чек-лист:
  - Есть ли уникальный индекс на `idempotency_key` в БД?
  - Используется ли атомарный `INSERT … ON CONFLICT` (или `SET NX` в Redis)?
  - Убедиться, что уровень изоляции транзакции не ниже `READ COMMITTED` (для `SERIALIZABLE` возможно, но с перехватом ошибок).
  - Проверить обработку ответа: при дубликате ключа должен возвращаться код 200 (не 500) и тот же результат, что в первом успешном запросе.

---

### Идеи для постов
- **«ИИ не увидит race condition: почему автогенерация тестов не спасёт от дублей в БД»** — опираясь на твит Эдди о бесполезности ИИ, показать, что конкурентные баги требуют ручного проектирования кейсов и понимания блокировок.
- **«Слабое звено идемпотентности: как Stripe училась на своих дублях»** — разбор реального бага, пошаговое воспроизведение и тестирование идемпотентности (с контраргументом к позиции Эдди «ИИ заменит тестировщиков» — именно такие баги ИИ не ловит).
- **«Три способа поймать дубль при параллельных запросах (pgbench, ab, ваша ручка)»** — практический чек-лист для канала, с командами и примерами логов — высокая вовлекающая ценность без лишней теории.