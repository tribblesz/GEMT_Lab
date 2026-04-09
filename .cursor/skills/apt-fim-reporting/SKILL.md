---
name: apt-fim-reporting
description: Use when creating, editing, or restructuring experiment notes for this vault around APT, FIM, hybrid FIM/APT integration, startup and shutdown logging, vacuum gauges, MCP imaging, ion column imaging, raw data inventories, or daily experimental run records.
---

# APT FIM Reporting

## Overview

This vault is a dedicated APT/FIM notebook. Use the APT/FIM note model in `ELN_vault/assets/ELN Settings.md` and prefer the active list pages and templates under `ELN_vault/Lists` and `ELN_vault/assets/templates`.

## Active Note Types

Use these note types instead of chemistry- or biology-oriented structures:

- `experiment-series`
- `experiment-log`
- `mcp-image-log`
- `ion-column-image-log`
- `specimen`
- `instrument-configuration`
- `startup-checklist`
- `shutdown-checklist`
- `daily-note`

Legacy note types that may still exist:

- `experiment-run`
- `data-record`

## Required Reporting Rules

When working on an `experiment-log`, preserve or add all of these sections:

- Experiment summary and purpose
- Parameter ranges
- Startup monitoring
- During-test observations
- Shutdown monitoring
- Raw data links
- Data formatting requirements
- MCP image metadata
- Ion column image metadata
- Experiment notes, deviations, delays, and incidental observations

## Required Monitoring Fields

Each experiment log should capture, either in frontmatter or in the body:

- Main chamber starting pressure
- Main chamber ending pressure
- Main ion pump current and pressure
- Puck nest temperature
- Cryo setpoint
- Load lock starting pressure
- Load lock ending pressure
- Ion column starting pressure
- Ion column ending pressure
- Ion column ion pump current and pressure
- Whether the ion column was used
- Specimen type and specimen ID
- Gases introduced into the main chamber
- Whether the load lock was vented

## Data Expectations

Always preserve space for:

- Raw data file names and archive locations
- Alignment settings file link when the ion column is used
- Data types recorded such as oscilloscope traces, digital logging, MCP images, and raw MCP hit files
- CSV-first formatting for two-axis data where possible
- Re-graphing guidance with labeled axes, units, and consistent plot styling
- Photo and image captions with capture context

## MCP Image Metadata

When documenting an `mcp-image-log`, include:

- MCP front voltage
- MCP back voltage
- Integration time
- Specimen stage HV
- Main chamber pressure
- Ion column settings
- Imaging gas used, if any

## Ion Column Image Metadata

When documenting an `ion-column-image-log`, include:

- Accelerating voltage
- Source pressure
- Aperture number or diameter
- Field of view
- Pixel dwell time
- Signal source
- Link or embed of the full-resolution signal-only image when available

## Editing Guidance

- Prefer the active APT/FIM pages such as `Experiment Series`, `Experiment Logs`, `MCP Image Logs`, `Ion Column Image Logs`, `Specimens`, `Instrument Configurations`, `Startup Checklists`, and `Shutdown Checklists`.
- Do not introduce new chemistry-oriented note types, templates, or dashboards.
- Preserve freeform note sections so operators can capture delays, anomalies, and context in plain language.
- Distinguish between series-level planning and experiment-log execution records.
- Treat `Experiment Runs` and `Data Records` as legacy compatibility flows unless the user explicitly asks to preserve or edit them.
