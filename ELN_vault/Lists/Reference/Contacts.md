---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2023-05-25
author: StarDustX
note type: contact-list
tags:
  - list/contacts
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

> [!info] Contact entry
> Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open [Contact Writer](http://127.0.0.1:8765/?form=contact).

```dataview
TABLE WITHOUT ID
  file.link as Contact,
  contact.work.email as Email,
  contact.work.phone as Phone, 
  address.work.building as Building, 
  address.work.room as Room
FROM #contact AND !"assets"
SORT file.link ASC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
