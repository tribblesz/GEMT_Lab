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

# Daily Notes

- ### [[Lists/Operations/Daily Notes|Daily Notes]]
  ```dataview
  LIST
  FROM #daily-note AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Experiment Control

- ### [[Lists/Experiment/Experiment Series|Experiment Series]]
  ```dataview
  LIST
  FROM #experiment-series AND !"assets"
  WHERE series.status = "active"
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

# Checklists And Imaging Data

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

# Coordination

- ### [[Lists/Operations/Meetings|Meetings]]
  ```dataview
  LIST
  FROM #meeting AND !"assets"
  SORT file.mtime.ts DESC
  LIMIT 6
  ```

# Resources

- ### [[Resources/APT-FIM/Library|APT/FIM Resources]]
  ```dataview
  TABLE WITHOUT ID
    file.link as "Summary Note",
    provider as "Provider",
    model as "Model",
    file.mtime as "Modified"
  FROM "Resources/APT-FIM/Summaries"
  SORT file.mtime DESC
  LIMIT 6
  ```

- ### Topic Notes
  ```dataview
  TABLE WITHOUT ID
    file.link as "Topic Note",
    provider as "Provider",
    model as "Model",
    file.mtime as "Modified"
  FROM "Resources/APT-FIM/Topics"
  SORT file.mtime DESC
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
- [[Lab Log Writer]]
- [[Resources/APT-FIM/Library|APT/FIM Resources]]
- [[Lists/Operations/Daily Notes|Daily Notes]]
- [[Lists/Experiment/Experiment Series|Experiment Series]]
- [[Lists/Experiment/Experiment Logs|Experiment Logs]]
- [[Lists/Experiment/MCP Image Logs|MCP Image Logs]]
- [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]]
- [[Lists/Experiment/Specimens|Specimens]]
- [[Lists/Experiment/Notes|Notes]]
- [[Lists/Operations/Instrument Configurations|Instrument Configurations]]
- [[Lists/Operations/Startup Checklists|Startup Checklists]]
- [[Lists/Operations/Shutdown Checklists|Shutdown Checklists]]
- [[Data Records]]

# Vault Stats

- File Count: **`$=dv.pages().length`**
- Experiment Series: **`$=dv.pages('#experiment-series AND !"assets"').length`**
- Experiment Logs: **`$=dv.pages('#experiment-log AND !"assets"').length`**
- MCP Image Logs: **`$=dv.pages('#mcp-image-log AND !"assets"').length`**
- Ion Column Image Logs: **`$=dv.pages('#ion-column-image-log AND !"assets"').length`**
- Specimens: **`$=dv.pages('#specimen AND !"assets"').length`**
- Data Records: **`$=dv.pages('#data-record AND !"assets"').length`**

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
