---
ELN version: 0.5.0
cssclasses:
  - wide-page
  - dashboard
date created: 2026-04-08
author: StarDustX
note type: list
tags:
  - list/lists
---

<div class="title" style="color:#edf">Lists</div>


# Experiment Work
- ### [[Experiment Series]]
  ```dataview
  LIST
  FROM #experiment-series AND !"assets"
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

- ### [[Meetings]]
  ```dataview
  LIST
  FROM #meeting AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Daily Notes]]
  ```dataview
  LIST
  FROM #daily-note AND !"assets"
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

# Recently Edited
- 
  ```dataviewjs
    dv.list(dv.pages('').sort(f=>f.file.mtime.ts,"desc").slice(0, 5).file.link)
   ```
- 
  ```dataviewjs
    dv.list(dv.pages('').sort(f=>f.file.mtime.ts,"desc").slice(5, 10).file.link)
   ```
- 
  ```dataviewjs
    dv.list(dv.pages('').sort(f=>f.file.mtime.ts,"desc").slice(10, 15).file.link)
   ```



```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
