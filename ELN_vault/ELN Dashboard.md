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

- [[Lists/Experiment/Experiment Series|Experiment Series]]
- [[Lists/Experiment/Experiment Logs|Experiment Logs]]
- [[Lists/Experiment/MCP Image Logs|MCP Image Logs]]
- [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]]
- [[Lists/Experiment/Specimens|Specimens]]
- [[Lists/Operations/Instrument Configurations|Instrument Configurations]]
- [[Lists/Operations/Startup Checklists|Startup Checklists]]
- [[Lists/Operations/Shutdown Checklists|Shutdown Checklists]]
- [[Data Records]]
- [[Lists]]

## Writer

Start the local writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`, then open:

- [Experiment Log Writer](http://127.0.0.1:8765/?form=experiment-log)
- [MCP Image Log Writer](http://127.0.0.1:8765/?form=mcp-image-log)
- [Ion Column Image Log Writer](http://127.0.0.1:8765/?form=ion-column-image-log)

## Recent Experiment Logs

```dataview
LIST
FROM #experiment-log AND !"assets"
SORT file.mtime.ts DESC
LIMIT 8
```

## Recent MCP Image Logs

```dataview
LIST
FROM #mcp-image-log AND !"assets"
SORT file.mtime.ts DESC
LIMIT 8
```

## Recent Ion Column Image Logs

```dataview
LIST
FROM #ion-column-image-log AND !"assets"
SORT file.mtime.ts DESC
LIMIT 8
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
