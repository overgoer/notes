# Задачи на сегодня

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed)
  .where(t => t.text.includes("{{date:DD MMMM Y}}")))
```

```dataviewjs
dv.taskList(dv.pages().file.tasks 
  .where(t => !t.completed)
  SORT file.name desc)
```
# Журнал
