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

# APT FIM Template Workflow

This guide explains how to use the active APT/FIM templates in the vault and how the main note types relate to each other.

## Recommended Order

1. Create or review an [[Instrument Configurations|instrument configuration]].
2. Create an [[Experiment Series]] for the integration campaign or test program.
3. Create one or more [[Specimens]] for the hardware or sample under test.
4. Review the [[Startup Checklists]] and [[Shutdown Checklists]] you want operators to follow.
5. Start the local GUI writer with `python tools/lab-log-writer/server.py` or `tools\lab-log-writer\start_writer.bat`.
6. Create an [[Experiment Logs|experiment log]] for each actual startup, test, and shutdown sequence.
7. Create one [[MCP Image Logs|MCP image log]] per MCP image and one [[Ion Column Image Logs|ion column image log]] per ion-column image when those images are part of the session record.

## Instrument Configurations

Use the `New Instrument Configuration` template when you need a reusable description of the machine state and operating setup.

This note should hold:
- gauge mapping for the main chamber, load lock, and ion column
- archived alignment settings file path
- interlocks and safeties
- startup targets
- default imaging settings

Create or update this note before starting a new experiment series when the instrument setup has changed.

## Experiment Series

Use the `New Experiment Series` template to define the higher-level campaign.

This note should answer:
- What is the purpose of the series?
- Which variables will be changed between runs?
- Which outputs are being measured?
- What are the emergency stop conditions?
- What kinds of data are expected?

Think of the series note as the planning record for a group of related logs.

## Specimens

Use the `New Specimen` template for each tip, needle, coupon, reference specimen, or other physical item that may appear in one or more runs.

This note should hold:
- specimen ID
- specimen type
- material system
- preparation state
- storage location
- handling notes

The specimen note is the long-lived record. The experiment log is the time-specific operating record.

## Startup And Shutdown Checklists

Use the checklist templates when you want repeatable operator workflows.

`Startup Checklist` is for:
- recording starting pressures
- recording pump current and pressure
- confirming puck nest temperature and cryo setpoint
- recording gas state
- documenting bypassed safeties or unusual startup conditions

`Shutdown Checklist` is for:
- recording ending pressures
- confirming safe HV and MCP state
- confirming gas isolation or shutdown state
- confirming data archival and follow-up actions

These checklist notes can be reused across many runs.

## Experiment Logs

Use the local GUI writer to create one experiment log for every real operating session.

The experiment log is the primary operational note. It includes dedicated sections for:
- startup monitoring
- shutdown monitoring
- operating description and parameter ranges
- raw data links
- linked MCP image logs
- linked ion column image logs
- experiment notes, delays, deviations, and observations

Use this note to capture what actually happened, not just what was planned.

## MCP Image Logs

Use one MCP image log per MCP image captured during a session.

This note is useful for:
- MCP front and back voltage
- integration time
- specimen stage high voltage
- main chamber pressure
- ion column settings state
- imaging gas
- image file names and links

Each MCP image log should link back to the parent [[Experiment Logs|experiment log]].

## Ion Column Image Logs

Use one ion-column image log per ion-column image captured during a session.

This note is useful for:
- accelerating voltage
- source pressure
- aperture number
- field of view
- pixel dwell time
- signal source
- image file names and links
- signal-only image file names and links

Each ion-column image log should link back to the parent [[Experiment Logs|experiment log]].

## Practical Example

For a new integration test campaign:

1. Create `Instrument Configuration` for the current hybrid tool state.
2. Create `Experiment Series` for the integration milestone being tested.
3. Create `Specimen` notes for the tips or reference specimens that may be loaded.
4. Review or update the `Startup Checklist` and `Shutdown Checklist`.
5. Start the GUI writer.
6. For each operating session, create an `Experiment Log`.
7. If the session produces meaningful MCP or ion-column images, create linked image-log notes for each image.

## Minimal Rule Of Thumb

- If it describes the machine setup: use `Instrument Configuration`.
- If it describes a campaign of related tests: use `Experiment Series`.
- If it describes a physical item under test: use `Specimen`.
- If it describes what happened during one operating session: use `Experiment Log`.
- If it describes one MCP image: use `MCP Image Log`.
- If it describes one ion-column image: use `Ion Column Image Log`.

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
