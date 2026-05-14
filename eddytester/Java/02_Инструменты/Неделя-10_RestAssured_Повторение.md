# Неделя 10: RestAssured — повторение с фокусом на собесе

> Ты это знаешь по работе. Цель — быстро освежить и усилить слабые места.

**Цель:** Пагинация, таймауты, параллельные запросы — то что спрашивают на собесах

## Ежедневная рутина

| День | Практика | Теория | Закрепление |
|------|----------|--------|-------------|
| Пн | CodingBat | RestAssured: given/when/then — быстрый повтор | написать GET + POST тест |
| Вт | CodingBat | пагинация: page/size, chunking | тест на 10 000 элементов (кейс с Яндекса) |
| Ср | CodingBat | таймауты: connect, socket, slf4j | настройка timeout в RestAssured |
| Чт | CodingBat | параллельные запросы (ExecutorService) | 5 потоков, проверить общую сумму |
| Пт | CodingBat | выделение @StressTest в CI | отдельный runner с большим таймаутом |
| Сб | CodingBat + повтор | mock-вопросы | письменно |
| Вс | **Отдых** | — | — |

## Контрольная точка

- [ ] Написал тест с пагинацией и параллельными запросами
- [ ] Настроил connectTimeout и socketTimeout
- [ ] Могу объяснить, как не сжечь CI бюджет

## Ключевые вопросы

1. Как настроить таймауты в RestAssured?
2. Как тестировать API с 10 000 элементов без таймаута?
3. Что будет, если запустить 50 параллельных тестов в CI?
4. Как пометить нагрузочный тест, чтобы он не выполнялся на каждый коммит?
5. Чем отличается connectTimeout от socketTimeout?

## 📱 Допы на почитать (в метро)

| Тема | Ссылка |
|------|--------|
| RestAssured Guide | [Baeldung: RestAssured](https://www.baeldung.com/rest-assured-tutorial) |
| RestAssured + пагинация | [Baeldung: RestAssured with Pagination](https://www.baeldung.com/rest-assured-pagination) |
| Настройка таймаутов | [GitHub: RestAssured Config](https://github.com/rest-assured/rest-assured/wiki/Usage) |
| Параллельные тесты в CI | [Baeldung: Parallel Tests](https://www.baeldung.com/java-parallel-tests) |
