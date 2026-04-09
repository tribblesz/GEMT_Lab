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

> [!warning] Legacy flow
> `Experiment Runs` is now the legacy Obsidian-native path. New work should use [[Lists/Experiment/Experiment Logs|Experiment Logs]] and the local GUI writer at [http://127.0.0.1:8765/?form=experiment-log](http://127.0.0.1:8765/?form=experiment-log) after starting `python tools/lab-log-writer/server.py`.
> Open [[Lab Log Writer]] for the active creation flow.

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
