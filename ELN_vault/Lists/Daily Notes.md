---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2023-03-11
author: StarDustX
note type: daily-note-list
tags:
  - list/daily-note
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Daily Note
type note(tmp-daily-note-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Daily Note.md
templater true
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Daily Note", 
  author, 
  date-created
FROM #daily-note AND !"assets"
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
