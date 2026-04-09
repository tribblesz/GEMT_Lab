---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: shutdown-checklist-list
tags:
  - list/shutdown-checklists
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Shutdown Checklist
type command
action Templater: Insert assets/templates/New Shutdown Checklist.md
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Checklist",
  checklist.configuration_name as "Configuration",
  checklist.status as "Status",
  file.mtime as "Modified"
FROM #shutdown-checklist AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
