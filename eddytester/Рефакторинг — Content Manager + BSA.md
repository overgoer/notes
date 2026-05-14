# Рефакторинг: Оркестратор → Content Manager + BSA

**Статус:** Запланировано
**→ Архитектура:** [[Оркестратор — архитектура]]
**→ Доска:** [[Оркестратор Доска]]

---

## 1. Зачем

Текущий «Оркестратор» делает только контент: тема → ресерч → GA → writer → email. Название не соответствует реальности — он не оркестрирует ничего, кроме постов.

**Новая схема:**
```
BSA (Стратег — ЧТО делать и КОГДА)
  │
  ├── Content Manager (бывший Оркестратор — контент)
  │     ├── Researcher
  │     ├── GA
  │     ├── RAW WRITER
  │     └── STYLE ADAPTER
  │
  ├── PM Agent (валидатор dev: задач)
  │     └── dev_runner (исполнитель кода)
  │
  ├── NEWS Agent
  │
  └── [будущие агенты]
```

BSA знает бизнес-цели, gaps, wishlist, статус проектов. Раз в неделю аудит → 3-5 Strategic Bets → диалог с Эдом → закрепление в Obsidian.

---

## 2. Технический план

### Phase A: Безопасное переименование (30 мин)

**Принцип:** новые файлы рядом со старыми → обновить всё → удалить старые. Ни секунды простоя.

**Шаг 1 — Создать новый код рядом со старым**
- `content_manager.py` — копия `orchestrator.py` с правками:
  - `ORCHESTRATOR_DIR` → `CONTENT_DIR`
  - `LOG_FILE` → `content_manager.log`
  - Импорты: `from gateway import ...` вместо `from orchestrator_cmds import ...`
  - Лог-сообщения: `CONTENT MANAGER START/COMPLETE`
  - Тема письма: `Дайджест Редактора` вместо `Дайджест Оркестратора`
- `gateway.py` — копия `orchestrator_cmds.py` с правками:
  - Докстринг
  - Внутренние пути не меняются (директория та же)

**Шаг 2 — Обновить зависимости**
- `imap_check.py`: import `from gateway import check_mail, log`
- `pm_context.json`: `"cron": ["content_manager", ...]`
- Крон: `orchestrator.py` → `content_manager.py`
- Лог: `/root/blog-analysis/logs/orchestrator.log` → `content_manager.log`

**Шаг 3 — Переключить крон**
- Новый cron entry с `content_manager.py`
- Старый временно оставить (закомментировать)

**Шаг 4 — Удалить старые файлы**
- После успешного цикла: `rm orchestrator.py orchestrator_cmds.py`
- ⚠️ __pycache__ рассосётся сам или `rm -rf __pycache__`

### Phase B: BSA Agent (отдельно, после Phase A)

**Шаг 1 — Создать `agents/bsa/bsa_agent.py`**
- Читает: `pm_context.json`, `wishlist.json`, `pm_history.json`, git-логи репозиториев
- DeepSeek с полным контекстом → State of Business + 3-5 Strategic Bets
- Пишет в Obsidian: `eddytester/Стратегия/BSA_<дата>.md`
- Отправляет email с темой `[BSA] Стратегический аудит`

**Шаг 2 — IMAP routing для диалога**
- В `gateway.py`: команда `стратегия: ...` → маршрутизация в BSA
- BSA читает фидбек → переосмысляет → 2-3 раунда → фикс

**Шаг 3 — Крон: воскресенье 09:00 МСК**

---

## 3. Потенциальные проблемы

| Проблема | Вероятность | Последствия |
|----------|------------|-------------|
| Крон дёргает старый `orchestrator.py` во время переименования | Средняя | Ошибка в логе, цикл пропущен |
| Импорт `from orchestrator_cmds` в `content_manager.py` забыли поменять | Низкая | ImportError при запуске |
| `__pycache__` кеширует старый байткод | Средняя | Python продолжает использовать старые `.pyc` |
| Log rotation — старый лог оркестратора теряется | Низкая | Статистика за прошлые запуски остаётся в старом файле |
| `pm_agent.py` внутри `agents/orchestrator/` ссылается на `orchestrator_cmds` | Низкая | — |
| BSA диалог: Эд отвечает, но IMAP не распознаёт тему письма | Средняя | Диалог обрывается |

---

## 4. Как избегаем

| Проблема | Решение |
|----------|---------|
| Крон во время переименования | **Новые файлы до удаления старых.** Старый крон работает → новый файл просто лежит рядом. Удаляем старые только когда новый cron entry активен |
| Забытые импорты | После создания `content_manager.py` и `gateway.py` — `grep -rn "orchestrat" /root/blog-analysis/agents/ --include="*.py"` до удаления. Если остались рефы — правим |
| __pycache__ | После удаления старых файлов: `find /root/blog-analysis/agents/ -name "__pycache__" -exec rm -rf {} + 2>/dev/null` |
| Старый лог | `orchestrator.log` не удаляем — просто перестаёт расти. Новый лог `content_manager.log` начинает писаться. Данные не теряются |
| BSA диалог | В `gateway.py` routing по теме письма: `[BSA]` в subject → BSA handler. Сохраняем thread в `bsa_threads/<date>.json` |

---

## 5. Откат (соломинка)

**Сценарий:** после переименования что-то пошло не так, нужно вернуть как было.

**Условия возврата:**
- Старые файлы НЕ удалены (лежат рядом)
- Старый cron entry закомментирован, не стёрт

**Процедура отката (5 минут):**
1. `crontab -e` → раскомментировать старую строку, закомментировать новую
2. `python3 orchestrator.py --no-email` — проверить что работает
3. Удалить `content_manager.py` и `gateway.py`
4. `find . -name "__pycache__" -exec rm -rf {} +`
5. Готово — система вернулась в исходное состояние

**Потери при откате:** ноль. Файлы не удаляются до подтверждения работоспособности. Единственное — тема письма обратно станет «Дайджест Оркестратора».

**Страховка:** перед началом — `cp orchestrator.py orchestrator.py.bak` для каждого файла.

---

## 6. Чеклист перед стартом

- [ ] Подключиться к серверу (доступ через sshpass, Bitwarden)
- [ ] Прочитать `orchestrator.py` — убедиться что понимаем все 708 строк
- [ ] Прочитать `orchestrator_cmds.py` — все импорты и роутинг
- [ ] Создать `content_manager.py` рядом с `orchestrator.py`
- [ ] Создать `gateway.py` рядом с `orchestrator_cmds.py`
- [ ] Обновить `imap_check.py`
- [ ] Обновить `pm_context.json`
- [ ] Обновить crontab
- [ ] `python3 -m py_compile content_manager.py gateway.py` — синтаксис
- [ ] `python3 content_manager.py --no-email` — тестовый прогон
- [ ] Обновить крон: новый entry активен
- [ ] Удалить старые файлы + __pycache__
- [ ] Финальный `grep -rn "orchestrat"` — чистый код
- [ ] Обновить документы в Obsidian
- [ ] Пушнуть изменения в Git (macOS vault)

---

> Связанные: [[Оркестратор — архитектура]], [[Оркестратор Доска]]
> Автор: Claude (14.05.2026)
