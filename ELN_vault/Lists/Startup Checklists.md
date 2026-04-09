---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: startup-checklist-list
tags:
  - list/startup-checklists
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```
sdss

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Startup Checklist
type note(tmp-startup-checklist-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Startup Checklist.md
templater true
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Checklist",
  checklist.configuration_name as "Configuration",
  checklist.status as "Status",
  file.mtime as "Modified"
FROM #startup-checklist AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
