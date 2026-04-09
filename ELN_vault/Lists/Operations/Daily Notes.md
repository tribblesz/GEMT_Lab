---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2023-03-11
author: StarDustX
note type: daily-note-list
tags:
  - list/daily-note
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] Daily note entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Daily Note Writer](http://127.0.0.1:8765/?form=daily-note).

```dataview
TABLE WITHOUT ID
  file.link as "Daily Note", 
  author, 
  date-created
FROM #daily-note AND !"assets"
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
