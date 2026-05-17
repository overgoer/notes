# Авто-проверка длинных тире (—) во всех постах

## Проблема
В постах используются длинные тире (—, U+2014) вместо коротких дефисов (-, U+002D).
В Telegram длинные тире выгляднее чужеродно, нарушают визуальное единообразие.

## Правило
ВСЕ тексты для TG-постов используют ТОЛЬКО короткий дефис (-).
Длинные тире (—, –) запрещены.

## Скрипт проверки

Создай файл `/root/obsidian-vault/scripts/check_long_dashes.sh`:

```bash
#!/bin/bash
# Скрипт проверки Obsidian-файлов на длинные тире
# Запуск: bash check_long_dashes.sh

VAULT="/root/obsidian-vault"
EXCLUDE=".git|node_modules|.obsidian"

echo "=== Проверка длинных тире (—) ==="
echo ""

FOUND=0

# Ищем во всех .md файлах, исключая системные папки
while IFS= read -r -d '' file; do
    if grep -P '—' "$file" > /dev/null 2>&1; then
        # Показываем строки с длинными тире
        matches=$(grep -n -P '—' "$file")
        if [ -n "$matches" ]; then
            echo "❌ $file"
            echo "$matches" | while IFS= read -r line; do
                echo "   $line"
            done
            echo ""
            FOUND=$((FOUND + 1))
        fi
    fi
done < <(find "$VAULT" -name "*.md" -not -path "*/\.*" -print0)

if [ "$FOUND" -eq 0 ]; then
    echo "✅ Длинных тире не найдено. Чисто!"
else
    echo "=== Найдено файлов с длинными тире: $FOUND ==="
    echo "🔥 Замени через: sed -i 's/—/-/g' <filepath>"
fi
```

## Интеграция в конвейер

### Вариант 1: Pre-save хук (если есть git)
Добавь в `.git/hooks/pre-commit`:

```bash
#!/bin/bash
VAULT="/root/obsidian-vault"
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
HAS_BAD=0

for file in $FILES; do
    if grep -P '—' "$VAULT/$file" > /dev/null 2>&1; then
        echo "❌ Длинное тире в $file"
        grep -n -P '—' "$VAULT/$file"
        HAS_BAD=1
    fi
done

if [ "$HAS_BAD" -eq 1 ]; then
    echo "🔥 Замени длинные тире перед коммитом!"
    exit 1
fi
```

### Вариант 2: Авто-замена при публикации
Listener может запускать перед commit:

```bash
find /root/obsidian-vault -name "*.md" -not -path "*/\.*" -exec sed -i 's/—/-/g' {} \;
```

## Правило для агентов (в промпт)
Добавь в system prompt всех контент-агентов:
> «При генерации и редактировании контента используй ТОЛЬКО короткий дефис (-). Длинные тире (—) запрещены. Перед выдачей проверь текст на наличие — и замени на -.»

## Чек-лист
- [ ] Скрипт проверки создан
- [ ] Промпт агентов обновлён
- [ ] Все существующие посты проверены (текущий: ✅)
