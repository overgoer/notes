# 🤖 Newman: как перестать гонять тесты руками и начать жить

Когда ты устал кликать по кнопке Run в Postman и хочешь наконец-то автоматизировать свои коллекции - знакомься, это Newman. Консольный друг тестировщика, который избавит тебя от рутины.

## 🛠 Установка (один раз и забыл)

1. Ставим Node.js v16+ (Как это сделать https://nodejs.org/en/download/package-manager)
2. `npm install -g newman`
3. Profit!

## 📋 Основные команды

### ▶️ Базовые операции

Запускать коллекции можно используя файл коллекции (экспорт )
**Простой запуск коллекции**
```bash
newman run my-collection.json
```

**Запуск с переменными окружения:**
```bash
newman run my-collection.json -e dev-env.json
```

**Запуск с URL (если коллекция опубликована):**
```bash
newman run https://www.postman.com/collections/<collection-id>
```

### ⚡️ Полезные флаги

Флаги, которые реально пригодятся в работе:

| Флаг | Описание |
|------|----------|
| `-n <число>` | Сколько раз прогнать коллекцию |
| `--delay-request <ms>` | Задержка между запросами |
| `--bail` | Остановка при первом упавшем тесте |
| `-r cli,json` | Отчеты в консоль + JSON файл |
| `--color off` | Убрать цветной вывод (для CI) |

## 🤓 Pro-tips

### 1. Добавление в CI через npm-скрипты

```json
{
  "scripts": {
    "test:api": "newman run collection.json -e env.json --bail",
    "test:prod": "newman run collection.json -e prod-env.json --bail",
    "test:all": "newman run collection1.json && newman run collection2.json"
  }
}
```

### 2. Запуск нескольких коллекций

```bash
newman run collection1.json && newman run collection2.json
```

### 3. Сохранение результатов в файл

```bash
newman run collection.json -r cli,json --reporter-json-export ./results.json
```

### 4. Полезные алиасы для терминала

```bash
# .bashrc или .zshrc
alias nrun='newman run'
alias ntest='newman run my-collection.json -e dev-env.json --bail'
alias nreport='newman run collection.json -r cli,json --reporter-json-export'
```

## ⚠️ Важные ограничения

1. **OAuth 2.0:**
   - Не поддерживается интерактивная авторизация
   - Используйте токены или Basic auth для CI

2. **Коллекции:**
   - Храните актуальные версии
   - Используйте версионирование
   - Регулярно синхронизируйте с Postman

3. **Переменные окружения:**
   - Не храните sensitive data в репозитории
   - Используйте CI/CD переменные
   - Имейте разные env файлы для разных окружений

## 🎯 Сценарии использования

1. **CI/CD пайплайны:**
   - Интеграционное тестирование
   - Проверка деплоев
   - Мониторинг критических эндпоинтов

2. **Регулярные прогоны:**
   - Smoke тесты
   - Регрессионное тестирование
   - Health чеки

3. **Мониторинг:**
   - Проверка доступности API
   - Валидация контрактов
   - Отслеживание производительности

4. **Нагрузочное тестирование:**
   - Параллельные запуски
   - Многократные прогоны
   - Симуляция нагрузки

## 💡 Полезные практики

1. **Структура проекта:**
```
/api-tests
  /collections
    - main.json
    - smoke.json
  /environments
    - dev.json
    - stage.json
    - prod.json
  /reports
  package.json
  README.md
```

2. **Именование файлов:**
   - Используйте понятные префиксы
   - Добавляйте даты для отчетов
   - Следуйте единому стилю

3. **Документация:**
   - Описывайте настройку окружения
   - Документируйте специфичные кейсы
   - Ведите changelog коллекций

## 🐛 Типичные проблемы и решения

1. **Newman не видит переменные окружения:**
   - Проверьте путь к env файлу
   - Убедитесь что файл актуален
   - Проверьте формат JSON

2. **Падают тесты в CI, но локально работают:**
   - Проверьте версию Newman
   - Сравните переменные окружения
   - Проверьте сетевые ограничения

3. **Проблемы с SSL сертификатами:**
   ```bash
   newman run collection.json --insecure
   ```

4. **Timeout на медленных запросах:**
   ```bash
   newman run collection.json --timeout-request 60000
   ```

## 📚 Полезные ресурсы

1. [Newman GitHub](https://github.com/postmanlabs/newman)
2. [Postman Learning Center](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/)
3. [Newman Reporter HTML](https://github.com/postmanlabs/newman-reporter-html)

Сохраняй, пока не началась новая спринт-планка! 😉

#postman #newman #testing #automation