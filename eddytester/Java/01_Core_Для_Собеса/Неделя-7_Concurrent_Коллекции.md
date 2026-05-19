# Неделя 7: ConcurrentHashMap, race conditions в тестах

> ⚠️ **Топ-тема с собесований Ozon, Т-Банк.** Почему HashMap в тестах — баг.

**Цель:** Thread-safe коллекции, параллельные тесты, flaky-фиксы

## Ежедневная рутина

| День | Практика | Теория | Закрепление |
|------|----------|--------|-------------|
| Пн | CodingBat | ConcurrentHashMap vs HashMap vs synchronizedMap | сравнить производительность |
| Вт | CodingBat | Concurrent коллекции: CopyOnWriteArrayList, BlockingQueue | написать producer-consumer |
| Ср | LeetCode Easy | потокобезопасные тестовые данные | пример flaky теста и фикс |
| Чт | CodingBat | причины flaky тестов в параллельном CI | чек-лист анти-flaky |
| Пт | CodingBat | ThreadLocal, ForkJoinPool | ThreadLocal для test context |
| Сб | повтор + mock-вопросы | ответить на вопросы письменно | — |
| Вс | **Отдых** | — | — |

## Контрольная точка

- [ ] Понимаю, почему HashMap в параллельных тестах — баг
- [ ] Знаю разницу ConcurrentHashMap vs synchronizedMap
- [ ] Могу объяснить, откуда берутся flaky тесты и как чинить

## Ключевые вопросы

1. Чем ConcurrentHashMap лучше synchronizedMap?
2. Почему CopyOnWriteArrayList так называется?
3. Как BlockingQueue используется в producer-consumer?
4. Что такое flaky test? Топ-3 причины?
5. Зачем ThreadLocal в тестах?

## 📱 Допы на почитать (в метро)

| Тема | Ссылка |
|------|--------|
| ConcurrentHashMap guide | [Baeldung: ConcurrentHashMap](https://www.baeldung.com/java-concurrent-hashmap) |
| Обзор concurrent коллекций | [Baeldung: Java Concurrent Collections](https://www.baeldung.com/java-concurrent-collections) |
| Flaky tests: причины и фиксы | [Baeldung: Flaky Tests](https://www.baeldung.com/java-flaky-tests) |
| BlockingQueue + Producer-Consumer | [Baeldung: BlockingQueue](https://www.baeldung.com/java-blocking-queue) |
| Как Ozon тестирует параллельно | [Habr: Flaky tests в Ozon](https://habr.com/ru/companies/ozontech/articles/692536/) |
