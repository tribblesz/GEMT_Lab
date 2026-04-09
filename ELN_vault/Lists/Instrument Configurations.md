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
srert
```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Instrument Configuration
type note(tmp-instrument-configuration-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Instrument Configuration.md
templater true
class accent-button
```

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
