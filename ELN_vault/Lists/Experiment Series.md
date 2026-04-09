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

```button
name New Experiment Series
type command
action Templater: Insert assets/templates/New Experiment Series.md
class accent-button
```

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
