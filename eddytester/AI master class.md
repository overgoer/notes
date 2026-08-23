# AI Master Class — ИИ для тестировщика (без булшита)

> Прямой эфир / мастер-класс. Позиционирование: не «AI заменит тестировщиков», а «AI — бесплатный младший коллега, если знать как его подключить».
>
> **Контекст для новой ИИ-сессии:** [[AI master class - контекст для ИИ]] — указать на этот файл в начале сессии, ИИ сразу знает цель и что уже исследовано.

## Структура (75–90 мин)

1. **Интро (5)** — мой стек: 90% терминал, DeepSeek в Claude Code, Gemini через свой туннель. Почему без булшита
2. **Инструменты под задачи (15)** — PDF / Excel / доки / код
3. **Скиллы (10)** — что прокачивать, что AI умеет и не умеет для тестера
4. **Модели (5)** — классы, контекст, reasoning vs fast
5. **КОРОНА: бесплатный Claude-like из РФ (25)** — 4 уровня доступа
6. **Ограничения и приватность (5)**
7. **Демка + Q&A (10)**

---

## Инструменты под задачи

### PDF
- **Gemini в AI Studio** (aistudio.google.com) — контекст 1–2M, PDF целиком, бесплатный фритир
- **NotebookLM** (notebooklm.google.com) — RAG по пачке файлов, вопросы по докам, авто-подкаст
- **Docling** (github.com/DS4SD/docling) / **Marker** (github.com/datalab-to/marker) — PDF → Markdown, дальше любая модель
- Приватно: **AnythingLLM** (anythingllm.com) + Ollama локально — доки не уходят наружу

### Excel / таблицы
- xlsx в чат не тащить — конвертить в CSV / Markdown
- Gemini понимает таблицы лучше всех
- Кейсы: тест-данные, матрицы покрытия, отчёты по прогонам
- SQL-генерация по таблице → прогнать в DBeaver (проверка обязательна)

### Документация / спеки
- Swagger/OpenAPI закинуть в AI Studio → вопросы по эндпоинтам
- Терминал: `cat spec.md | llm "составь тест-кейсы"` (llm.datasette.io)
- Claude Code: `/init` в репозитории → AI в контексте всего кода

### Код
- **Claude Code** — агент в терминале, мой основной инструмент
- **Gemini CLI** (github.com/google-gemini/gemini-cli) — бесплатный терминальный агент
- **Cline** (cline.bot) / **Roo Code** (roocode.com) — в VS Code, любой API
- **Trae** (trae.ai) — бесплатный IDE от ByteDance, Claude внутри
- **Aider** (aider.chat) / **OpenCode** (opencode.ai) — парное программирование в терминале
- **Copilot Free** — 2000 автодополнений + 50 чатов/мес, работает из РФ

---

## Поиск в интернете и генерация картинок

### ИИ умеет гуглить — два пути
- **Встроенный поиск в чатах:** DeepSeek (кнопка «Поиск», без VPN), Qwen, Gemini (Google Search grounding в AI Studio, VPN)
- **Свой инструмент с поиском:** Open WebUI / Cherry Studio — поиск подмешивается в ответ модели

### SearXNG + MCP — свой поиск для AI
- **SearXNG** (searxng.github.io) — метапоиск в одном контейнере: агрегирует Bing/Yandex/DDG без API-ключей, бесплатно навсегда; из РФ — движки Bing/Yandex (Google недоступен)
- **MCP-searxng** (github.com/SecretiveShell/MCP-searxng) — мост: `claude mcp add searxng npx -y @secretiveshell/mcp-searxng` → Claude Code / Cherry Studio
- Готовые поисковые MCP без self-host: **Tavily** (фритир 1000 запр/мес, официальный MCP), **Brave Search** (2000/мес), **Firecrawl** (поиск + скрейп страниц)
- Без MCP вообще: **Gemini CLI** — встроенный Google Search grounding на фритире AI Studio

### Легче всего нубу поднять у себя: Open WebUI
- Один контейнер (версия `:ollama` — с моделью внутри, ничего больше ставить не надо):
  `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:ollama`
- Внутри из коробки: чат (Ollama / любой API-ключ), RAG по своим докам
- **Поиск:** Settings → Web Search → SearXNG или Google PSE
- **Картинки:** Settings → Images → AUTOMATIC1111 / ComfyUI / OpenAI-совместимый image API (напр. SiliconFlow)
- Без Docker, ещё проще: **Cherry Studio** (cherry-ai.com) — десктоп-приложение, DeepSeek/Ollama/Gemini, встроенный веб-поиск

Честная сложность: текст — тривиально; поиск и картинки — средняя (нужен SearXNG рядом или API-ключ).

### Картинки бесплатно из РФ
- **Fusion Brain** (fusionbrain.ai) — Kandinsky от Сбера, без VPN
- **Shedevrum / Yandex ART** — без VPN
- **SiliconFlow** (siliconflow.com) — FLUX / SDXL по API, фритир
- **Pollinations** — вообще без ключа: `image.pollinations.ai/prompt/...`
- **Bing Image Creator** (bing.com/images/create) — бесплатный DALL-E
- Локально: **Draw Things** (Mac) / **Fooocus** (Win)

---

## Скиллы

1. **Структура промпта:** роль → контекст → задача → формат → примеры (few-shot)
2. **Итерация вместо идеального промпта** — диалог сильнее одной формулировки
3. **Верификация — главный скилл тестера:** ответ AI = гипотеза. Как с нашим API: есть v1 (ответ модели) и эталон (дока/логика) — сравнивай
4. **Reasoning для анализа** (R1, Gemini Thinking), **fast для рутины** (V3, Flash, Lite)

Что AI умеет для тестера:
- тест-кейсы из спеки / Swagger
- причёсывание баг-репортов (ОР/ФР, шаги)
- SQL, regex, XPath/CSS-селекторы
- разбор стектрейсов и логов
- тест-данные, Gherkin

---

## Модели — что реально знать

- Флагманы (Claude, GPT) из РФ напрямую недоступны — и не нужны для 90% задач
- Рабочие лошадки: **DeepSeek, Qwen, GLM, Kimi**
- Reasoning vs Fast: R1 / QwQ / Gemini Thinking — думают; V3 / Flash / Lite — быстрые
- Контекст: 128K стандарт → Gemini 1–2M для доков

---

## КОРОНА: бесплатный Claude-like из РФ — 4 уровня

### Уровень 0 — без API вообще
- deepseek.com — чат, reasoning, без VPN
- chat.qwen.ai — без VPN
- GigaChat по SberID — без VPN
- Trae — Claude внутри, бесплатно
- Ollama (ollama.com) — локально, приватно, бесплатно навсегда

### Уровень 1 — бесплатные API (нужен только аккаунт)
| Провайдер | Что даёт | VPN |
|---|---|---|
| Google AI Studio (aistudio.google.com) | Gemini Flash — щедрый фритир, API-ключ | да (мой туннель) |
| GitHub Models + Copilot Free (github.com/marketplace/models) | GPT-4o-mini, Llama, Phi… | нет |
| NVIDIA NIM (build.nvidia.com) | DeepSeek-R1, Llama, Qwen — 40 запр/мин | нет |
| Cloudflare Workers AI (developers.cloudflare.com/workers-ai) | 10K нейронов/день | нет |
| OpenRouter :free (openrouter.ai/models?max_price=0) | 50 запр/день (1000 при $10 на счёте) | нет |
| Groq (groq.com) / Cerebras (inference.cerebras.ai) | быстрый Llama-инференс | да |

### Уровень 2 — копеечные API (мой стек)
- **DeepSeek API** (platform.deepseek.com) — ~$0.3/1M токенов, off-peak −50% (V3) / −75% (R1). $5 = месяц активной работы. Пополнение: зарубежная карта / посредники
- **OpenRouter** — один ключ на все модели
- GigaChat API (developers.sber.ru/gigachat) — физлицам бесплатно по SberID
- YandexGPT (yandex.cloud) — триал/квоты, без VPN

### Уровень 3 — Claude-like в терминале
- **Claude Code + claude-code-router** (github.com/musistudio/claude-code-router) / **cc-switch** (github.com/farion1231/cc-switch) → DeepSeek / GLM / Kimi. Это я прямо сейчас
- **Gemini CLI** на фритире AI Studio — через мой launchd-туннель (стабильно, переживает смену Wi-Fi)
- **llm** (llm.datasette.io) — AI в пайпах: `cat bug.log | llm "найди причину"`
- **aichat** (github.com/sigoden/aichat) — универсальный терминальный чат

---

## No bullshit

- Галлюцинируют все — проверять всегда
- **Приватность:** рабочие доки компании ≠ публичные облака (NDA). Конфиденциальное — только Ollama локально
- AI не заменит тестера — заменит рутину. Суждение и ответственность — твои
- Reasoning не нужен везде — на рутине жжёт токены и время

---

## Демка

1. `llm`: лог → баг-репорт за 10 секунд
2. Claude Code + DeepSeek: живой запрос к нашему API → тест-кейсы
3. AI Studio: Swagger → вопросы по эндпоинтам
