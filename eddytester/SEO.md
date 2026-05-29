# SEO AI Agent — полный цикл для eddytester.com

## Контекст

- **Цель**: конвертировать контент из Telegram и YouTube в SEO-оптимизированные статьи на eddytester.com
- **Аудитория**: тестировщики (QA, automation, API testing)
- **Продукт**: API Practicum (платный)
- **Сервер**: Amsterdam (77.73.135.110)
- **Текущий сайт**: лендинг, нужно превратить в контентный сайт
- **Темы**: берём из существующего контента (TG посты, YouTube), не используем researcher

---

## Стек

### SEO Machine (основной)
**GitHub**: https://github.com/TheCraigHewitt/seomachine

Python, MIT лицензия, self-hosted, ~7k stars. Нужен форк с заменой Claude API → DeepSeek API.

**Агенты SEO Machine (10 шт):**

| Агент | Что делает |
|---|---|
| Content Analyzer | Разбирает исходный пост TG/YouTube |
| SEO Optimizer | Оптимизация под поисковики, плотность ключей, LSI |
| Meta Element Creator | Title, meta description, Open Graph |
| Internal Linker | Внутренняя перелинковка между статьями + ссылки на Practicum |
| Keyword Mapper | Кластеризация ключей по статьям |
| Editor | Правка текста, TLDR, читаемость |
| Headline Generator | Заголовки H1 + H2 |
| Landing Page Optimizer | Оптимизация лендинга Practicum |
| CRO Analyst | Конверсия (призывы, цеплялки) |
| Performance Analyst | Core Web Vitals, скорость |

### LibreCrawl MCP (дополнительно)
Self-hosted краулер (аналог Screaming Frog). Проверяет сайт раз в неделю: битые ссылки, дубли, meta-ошибки.

### WordPress + Yoast (существующее)
Финишный слой — schema markup, sitemap, canonical, OG-теги.

---

## Кто за что отвечает (on-page SEO)

| Техника | Кто делает | Как |
|---|---|---|
| **H1-H3 структура** | SEO Machine → Content Analyzer + Editor | Иерархия от заголовка до подразделов |
| **Meta Title + Description** | SEO Machine → Meta Element Creator | Уникальный для каждой статьи |
| **TLDR (featured snippet)** | SEO Machine → Editor | Первые 2-3 предложения = краткий ответ на главный вопрос. Google забирает их в AI Overviews |
| **Ключ в первом абзаце** | SEO Machine → SEO Optimizer | Главный ключ в первом 50 слов |
| **LSI + long-tail** | SEO Machine → Keyword Mapper | Распределение по заголовкам |
| **Internal linking** | SEO Machine → Internal Linker | Ссылки между статьями + на Practicum |
| **Ссылка на Practicum** | Internal Linker | Каждая статья → 1-2 ссылки на продукт |
| **Alt text** | SEO Machine → Editor | Описание картинок |
| **Open Graph / Twitter** | Yoast | Автоматически из meta |
| **Article Schema** | Yoast | Автоматически |
| **FAQ Schema** | Yoast | Вручную где нужно |
| **Canonical** | Yoast | Автоматически |
| **Sitemap** | Yoast | Автообновление |
| **Readability** | SEO Machine → Readability Scorer | Оценка 0-100 |
| **Битые ссылки** | LibreCrawl | Еженедельная проверка |
| **Дубли (cannibalization)** | LibreCrawl | Проверка пересечения ключей |

---

## Архитектура на Amsterdam

```
┌──────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  TG / YouTube│────▶│  SEO Machine (fork)  │────▶│  eddytester.com │
│  (контент)   │     │                      │     │  (WordPress)     │
└──────────────┘     │  1. Content Analyzer  │     └────────┬────────┘
                     │  2. Editor            │              │
                     │  3. SEO Optimizer     │     ┌────────┴────────┐
                     │  4. Meta Creator      │     │  Yoast SEO      │
                     │  5. Internal Linker   │     │  - schema       │
                     │  6. Keyword Mapper    │     │  - sitemap      │
                     │  7. Headline Gen.     │     │  - OG/canonical │
                     │  8. CRO Analyst       │     └─────────────────┘
                     │  9. Performance An.   │
                     │  10. Landing Page Opt.│     ┌─────────────────┐
                     │                      │────▶│  LibreCrawl MCP  │
                     │  DeepSeek API бэкенд  │     │  (раз в неделю)  │
                     └──────────────────────┘     └─────────────────┘
```

---

## План реализации

### Stage 1: Форк SEO Machine + адаптация под DeepSeek (1 день)

1. **Форкнуть** https://github.com/TheCraigHewitt/seomachine на Amsterdam
2. **Заменить LLM бэкенд**: Claude API → DeepSeek API
   - Везде где вызывается Anthropic SDK → заменить на `requests` к DeepSeek API
   - Промпты адаптировать под формат DeepSeek (ChatML)
3. **Подключить существующие API ключи**: DEEPSEEK_API_KEY (уже есть)
4. **Проверить**: прогнать тестовую статью

### Stage 2: Конвейер TG/YouTube → статья (1 день)

1. **TG API**: скрипт, который забирает последние N постов
2. **YouTube API**: скрипт забирает расшифровки (или берем готовый текст)
3. **SEO Machine pipeline**: post → Content Analyzer → Editor → SEO Optimizer → Meta Creator → Internal Linker
4. **WordPress API**: SEO Machine умеет публиковать через REST API + Yoast

### Stage 3: Template для статей под нишу QA (0.5 дня)

Промпт для Editor в SEO Machine:

```
Для статьи на тему "{topic}" для аудитории тестировщиков:
- TLDR: 2-3 предложения с главным выводом (для featured snippet)
- Целевой ключ: в первом абзаце
- Структура: H1 → H2 (3-5 разделов) → H3 (примеры кода, curl, postman)
- Глоссарий: define термины для джунов (regression, smoke, stub/mock)
- Примеры: curl-команды, Postman скриншоты, HTTP-ответы
- Internal link: ссылка на смежную статью + ссылка на API Practicum
- CTA: "Хочешь попрактиковаться? Попробуй API Practicum"
- Readability: 60-80 (Flesch)
- Длина: 800-1200 слов
```

### Stage 4: LibreCrawl — еженедельный аудит (0.5 дня)

1. Развернуть контейнер
2. Настроить проверки: meta, битые ссылки, дубли, core web vitals
3. Результат → отчет в Obsidian

### Stage 5: Первый запуск (live)

1. Взять 3 лучших TG поста (например: "HTTP 204 No Content", "JSON vs XML vs Protobuf", "SQL injection")
2. Прогнать через pipeline
3. Опубликовать на eddytester.com
4. Проверить: индексация, позиции, meta, schema

---

## SEO техники для ниши QA (которые нужны, но я о них не знал)

| Техника | Суть |
|---|---|
| **Featured Snippet оптимизация** | Структурировать первые абзацы под "прямой ответ" — Google забирает их в блок "0 позиция" |
| **E-E-A-T** | Experience, Expertise, Authoritativeness, Trustworthiness. Для статей про тестирование: показать, что автор — практик, а не рерайтер |
| **Keyword Cannibalization** | Две статьи на один запрос — Google их обе ранжирует низко. LibreCrawl ловит это |
| **LSI Keywords** | Не синонимы, а семантически связанные слова. Для "REST API testing": "endpoint, idempotency, payload, status codes, Postman" |
| **Silo структура** | Статьи группируются по темам и перелинковываются внутри группы. Для QA: "основы" → "API" → "инструменты" → "Practicum" |
| **Content Gap** | Что ищут, но никто в нише не пишет. Например: "как тестировать race conditions в API" — мало статей, но ищут |
| **Skyscraper Technique** | Берем конкурентную статью, делаем в 2 раза глубже и качественнее |
| **Inbound links** | Ссылки с других сайтов на твои статьи. Пока не актуально, но потом — обмен с другими QA-блогами |
| **Core Web Vitals** | LCP < 2.5s, FID < 100ms, CLS < 0.1. WordPress с хорошей темой обычно ок |

---

## Первые темы для статей (из существующих TG постов)

1. HTTP 204 No Content — как тестировать
2. JSON vs XML vs Protobuf — что и когда выбирать
3. Blind SQL injection — тестирование для manual QA
4. HTTP headers deep dive — CORS, cache, security
5. Postman advanced коллекции
6. SQL injection for beginners
7. 10 багов API реальных компаний
8. Чек-лист тестирования REST API
9. Postman: как тестировать авторизацию
10. API Practicum review: мой опыт

---

## Что нужно для старта

- [ ] Форкнуть SEO Machine на Amsterdam
- [ ] Заменить API вызовы Claude → DeepSeek
- [ ] WordPress API доступ (уже есть на eddytester.com?)
- [ ] LibreCrawl контейнер
- [ ] Первые 3 статьи = тест

---

*Последнее обновление: 2026-05-29*
*На основе анализа: SEO Machine (основной), LibreCrawl MCP (дополнительно), WordPress+Yoast (база)*
