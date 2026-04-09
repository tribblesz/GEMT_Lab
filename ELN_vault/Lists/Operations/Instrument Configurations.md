---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: instrument-configuration-list
tags:
  - list/instrument-configurations
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Instrument Configuration Writer](http://127.0.0.1:8765/?form=instrument-configuration).

```dataview
TABLE WITHOUT ID
  file.link as "Configuration",
  configuration.type as "Type",
  configuration.status as "Status",
  configuration.instrument_name as "Instrument",
  file.mtime as "Modified"
FROM #instrument-config AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
