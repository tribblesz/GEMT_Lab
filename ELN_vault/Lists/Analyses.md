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

The active notebook structure now uses [[Experiment Logs]], [[MCP Image Logs]], and [[Ion Column Image Logs]] instead of generic analysis pages.

- Use [[Experiment Logs]] for the actual operating record of a startup, test, or shutdown.
- Use [[MCP Image Logs]] and [[Ion Column Image Logs]] for image-specific metadata and file tracking.

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```