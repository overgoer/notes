# Неделя 8: CompletableFuture, Lambda, Streams + Mock #1

> ⚠️ CompletableFuture — частый вопрос на собесах: тест проходит локально, падает в CI.

**Цель:** Асинхронность через CompletableFuture, Stream API для обработки данных

## Ежедневная рутина

| День | Практика | Теория | Закрепление |
|------|----------|--------|-------------|
| Пн | LeetCode Easy | Lambda-выражения: (x) -> x * 2 | переписать анонимный класс в лямбду |
| Вт | LeetCode Easy | Stream API: filter, map, collect | обработать список строк через stream |
| Ср | LeetCode Easy | CompletableFuture: supplyAsync, thenApply | асинхронный вызов + обработка результата |
| Чт | LeetCode Easy | CompletableFuture: allOf, exception | 2 параллельных запроса и объединение |
| Пт | LeetCode Easy | race condition в CI: почему локально работает | кейс с CompletableFuture |
| Сб | **Mock #1 (45 мин)** | самопроверка | записать результат |
| Вс | **Отдых** | — | — |

## Контрольная точка

- [ ] Могу написать filter + map + collect без подсказок
- [ ] CompletableFuture: supplyAsync + thenAcceptAsync
- [ ] Mock #1 — оценка (цель ≥ 2.5/5)

## Ключевые вопросы

1. Чем intermediate отличается от terminal операции stream?
2. Что делает `.collect(Collectors.toList())`?
3. Как объединить 2 CompletableFuture?
4. Почему CompletableFuture тест проходит локально, но падает в CI?
5. Что такое ForkJoinPool.commonPool?

## 📱 Допы на почитать (в метро)

| Тема | Ссылка |
|------|--------|
| Лямбды в Java | [Baeldung: Java Lambdas](https://www.baeldung.com/java-8-lambda-expressions-tips) |
| Stream API | [Baeldung: Java Streams](https://www.baeldung.com/java-8-streams) |
| CompletableFuture | [Baeldung: CompletableFuture](https://www.baeldung.com/java-completablefuture) |
| CompletableFuture + тесты в CI | [Baeldung: Testing CompletableFuture](https://www.baeldung.com/java-testing-completablefuture) |
| Optional | [Baeldung: Java Optional](https://www.baeldung.com/java-optional) |
