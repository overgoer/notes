/*
LeetCode #1: Two Sum

Задача: Дан массив целых чисел `nums` и целое число `target`, верни индексы двух чисел,
сумма которых равна `target`.

Пример:
Input: nums = [2,7,11,15], target = 9
Output: [0,1] (nums[0] + nums[1] = 2 + 7 = 9)

Решение 1 (HashMap): Time O(n), Space O(n)
Решение 2 (Brute Force): Time O(n²), Space O(1)
*/

import java.util.*;

public class Task03_HashMap {
    // Решение 1: HashMap (оптимально)
    public int[] twoSum(int[] nums, int target) {
        // Ключ = число, значение = индекс
        Map<Integer, Integer> numToIndex = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];  // какое число нужно найти

            if (numToIndex.containsKey(complement)) {
                // нашли пару: complement + nums[i] = target
                return new int[]{numToIndex.get(complement), i};
            }

            numToIndex.put(nums[i], i); // запомним текущее число и его индекс
        }

        throw new IllegalArgumentException("No two sum solution");
    }

    // Решение 2: Brute Force (для сравнения)
    public int[] twoSumBrute(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        throw new IllegalArgumentException("No two sum solution");
    }

    // Тестовые примеры
    public static void main(String[] args) {
        Task03_HashMap solver = new Task03_HashMap();

        // Пример 1: [2,7,11,15], target=9 → [0,1]
        int[] nums1 = {2, 7, 11, 15};
        int[] result1 = solver.twoSum(nums1, 9);
        System.out.println("Пример 1: " + java.util.Arrays.toString(result1)); // [0, 1]

        // Пример 2: [3,2,4], target=6 → [1,2]
        int[] nums2 = {3, 2, 4};
        int[] result2 = solver.twoSum(nums2, 6);
        System.out.println("Пример 2: " + java.util.Arrays.toString(result2)); // [1, 2]

        // Пример 3: [3,3], target=6 → [0,1]
        int[] nums3 = {3, 3};
        int[] result3 = solver.twoSum(nums3, 6);
        System.out.println("Пример 3: " + java.util.Arrays.toString(result3)); // [0, 1]

        // Сравнение времени (для понимания, почему HashMap лучше):
        long startTime = System.nanoTime();
        solver.twoSumBrute(new int[1000], 1000); // тяжёлая версия
        long bruteTime = System.nanoTime() - startTime;

        startTime = System.nanoTime();
        solver.twoSum(new int[1000], 1000); // лёгкая версия
        long hashMapTime = System.nanoTime() - startTime;

        System.out.printf("Brute Force: %d ns\nHashMap: %d ns\n", bruteTime, hashMapTime);
    }
}
