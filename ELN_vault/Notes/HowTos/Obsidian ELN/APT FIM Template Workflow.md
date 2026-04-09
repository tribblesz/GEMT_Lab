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
5. Create an [[Experiment Runs|experiment run]] for each actual startup, test, and shutdown sequence.
6. Create a [[Data Records]] note when you need a dedicated inventory of files, images, and formatting checks.

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

Think of the series note as the planning record for a group of related runs.

## Specimens

Use the `New Specimen` template for each tip, needle, coupon, reference specimen, or other physical item that may appear in one or more runs.

This note should hold:
- specimen ID
- specimen type
- material system
- preparation state
- storage location
- handling notes

The specimen note is the long-lived record. The run note is the time-specific operating record.

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

## Experiment Runs

Use the `New Experiment Run` template for every real operating session.

When creating a run, select or enter:
- experiment series
- specimen
- instrument configuration
- run mode
- run status
- whether the ion column was used
- whether the load lock was vented
- gases introduced into the main chamber

The run template is the most important operational note. It includes dedicated sections for:
- startup monitoring
- during-test observations
- shutdown monitoring
- raw data links
- data formatting requirements
- MCP image metadata
- ion column image metadata
- experiment notes, delays, deviations, and observations

Use this note to capture what actually happened, not just what was planned.

## Data Records

Use the `New Data Record` template when the files and images for a run need a dedicated note.

This note is useful for:
- raw data folder links
- archived alignment settings links
- MCP image metadata
- ion column image metadata
- plot formatting checks
- photo formatting checks

You do not need a separate data record for every run, but it is recommended when the run produces multiple file types or images that need tracking.

## Practical Example

For a new integration test campaign:

1. Create `Instrument Configuration` for the current hybrid tool state.
2. Create `Experiment Series` for the integration milestone being tested.
3. Create `Specimen` notes for the tips or reference specimens that may be loaded.
4. Review or update the `Startup Checklist` and `Shutdown Checklist`.
5. For each operating session, create an `Experiment Run`.
6. If the run produces meaningful files or images, create a linked `Data Record`.

## Minimal Rule Of Thumb

- If it describes the machine setup: use `Instrument Configuration`.
- If it describes a campaign of related tests: use `Experiment Series`.
- If it describes a physical item under test: use `Specimen`.
- If it describes what happened during one operating session: use `Experiment Run`.
- If it describes the file outputs and image metadata: use `Data Record`.

```dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
```
