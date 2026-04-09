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

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Startup Checklist
type command
action Templater: Insert assets/templates/New Startup Checklist.md
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
