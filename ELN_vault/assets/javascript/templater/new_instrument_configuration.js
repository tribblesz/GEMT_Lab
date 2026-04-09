const common = require("./apt_fim_common");

async function new_instrument_configuration(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const dateCreated = common.getToday();

  const configTypes =
    common.getNested(settings, "instrument configuration", "type") || [
      "APT",
      "FIM",
      "Hybrid",
    ];

  const configurationName = await tp.system.prompt(
    "Enter instrument configuration name:",
    "Hybrid FIM/APT Integration Baseline"
  );
  if (!configurationName) {
    return "";
  }

  const configurationType = await common.chooseFromList(
    tp,
    configTypes,
    "Select instrument configuration type:",
    "Enter instrument configuration type:"
  );
  const instrumentName = await tp.system.prompt(
    "Enter the instrument name:",
    "Hybrid FIM/APT Tool"
  );
  const alignmentSettingsFile = await tp.system.prompt(
    "Enter the alignment settings file location:",
    ""
  );
  const configurationStatus = await tp.system.prompt(
    "Enter configuration status:",
    "active"
  );
  const mainChamberGauge =
    common.getNested(settings, "gauge", "main chamber", "name") || "Ion Gauge";
  const loadLockGauge =
    common.getNested(settings, "gauge", "load lock", "name") ||
    "LL Wide Range Gauge";
  const ionColumnGauge =
    common.getNested(settings, "gauge", "ion column", "name") ||
    "Ion Column Wide Range Gauge";
  const mainIonPumpLabel = "Main Ion Pump";
  const ionColumnIonPumpLabel = "Ion Column Ion Pump";

  const folder = common.getFolder(
    settings,
    "instrument configurations",
    "Instrument Configurations"
  );

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
cssclasses:
  - wide-page
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: instrument-configuration
tags:
  - "#instrument-config"
configuration:
  name: ${common.yamlString(configurationName)}
  type: ${common.yamlString(configurationType, "Hybrid")}
  status: ${common.yamlString(configurationStatus, "active")}
  instrument_name: ${common.yamlString(instrumentName, "Hybrid FIM/APT Tool")}
  alignment_settings_file: ${common.yamlString(
    alignmentSettingsFile,
    "Add the archived alignment settings path or link."
  )}
  main_chamber_gauge: ${common.yamlString(mainChamberGauge)}
  load_lock_gauge: ${common.yamlString(loadLockGauge)}
  ion_column_gauge: ${common.yamlString(ionColumnGauge)}
  main_ion_pump_label: ${common.yamlString(mainIonPumpLabel)}
  ion_column_ion_pump_label: ${common.yamlString(ionColumnIonPumpLabel)}
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Configuration Summary

| Field | Value | Notes |
| --- | --- | --- |
| Configuration | ${configurationName} | |
| Type | ${configurationType || "Add a configuration type."} | |
| Status | ${configurationStatus || "active"} | |
| Instrument | ${instrumentName || "Add the instrument name."} | |
| Alignment settings archive | ${
    alignmentSettingsFile || "Add the alignment settings file path or link."
  } | |

## Gauge Mapping

| Location | Gauge / Readback | Notes |
| --- | --- | --- |
| Main chamber | ${mainChamberGauge} | Primary pressure reference during runs |
| Load lock | ${loadLockGauge} | Record starting and ending pressure |
| Ion column | ${ionColumnGauge} | Record starting and ending pressure |
| Main pump | ${mainIonPumpLabel} current and pressure | Record current and inferred pressure |
| Ion column pump | ${ionColumnIonPumpLabel} current and pressure | Record current and inferred pressure |

## Interlocks And Safeties

| Item | Configured State | Notes |
| --- | --- | --- |
| Vacuum interlocks active | | |
| High-voltage interlocks active | | |
| MCP protection active | | |
| Ion column protection active | | |
| Safeties intentionally bypassed | none | |
| Required stop conditions beyond interlocks | | |

## Startup Targets

| Parameter | Target | Units / Notes |
| --- | --- | --- |
| Main chamber target pressure | | mbar |
| Load lock target pressure | | mbar |
| Ion column target pressure | | mbar |
| Main ion pump target current | | A |
| Ion column ion pump target current | | A |
| Puck nest target temperature | | K |
| Cryo target | | K |

## Imaging Defaults

| Parameter | Default | Units / Notes |
| --- | --- | --- |
| MCP front voltage | | V |
| MCP back voltage | | V |
| Specimen stage HV | | V |
| Ion column accelerating voltage | | V |
| Ion column source pressure | | mbar |
| Preferred image export format | | |
| Preferred signal source | | |

## Operating Notes

| Topic | Entry |
| --- | --- |
| Standard operating mode | |
| Allowed imaging gases | |
| Warm-up / stabilization steps | |
| Shutdown prerequisites | |
| Archive / file naming notes | |

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(
    tp,
    noteContent,
    configurationName,
    folder,
    return_type
  );
}

module.exports = new_instrument_configuration;
