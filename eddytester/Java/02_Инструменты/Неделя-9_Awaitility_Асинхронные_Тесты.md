# Неделя 9: Awaitility, async-тесты без Thread.sleep

> ⚠️ Критично для собеса. `Thread.sleep` — антипаттерн. Awaitility — стандарт в бигтехе.

**Цель:** Заменить Thread.sleep на правильные асинхронные ожидания

## Ежедневная рутина

| День | Практика | Теория | Закрепление |
|------|----------|--------|-------------|
| Пн | CodingBat | проблема Thread.sleep (почему плохо) | написать тест со sleep — понять недостатки |
| Вт | CodingBat | Awaitility: await().atMost().until() | базовый async тест с Awaitility |
| Ср | CodingBat | untilAsserted, custom conditions | несколько условий в одном await |
| Чт | CodingBat | catchUncaughtExceptions | тест с CompletableFuture + Awaitility |
| Пт | CodingBat | awaitility в CI, best practices | чек-лист async testing |
| Сб | CodingBat + повтор | mock-вопросы | письменно |
| Вс | **Отдых** | — | — |

## Контрольная точка

- [ ] Могу объяснить, почему Thread.sleep — плохо
- [ ] Написал тест с Awaitility.await().atMost().untilAsserted()
- [ ] Могу объяснить, как Awaitility ловит исключения из других потоков

## Ключевые вопросы

1. Почему Thread.sleep — антипаттерн для тестов?
2. Как Awaitility решает проблему flaky тестов?
3. Что такое untilAsserted? Чем отличается от until?
4. Как Awaitility взаимодействует с CompletableFuture?
5. Как настроить poll interval и timeout?

## 🛠 Код в репозитории

Добавь в `pom.xml`:
```xml
<dependency>
    <groupId>org.awaitility</groupId>
    <artifactId>awaitility</artifactId>
    <version>4.2.0</version>
    <scope>test</scope>
</dependency>
```

Пример:
```java
await().atMost(5, SECONDS)
    .untilAsserted(() -> assertThat(result).isEqualTo(expected));
```

## 📱 Допы на почитать (в метро)

| Тема | Ссылка |
|------|--------|
| Awaitility: гайд | [Baeldung: Awaitility Guide](https://www.baeldung.com/awaitility-testing) |
| Thread.sleep vs Awaitility | [StackOverflow: Sleep vs Awaitility](https://stackoverflow.com/questions/68687755/java-thread-sleep-vs-awaitility-await) |
| Тестирование async кода | [Baeldung: Testing Async Code](https://www.baeldung.com/java-asynchronous-testing) |
| Awaitility документация | [GitHub: Awaitility Wiki](https://github.com/awaitility/awaitility/wiki/Usage) |
