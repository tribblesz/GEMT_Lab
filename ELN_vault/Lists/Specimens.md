---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: specimen-list
tags:
  - list/specimens
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] GUI writer entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Specimen Writer](http://127.0.0.1:8765/?form=specimen).

```dataview
TABLE WITHOUT ID
  file.link as "Specimen",
  specimen.id as "Specimen ID",
  specimen.type as "Type",
  specimen.material as "Material",
  specimen.preparation_state as "Preparation State",
  file.mtime as "Modified"
FROM #specimen AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
