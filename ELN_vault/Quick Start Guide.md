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

2. Open the [[Home]] dashboard page. This dashboard is now focused on APT/FIM work: experiment series, experiment runs, specimens, instrument configurations, startup checklists, shutdown checklists, and data records.
3. Create or review an [[Instrument Configurations|instrument configuration]] before logging runs. This note is where you document gauge mapping, alignment settings archives, interlocks, startup targets, and default imaging settings.
4. Create the working [[Startup Checklists]] and [[Shutdown Checklists]] that your operators will follow. These pages are meant to capture the vacuum gauges, pump currents, temperatures, and gas state that must be recorded at startup and shutdown.
5. Create an [[Experiment Series]] note for the integration campaign you are running. Use the series note to document the purpose of the campaign, the independent and dependent variables, emergency stop conditions, and the expected data products.
6. Create [[Specimens]] for the tips, needles, coupons, or reference specimens you are loading into the instrument. Each specimen note stores the specimen ID, type, material system, preparation state, and handling notes.
7. Create an [[Experiment Runs|experiment run]] for each startup/test/shutdown sequence you perform. The run template includes dedicated sections for:
   - startup monitoring
   - during-test observations
   - shutdown monitoring
   - raw data links
   - MCP image metadata
   - ion column image metadata
   - freeform experiment notes
8. Create a [[Data Records]] note when you want a dedicated page for raw-file inventories, alignment settings links, MCP or ion column image metadata, and plot/photo formatting checks.
9. Use [[Daily Notes]] for general lab-day context, operator handoff notes, and links back to the specific runs completed that day.
10. For a template-by-template walkthrough of the APT/FIM workflow, read [[APT FIM Template Workflow]].



```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
