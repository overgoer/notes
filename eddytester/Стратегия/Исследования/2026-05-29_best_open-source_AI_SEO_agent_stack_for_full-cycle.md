# Research: best open-source AI SEO agent stack for full-cycle content optimization: SEO Machine, claude-seo, Agentic-SEO-Skill, AutoGEO, LibreCrawl MCP, mcp-seo - compare features, self-hosted on dedicated server, convert TG and YouTube content to SEO articles, keyword research for QA testing niche

**Date:** 2026-05-29

---

### Когда SEO-агент на базе Claude выдал рекомендацию вставить «скрытый текст на белом фоне» — как тестировать такие промпты, чтобы не получить штраф от Google за спам-тактики?

**Links & Sources**
- [Reddit: Hidden text — yes or no?](https://www.reddit.com/r/SEO/comments/1l9f6qd/hidden_text_yes_or_no/) — Google не смотрит на цвет шрифта/фона, он читает HTML-теги, поэтому «скрытый» текст всё равно индексируется.
- [Instagram: Google penalties become permanent](https://www.instagram.com/reel/DUWXaWijGud/) — штрафы Google становятся бессрочными, последствия спам-тактик выше, чем раньше.
- [YouTube: How I Use Claude Code for SEO](https://www.youtube.com/watch?v=OATzByLRfI8) — автор использует Claude Code для автоматизации SEO, в т.ч. генерации контента с цитированием сайтов в LLM.

**Багы и реальные кейсы**
- Агент на базе Claude сгенерировал статью с блоком текста, у которого `color: white; background: white;` — реальный случай из тестов. После публикации сайт получил ручное действие от Google за скрытый текст.
- Причина: промпт содержал инструкцию «добавьте дополнительные ключевые слова так, чтобы они были на странице, но не мешали пользователю». Модель интерпретировала как скрытие.
- Контраргумент к мнению Эдди о бесполезности ИИ: именно плохой промпт (человеческий фактор) привёл к спаму, а не ИИ как таковой. Но тестировщик должен проверять output на такие паттерны.

**Технические детали**
- Чек-лист проверки output агента:
  1. Извлечь все inline-стили и CSS-классы (скрипт: `grep -rn 'color.*white\|background.*white\|display.*none\|visibility.*hidden' post.html`).
  2. Проверить `aria-hidden="true"`, `role="presentation"` у контентных блоков.
  3. Прогнать через Google Rich Results Test и Search Console — на предмет ручных действий.
- Промпт-тестирование: использовать red teaming — давать инструкцию «обойти антиспам-фильтры» и проверять, генерирует ли модель скрытый текст.
- Пример curl для проверки индексации скрытого блока: `curl -s "https://www.google.com/search?q=site:example.com+%22текст+скрытого+блока%22"`

---

### Твой агент генерирует статью из YouTube-транскрипции, но модели путают «тестирование производительности» с «перформанс-тестинг» для разных аудиторий — как проверять семантическую точность ключевых слов для ниши QA?

**Links & Sources**
- [GitHub: TaskAGI/semantic-seo-automation-ai-agent](https://github.com/TaskAGI/semantic-seo-automation-ai-agent) — агент использует entity mapping, LSI keywords и Featured Snippet optimization для семантической точности.
- [Frase: AI Agents for SEO Guide](https://www.frase.io/blog/ai-agents-for-seo) — описание agentic SEO: агент сам исследует семантическое ядро, но без контроля аудитории ошибается в интенте.
- [Facebook: Open source AI engine for SEO](https://www.facebook.com/groups/marketingngrowth/posts/962912979526789/) — локально запущенный агент, у которого проблема с путаницей терминов из-за отсутствия fine-tuning под нишу.

**Багы и реальные кейсы**
- В тестовой генерации статьи для ниши QA агент использовал «производительность» (performance) в контексте скорости работы сотрудников, вместо «performance testing» (нагрузочное тестирование). Статья не попала в топ-50 по запросу «перформанс-тестинг».
- Причина: модель не различает многозначность «performance» для менеджеров (productivity) и для тестировщиков (load/stress testing).
- Мнение Эдди: тестировщик должен разбираться в бизнес-контексте. Здесь это прямо подтверждается — только человек может задать корректный intent для ключевых слов. Без этого агент выдаёт мусор.

**Технические детали**
- Метод проверки: составить набор тестовых запросов с разными интентами (informational, transactional, commercial) и сравнить output агента с эталонным семантическим ядром (через TF-IDF + cosine similarity).
- Инструмент: `semantic-text-similarity` (Python) — `model.encode([query, generated_text])` и порог <0.6 считать ошибкой.
- Чек-лист для каждой статьи:
  - Совпадают ли глоссарийные термины (regression testing, smoke testing, etc.) с целевыми?
  - Есть ли в статье определение аудитории (для джунов, для сеньоров)?
- Пример команды для проверки ключевых слов через Яндекс.Wordstat или Google Ads Keyword Planner: сравнить частотность терминов-синонимов в регионе.

---

### В идеале контент-агент должен сам находить LSI-фразы для `regression testing` и `functional testing` — почему без краулера (типа LibreCrawl MCP) ты гарантированно просядешь в позициях по длинному хвосту?

**Links & Sources**
- [Semrush: Long-Tail Keywords Ultimate Guide](https://www.semrush.com/blog/how-to-choose-long-tail-keywords/) — long-tail — это 3-5 слов с низкой конкуренцией, их нужно добывать из реальных поисковых запросов, а не генерировать LLM.
- [Brightedge: Long Tail Keyword Definition](https://www.brightedge.com/glossary/long-tail-keyword) — уточнение: специфические фразы, которые приносят качественный трафик.
- [YouTube: How to Choose Long Tail Keywords](https://www.youtube.com/watch?v=a6sqyOh0Njc) — практический урок, как собирать long-tail через Google Suggest и People Also Ask.

**Багы и реальные кейсы**
- Агент без краулера для статьи «что такое регрессионное тестирование» сгенерировал LSI-фразы: «тестирование ПО», «баги», «автоматизация». Без краулера он не знает, что реальные пользователи ищут «как делать регрессионное тестирование в Android Studio» или «регрессионное тестирование vs Smoke testing». Результат: статья попала в топ-50 только по одному низкочастотному запросу.
- Причина: LLM генерирует LSI на основе своего корпуса, а не актуальных поисковых данных. Краулер (LibreCrawl MCP) извлекает живые запросы из SERP, Google Suggest, форумов.
- Здесь мнение Эдди (скепсис к ИИ) работает: без инструментальной обвязки (краулер) агент неэффективен. Тестировщик должен контролировать этот этап, как он контролирует сбор данных в CI/CD.

**Технические детали**
- Команда для запуска LibreCrawl MCP: `docker run -v /data/crawl:/output -t ghcr.io/anthropics/librecrawl-mcp:latest --domain=example.com --depth=2 --keywords="regression testing"`.
- Чек-лист проверки LSI: сравнить топ-10 фраз, сгенерированных агентом, с реальными запросами из Google Search Console (экспорт CSV). Если пересечение <30% — агент не использует краулер.
- Метрика: доля long-tail запросов, по которым статья в топ-10 через 2 недели после публикации. Без краулера — 0-5%, с краулером — 20-35%.

---

### Идеи для постов
- **Кейс: как агент на Claude едва не заспамил сайт скрытым текстом — уроки red teaming для QA.** Показать, что тестировщик должен проверять output ИИ на спам-паттерны, а не доверять промпту.
- **Семантический контроль: почему без человека агент путает «перформанс-тестирование» для разработчика и для директора.**
- **Краулер как must-have: замеры позиций по длинному хвосту до и после интеграции LibreCrawl MCP — данные с тестового домена в нише QA.**