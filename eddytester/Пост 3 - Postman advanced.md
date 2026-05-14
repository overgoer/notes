---
created: 2026-05-12
tags: postman, api-testing, collections, manual-testing
angle: Postman collection patterns that prevent real-world bugs — from environment mix-ups to chaining failures and data-driven stagnation
---

# Postman: продвинутые техники тестирования API

**Дата:** 2026-05-12
**GA RATING:** MUST POST

---

## GA Review

RATING: MUST POST
VERDICT: This brief is packed with real, painful, and highly specific scenarios (prod vs stage mix-up, chaining failures, data-driven stagnation) that directly match the channel's audience — juniors and middles who use Postman for manual backend testing but lack structured practices.
BEST_ANGLE: Postman collection patterns that prevent real-world bugs — from environment mix-ups to chaining failures and data-driven stagnation.
POST_IDEA: "Postman: 4 привычки, которые спасут твой API от дурацких багов"
WHY: Each pattern is a concrete, painful scenario. The post should walk through each with before/after code.

---

## Post Draft (Channel Agent)

**Situation**
Ты используешь Postman каждый день. Но в твоей коллекции — бомба замедленного действия: переменная окружения ведёт на прод, цепочка запросов ломается при первом сбое, а data-driven тесты не обновлялись годами.

**Analysis**

**Баг #1: Продакшен вместо стейджинга**
Одно неверное имя переменной — и тестовые данные ушли на боевой сервер.
*Как защититься:* добавить в pre-request script защиту:
```javascript
if (pm.environment.name === 'Production') {
    throw new Error('Запуск на проде запрещён!');
}
```
Именуй окружения так, чтобы production нельзя было спутать: `prod-api`, `stage-api`.

**Баг #2: Цепочка запросов ломается при отсутствии предыдущего ответа**
Коллекция запускается в Runner. Первый запрос вернул 500. Токен не сохранился. Второй падает с `TypeError: Cannot read property 'access_token' of undefined`. Весь прогон остановлен.
*Как проверить:* в тестах первого запроса добавлять гард:
```javascript
pm.test('Токен получен', () => {
    const json = pm.response.json();
    pm.expect(json.access_token).to.not.be.undefined;
    pm.collectionVariables.set('token', json.access_token);
});
```
Во втором запросе — pre-request script:
```javascript
if (!pm.collectionVariables.get('token')) {
    console.warn('Токен отсутствует — пропускаем запрос');
    pm.request.skip();
}
```

**Баг #3: Data-driven тесты не обновляются годами**
JSON-файл для data-driven тестов живёт годами. Граничные случаи не добавляются. Тесты проходят, но баги пропускают.
*Как проверить:* аудит data-файла раз в месяц. Добавлять кейсы: пустые значения, null, спецсимволы, длинные строки, негативные сценарии.

**Баг #4: Параллельный запуск перезатирает переменные**
Две коллекции бегут параллельно, обе пишут в одну переменную окружения. Конфликт токенов. Одна коллекция падает.
*Решение:* использовать collection-scoped переменные вместо environment-scoped для временных данных (токены, ID созданных ресурсов).
```javascript
pm.collectionVariables.set('token', json.access_token);
```
Вместо:
```javascript
pm.environment.set('token', json.access_token);
```

**Verdict**
Это не баги кода — это **баги практики**. Postman-коллекция — такой же код, как и тесты. Она должна быть устойчивой к сбоям, предсказуемой и документированной.

**Takeaway**
Постман-коллекция — не скрипт для одного запуска, а артефакт, который живёт годами. Относись к ней как к коду: защита от дурака, обработка ошибок, регулярный аудит.

**Реалы**
- Баг #1 случался с каждым, кто работал с Postman дольше месяца. Вопрос не «если», а «когда».
- Баг #2 — причина, по которой многие ненавидят Collection Runner. Он не прощает ошибок.
- Data-driven тесты без аудита — это тесты, которые проверяют только то, что уже работает.

**Полезно:**
[Postman: Extracting Data from Responses and Chaining Requests](https://blog.postman.com/extracting-data-from-responses-and-chaining-requests/)
[Postman: Variable Scopes](https://learning.postman.com/docs/sending-requests/variables/variables/)

---

## Post Draft (Style Adapter)

Ты используешь Postman каждый день. Но твоя коллекция — бомба замедленного действия. Четыре сценария, которые однажды тебя накажут.

Первый — переменная окружения ведёт на прод. Одно неверное имя — и тестовые данные ушли на боевой сервер. Защита: `if (pm.environment.name === 'Production') { throw new Error('Запуск на проде запрещён!'); }` в pre-request script production-окружения. И именуй окружения так, чтобы прод нельзя было спутать: `prod-api`, `stage-api`.

Второй — цепочка запросов ломается при первом же сбое. Первый запрос вернул 500, токен (временный ключ доступа) не сохранился — второй падает с `TypeError`. Весь прогон встал. Лечение: в тестах первого запроса проверяй, что токен действительно есть: `pm.expect(json.access_token).to.not.be.undefined`. А во втором — pre-script с гардом: если токена нет — пропускай запрос.

Третий — data-driven тесты не обновляются годами. JSON-файл живёт с момента создания коллекции, граничные случаи не добавлены. Тесты зелёные, но баги пропускают. Правило: аудит data-файла раз в месяц. Добавляй пустые строки, null, спецсимволы, негатив.

Четвёртый — параллельный запуск перезатирает переменные. Две коллекции бегут одновременно, обе пишут в одну переменную окружения — конфликт токенов. Решение: используй collection-scoped переменные (`pm.collectionVariables`) для временных данных, а не environment-scoped. Они не конфликтуют между коллекциями.

**Что делать:** относись к Postman-коллекции как к коду. Pre- и post-скрипты, защита от дурака, регулярный аудит. Она будет жить дольше, чем ты думаешь.

**Полезно:** [Postman: Extracting Data from Responses](https://blog.postman.com/extracting-data-from-responses-and-chaining-requests/), [Postman: Variable Scopes](https://learning.postman.com/docs/sending-requests/variables/variables/)

---

## Research Brief

Тема: Postman collections for advanced API testing: environments, chaining requests, data-driven tests

Ключевые находки:
- Переменная окружения ведёт на прод — защита через pm.environment.name
- Цепочка запросов: токен не сохранился → второй запрос падает с TypeError
- Data-driven тесты: один JSON годами, граничные случаи не покрыты
- Параллельный запуск: конфликт переменных окружения
- Fintech: тест создания пользователя без проверки ответа создал 1000 дублей
- Глобальные переменные vs окружения: scope имеет значение
- Тестирование регионов: одна коллекция на все регионы через переменные
