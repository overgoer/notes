# 🔍 Как тестировать UI через Selenium Grid

## Сценарий
Ты тестируешь веб-приложение (например, Ozon / Авито), которое поддерживает 8 браузеров и 3 ОС: Windows 11, macOS Sonoma, Ubuntu.
Текущий тест-раннер на локальной машине: 1 браузер, 1 ОС → 1 тест за 2 мин → 100 тестов = 3.3 часа.

## Задача
Опиши, как ты внедришь **Selenium Grid** для параллельного запуска тестов в облаке — и как это решит проблему.

---

## ✅ Ответ: план внедрения

### 1. Что такое Selenium Grid?
- **Selenium Grid** — инструмент для распределённого запуска UI-тестов на нескольких машинах (нодах) с разными ОС и браузерами.
- Состоит из **Hub** (координатор) и **Nodes** (узлы, где выполняются тесты).
- Поддерживает облачные решения: **Sauce Labs**, **BrowserStack**, **Lambdatest**, **Selenoid**.

### 2. Как это решит проблему 3.3 часа?

| Подход | Конфигурация | Время на 100 тестов | Плюсы / Минусы |
|--------|--------------|---------------------|----------------|
| **Локально** | 1 браузер, 1 ОС | ~3.3 часа | Просто, но медленно. Не охватывает кроссплатформенность. |
| **Selenium Grid (локальный кластер)** | Hub + 10 нод (разные браузеры/ОС) | ~20 мин | Полный контроль, но сложна настройка и обслуживание. |
| **Облако (Sauce Labs)** | `@SauceLabs` + 10 параллельных сессий | ~10 мин | Быстро, масштабируется, готовые БД браузеров, отчётность и video-записи. |

✅ **Решение:** Использовать **Sauce Labs** (или аналог) — это промышленный стандарт для российских BigTech.

### 3. Практическая реализация

#### Шаг 1: Интеграция с Selenide (упрощённый синтаксис)
```java
// В @BeforeAll
Configuration.remote = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub";
Configuration.browser = "chrome";
Configuration.browserVersion = "120.0";
Configuration.browserSize = "1920x1080";
Configuration.timeout = 10000;

// Добавляем Sauce Labs Capabilities
Configuration.browserCapabilities = new BrowserCapabilities()
    .setUsername(System.getenv("SAUCE_USERNAME"))
    .setAccessKey(System.getenv("SAUCE_ACCESS_KEY"))
    .setBuild("Ozon-Regression-2026-04")
    .enableVNC();
```

#### Шаг 2: Параметризованные тесты (для кросс-браузерного запуска)
```java
@ParameterizedTest
@ValueSource(strings = {"chrome", "firefox", "safari"})
void checkoutFlow_worksOnAllBrowsers(String browser) {
    Configuration.browser = browser;
    open("https://ozon.ru");
    // ... шаги чекаута ...
    $("#order-success").should(exist);
}
```

#### Шаг 3: Интеграция с CI (GitHub Actions)
```yaml
# .github/workflows/selenium-grid.yml
- name: Run Selenium Tests
  run: mvn test -Dtest=SeleniumTests
  env:
    SAUCE_USERNAME: ${{ secrets.SAUCE_USERNAME }}
    SAUCE_ACCESS_KEY: ${{ secrets.SAUCE_ACCESS_KEY }}
```

### 4. Как измерить успех внедрения?

| Метрика | Цель | Как измерить |
|---------|------|--------------|
| **Скорость тестов** | ↓ на 90% | `before`: 200 мин → `after`: 20 мин |
| **Покрытие** | 8 браузеров × 3 ОС = 24 конфигурации | `sauce:platforms: ["Windows 11", "macOS Sonoma"]` |
| **Flakiness** | ↓ на 80% | Доля падающих тестов: `flaky-rate = (flaky-tests / total-tests) × 100%` |
| **Стоимость владения** | < 2 часа/неделю | Время настройки/обслуживания Grid — в репорте `Selenium-DevOps-Report.md` |

### 5. Что делать, если Grid «упал» в CI?
- **Резервный план:** добавить `@Tag("smoke")` — smoke-тесты в любом случае запустятся локально без Grid.
- **Вебхук-уведомление:** при ошибках Grid — писать в Slack-канал `#qa-alerts`.
- **Автоматический retry:** `@Test` с `@Retry(times = 2)` — чтобы исключить временные сетевые ошибки.

---

## 📌 Вопрос на интервью
> «Почему ты выбрал Sauce Labs, а не локальный Grid?»

**Ответ:** «Потому что в BigTech критичны скорость и надёжность тестов. Локальный Grid — это инфраструктурная задача: поддержка, обновление ОС/браузеров, восстановление. Sauce Labs гарантирует готовые, преднастроенные машины, video-записи, мониторинг и SLA. Я не хочу быть DevOps-инженером, я хочу писать тесты. Sauce Labs — это правильное распределение зон ответственности».

---

## 📚 Ссылки

- [Selenium Grid Docs](https://www.selenium.dev/documentation/grid/)
- [Sauce Labs + Java](https://docs.saucelabs.com/dev/java/)
- [Selenide + Sauce Labs](https://selenide.org/2020/05/12/selenide-5.13.0/)
- [GitHub Actions + Selenium](https://github.com/marketplace/actions/selenium-grid-action)

---

**Следующий кейс:** [`How_To_Test_Microservice_Communication.md`](How_To_Test_Microservice_Communication.md)