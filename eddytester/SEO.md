# SEO AI Agent — полный цикл для eddytester.com

## Контекст

- **Цель**: конвертировать контент из Telegram и YouTube в SEO-оптимизированные статьи на eddytester.com
- **Аудитория**: тестировщики (QA, automation, API testing)
- **Продукт**: API Practicum (платный)
- **Сервер**: Amsterdam (77.73.135.110), там же BSA → DeepSeek researcher
- **Текущий сайт**: лендинг, нужно превратить в контентный сайт

---

## Рекомендуемый стек

### SEO Machine (основной кандидат)
**GitHub**: https://github.com/TheCraigHewitt/seomachine

**Почему он**:
- Единственный проект, покрывающий полный цикл: research → rewrite → optimize → publish
- 10 встроенных AI агентов под разные задачи SEO
- Работает с WordPress/Yoast (прямая публикация)
- Python — легко адаптировать под DeepSeek

**Агенты SEO Machine**:
| Агент | Назначение |
|---|---|
| Content Analyzer | Анализ существующего контента |
| SEO Optimizer | Оптимизация под поисковики |
| Meta Element Creator | Title, description, og-tags |
| Internal Linker | Внутренняя перелинковка |
| Keyword Mapper | Кластеризация ключей |
| Editor | Редактура |
| Performance Analyst | Core Web Vitals |
| Headline Generator | Заголовки |
| Landing Page Optimizer | Посадочные страницы |
| CRO Analyst | Конверсия |

### Адаптация под нишу "тестировщики"

Стратегия контента (что должен делать агент):
1. **Забрать контент** из Telegram и YouTube (API)
2. **DeepSeek researcher** анализирует, определяет:
   - Ключевые слова ниши (API testing, Postman, SQL injection, HTTP, JSON/XML/Protobuf и т.д.)
   - Поисковые интенты аудитории
   - Конкурентные разрывы (что ищут, но никто не покрывает)
3. **SEO Machine** перерабатывает в статьи:
   - Улучшает структуру (H1-H3, списки, читаемость)
   - Оптимизирует meta-теги
   - Добавляет внутренние ссылки на Practicum
4. **Публикация** на eddytester.com

### Архитектура на Amsterdam сервере

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  TG/YouTube  │────▶│  DeepSeek        │────▶│  SEO Machine │
│  API         │     │  Researcher      │     │  (adapted)   │
└─────────────┘     │  (стратегия,      │     └──────┬──────┘
                    │   ключи, темы)    │            │
                    └──────────────────┘     ┌───────┴────────┐
                                             │  eddytester.com │
                                             │  (WordPress)    │
                                             └────────────────┘
```

### Альтернативы (запасные)

| Проект | Когда использовать |
|---|---|
| **claude-seo** | Если нужен аудит сайта / быстрая диагностика |
| **LibreCrawl MCP** | Если нужен глубокий технический краулинг (как Screaming Frog) |
| **AutoGEO** | Когда понадобится оптимизация под AI-поиск (ChatGPT, Perplexity) |
| **OpenSEO** | Если нужно заменить Ahrefs/Semrush (ранжирование, бэклинг) |

### План развертывания

1. Установить Python-окружение на Amsterdam сервере
2. Форкнуть/склонировать SEO Machine
3. Заменить LLM бэкенд (Claude API → DeepSeek API)
4. Подключить researcher как "стратег" (generates prompts/plans)
5. Настроить WordPress API для публикации
6. Запустить первый pipeline: взять пост из TG → статья

---

## Ключевые SEO-термины для ниши тестировщиков (предварительно)

- API testing, API testing tutorial, REST API testing
- Postman tutorial, Postman advanced
- SQL injection testing
- HTTP headers, HTTP methods
- JSON vs XML vs Protobuf
- Blind SQL injection
- HTTP 204 No Content, HTTP status codes
- API automation testing
- API security testing
- Regression testing, integration testing
- QA engineer roadmap
- Как стать тестировщиком
- API Practicum, API testing course

*(это подсветит DeepSeek researcher — какие из них реально залетят)*
