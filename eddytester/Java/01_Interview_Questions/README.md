# 📋 Вопросы для интервью

**Назначение:** Хранение вопросов и ответов из реальных собеседований на позицию Senior QA (Java).

**Структура:**
- Файлы по темам: `==_vs_equals.md`, `hashCode_contract.md`, `collections_interview.md`
- Каждый файл содержит:
  1. Вопрос (как задают на интервью)
  2. Ожидаемый ответ (структурированный)
  3. Пример кода (если нужно)
  4. Частые ошибки кандидатов
  5. Оценка (как оценивают интервьюеры)

**Источники:**
- Сливы с Хабра (Яндекс, Авито, Т-Банк 2024-2025)
- Telegram-каналы (@qa_interviews, @java_interviews)
- Личный опыт

---

## 🗂️ Список тем (приоритет)

1. **Java Core**
   - `==` vs `equals()`
   - `hashCode()` и контракт
   - String immutability, StringBuilder vs StringBuffer
   - Исключения (checked/unchecked)
   - Дженерики, type erasure, wildcards

2. **Коллекции**
   - List vs Set vs Map
   - HashMap internals (хеширование, коллизии)
   - ConcurrentHashMap vs synchronizedMap
   - Fail-fast vs fail-safe итераторы

3. **Многопоточность**
   - Thread vs Runnable
   - `synchronized`, `volatile`
   - Race condition, deadlock, livelock
   - ExecutorService, ForkJoinPool

4. **Тестирование (QA специфика)**
   - JUnit 5 annotations
   - Mockito, PowerMock
   - TestContainers
   - REST Assured, Selenide

5. **Системный дизайн для QA**
   - Пирамида тестов
   - CI/CD для тестов
   - Мониторинг и логирование тестов

---

## 📝 Шаблон файла

```markdown
# [Название темы]

## Вопрос
> Как задают на интервью

## Ожидаемый ответ
1. Первый пункт
2. Второй пункт
3. Пример кода (если нужно)

## Код
```java
// пример
```

## Частые ошибки кандидатов
- ...

## Оценка
- **Junior:** знает базовое определение
- **Middle:** может объяснить нюансы
- **Senior:** приводит примеры из production, знает альтернативы

## Ссылки
- [Документация](...)
- [Статья на Хабре](...)
```

---

## 🚀 Начало работы

1. Создай файл для новой темы: `topic_name.md`
2. Заполни по шаблону
3. Добавь в этот README ссылку

**Первые файлы к созданию:**
- `==_vs_equals.md`
- `hashCode_contract.md`
- `string_immutability.md`

---

**Обновлено:** 22 марта 2026