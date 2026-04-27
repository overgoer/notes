# Задачи на сегодня

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed)
  .where(t => t.text.includes("25 September 2024")))
```

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed))
```
# Журнал
