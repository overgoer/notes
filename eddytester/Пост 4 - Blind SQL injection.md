---
created: 2026-05-13
tags: security, sqli, manual-testing
angle: Blind SQL injection — how a manual tester can detect it even when the database is invisible
---

# Ты не видишь базу данных. Как найти SQL-инъекцию вслепую? Разбор на реальном кейсе (Equifax + простой пример)

**Дата:** 2026-05-13
**GA RATING:** GOOD

---

## GA Review

RATING: GOOD
VERDICT: The topic is valuable and fills a content gap (security testing), but the brief covers too broad a scope (SQLi, XSS, CSRF) for a single post. Pick one concrete angle from the brief for a focused, actionable post.
BEST_ANGLE: Blind SQL injection — how a manual tester can detect it even when the database is invisible, using practical techniques like `CASE WHEN` in `ORDER BY` and timing-based checks (without any access to server logs or DB).
POST_IDEA: "Ты не видишь базу данных. Как найти SQL-инъекцию вслепую? Разбор на реальном кейсе (Equifax + простой пример)"
WHY: The angle is specific, grounded in a famous real-world breach, and offers concrete steps (e.g., `ORDER BY`, `CASE WHEN`, payloads) that a junior can try in any API.

---

## Post Draft (Channel Agent)

**Situation**
Ты тестируешь поиск товаров, но в ответе нет сырых данных — только «найдено/не найдено». Или сортировка по цене работает, а саму БД не видно. Как найти SQL-инъекцию, если база молчит? Пример: в 2017 году Equifax утекли 147M записей через поисковый запрос — без прямого вывода, по косвенным признакам.

**Analysis**
Два простых метода для ручного теста (ни логов, ни доступа к серверу):

1. **CASE WHEN в ORDER BY**
   Вставляем в параметр `sort` конструкцию:
   `CASE WHEN (SELECT substring(password,1,1) FROM users LIMIT 1)='a' THEN 1 ELSE 2 END`
   Если условие истинно — порядок один, если ложно — другой. Меняя букву, можно «угадать» пароль посимвольно, даже не видя ответа, только сравнивая порядок строк.

2. **Timing-based (blind)**
   Если сервер не показывает разницу в контенте, используем `sleep`:
   `' OR IF(1=1, SLEEP(5), 0) --`
   Задержка ответа на 5 секунд говорит, что инъекция сработала. Подходит для `WHERE`, `UPDATE`, `INSERT`.

**Verdict**
Это **баг**. Если сервер выполняет произвольный SQL, значит уязвимость есть. Что делать:
- Зафиксировать точку входа (параметр).
- Сообщить разработчикам — нужна параметризация запросов (prepared statements).
- Важно: `ORDER BY` часто не экранируют, но он так же опасен, как `WHERE`.

**Takeaway**
Любая строка, которая попадает в SQL-запрос — потенциальная дыра. Тестируй места, где сервер реагирует на твой ввод (сортировка, поиск, фильтры) даже без прямого вывода данных. Если видишь изменение поведения — копай глубже.

**Реалы**
- Blind SQLi — нудная техника: тыкать в `CASE WHEN` по 50 раз, но именно так Equifax и взломали.
- Тайминги `sleep` на проде могут вызвать ДДОС-эффект, лучше использовать минимальные задержки (1-2 сек).
- Не все тестировщики знают, что `ORDER BY` — тоже поверхность атаки, так что можешь удивить разработчика своим репортом.

**Полезно:**
[PortSwigger: Blind SQLi tutorial](https://portswigger.net/web-security/sql-injection/blind)
[OWASP: Testing for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.html)

---

## Post Draft (Style Adapter)

Ты тестируешь поиск товаров. В ответе нет сырых данных — только "найдено" или "не найдено". Сортировка по цене работает, но саму базу данных не видно. Как найти SQL-инъекцию, когда сервер молчит?

Equifax в 2017 году утекли 147 миллионов записей именно так — через поисковый запрос без прямого вывода данных. Уязвимость нашли по косвенным признакам. Вот два метода для ручного теста без доступа к серверу.

Первый — CASE WHEN в ORDER BY. Вставляешь в параметр сортировки конструкцию вроде `CASE WHEN (SELECT substring(password,1,1) FROM users LIMIT 1)='a' THEN 1 ELSE 2 END`. Если условие истинно — порядок строк один, если ложно — другой. Меняя букву в условии, можно "угадать" пароль посимвольно, даже не видя его, только по порядку результатов запроса.

Второй — timing-based (слепая инъекция по времени). Если сервер не меняет тело ответа, используй sleep: `' OR IF(1=1, SLEEP(5), 0) --`. Задержка ответа на 5 секунд — инъекция сработала. Подходит для WHERE, UPDATE, INSERT.

**Почему это важно:** ORDER BY часто не экранируют, считая его безопасным. Но он так же опасен, как WHERE. Любая строка, которая попадает в SQL-запрос — потенциальная дыра.

**Verdict:** баг. Фикс — параметризация запросов (prepared statements, отделяющие код от данных). Если сервер выполняет произвольный SQL, значит уязвимость есть.

**Реалы:** Blind SQLi — нудная техника, но именно так взломали Equifax. Тайминги sleep на проде могут вызвать ДДОС, используй 1-2 секунды. И не все знают, что ORDER BY — тоже поверхность атаки, так что твой репорт может удивить разработчика.

**Полезно:** [PortSwigger: Blind SQLi](https://portswigger.net/web-security/sql-injection/blind), [OWASP: Testing for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.html)

---

## Research Brief

Тема: Security testing for manual QA: SQL injection, XSS, CSRF — real cases and checklists

Ключевые находки из research brief:
- Equifax 2017: утекли 147M записей через поисковый запрос (Apache Struts CVE-2017-5638)
- Blind SQLi: техники CASE WHEN в ORDER BY и timing-based detection
- PortSwigger Academy: полный гайд по Blind SQLi с лабораторными работами
- OWASP: чек-лист тестирования SQL-инъекций
- XSS: отраженные, хранимые, DOM-based — методы обнаружения
- CSRF: отсутствие токенов, неправильная валидация Origin/Referer
