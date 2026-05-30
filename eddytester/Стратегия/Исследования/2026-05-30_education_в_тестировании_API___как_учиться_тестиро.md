# Research: education в тестировании API — как учиться тестировать бэкенд, работа с БД в тестах, практикум для тестировщиков

**Date:** 2026-05-30

---

### Моделирование сценария сбоя идемпотентности Stripe

**Links & Sources**
- [Stripe API Idempotent Requests](https://docs.stripe.com/api/idempotent_requests) — механизм: повтор запроса с тем же ключом не создаёт дубликат.
- [Stripe Automated Testing](https://docs.stripe.com/automated-testing) — как симулировать ошибки API и проверять recovery.
- [Implementing Stripe-like Idempotency Keys in Postgres (Brandur)](https://brandur.org/idempotency-keys) — разбор атомарной фазы: если падает между проверкой и вставкой, клиент ретраит — дубль возможен.

**Баги и реальные кейсы**
- 2023: race condition в обработке идемпотентных запросов Stripe — два параллельных запроса с одинаковым ключом прошли проверку «ключ не найден» одновременно, оба провели платёж → двойное списание.
- В учебном проекте воспроизводится: эндпоинт /pay c идемпотент-ключом; без блокировки (SELECT FOR UPDATE) два параллельных POST с одним ключом вставляют две записи.

**Технические детали**
- Поднять локально Postgres, таблица `idempotency_keys` c unique constraint. В серверный код добавить `SELECT … FOR UPDATE` внутри транзакции.
- Тест на pytest + httpx:
  ```python
  async def test_idempotency_race():
      key = "test-key-1"
      async with httpx.AsyncClient() as client:
          tasks = [client.post("/pay", headers={"Idempotency-Key": key}) for _ in range(2)]
          resp = await asyncio.gather(*tasks)
          # Без FOR UPDATE — оба 200, с FOR UPDATE — один 200, другой 409
  ```
- Чек-лист: BEGIN + SELECT FOR UPDATE + INSERT + COMMIT; в тесте проверять кол-во записей в БД.

---

### Почему SQL в тестах API — must have: пример бага без SELECT

**Links & Sources**
- [SQL Database Testing Tutorial](https://www.stadsolution.com/sql-database-testing-tutorial) — база: проверка целостности после CRUD, JOIN для e-commerce.
- [API Testing and Database Integration Guide](https://tenjinonline.com/blog/api-testing/api-testing-database-integration-guide) — интеграция проверок БД в тест-сьют, assert на статус и данные.

**Баги и реальные кейсы**
- POST /order: API возвращает 200, UI «успешно», но в БД `status = 'pending'` — разработчик забыл COMMIT после UPDATE остатка. Только SELECT выявит.
- DELETE /user: 204, но SELECT показывает, что строки в связанных таблицах не удалены — нарушение ссылочной целостности (каскад не настроен).

**Технические детали**
- Тест Python + psycopg2:
  ```python
  with connection.cursor() as cur:
      cur.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
      assert cur.fetchone()[0] == "confirmed"
  ```
- Проверка каскада: `SELECT COUNT(*) FROM user_roles WHERE user_id = deleted_id`.
- Чек-лист: после каждого API-вызова (POST/PUT/DELETE) добавлять этап верификации базы — вставка, обновление, удаление, NULL-constraints, уникальность.

---

### Идеи для постов
- «Без SQL ты слеп, а AI тебя заменит быстрее» — контраргумент Эдди: AI не понимает бизнес-контекст, SQL-верификация остаётся за человеком.
- «Как Stripe уронил прод из-за race condition на идемпотентности — воспроизводим в учебном проекте за 20 минут».
- «Спор: тестировщик превращается в аудитора процесса разработки — не хочешь? Тогда хотя бы научись писать SELECT».