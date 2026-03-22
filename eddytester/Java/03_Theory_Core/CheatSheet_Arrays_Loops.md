# 📚 Шпаргалка: Массивы и Циклы в Java

**Создано:** 21 марта 2026  
**Для:** Ed (Senior QA Prep)  
**Важно:** Выучить наизусть!

---

## 🔄 Цикл `for` — 2 варианта

### Вариант 1: for-each (перебор элементов)

```java
// Для массива строк
String[] names = {"Alice", "Bob", "Charlie"};

for (String name : names) {
    System.out.println(name);
}
```

**Синтаксис:**
```java
for (Тип переменная : массив) {
    // тело цикла
}
```

**Когда использовать:**
- ✅ Нужно перебрать все элементы по порядку
- ✅ Не нужен индекс элемента
- ✅ Не нужно менять элементы массива

---

### Вариант 2: классический for (по индексу)

```java
int[] numbers = {1, 2, 3, 4, 5};

for (int i = 0; i < numbers.length; i++) {
    System.out.println("Index " + i + ": " + numbers[i]);
}
```

**Синтаксис:**
```java
for (инициализация; условие; инкремент) {
    // тело цикла
}
```

**Когда использовать:**
- ✅ Нужен индекс элемента
- ✅ Нужно менять элементы массива
- ✅ Нужно пропускать элементы (шаг > 1)

---

## 📦 Массивы — 3 способа объявления

### Способ 1: Объявление + выделение памяти

```java
int[] myArray = new int[5];  // массив из 5 элементов (заполнен 0)
myArray[0] = 10;             // присвоить значение
myArray[1] = 20;
```

### Способ 2: Объявление + инициализация

```java
int[] myArray = {1, 2, 3, 4, 5};  // сразу со значениями
```

### Способ 3: Раздельное объявление

```java
int[] myArray;           // объявление
myArray = new int[5];    // выделение памяти
myArray = {1, 2, 3, 4, 5};  // ❌ ТАК НЕЛЬЗЯ! Только при объявлении!
```

**Правильно:**
```java
int[] myArray;
myArray = new int[]{1, 2, 3, 4, 5};  // ✅
```

---

## 🔑 Ключевые моменты

### Длина массива
```java
int[] arr = {1, 2, 3};
int length = arr.length;  // 3 (поле, не метод!)
```

### Доступ к элементу
```java
int[] arr = {10, 20, 30};
int first = arr[0];    // 10
int last = arr[2];     // 30
arr[1] = 99;           // изменить элемент
```

### Ошибки (запомни!)
```java
// ❌ Int не существует!
Int[] arr = new Int[5];

// ✅ Правильно:
int[] arr = new int[5];           // примитивы
Integer[] arr = new Integer[5];   // обёртки
```

---

## 📊 Примитивы vs Обёртки

| Примитив | Обёртка | Значение по умолчанию |
|----------|---------|----------------------|
| `int` | `Integer` | `0` |
| `double` | `Double` | `0.0` |
| `boolean` | `Boolean` | `false` |
| `char` | `Character` | `'\u0000'` |
| `long` | `Long` | `0L` |
| `float` | `Float` | `0.0f` |
| `byte` | `Byte` | `0` |
| `short` | `Short` | `0` |

---

## 🎯 Примеры для практики

### Пример 1: Сумма элементов массива

```java
int[] numbers = {1, 2, 3, 4, 5};
int sum = 0;

// for-each
for (int num : numbers) {
    sum += num;
}

// классический for
for (int i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
```

### Пример 2: Поиск максимума

```java
int[] numbers = {5, 2, 9, 1, 7};
int max = numbers[0];

for (int i = 1; i < numbers.length; i++) {
    if (numbers[i] > max) {
        max = numbers[i];
    }
}
```

### Пример 3: Разворот массива

```java
int[] arr = {1, 2, 3, 4, 5};

for (int i = 0; i < arr.length / 2; i++) {
    int temp = arr[i];
    arr[i] = arr[arr.length - 1 - i];
    arr[arr.length - 1 - i] = temp;
}
```

---

## 📝 Для запоминания

**Выучи наизусть (прямо сейчас!):**

```java
// 1. for-each
for (int num : numbers) { }

// 2. классический for
for (int i = 0; i < arr.length; i++) { }

// 3. массив (3 способа)
int[] arr1 = new int[5];
int[] arr2 = {1, 2, 3, 4, 5};
int[] arr3 = new int[]{1, 2, 3};
```

**Повтори 5 раз без подглядывания!**

---

## 🔗 Ссылки

- [Metanit: Массивы в Java](https://metanit.com/java/tutorial/2.6.php)
- [Metanit: Цикл for](https://metanit.com/java/tutorial/2.7.php)
- Хорстманн, том 1, глава 1.3-1.4

---

**Сохраните в `03_Theory_Core/` для быстрого доступа!**
