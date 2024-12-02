# 🤖 Newman: как перестать гонять тесты в Postman руками

Newman - Консольный друг тестировщика, который избавит тебя от рутины.

## 🛠 Установка (один раз и забыл)

1. Ставим Node.js v16+ (Как это сделать https://nodejs.org/en/download/package-manager)
2. `npm install -g newman`
3. Готово, можно готовить коллекцию для прогона

В Newman есть 2 режима:
- запуск коллекции из локальных файлов
- запуск коллекции, опубликованной онлайн

**Запуск коллекции локально:**
- Сперва нужно сохранить коллекцию в формате JSON.
- Важно знать точный путь до коллекции и переменных, или работать в паке, в которой лежат эти файлы.
**Запуск коллекции без переменных**
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
**Запуск онлайн-коллекции с переменными окружения**

**Базовый вариант:**
```bash
newman run "https://api.postman.com/collections/<collection-id>" -e dev-env.json
```
Коллекция может быть приватной, в этом случае понадобится указать API-ключ:
```bash
newman run "https://api.postman.com/collections/<collection-id>" \
  -e dev-env.json \
  --apiKey <your-postman-api-key>
```

### ⚡️ Полезные флаги
Флаги, которые реально пригодятся в работе:

| Флаг                   | Описание                                              |
| ---------------------- | ----------------------------------------------------- |
| `-n <число>`           | Сколько раз прогнать коллекцию (по дефолту 1)         |
| `--delay-request <ms>` | Задержка между запросами (по дефолту 0)               |
| `--bail`               | Остановка при первом упавшем тесте (по дефолту false) |
| `-r cli,json`          | Отчеты в консоль + JSON файл (по дефолту только cli)  |
| `--color off`          | Убрать цветной вывод (по дефолту on)                  |

### Где найти collection-id:
1. Откройте коллекцию в Postman
2. Нажмите на ⓘ (информация) справа
3. Скопируйте Collection ID

### 🤓Полезно знать:

1. **Запуск с глобальными переменными:**
```bash
newman run "https://api.postman.com/collections/<collection-id>" \
  -e dev-env.json \
  -g globals.json
```

2. **Запуск с несколькими окружениями:**
```bash
newman run "https://api.postman.com/collections/<collection-id>" \
  -e dev-env.json \
  -e common-env.json
```

3. **Переопределение переменных:**
```bash
newman run "https://api.postman.com/collections/<collection-id>" \
  -e dev-env.json \
  --env-var "API_KEY=newkey" \
  --env-var "BASE_URL=http://newurl"
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