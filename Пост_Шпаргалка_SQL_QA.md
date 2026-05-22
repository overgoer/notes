---
type: пост
формат: шпаргалка
статус: черновик
дата: 2026-05-22
охват: средний (репосты, цель 50+ сохранений)
теги: #пригодитсяТочно
---

# Пост: 5 SQL-запросов, которые спасают меня каждый день

#пригодитсяТочно 👇

**1. Все записи за последние N дней**
```sql
SELECT * FROM orders
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
```

**2. Дубликаты в таблице (баг №1 тестировщика)**
```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

**3. Строки, которые есть в А, но нет в Б**
```sql
SELECT id FROM table_a
EXCEPT
SELECT id FROM table_b;
```
Без этого на каждом регресс ищу потерянные записи.

**4. Первые N записей в группе (топ пользователей по заказам)**
```sql
SELECT user_id, total
FROM (
  SELECT user_id, SUM(amount) as total,
  ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) as rn
  FROM orders GROUP BY user_id
) sub WHERE rn <= 10;
```

**5. Размер базы данных (спойлер: тестовая база не чистится никогда)**
```sql
SELECT pg_size_pretty(pg_database_size('practicum'));
```

**Сохраняй в закладки — пригодится на код-ревью и при тестировании БД.** 🔖

**Вопрос:** какой SQL-запрос ты чаще всего пишешь на работе?
