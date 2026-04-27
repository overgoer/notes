/*
LeetCode #344: Reverse String

Задача: Дан массив символов (char[]), переверни его на месте (in-place).
Используй StringBuilder как инструмент для понимания разницы.

Пример:
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]

Решение 1 (StringBuilder): Time O(n), Space O(n)
Решение 2 (Two Pointers): Time O(n), Space O(1)
*/

public class Task02_StringBuilder {
    // Решение 1: StringBuilder (для понимания, не in-place!)
    public void reverseStringSB(char[] s) {
        StringBuilder sb = new StringBuilder(new String(s));
        sb.reverse();
        // Копируем обратно в массив
        for (int i = 0; i < s.length; i++) {
            s[i] = sb.charAt(i);
        }
    }

    // Решение 2: Two Pointers (in-place, оптимально)
    public void reverseString(char[] s) {
        int left = 0;
        int right = s.length - 1;

        while (left < right) {
            // Меняем местами
            char temp = s[left];
            s[left] = s[right];
            s[right] = temp;

            left++;
            right--;
        }
    }

    // Тестовые примеры
    public static void main(String[] args) {
        Task02_StringBuilder solver = new Task02_StringBuilder();

        // Пример 1: "hello"
        char[] s1 = {'h', 'e', 'l', 'l', 'o'};
        System.out.println("До: " + java.util.Arrays.toString(s1));
        solver.reverseString(s1);
        System.out.println("После (2-указателя): " + java.util.Arrays.toString(s1));

        // Пример 2: "world"
        char[] s2 = {'w', 'o', 'r', 'l', 'd'};
        System.out.println("До: " + java.util.Arrays.toString(s2));
        solver.reverseStringSB(s2); // через StringBuilder
        System.out.println("После (StringBuilder): " + java.util.Arrays.toString(s2));

        // Пример 3: пустой массив
        char[] s3 = {};
        solver.reverseString(s3);
        System.out.println("Пустой массив: " + java.util.Arrays.toString(s3));
    }
}
