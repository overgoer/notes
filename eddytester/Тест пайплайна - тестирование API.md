# Тест пайплайна: "Тестирование API"

## Что делали

1. **Research** — Researcher v3 прогнал тему "тестирование API" через Serper/DeepSeek
2. **Pipeline** — SEO Machine (Editor → SEO Optimizer → Meta Creator → Internal Linker → Keyword Mapper)

## Результат исследования (Researcher)

7 вопросов, реальные Google-запросы, разбор конкурентов:

1. Когда в GitHub API кэш маскирует ошибки бэкенда
2. Rate limiting превращает тесты в «меня забанили»
3. Идемпотентность GET/POST/DELETE
4. Заголовки Vary и чужие данные (кейс Яндекса)
5. PUT vs PATCH — неотправленные поля исчезают
6. Кэш-отравление (cache poisoning)
7. Идемпотентность POST /orders

**Полный research brief**: `research_тестирование_api_2026-05-29.md` на сервере

---

## Результат пайплайна (SEO Machine)

### Статья
- **Заголовок**: Тестирование API: как отличить баг кэширования от реальной ошибки бэкенда
- **Длина**: 2092 слова
- **Структура**: Введение → Кэш прячет ошибки → Rate limiting → Идемпотентность → Vary → PUT vs PATCH → Чек-лист
- **Стиль**: сторителлинг (Настя, Василий/арбуз, Павел), curl-примеры, чек-лист в конце

### SEO-оценка: 63/100
- Ключевые слова: 12/25 (основной ключ только в H1, нет в H2)
- Структура: 18/25 (нет H3)
- Техническое SEO: 10/25 (нет внутренних ссылок)
- Пользовательский опыт: 23/25

### Проблемы
1. **Meta не распарсилась** — extract_meta() не понимает формат DeepSeek
2. **Internal Linker ссылается на Castos** (чужой продукт из шаблонов), а не на eddytester.com/Practicum
3. **Keyword Analysis пустой** — DeepSeek V4 Flash не хватило токенов

---

## Выводы для настройки

### Нужно поправить в промптах агентов SEO Machine:

| Агент | Что править |
|-------|------------|
| **Editor** | Добавить: стиль Эдди, ссылки на Practicum, target audience QA |
| **Meta Creator** | Формат вывода под extract_meta() regex |
| **Internal Linker** | Поменять Castos → eddytester.com / Practicum |
| **Keyword Mapper** | Увеличить max_tokens (сейчас 2048, мало) |
| **SEO Optimizer** | Заточить под русскоязычное SEO, а не английский подкастинг |

### Что нужно добавить в pipeline:
- Research Phase (Serper → Researcher → Editor) как отдельный шаг
- p. s. ContentScorer требует `pip install textstat`

---

*Дата теста: 2026-05-29*
*Модели: Editor → DeepSeek V4 Pro, остальные → DeepSeek V4 Flash*
