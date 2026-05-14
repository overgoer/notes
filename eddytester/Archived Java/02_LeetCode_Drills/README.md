# 💻 LeetCode задачи (без IDE)

**Назначение:** Хранение решений алгоритмических задач, которые нужно решать "на доске" (без IDE) для подготовки к интервью.

**Правила:**
1. **Без IDE** — пиши код в простом текстовом редакторе или на бумаге.
2. **Объясняй Big O** — для каждого решения указывай временную и пространственную сложность.
3. **Тестируй в уме** — прогони 2-3 тестовых случая мысленно.
4. **Альтернативные решения** — если есть несколько подходов, реализуй все.

**Структура файла:**
```
TaskXX_ProblemName.java
```
Пример: `Task01_ContainsDuplicate.java`

**Содержание файла:**
```java
/*
LeetCode #217: Contains Duplicate

Задача: Дан массив целых чисел, верни true если любое значение встречается хотя бы дважды.
Иначе верни false.

Пример:
Input: nums = [1,2,3,1]
Output: true

Решение 1 (HashSet): Time O(n), Space O(n)
Решение 2 (Sorting): Time O(n log n), Space O(1)
*/

import java.util.*;

public class Task01_ContainsDuplicate {
    // Решение 1
    public boolean containsDuplicateSet(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) return true;
            seen.add(num);
        }
        return false;
    }
    
    // Решение 2
    public boolean containsDuplicateSort(int[] nums) {
        Arrays.sort(nums);
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i-1]) return true;
        }
        return false;
    }
}
```

---

## 🗂️ Категории (по Neetcode.io)

1. **Arrays & Hashing**
   - Contains Duplicate
   - Two Sum
   - Group Anagrams
   - Top K Frequent Elements

2. **Two Pointers**
   - Valid Palindrome
   - 3Sum
   - Container With Most Water

3. **Sliding Window**
   - Best Time to Buy/Sell Stock
   - Longest Substring Without Repeating Characters

4. **Stack**
   - Valid Parentheses
   - Min Stack

5. **Linked List**
   - Reverse Linked List
   - Detect Cycle

6. **Trees**
   - Invert Binary Tree
   - Maximum Depth of Binary Tree

7. **Graphs**
   - Number of Islands
   - Clone Graph

---

## 📊 Трекинг прогресса

| Задача | Ссылка | Решено | Сложность | Дата | Примечания |
|--------|--------|--------|-----------|------|------------|
| Contains Duplicate | [#217](https://leetcode.com/problems/contains-duplicate/) | ✅ | Easy | 2026-03-22 | HashSet, Sorting |
| Two Sum | [#1](https://leetcode.com/problems/two-sum/) | ⬜ | Easy | | |

**Легенда:**
- ✅ — решена без IDE, объяснена сложность
- 🔄 — в процессе
- ⬜ — не начата

---

## 🎯 Практические советы

1. **Пиши на бумаге** — имитация белой доски.
2. **Говори вслух** — объясняй решение, как на интервью.
3. **Сначала brute force** — потом оптимизируй.
4. **Edge cases** — пустой массив, один элемент, большие числа.
5. **Тестируй** — хотя бы 3 примера.

---

## 🔗 Полезные ссылки

- [LeetCode Top 100 Liked](https://leetcode.com/problem-list/top-100-liked-questions/)
- [Neetcode.io](https://neetcode.io/) — структурированный путь
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

---

## 🚀 Начало работы

1. Выбери задачу из LeetCode Top 100.
2. Реши без IDE в файле `TaskXX_ProblemName.java`.
3. Добавь в таблицу прогресса.
4. Повтори через неделю — реши по памяти.

**Первые задачи:**
- `Task01_ContainsDuplicate.java`
- `Task02_TwoSum.java`
- `Task03_ValidAnagram.java`

---

**Обновлено:** 22 марта 2026