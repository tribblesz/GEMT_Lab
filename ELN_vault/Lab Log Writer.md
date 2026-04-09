---
ELN version: 0.5.0
cssclasses:
  - normal-page
date created: 2026-04-08
author: StarDustX
note type: how-to
tags:
  - "#note/how-to"
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

# Lab Log Writer

The local GUI writer is the preferred entry path for:

- [[Lists/Experiment/Experiment Series|Experiment Series]]
- [[Lists/Experiment/Experiment Logs|Experiment Logs]]
- [[Lists/Experiment/MCP Image Logs|MCP Image Logs]]
- [[Lists/Experiment/Ion Column Image Logs|Ion Column Image Logs]]
- [[Lists/Operations/Instrument Configurations|Instrument Configurations]]
- [[Lists/Experiment/Specimens|Specimens]]
- [[Lists/Reference/Contacts|Contacts]]
- [[Lists/Operations/Daily Notes|Daily Notes]]
- [[Lists/Operations/Meetings|Meetings]]
- [[Lists/Operations/Notes|Notes]]
- [[Tasks/My Tasks|Task Lists]]
- [[Lists/Operations/Startup Checklists|Startup Checklists]]
- [[Lists/Operations/Shutdown Checklists|Shutdown Checklists]]

## Start The Writer

Run one of these from the repository root on the same machine as the vault:

```powershell
python tools/lab-log-writer/server.py
```

```bat
tools\lab-log-writer\start_writer.bat
```

The writer serves a local browser UI at `http://127.0.0.1:8765/`.

## Open A Form

- [Experiment Log Writer](http://127.0.0.1:8765/?form=experiment-log)
- [MCP Image Log Writer](http://127.0.0.1:8765/?form=mcp-image-log)
- [Ion Column Image Log Writer](http://127.0.0.1:8765/?form=ion-column-image-log)
- [Experiment Series Writer](http://127.0.0.1:8765/?form=experiment-series)
- [Instrument Configuration Writer](http://127.0.0.1:8765/?form=instrument-configuration)
- [Specimen Writer](http://127.0.0.1:8765/?form=specimen)
- [Contact Writer](http://127.0.0.1:8765/?form=contact)
- [Daily Note Writer](http://127.0.0.1:8765/?form=daily-note)
- [Meeting Writer](http://127.0.0.1:8765/?form=meeting)
- [Note Writer](http://127.0.0.1:8765/?form=note)
- [Task List Writer](http://127.0.0.1:8765/?form=task-list)
- [Startup Checklist Writer](http://127.0.0.1:8765/?form=startup-checklist)
- [Shutdown Checklist Writer](http://127.0.0.1:8765/?form=shutdown-checklist)

## Notes

- Obsidian remains the reader, search, and Dataview layer.
- The writer creates markdown notes directly in `ELN_vault`.
- `Experiment Runs` and `Data Records` remain available only as legacy note flows.
- Core note creation now routes through the local writer instead of Templater.

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
