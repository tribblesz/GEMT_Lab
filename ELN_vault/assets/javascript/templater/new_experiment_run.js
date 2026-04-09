const common = require("./apt_fim_common");

function getFrontmatter(noteName) {
  const file = app.metadataCache.getFirstLinkpathDest(noteName, "");
  if (!file) {
    return {};
  }

  return app.metadataCache.getFileCache(file)?.frontmatter || {};
}

async function new_experiment_run(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const operator = await tp.user.get_operator(tp);
  const dateCreated = common.getToday();

  const seriesNames = common.getDataviewPageNames("#experiment-series AND !\"assets\"");
  const specimenNames = common.getDataviewPageNames("#specimen AND !\"assets\"");
  const configurationNames = common.getDataviewPageNames("#instrument-config AND !\"assets\"");

  const runModes =
    common.getNested(settings, "experiment run", "mode") || [
      "APT",
      "FIM",
      "Hybrid",
      "startup only",
      "shutdown only",
    ];
  const runStatuses =
    common.getNested(settings, "experiment run", "status") || [
      "planned",
      "setup",
      "running",
      "completed",
      "aborted",
      "needs review",
    ];

  const seriesName = await common.chooseFromList(
    tp,
    seriesNames,
    "Select experiment series:",
    "Enter experiment series:"
  );
  const specimenName = await common.chooseFromList(
    tp,
    specimenNames,
    "Select specimen:",
    "Enter specimen name:"
  );
  const configurationName = await common.chooseFromList(
    tp,
    configurationNames,
    "Select instrument configuration:",
    "Enter instrument configuration:"
  );
  const runMode = await common.chooseFromList(
    tp,
    runModes,
    "Select experiment run mode:",
    "Enter experiment run mode:"
  );
  const runStatus = await common.chooseFromList(
    tp,
    runStatuses,
    "Select run status:",
    "Enter run status:"
  );
  const runId = await tp.system.prompt(
    "Enter experiment run ID:",
    `${dateCreated}-${common.slugify(seriesName || "integration")}-run`
  );
  if (!runId) {
    return "";
  }

  const ionColumnUsed = await common.chooseYesNo(tp, "Was the ion column used?");
  const gasesIntroduced = await tp.system.prompt(
    "Enter gases introduced into the main chamber (comma separated):",
    "He"
  );
  const loadLockVented = await common.chooseYesNo(tp, "Was the load lock vented?");
  const gasList = (gasesIntroduced || "He")
    .split(",")
    .map((gas) => gas.trim())
    .filter(Boolean);
  const gasYaml = (gasList.length > 0 ? gasList : ["none"])
    .map((gas) => `    - ${common.yamlString(gas)}`)
    .join("\n");

  const specimenMeta = getFrontmatter(specimenName);
  const configurationMeta = getFrontmatter(configurationName);
  const specimenData = specimenMeta.specimen || {};
  const configurationData = configurationMeta.configuration || {};

  const runsFolder = common.getFolder(
    settings,
    "experiment runs",
    "Experiment Runs"
  );
  const folder = `${runsFolder}/${common.sanitizeFileName(seriesName || "Unassigned Series")}`;

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
cssclasses:
  - wide-page
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: experiment-run
tags:
  - "#experiment-run"
run:
  run_id: ${common.yamlString(runId)}
  date: ${common.yamlString(dateCreated)}
  operator: ${common.yamlString(operator.name)}
  mode: ${common.yamlString(runMode, "Hybrid")}
  status: ${common.yamlString(runStatus, "planned")}
  series_name: ${common.yamlString(seriesName, "Unassigned Series")}
  ion_column_used: ${common.yamlString(ionColumnUsed)}
  load_lock_vented: ${common.yamlString(loadLockVented)}
specimen:
  name: ${common.yamlString(specimenName, specimenData.name || "Unassigned specimen")}
  id: ${common.yamlString(specimenData.id, "Add specimen ID")}
  type: ${common.yamlString(specimenData.type, "Add specimen type")}
configuration:
  name: ${common.yamlString(configurationName, configurationData.name || "Unassigned configuration")}
  alignment_settings_file: ${common.yamlString(
    configurationData.alignment_settings_file,
    "Add the archived alignment settings path when the ion column is used."
  )}
gas:
  introduced:
${gasYaml}
monitoring:
  startup:
    main_chamber_pressure: ${common.yamlString("~~ mbar")}
    main_ion_pump_current: ${common.yamlString("~~ A")}
    main_ion_pump_pressure: ${common.yamlString("~~ mbar")}
    puck_nest_temperature: ${common.yamlString("~~ K")}
    cryo_setpoint: ${common.yamlString("~~ K")}
    load_lock_pressure: ${common.yamlString("~~ mbar")}
    ion_column_pressure: ${common.yamlString("~~ mbar")}
    ion_column_ion_pump_current: ${common.yamlString("~~ A")}
    ion_column_ion_pump_pressure: ${common.yamlString("~~ mbar")}
  shutdown:
    main_chamber_pressure: ${common.yamlString("~~ mbar")}
    main_ion_pump_current: ${common.yamlString("~~ A")}
    main_ion_pump_pressure: ${common.yamlString("~~ mbar")}
    load_lock_pressure: ${common.yamlString("~~ mbar")}
    ion_column_pressure: ${common.yamlString("~~ mbar")}
    ion_column_ion_pump_current: ${common.yamlString("~~ A")}
    ion_column_ion_pump_pressure: ${common.yamlString("~~ mbar")}
data:
  raw_data_location: ${common.yamlString("Add the primary data folder or archive link.")}
  alignment_settings_file: ${common.yamlString(
    configurationData.alignment_settings_file,
    "Add alignment settings path if IonOptika was used."
  )}
  data_types_recorded:
    - "oscilloscope traces"
    - "digital logging"
    - "MCP images"
    - "raw MCP hit files"
imaging:
  mcp:
    front_voltage: ${common.yamlString("~~ V")}
    back_voltage: ${common.yamlString("~~ V")}
    integration_time: ${common.yamlString("~~ s")}
    specimen_stage_hv: ${common.yamlString("~~ V")}
    chamber_pressure: ${common.yamlString("~~ mbar")}
    ion_column_settings: ${common.yamlString("inactive")}
    imaging_gas: ${common.yamlString("N/A")}
  ion_column:
    accelerating_voltage: ${common.yamlString("~~ V")}
    source_pressure: ${common.yamlString("~~ mbar")}
    aperture: ${common.yamlString("~~")}
    field_of_view: ${common.yamlString("~~ um")}
    pixel_dwell_time: ${common.yamlString("~~ ms")}
    signal_source: ${common.yamlString("SED")}
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

\`\`\`button
name New Data Record
type note(tmp-data-record-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Data Record.md
templater true
class accent-button
\`\`\`

# Experiment Run Summary

- **Run ID:** ${runId}
- **Series:** ${seriesName || "Link this run to an experiment series."}
- **Specimen:** ${specimenName || "Link this run to a specimen note."}
- **Configuration:** ${configurationName || "Link this run to an instrument configuration."}
- **Mode:** ${runMode || "Add the run mode."}
- **Ion column used:** ${ionColumnUsed}
- **Load lock vented:** ${loadLockVented}

## Description

Add a brief description of what this run is trying to demonstrate, what changed relative to the plan, and any special instrument conditions or bypassed safeties.

## Parameter Ranges

- Independent variable range:
- Dependent measurement range:
- Step size or sequencing:
- Emergency stop parameters:

## Startup Monitoring

| Parameter | Condition |
| --- | --- |
| Main chamber starting pressure | |
| Main ion pump current and pressure | |
| Puck nest temperature | |
| Cryo setpoint | |
| Load lock starting pressure | |
| Ion column starting pressure | |
| Ion column ion pump current and pressure | |

## During Test

- Timeline of major events:
- Drift, instability, or delays:
- Independent variable changes:
- Operator observations:

## Shutdown Monitoring

| Parameter | Condition |
| --- | --- |
| Main chamber ending pressure | |
| Load lock ending pressure | |
| Ion column ending pressure | |
| Ion column ion pump current and pressure | |

## Raw Data Links

- Primary raw data folder:
- Alignment settings archive:
- Additional linked files:

## Data Formatting Requirements

- Save two-axis data as CSV with column headings where possible.
- Re-graph data in a consistent format with labeled axes and units.
- Use separate plots for separate units instead of multiple y-axes where possible.

## MCP Image Metadata

| Parameter | Condition |
| --- | --- |
| MCP front voltage | |
| MCP back voltage | |
| Integration time | |
| Specimen stage HV | |
| Main chamber pressure | |
| Ion column settings | |
| Imaging gas used | |

## Ion Column Image Metadata

| Parameter | Condition |
| --- | --- |
| Accelerating voltage | |
| Source pressure | |
| Aperture number | |
| Field of view | |
| Pixel dwell time | |
| Signal source | |

## Experiment Notes

- Record issues, deviations, delays, and incidental observations here.
- Capture what changed from the original plan and why.

## Linked Data Records

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Data Record",
  data.formatting_status as "Formatting Status",
  file.mtime as "Modified"
FROM #data-record AND !"assets"
WHERE data.run_name = this.file.name
SORT file.mtime DESC
\`\`\`

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(tp, noteContent, runId, folder, return_type);
}

module.exports = new_experiment_run;
