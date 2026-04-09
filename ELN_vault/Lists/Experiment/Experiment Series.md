---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: experiment-series-list
tags:
  - list/experiment-series
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Experiment Series Writer](http://127.0.0.1:8765/?form=experiment-series).

```dataview
TABLE WITHOUT ID
  file.link as "Series",
  series.type as "Type",
  series.status as "Status",
  series.abbreviation as "Abbrev",
  file.mtime as "Modified"
FROM #experiment-series AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
