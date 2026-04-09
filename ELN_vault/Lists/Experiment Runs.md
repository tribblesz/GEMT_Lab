---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: experiment-run-list
tags:
  - list/experiment-runs
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Experiment Run
type command
action Templater: Insert assets/templates/New Experiment Run.md
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Run",
  run.run_id as "Run ID",
  run.series_name as "Series",
  specimen.id as "Specimen ID",
  run.mode as "Mode",
  run.status as "Status",
  file.mtime as "Modified"
FROM #experiment-run AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
