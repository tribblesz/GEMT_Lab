---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: experiment-log-list
tags:
  - list/experiment-logs
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Experiment Log Writer](http://127.0.0.1:8765/?form=experiment-log).

```dataview
TABLE WITHOUT ID
  file.link as "Experiment Log",
  experiment.log_id as "Log ID",
  experiment.series_name as "Series",
  experiment.series_number as "Series No.",
  experiment.status as "Status",
  experiment.date_time as "Date / Time",
  file.mtime as "Modified"
FROM #experiment-log AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
