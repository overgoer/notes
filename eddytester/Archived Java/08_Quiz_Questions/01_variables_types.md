# 🧪 Викторина: Переменные, типы, синтаксис

**Тема:** Базовые типы, переменные, объявление
**Дата добавления:** 28 апреля 2026
**Источник:** Хорстманн гл.1-2, Metanit, CodingBat

---

## Вопросы с вариантами

### 1. Какой тип данных выберешь для хранения `true`/`false`?
- [ ] `boolean`
- [ ] `bool`
- [ ] `Boolean` (класс-обёртка)
- [ ] `int`

<details>
<summary>✅ Ответ</summary>
**boolean**

`bool` — нет такого в Java. `Boolean` — это класс-обёртка (для коллекций, дженериков), для простой переменной — `boolean`.
</details>

📖 **Почитать:** Metanit — [Типы данных](https://metanit.com/java/tutorial/2.2.php)

---

### 2. Что выведет код?
```java
int a = 5 / 2;
System.out.println(a);
```
- [ ] 2.5
- [ ] 2
- [ ] 2.0
- [ ] Ошибка компиляции

<details>
<summary>✅ Ответ</summary>
**2**

Деление двух целых чисел даёт целый результат с отбрасыванием дробной части (не округление). `5 / 2 = 2`.
</details>

📖 **Почитать:** Metanit — [Арифметические операции](https://metanit.com/java/tutorial/2.9.php)

---

### 3. Какая из переменных объявлена **НЕВЕРНО**?
- [ ] `int num = 10;`
- [ ] `double price = 5.99;`
- [ ] `float pi = 3.14;`
- [ ] `char letter = 'A';`

<details>
<summary>✅ Ответ</summary>
**`float pi = 3.14;`**

В Java дробные литералы по умолчанию — `double`. Для `float` нужно суффикс `f`: `float pi = 3.14f;`
</details>

📖 **Почитать:** Metanit — [Литералы](https://metanit.com/java/tutorial/2.3.php)

---

### 4. Что выведет код?
```java
String s = null;
System.out.println(s.length());
```
- [ ] 0
- [ ] null
- [ ] Ошибка NullPointerException
- [ ] Зависит от версии Java

<details>
<summary>✅ Ответ</summary>
**Ошибка NullPointerException**

`null` означает отсутствие объекта. Вызов метода на `null` — NPE.
</details>

📖 **Почитать:** Baeldung — [NullPointerException](https://www.baeldung.com/java-14-nullpointerexception)

---

## Короткие задачи (написать код)

### 5. Объяви две переменные:
- `String name` со значением `"Эд"`
- `int age` со значением `28`

и выведи на экран строку: `"Меня зовут Эд, мне 28 лет"`.

<details>
<summary>✅ Решение</summary>

```java
String name = "Эд";
int age = 28;
System.out.println("Меня зовут " + name + ", мне " + age + " лет");
```
</details>

📖 **Почитать:** Baeldung — [Strings in Java](https://www.baeldung.com/java-string)

---

### 6. Поменяй значения двух переменных местами (без третьей переменной).
```java
int a = 5;
int b = 10;
// твой код — a должно стать 10, b должно стать 5
```

<details>
<summary>✅ Решение</summary>

```java
a = a + b; // a = 15
b = a - b; // b = 5
a = a - b; // a = 10
```
Работает не для всех типов, но для `int` — ок.
</details>

📖 **Почитать:** GeeksforGeeks — [Swap without temp](https://www.geeksforgeeks.org/swap-two-numbers-without-using-temporary-variable/)

---

## 🔄 Повторение (появляются через неделю)
_Сюда переносим вопросы из этой темы, если ответил неправильно_

### ❌ (дата)
_Сюда копируем неудачные вопросы для повторения_
