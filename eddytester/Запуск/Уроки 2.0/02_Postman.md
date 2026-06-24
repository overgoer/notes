# 🛠️ 2. Postman и первый запрос

<div align="center">
<div align="left">

20 минут.<br>Установка, коллекция, авторизация, первый запрос, очистка базы.

</div>
</div>

---

# 🎯 Сегодня

<br>

<div align="center">
<div align="left">

**1. Скачать** — Postman с официального сайта<br>
**2. Импортировать** — коллекцию запросов<br>
**3. Авторизоваться** — API-ключ в X-Fix-Bug<br>
**4. Запрос** — POST /users, первый Send<br>
**5. Очистка** — DELETE /reset, убрать за собой

</div>
</div>

<br>

<div align="center">
<div align="left">

Через 20 минут ты **своими руками** отправишь первый запрос к живому API.

Не смотреть. Не запоминать. Делать.

</div>
</div>

---

# 📥 Шаг 1: Скачать Postman

<div align="center">
<div align="left">

- [postman.com/downloads](https://www.postman.com/downloads/)
- Windows / Mac / Linux — выбирай свою ОС

</div>
</div>

<br>

<div align="center">
  <span style="font-size: 100px;">⬇️</span>
</div>

---

# 📦 Шаг 2: Импортировать коллекцию

<br>

**Коллекция** — это готовый набор запросов. Я подготовил его, чтобы тебе не нужно было набирать всё вручную.

<br>

<div align="center">
  <span style="font-size: 100px;">📦</span>
</div>

<div align="center">
<div align="left">

После импорта слева появится коллекция **V1 Candidates API**.

</div>
</div>

---
# 🪪 Что внутри коллекции

<br>

<div align="center">

_📎 Скрин: коллекция в Postman, папки GET / POST / PATCH / DELETE развёрнуты, видно запросы._

</div>

<br>

<div align="center">
<div align="left">

Каждый запрос уже настроен: URL, метод, заголовки. Тебе остаётся только нажать **Send**.

Позже ты научишься писать запросы сам. Сейчас — осмотрись.

</div>
</div>

---

# 🔑 Шаг 3: Авторизация

<div align="center">
<div align="left">

API не пускает кого попало. Нужен **API-ключ** — твой пропуск.

</div>
</div>

<br>

<div align="center">
<div align="left">

1. Найди письмо с ключом в своей почте (тема: «API Практикум — твой ключ»)
2. Скопируй ключ — длинная строка из букв и цифр
3. В Postman открой вкладку **Headers** у любого запроса
4. Найди заголовок **X-Fix-Bug** и вставь ключ в поле Value

</div>
</div>

<br>

<div align="center">
  <span style="font-size: 100px;">🔑</span>
</div>

<div align="center">
<div align="left">

Заголовок X-Fix-Bug — это как паспорт. Без него сервер ответит «401 — кто ты такой?»

</div>
</div>

---

# 🚀 Шаг 4: Первый запрос

<br>

<div align="center">
<div align="left">

Открой **POST Create User** в папке POST. Нажми синюю кнопку **Send**.

</div>
</div>

<br>

<div align="center">
  <span style="font-size: 110px;">🚀</span>
</div>

<br>

<div align="center">
<div align="left">

Сервер ответил.

Снизу появился ответ — куча букв в фигурных скобках. Это **JSON**.

Неважно что там внутри. Важно: ты только что создал пользователя в настоящей базе данных. Он существует.

</div>
</div>

---

# 📋 Тело запроса: что мы отправили

<br>

<div align="center">
<div align="left">

Вот что было в теле запроса:

</div>
</div>

```json
{
  "name": "Demo User",
  "age": 30
}
```

<br>

<div align="center">
<div align="left">

**name** — имя пользователя (текст)<br>
**age** — возраст (число)

Всё. Ты отправил серверу два поля, сервер создал пользователя и вернул ответ.

На следующих уроках ты будешь менять эти поля и смотреть что происходит.

</div>
</div>

---

# 🧹 Шаг 5: Очистка базы

<br>

<div align="center">
<div align="left">

После тестов нужно убирать за собой. Чтобы данные не копились.

</div>
</div>

<br>

<div align="center">
<div align="left">

В папке коллекции найди **DELETE Reset DB** → **Send**.

</div>
</div>

<br>

<div align="center">
  <span style="font-size: 100px;">🧹</span>
</div>

<br>

<div align="center">
<div align="left">

База очищена. Все созданные пользователи удалены.

**Важно:** очистка работает только с твоим ключом. Ты удаляешь только свои данные, не чужие.

</div>
</div>

<div align="center">
<div align="left">

Привыкай: создал → протестировал → очистил. Это цикл.

</div>
</div>

---

# 🧠 Если ты сейчас думаешь...

<br>

<div align="center">
<div align="left">

«Я ничего не понимаю что здесь происходит»

</div>
</div>

<br>

<div align="center">
<div align="left">

**Так и должно быть.** HTTP-заголовки, JSON, статус-коды — это новый язык. Никто не понимает его с первого взгляда. Я когда открыл Postman впервые, я не мог отличить где запрос а где ответ.

</div>
</div>

<br>

<div align="center">
<div align="left">

Моя задача сегодня — **не чтобы ты всё понял.** Моя задача — чтобы ты прошёл путь руками. Скачал. Импортировал. Нажал Send.

</div>
</div>

<br>

<div align="center">

**Понимание придёт на следующих уроках, шаг за шагом.**

</div>

<br>

<div align="center">
<div align="left">

А сейчас ты как человек который впервые сел за руль. Не надо понимать как работает двигатель. Просто крути руль и не врежься.

</div>
</div>

---

# ⚡ Что мы сделали

<br>

<div align="center">
<div align="left">

✅ Скачали и установили Postman
✅ Импортировали коллекцию запросов
✅ Настроили авторизацию (X-Fix-Bug)
✅ Отправили POST /users — создали пользователя
✅ Очистили базу (DELETE /reset)

</div>
</div>

<br>

<div align="center">
  <span style="font-size: 100px;">✅</span>
</div>

---

# 📤 Домашнее задание

<br>

<div align="center">
<div align="left">

1. Убедись что Postman установлен и открывается
2. Импортируй коллекцию v1 (если ещё не)
3. Создай пользователя через POST /users
4. Очисти базу через DELETE /reset
5. Пройди туториал-тест на **/glearning** (если ещё не прошёл)

</div>
</div>

<br>

<div align="center">
<div align="left">

Ничего присылать не нужно. Просто убедись что всё работает.

</div>
</div>

---

# 📌 Что дальше

<br>

<div align="center">
<div align="left">

В уроке 3 разберём **что сервер тебе ответил и почему.**

</div>
</div>

<div align="center">
<div align="left">

Ты узнаешь:
- Что такое HTTP-заголовки и как их читать
- Что означают эти цифры (200, 201, 400, 500)
- Как отличить хороший ответ от плохого
- Что такое JSON и как в нём ориентироваться

</div>
</div>

<br>

<div align="center">
<div align="left">

Загляни в доп. материалы ⬇️ и переходи когда готов.

</div>
</div>

---

# 🔄 Буллиты на слайды

<div align="center">
<div align="left">

Тот же материал, логически разделённый на слайды. Можно использовать для записи.

</div>
</div>

---

# 🎯 Сегодня

<div align="center">
  <span style="font-size: 110px;">🛠️</span>
</div>

<br>

<div align="center">
<div align="left">

К концу этого урока ты своими руками отправишь первый запрос к живому API.

</div>
</div>

<div align="center">
<div align="left">

**Скачать** — Postman с оф. сайта<br>
**Импортировать** — коллекцию запросов<br>
**Авторизоваться** — ключ в X-Fix-Bug<br>
**Запрос** — POST /users → Send<br>
**Очистка** — DELETE /reset

</div>
</div>

<div align="center">
<div align="left">

Не смотреть. Не запоминать. Делать.

</div>
</div>

---

# 📥 Скачать Postman

<div align="center">
  <span style="font-size: 110px;">⬇️</span>
</div>

<br>

<div align="center">
<div align="left">

- [postman.com/downloads](https://www.postman.com/downloads/)
- Windows / Mac / Linux
- Бесплатной версии достаточно

Установи как обычную программу.

</div>
</div>

---

# 📦 Импортировать коллекцию

<div align="center">
  <span style="font-size: 110px;">📦</span>
</div>

<br>

<div align="center">
<div align="left">

1. Скачай JSON: [Коллекция Postman v1](https://disk.yandex.com/d/ts51e5Tgh3ciYA)
2. Postman → Import → перетащи файл
3. Слева появится **V1 Candidates API**

Коллекция — готовый набор запросов. Всё уже настроено.

</div>
</div>

---

# 🔑 Авторизация

<div align="center">
  <span style="font-size: 110px;">🔑</span>
</div>

<br>

<div align="center">
<div align="left">

- API-ключ в письме на почте
- Вкладка Headers → **X-Fix-Bug: твой-ключ**

Без ключа — 401. С ключом — проход открыт.

</div>
</div>

---

# 🚀 Первый запрос

<div align="center">
  <span style="font-size: 110px;">🚀</span>
</div>

<br>

<div align="center">
<div align="left">

POST Create User → **Send**

Сервер ответил. Ты только что создал пользователя в настоящей базе данных.

</div>
</div>

---

# 🧹 Очистка базы

<div align="center">
  <span style="font-size: 110px;">🧹</span>
</div>

<br>

<div align="center">
<div align="left">

DELETE Reset DB → **Send**

База чистая. Создал → протестировал → очистил. Всегда.

</div>
</div>

---

# 🧠 Я ничего не понимаю

<div align="center">
  <span style="font-size: 110px;">🤷</span>
</div>

<br>

<div align="center">
<div align="left">

**Так и должно быть.** Это новый язык.

Моя задача сегодня — не чтобы ты всё понял. Моя задача — чтобы ты прошёл путь руками.

</div>
</div>

<div align="center">
<div align="left">

Понимание придёт шаг за шагом.

</div>
</div>

---

# Что сделали

<br>

<div align="center">
<div align="left">

✅ Установили Postman<br>
✅ Импортировали коллекцию<br>
✅ Настроили авторизацию<br>
✅ Создали пользователя (POST /users)<br>
✅ Очистили базу (DELETE /reset)<br>
</div>
</div>

---

# 📤 ДЗ

<div align="center">
  <span style="font-size: 110px;">📤</span>
</div>

<br>

<div align="center">
<div align="left">

1. Postman установлен и открывается
2. Коллекция импортирована
3. Пользователь создан
4. База очищена
5. Туториал-тест на /glearning пройден

Ничего не присылай. Просто убедись что всё работает.

</div>
</div>

---

# 📌 Урок 3 — HTTP + API

<div align="center">
  <span style="font-size: 110px;">📌</span>
</div>

<br>

<div align="center">
<div align="left">

Разберём **что сервер ответил и почему:**

</div>
</div>

<div align="center">
<div align="left">

- HTTP-заголовки (Content-Type, Cache-Control...)
- Статус-коды (200, 201, 400, 500)
- JSON и как в нём ориентироваться

</div>
</div>

<div align="center">
<div align="left">

Переходи когда готов.

</div>
</div>
