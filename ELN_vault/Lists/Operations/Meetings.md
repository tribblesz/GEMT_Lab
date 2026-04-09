---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2023-03-11
author: StarDustX
note type: meeting-list
tags:
  - list/meeting
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] Meeting entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Meeting Writer](http://127.0.0.1:8765/?form=meeting).

## 2024

```dataview
TABLE WITHOUT ID
  meeting.date as Date,
  "[["+ file.name +"|"+ meeting.title +"]]" as Meeting,
  meeting.topics.title as Topics,
  meeting.type as Type
FROM #meeting AND !"assets"
WHERE file.ctime.year = 2024
SORT file.ctime DESC
```

## 2025

```dataview
TABLE WITHOUT ID
  meeting.date as Date,
  "[["+ file.name +"|"+ meeting.title +"]]" as Meeting,
  meeting.topics.title as Topics,
  meeting.type as Type
FROM #meeting AND !"assets"
WHERE file.ctime.year = 2025
SORT file.ctime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
