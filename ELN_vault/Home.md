---
ELN version: 0.5.0
cssclasses:
  - wide-page
  - dashboard
date created: 2026-04-08
author: StarDustX
note type: dashboard
tags:
  - dashboard
---

<div class="title" style="color:rgba(150, 210, 170, 0.4); text-align:center; font-size:0.9rem;">GEMT</div>

# Experiment Control

- ### [[Experiment Series]]
  ```dataview
  LIST
  FROM #experiment-series AND !"assets"
  WHERE series.status = "active"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Experiment Runs]]
  ```dataview
  LIST
  FROM #experiment-run AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Specimens]]
  ```dataview
  LIST
  FROM #specimen AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Instrument Configurations]]
  ```dataview
  LIST
  FROM #instrument-config AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Checklists And Data

- ### [[Startup Checklists]]
  ```dataview
  LIST
  FROM #startup-checklist AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Shutdown Checklists]]
  ```dataview
  LIST
  FROM #shutdown-checklist AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Data Records]]
  ```dataview
  LIST
  FROM #data-record AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Notes And Coordination

- ### [[Daily Notes]]
  ```dataview
  LIST
  FROM #daily-note AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Meetings]]
  ```dataview
  LIST
  FROM #meeting AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Notes]]
  ```dataview
  LIST
  FROM "Notes" AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Open Tasks

```dataview
TASK
FROM !"assets"
WHERE !completed
SORT file.mtime DESC
LIMIT 20
```

# Quick Links

- [[Lists]]
- [[Experiment Series]]
- [[Experiment Runs]]
- [[Specimens]]
- [[Instrument Configurations]]
- [[Startup Checklists]]
- [[Shutdown Checklists]]
- [[Data Records]]

# Vault Stats

- File Count: **`$=dv.pages().length`**
- Experiment Series: **`$=dv.pages('#experiment-series AND !"assets"').length`**
- Experiment Runs: **`$=dv.pages('#experiment-run AND !"assets"').length`**
- Specimens: **`$=dv.pages('#specimen AND !"assets"').length`**
- Data Records: **`$=dv.pages('#data-record AND !"assets"').length`**

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
