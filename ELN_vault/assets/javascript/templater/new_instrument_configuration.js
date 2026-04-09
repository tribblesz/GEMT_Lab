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
  main_chamber_gauge: ${common.yamlString(
    common.getNested(settings, "gauge", "main chamber", "name") || "Ion Gauge"
  )}
  load_lock_gauge: ${common.yamlString(
    common.getNested(settings, "gauge", "load lock", "name") ||
      "LL Wide Range Gauge"
  )}
  ion_column_gauge: ${common.yamlString(
    common.getNested(settings, "gauge", "ion column", "name") ||
      "Ion Column Wide Range Gauge"
  )}
  main_ion_pump_label: ${common.yamlString("Main Ion Pump")}
  ion_column_ion_pump_label: ${common.yamlString("Ion Column Ion Pump")}
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Configuration Summary

- **Configuration:** ${configurationName}
- **Type:** ${configurationType || "Add a configuration type."}
- **Instrument:** ${instrumentName || "Add the instrument name."}
- **Alignment settings archive:** ${
    alignmentSettingsFile || "Add the alignment settings file path or link."
  }

## Gauge Mapping

| Location | Gauge / Readback | Notes |
| --- | --- | --- |
| Main chamber | Ion Gauge | Primary pressure reference during runs |
| Load lock | LL Wide Range Gauge | Record starting and ending pressure |
| Ion column | Ion Column Wide Range Gauge | Record starting and ending pressure |
| Main pump | Main Ion Pump current and pressure | Record current and inferred pressure |
| Ion column pump | Ion Column Ion Pump current and pressure | Record current and inferred pressure |

## Interlocks And Safeties

- Active interlocks:
- Safeties intentionally bypassed:
- Required stop conditions beyond interlocks:

## Startup Targets

- Main chamber target pressure:
- Load lock target pressure:
- Ion column target pressure:
- Cryo target:

## Imaging Defaults

- Default MCP front voltage:
- Default MCP back voltage:
- Default specimen stage HV:
- Default ion column accelerating voltage:
- Preferred image export format:

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
