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
type command
action Templater: Insert assets/templates/New Note.md
class accent-button
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
