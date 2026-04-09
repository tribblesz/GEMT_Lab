---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: data-record-list
tags:
  - list/data-records
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Data Record
type command
action Templater: Insert assets/templates/New Data Record.md
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Data Record",
  data.run_name as "Run",
  data.raw_data_location as "Raw Data",
  data.formatting_status as "Formatting Status",
  file.mtime as "Modified"
FROM #data-record AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
