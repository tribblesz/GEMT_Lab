---
ELN version: 0.4.2
cssclass: normal-page
date created: 2024-07-17
author: StarDustX
note type: contact
tag: contact
name:
  title:
  given name: Primary
  family name: Contact
contact:
  work:
    email: contact@example.edu
    phone: +00 xxx xxx xxx
    mobile:
    fax: +00 xxx xxx xxx
address:
  work:
    affiliation: Research Facility
    division: Instrument Operations
    street: Research Street 1
    building: Main Building
    room: Control Room
    city: City
    zip code: 00000
    country: Country
job position: Primary Contact
group: Operations
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/contact", {obsidian: obsidian});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
