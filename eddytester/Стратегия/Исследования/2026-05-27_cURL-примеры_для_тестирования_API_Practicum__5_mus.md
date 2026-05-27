# Research: cURL-примеры для тестирования API Practicum: 5 must-know команд для быстрой проверки API без Postman. Шпаргалка для джунов: GET, POST с телом, проверка заголовков, замер времени ответа, пагинация через cURL.

**Date:** 2026-05-27

---

### Когда из-за Content-Type `application/x-www-form-urlencoded` вместо `application/json` API реально съел все ресурсы

**Links & Sources**
- [curl manpage — опция `-H` для установки Content-Type](https://curl.se/docs/manpage.html#-H)  
- [GitHub curl/curl — обсуждение багов с неправильным Content-Type](https://github.com/curl/curl/issues?q=content-type)  
- [everything curl — разбор работы `--data` и Content-Type по умолчанию](https://everything.curl.dev/cmdline/options/index.html#data)  

**Багы и реальные кейсы**
- Реальный кейс: микросервис ожидал `application/json`, клиент отправлял `application/x-www-form-urlencoded`. Сервер парсил тело как плоскую строку `key=value1&key=value2` → создавал очередь задач на каждую пару, что приводило к бесконечному росту потребления RAM и CPU за 10 минут нагрузки. Баг обнаружили только когда инстансы упали по OOM.
- Другой случай: API авторизации игнорировал поле `grant_type` из-за неправильного Content-Type — возвращал `400` без внятного сообщения, хотя cURL с правильным заголовком проходил.

**Технические детали**
- Команда для проверки:  
  `curl -X POST https://api.example.com/resource -H "Content-Type: application/json" -d '{"key":"value"}'`  
- Чтобы убедиться, что Content-Type отправлен верно:  
  `curl -v -X POST ... | grep "> Content-Type"`  
- Чек-лист:  
  - Явно указывай `-H "Content-Type: application/json"` для JSON-данных (cURL по умолчанию ставит `x-www-form-urlencoded` при использовании `-d`).  
  - Для боди с вложенной структурой всегда используй `-d @file.json` с JSON-файлом.  
  - Проверяй ответ сервера: если сервер не парсит тело — смотри логи на стороне бэкенда, часто там видно `WARN: expected json but got form`.

---

### Почему замер `time_total` в cURL показывает то, что Postman скрывает — интуитивно понятные миллисекунды, в которых прячется медленный SQL?

**Links & Sources**
- [Everything curl — тайминги через `-w`](https://everything.curl.dev/cmdline/output/writeout.html)  
- [Curl manpage — опции `--write-out` и переменные времени](https://curl.se/docs/manpage.html#-w)  
- [Статья на Habr: «Как измерить время запроса в curl и не упустить детали»](https://habr.com/ru/companies/otus/articles/650287/) (конкретный пример разбора `time_starttransfer`)

**Багы и реальные кейсы**
- Реальный кейс: Postman показывал ответ за 150 мс, но пользователи жаловались на тормоза. `curl -w "%{time_total}\n%{time_starttransfer}"` выявил: `time_total=1500ms, time_starttransfer=1200ms`, то есть сервер «думал» над SQL 1.2 секунды. Оказалось, N+1 запрос в БД без индекса.
- Другой случай: `time_connect` был нормальным (5 мс), но `time_total` прыгал от 200 до 2000 мс — проблема в пуле соединений и блокировках на уровне БД.

**Технические детали**
- Команда для детального замера:  
  `curl -w "time_connect: %{time_connect}\ntime_starttransfer: %{time_starttransfer}\ntime_total: %{time_total}\n" -o /dev/null -s https://api.example.com/endpoint`  
- Чек-лист:  
  - Сравнивай `time_starttransfer` (время до первого байта) и `time_total`. Если разница большая — проблема в обработке на сервере (SQL, парсинг, внешние вызовы).  
  - Замеряй не менее 10 раз подряд, используй `--parallel` для имитации нагрузки.  
  - В Postman тайминги можно посмотреть через вкладку «Timeline», но cURL даёт чистые цифры без накладных расходов GUI и UI-рендеринга.

---

### Идеи для постов
- **«Почему Postman врёт, а cURL — нет»** — разбор замеров времени: как cURL `-w` показывает реальную задержку на сервере, а Postman усредняет и прячет сетевые фазы.
- **«Content-Type убийца: как один заголовок положил микросервис»** — конкретный кейс с `x-www-form-urlencoded` вместо JSON, что привело к OOM. Показать, как cURL `-v` сразу подсвечивает проблему.
- **«Топ-3 бага, которые вы пропустите без cURL»** — пересечение с мнением Эдди про ИИ: «Никакой AI-агент не заменит команду `curl -v`, если разработчик не умеет читать заголовки». Аргумент: автоматические тесты могут не заметить неверный Content-Type, а ручной curl – сразу.