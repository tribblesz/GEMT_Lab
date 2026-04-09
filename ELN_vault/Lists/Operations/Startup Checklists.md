---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: startup-checklist-list
tags:
  - list/startup-checklists
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```
```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Startup Checklist Writer](http://127.0.0.1:8765/?form=startup-checklist).

```dataview
TABLE WITHOUT ID
  file.link as "Checklist",
  checklist.configuration_name as "Configuration",
  checklist.status as "Status",
  file.mtime as "Modified"
FROM #startup-checklist AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
