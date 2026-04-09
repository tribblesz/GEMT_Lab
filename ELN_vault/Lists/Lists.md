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

## Folders

- Daily: [[Lists/Operations/Daily Notes|Daily Notes]]
- Experiment: [[Lists/Experiment/Experiment Series|Experiment Series]], [[Lists/Experiment/Experiment Logs|Experiment Logs]], [[Lists/Experiment/MCP Image Logs|MCP Image Logs]], [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]], [[Lists/Experiment/Specimens|Specimens]], [[Lists/Experiment/Experiment Runs|Experiment Runs]], [[Lists/Experiment/Notes|Notes]]
- Reference: [[Lists/Reference/Contacts|Contacts]], [[Lists/Reference/Publications|Publications]], [[Lists/Reference/ELN Note Versions|ELN Note Versions]]
- Operations: [[Lists/Operations/Instrument Configurations|Instrument Configurations]], [[Lists/Operations/Startup Checklists|Startup Checklists]], [[Lists/Operations/Shutdown Checklists|Shutdown Checklists]], [[Lists/Operations/Meetings|Meetings]]

# Daily Notes
- ### [[Lists/Operations/Daily Notes|Daily Notes]]
  ```dataview
  LIST
  FROM #daily-note AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Experiment Work
- ### [[Lists/Experiment/Experiment Series|Experiment Series]]
  ```dataview
  LIST
  FROM #experiment-series AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Experiment/Experiment Logs|Experiment Logs]]
  ```dataview
  LIST
  FROM #experiment-log AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Experiment/MCP Image Logs|MCP Image Logs]]
  ```dataview
  LIST
  FROM #mcp-image-log AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]]
  ```dataview
  LIST
  FROM #ion-column-image-log AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Experiment/Specimens|Specimens]]
  ```dataview
  LIST
  FROM #specimen AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Experiment/Notes|Notes]]
  ```dataview
  LIST
  FROM "Notes" AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Operations/Instrument Configurations|Instrument Configurations]]
  ```dataview
  LIST
  FROM #instrument-config AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Operations/Startup Checklists|Startup Checklists]]
  ```dataview
  LIST
  FROM #startup-checklist AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

- ### [[Lists/Operations/Shutdown Checklists|Shutdown Checklists]]
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

- ### [[Lists/Operations/Meetings|Meetings]]
  ```dataview
  LIST
  FROM #meeting AND !"assets"
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
