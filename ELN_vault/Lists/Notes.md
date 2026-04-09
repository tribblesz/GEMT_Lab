---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2023-03-27
author: StarDustX
note type: note-list
tags:
  - list/notes
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Note
type note(tmp-note-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Note.md
templater true
class accent-button
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
