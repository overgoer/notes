# Задачи на сегодня

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed)
  .where(t => t.text.includes("08 October 2024")))
```

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed))
```
# Журнал