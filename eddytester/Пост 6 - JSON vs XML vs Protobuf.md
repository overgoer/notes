---
created: 2026-05-13
tags: json, xml, protobuf, data-formats, api-testing, manual-testing
angle: Focus on one specific, junior-friendly scenario: testing that JSON and XML return identical data, plus Protobuf gotchas
---

# JSON vs XML vs Protobuf: как тестировать разные форматы данных в API

**Дата:** 2026-05-13
**GA RATING:** GOOD

---

## GA Review

RATING: GOOD
VERDICT: The research is rich in concrete, real-world bugs and edge cases — exactly what the channel needs. However, the topic is too broad for a single post; trying to cover JSON, XML, and Protobuf in one go would dilute the meat.
BEST_ANGLE: Focus on one specific, junior-friendly scenario: testing that JSON and XML return identical data, plus Protobuf gotchas for those who work with gRPC.
POST_IDEA: "Три формата, один API: как тестировать JSON, XML и Protobuf, чтобы ничего не сломать"
WHY: Pick the most impactful sub-topics: format conformance (JSON != XML via Accept), XXE for XML, Protobuf field numbering.

---

## Post Draft (Style Adapter)

Твой API поддерживает JSON, XML и Protobuf. Клиент шлёт Accept: application/json — получает JSON. Accept: application/xml — XML. Всё работает. Пока не выясняется, что JSON и XML отдают разные данные.

Самый частый баг — сервер по-разному округляет числа в JSON и XML. JSON скажет `price: 10.99`, XML — `<price>10.9900000001</price>`. Клиент на XML получит неверную цену. Причина: разные сериализаторы в бэкенде.

Вторая категория — XXE (XML External Entity). Да, в 2025 это всё ещё актуально. XML-парсер может подтянуть файл с диска через entity expansion. Проверяется одним запросом:
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```
Если в ответе увидишь содержимое /etc/passwd — XXE есть. Лечение: отключить DOCTYPE и внешние сущности в парсере.

Protobuf — отдельная песочница. Он не хранит имена полей, только номера. Разработчик удалил поле `user_email` (номер 5) и добавил `user_phone` (тоже номер 5). Старый клиент с протобафом получит телефон вместо емейла — и не заметит, потому что номера совпадают. А ещё если клиент на старой схеме, а сервер добавил новое поле — unknown fields должны передаваться без потерь через прокси. И это часто ломается.

**Как тестировать:**
1. Отправь один запрос с Accept: application/json и Accept: application/xml. Сравни canonical form (отбрось форматирование, сравни значения).
2. XXE-тест: одно тело XML с entity expansion. Если работает — критический баг.
3. Protobuf: проверь все field numbers на уникальность. Удали поле — убедись, что номер не переиспользован.
4. Conformance-тест: для каждого формата — один и тот же набор данных, сравнивай бизнес-логику, не структуру.

**Полезно:**
[PortSwigger: XXE](https://portswigger.net/web-security/xxe)
[Protobuf: Field Number Best Practices](https://earthly.dev/blog/backward-and-forward-compatibility/)

---

## Post Draft (Channel Agent — старая версия)

**Situation**
Твой API отдаёт данные в трёх форматах. Ты тестируешь JSON — всё ок. XML — ок. Protobuf — ок. А в проде — клиенты получают разные данные в зависимости от формата.

**Analysis**

**JSON vs XML: разные округления**
Сериализаторы JSON и XML по-разному работают с числами. `10.99` в JSON может стать `10.9900000001` в XML.
*Как проверить:* отправить запрос `Accept: application/json`, потом `Accept: application/xml`. Сравнить значения. Хорошо — canonical form (JSON нормализация + XML canonical).

**XXE (XML External Entity)**
Если сервер принимает XML и не отключил парсинг внешних сущностей — атакующий может читать файлы с сервера.
*Как проверить:*
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```
Ответ содержит /etc/passwd — баг.

**Protobuf: переиспользование field numbers**
Номера полей — идентификаторы. Если удалить поле и добавить новое с тем же номером — старый клиент получит не те данные.
*Как проверить:* открыть .proto файл, проверить, что ни один field number не повторяется, а удалённые помечены reserved.

**Protobuf: missing vs null**
В JSON `null` и отсутствие поля — разные вещи? Нет. В Protobuf — да. Поле со значением по умолчанию (0, "") не отправляется на проводах. Клиент не может отличить «поле не установлено» от «поле равно 0».
*Как проверить:* отправить запрос с явным null. В Protobuf-ответе поле может отсутствовать.

**Unknown fields через прокси**
Если прокси не умеет передавать незнакомые protobuf-байты — старый клиент теряет данные при обновлении схемы.
*Как проверить:* добавить новое поле на сервере → запросить через старого клиента. Поле должно быть в raw-байтах.

**Verdict**
Это **баги имплементации**. Форматы ведут себя по-разному, и это нормально. Но если бизнес-логика меняется от формата к формату — это баг.

**Takeaway**
Одна бизнес-логика = один набор данных = одинаковый ответ во всех форматах. Тестируй conformance, не формат. И не забывай про XXE — он жив.

**Реалы**
- XXE в 2025 — это как «майнкрафт всё ещё популярен». Все знают, но не все чинят.
- Protobuf field numbers — ошибка на миллион. Github Slack угорают.
- JSON vs XML rounding — кейс из Stripe docs. Они через это прошли.

**Полезно:**
[PortSwigger: XXE](https://portswigger.net/web-security/xxe)
[OWASP: XXE Processing](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing)
[Protobuf: Backward Compatibility](https://earthly.dev/blog/backward-and-forward-compatibility/)

---

## Research Brief

Тема: JSON vs XML vs Protobuf: testing different data formats in API requests

Ключевые находки:
- GitLab перепутал Content-Type: отдавал XML вместо JSON
- JSON и XML: разные округления чисел, разные null-семантики
- XXE: всё ещё актуально, даже в 2025
- Protobuf: field numbers unique, нельзя переиспользовать
- missing vs null: в Protobuf нет разницы, в JSON есть
- Unknown fields должны проходить через прокси без потерь
- Conformance test: canonical form для сравнения ответов
