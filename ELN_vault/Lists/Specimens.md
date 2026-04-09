---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: specimen-list
tags:
  - list/specimens
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```button
name New Specimen
type note(tmp-specimen-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Specimen.md
templater true
class accent-button
```

```dataview
TABLE WITHOUT ID
  file.link as "Specimen",
  specimen.id as "Specimen ID",
  specimen.type as "Type",
  specimen.material as "Material",
  specimen.preparation_state as "Preparation State",
  file.mtime as "Modified"
FROM #specimen AND !"assets"
SORT file.mtime DESC
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
