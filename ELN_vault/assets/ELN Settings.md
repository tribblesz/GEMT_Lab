---
ELN version: 0.5.0
note:
  author:
    - name: StarDustX
      initials: SDX
    - Mehdi: ~~
      initials: ~~
    - Austin: ~~
      initials: ~~
    - Angelo: ~~
      initials: ~~
operators:
  - name: StarDustX
    initials: SDX
folder:
  local data: /path/to_your/local_data/folder
  remote data: /path/to_your/remote_data/folder
  experiment series: Experiment Series
  experiment runs: Experiment Runs
  specimens: Specimens
  instrument configurations: Instrument Configurations
  startup checklists: Checklists/Startup
  shutdown checklists: Checklists/Shutdown
  data records: Data Records
  contacts: Contacts
  daily notes: Daily Notes
  meetings: Meetings
  tasks: Tasks
  notes: Notes
  templates: assets/templates
  custom templates: assets/templates/Custom Templates
  dataview queries: assets/templates/DataView Queries
  mermaid charts: assets/templates/Mermaid Charts
experiment series:
  type:
    - integration status
    - commissioning
    - vacuum characterization
    - startup qualification
    - shutdown qualification
    - timing synchronization
    - MCP imaging
    - ion column imaging
    - APT acquisition
    - FIM acquisition
  status:
    - planned
    - active
    - paused
    - completed
specimen:
  type:
    - APT needle
    - FIM tip
    - reference specimen
    - calibration specimen
    - coupon
    - witness specimen
    - other
instrument configuration:
  type:
    - APT
    - FIM
    - Hybrid
    - Vacuum only
    - Imaging only
experiment run:
  mode:
    - APT
    - FIM
    - Hybrid
    - startup only
    - shutdown only
  status:
    - planned
    - setup
    - running
    - completed
    - aborted
    - needs review
gas:
  allowed:
    - none
    - He
    - Ne
    - H2
    - O2
    - N2
    - Ar
    - Kr
    - Xe
gauge:
  main chamber:
    name: Ion Gauge
  load lock:
    name: LL Wide Range Gauge
  ion column:
    name: Ion Column Wide Range Gauge
monitoring:
  startup:
    - main chamber pressure
    - main ion pump current and pressure
    - puck nest temperature
    - cryo setpoint
    - load lock pressure
    - ion column pressure
    - ion column ion pump current and pressure
  shutdown:
    - main chamber pressure
    - load lock pressure
    - ion column pressure
    - main ion pump current and pressure
    - ion column ion pump current and pressure
---

## Settings

```dataviewjs
await dv.view("/assets/javascript/dataview/views/properties", {obsidian: obsidian});
```


```dataviewjs
console.log(this.name)
```
