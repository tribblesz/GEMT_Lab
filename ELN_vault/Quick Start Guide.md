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

1. All configuration and template files for the vault are located in the **assets** folder. Before creating notes, open [[ELN Settings]] and update the note author, operator list, folder paths, experiment run statuses, allowed gases, and any gauge labels that differ from your instrument. These values drive the prompts used when you create new APT/FIM notes.

   > [!Info] ELN Settings Info
   > The [[ELN Settings]] file stores the active APT/FIM schema as YAML metadata. It defines the folders, run modes, specimen types, configuration types, gases, and standard monitoring readbacks used throughout the vault.

2. Open the [[Home]] dashboard page. This dashboard is now focused on APT/FIM work: experiment series, experiment logs, MCP image logs, ion column image logs, specimens, instrument configurations, startup checklists, shutdown checklists, and legacy data records.
3. Start the local GUI writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`. This launches a browser-based form layer that writes markdown directly into the vault. [[Lab Log Writer]] stores the launch links in one place inside the vault.
4. Create or review an [[Instrument Configurations|instrument configuration]] in the writer before logging runs. This note is where you document gauge mapping, alignment settings archives, interlocks, startup targets, and default imaging settings.
5. Create the working [[Startup Checklists]] and [[Shutdown Checklists]] in the writer. These pages capture the vacuum gauges, pump currents, temperatures, and gas state that must be recorded at startup and shutdown.
6. Create an [[Experiment Series]] note in the writer for the integration campaign you are running. Use the series note to document the purpose of the campaign, the independent and dependent variables, emergency stop conditions, and the expected data products.
7. Create [[Specimens]] in the writer for the tips, needles, coupons, or reference specimens you are loading into the instrument. Each specimen note stores the specimen ID, type, material system, preparation state, and handling notes.
8. Create an [[Experiment Logs|experiment log]] for each startup/test/shutdown sequence you perform. The experiment log captures startup and shutdown monitoring, raw data links, alignment settings links, and freeform experiment notes.
9. Create one [[MCP Image Logs|MCP image log]] per MCP image and one [[Ion Column Image Logs|ion column image log]] per ion-column image. These notes are linked back to the parent experiment log and keep image metadata separate from the main experiment narrative.
10. Use [[Data Records]] only when you need to preserve the earlier legacy inventory format. New work should go into experiment logs and the two image-log note types.
11. Use [[Daily Notes]] for general lab-day context, operator handoff notes, and links back to the specific logs completed that day.



```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
