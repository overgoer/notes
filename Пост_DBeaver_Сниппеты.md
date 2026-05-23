---
type: пост
формат: шпаргалка
статус: черновик
дата: 2026-05-23
охват: средний (репосты, цель 50+ сохранений)
теги: #пригодитсяТочно #dbeaver
---

# Пост: Фишка в DBeaver, которая экономит мне часы в неделю

Знаешь эту ситуацию: открываешь DBeaver, и начинается — SELECT * FROM…, потом WHERE…, потом GROUP BY… Каждый раз одно и то же.

Так вот. В DBeaver есть **сниппеты** (они же шаблоны / templates).

Пишешь короткое сокращение → жмёшь Tab → оно разворачивается в полный запрос.

**Как настроить:**
ПКМ по редактору SQL → Insert Template → New Template.
Или через меню: Database → SQL Editor → SQL Templates.

**Вот мои 5 сниппетов, которые всегда под рукой:**

`all` → SELECT * FROM ${table} LIMIT 100;
`cnt` → SELECT COUNT(*) FROM ${table};
`dup` → SELECT col, COUNT(*) FROM ${table} GROUP BY col HAVING COUNT(*) > 1;
`topn` → SELECT * FROM ${table} ORDER BY ${column} DESC LIMIT ${n};
`dbsize` → SELECT pg_size_pretty(pg_database_size(current_database()));

Просто пишу `dup` + Tab — и готовый запрос на поиск дубликатов. Ничего вспоминать не надо.

**Бонус для внимательных:**
Сниппеты хранятся в `~/.dbeaver/snippets/` как обычные XML-файлы. Можно:
- перекинуть на другой комп — синхронизация,
- зашить в .gitignore (чтобы не светить sensitive),
- расшарить с командой.

**Вопрос:** какие запросы ты повторяешь каждый день? Может, из этого сделаем шпаргалку?
