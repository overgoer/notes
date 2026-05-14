# Неделя 11: JUnit 5 + Mockito — для собеса (не углублённо)

**Цель:** Уверенно отвечать на вопросы про моки, стабы, spy

## Ежедневная рутина

| День | Практика | Теория | Закрепление |
|------|----------|--------|-------------|
| Пн | CodingBat | JUnit 5: @Test, @BeforeEach, Assertions | написать 5 простых юнит-тестов |
| Вт | CodingBat | @Mock, @InjectMocks, when/thenReturn | мок сервиса в тесте контроллера |
| Ср | CodingBat | verify(), times(), argument captor | проверить, что метод вызван 1 раз |
| Чт | CodingBat | @Spy vs @Mock, частичное мокание | когда spy, а когда mock |
| Пт | CodingBat | тесты с исключениями, параметризация | @ParameterizedTest + CsvSource |
| Сб | CodingBat + повтор | mock-вопросы | письменно |
| Вс | **Отдых** | — | — |

## Контрольная точка

- [ ] Написал тест с @Mock + @InjectMocks
- [ ] Использовал verify() для проверки вызова
- [ ] Понимаю разницу @Mock, @Spy, @InjectMocks

## Ключевые вопросы

1. Чем mock отличается от spy?
2. Как проверить, что метод был вызван ровно 1 раз?
3. Что такое argument captor?
4. Как протестировать метод, который бросает исключение?
5. Когда нужно использовать @InjectMocks?

## 📱 Допы на почитать (в метро)

| Тема | Ссылка |
|------|--------|
| JUnit 5 Guide | [Baeldung: JUnit 5](https://www.baeldung.com/junit-5) |
| Mockito Guide | [Baeldung: Mockito](https://www.baeldung.com/mockito-series) |
| @Mock vs @Spy | [Baeldung: Mock vs Spy](https://www.baeldung.com/mockito-spy) |
| ArgumentCaptor | [Baeldung: ArgumentCaptor](https://www.baeldung.com/mockito-argumentcaptor) |
| Parameterized Tests | [Baeldung: Parameterized Tests](https://www.baeldung.com/parameterized-tests-junit-5) |
