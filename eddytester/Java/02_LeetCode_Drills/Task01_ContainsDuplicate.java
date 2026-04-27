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
    // Решение 1: HashSet
    public boolean containsDuplicateSet(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) {
                return true;
            }
            seen.add(num);
        }
        return false;
    }

    // Решение 2: Сортировка
    public boolean containsDuplicateSort(int[] nums) {
        Arrays.sort(nums);
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) {
                return true;
            }
        }
        return false;
    }

    // Тестовые примеры (мысленные)
    public static void main(String[] args) {
        Task01_ContainsDuplicate solver = new Task01_ContainsDuplicate();

        // Пример 1: есть дубликат
        int[] nums1 = {1, 2, 3, 1};
        System.out.println("Пример 1: " + solver.containsDuplicateSet(nums1)); // true

        // Пример 2: нет дубликата
        int[] nums2 = {1, 2, 3, 4};
        System.out.println("Пример 2: " + solver.containsDuplicateSet(nums2)); // false

        // Пример 3: пустой массив
        int[] nums3 = {};
        System.out.println("Пример 3: " + solver.containsDuplicateSet(nums3)); // false

        // Пример 4: один элемент
        int[] nums4 = {5};
        System.out.println("Пример 4: " + solver.containsDuplicateSet(nums4)); // false
    }
}