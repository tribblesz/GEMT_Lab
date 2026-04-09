---
ELN version: 0.5.0
cssclasses:
  - wide-page
  - dashboard
date created: 2026-04-08
author: StarDustX
note type: dashboard
tags:
  - dashboard
---

<div class="title" style="color:#edf">APT / FIM Dashboard</div>

This page now mirrors the active APT/FIM workflow. For the main landing page, use [[Home]].

# Active Work

- [[Experiment Series]]
- [[Experiment Runs]]
- [[Specimens]]
- [[Instrument Configurations]]
- [[Startup Checklists]]
- [[Shutdown Checklists]]
- [[Data Records]]
- [[Lists]]

## Recent Experiment Runs

```dataview
LIST
FROM #experiment-run AND !"assets"
SORT file.mtime.ts DESC
LIMIT 8
```

## Recent Data Records

```dataview
LIST
FROM #data-record AND !"assets"
SORT file.mtime.ts DESC
LIMIT 8
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
