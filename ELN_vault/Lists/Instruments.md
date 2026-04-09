---
ELN version: 0.5.0
cssclasses:
  - wide-page
date created: 2026-04-08
author: StarDustX
note type: redirect-list
tags:
  - list/redirect
---

```dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
```

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_header", {});
```

## Redirect

The active notebook structure now uses [[Instrument Configurations]] instead of generic instrument pages.

- Use [[Instrument Configurations]] for gauge mapping, interlocks, alignment archives, and imaging defaults.
- Link each [[Experiment Runs|experiment run]] to the configuration that was active.

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
