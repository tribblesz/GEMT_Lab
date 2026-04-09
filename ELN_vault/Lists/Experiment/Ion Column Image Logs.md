---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: ion-column-image-log-list
tags:
  - list/ion-column-image-logs
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Ion Column Image Log Writer](http://127.0.0.1:8765/?form=ion-column-image-log).

```dataview
TABLE WITHOUT ID
  file.link as "Ion Column Image Log",
  image.parent_experiment_log as "Experiment Log",
  image.sequence_number as "Sequence",
  image.date_time as "Date / Time",
  image.signal_source as "Signal Source",
  file.mtime as "Modified"
FROM #ion-column-image-log AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
