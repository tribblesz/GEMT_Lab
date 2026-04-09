const common = require("./apt_fim_common");

async function new_experiment_series(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const dateCreated = common.getToday();

  const seriesName = await tp.system.prompt("Enter experiment series name:", "");
  if (!seriesName) {
    return "";
  }

  const seriesTypes =
    common.getNested(settings, "experiment series", "type") || [
      "integration status",
      "commissioning",
      "vacuum characterization",
    ];
  const seriesStatuses =
    common.getNested(settings, "experiment series", "status") || [
      "planned",
      "active",
      "completed",
    ];

  const seriesType = await common.chooseFromList(
    tp,
    seriesTypes,
    "Select experiment series type:",
    "Enter experiment series type:"
  );
  const seriesStatus = await common.chooseFromList(
    tp,
    seriesStatuses,
    "Select experiment series status:",
    "Enter experiment series status:"
  );

  const abbreviation = await tp.system.prompt(
    "Enter experiment series abbreviation:",
    common.slugify(seriesName).slice(0, 12)
  );
  const purpose = await tp.system.prompt("Enter the purpose of this series:", "");
  const independentVariables = await tp.system.prompt(
    "Enter the independent variables for this series:",
    ""
  );
  const dependentVariables = await tp.system.prompt(
    "Enter the dependent variables for this series:",
    ""
  );

  const folder = `${common.getFolder(
    settings,
    "experiment series",
    "Experiment Series"
  )}/${common.sanitizeFileName(seriesName)}`;

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
cssclasses:
  - wide-page
  - dashboard
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: experiment-series
tags:
  - "#experiment-series"
series:
  name: ${common.yamlString(seriesName)}
  abbreviation: ${common.yamlString(abbreviation, "N/A")}
  type: ${common.yamlString(seriesType, "integration status")}
  status: ${common.yamlString(seriesStatus, "planned")}
  purpose: ${common.yamlString(
    purpose,
    "Document the purpose of this series and the intended integration milestone."
  )}
  independent_variables: ${common.yamlString(
    independentVariables,
    "List the variables intentionally changed between runs."
  )}
  dependent_variables: ${common.yamlString(
    dependentVariables,
    "List the measured outcomes or observed signals tracked for this series."
  )}
  data_types_recorded:
    - "oscilloscope traces"
    - "digital logging"
    - "MCP images"
    - "raw MCP hit files"
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

\`\`\`button
name New Experiment Run
type note(tmp-experiment-run-<% tp.date.now("YYYYMMDDHHmmssSSS") %>) template
action assets/templates/New Experiment Run.md
templater true
class accent-button
\`\`\`

# Experiment Series Summary

- **Series:** ${seriesName}
- **Type:** ${seriesType || "Add the experiment series type."}
- **Status:** ${seriesStatus || "Add the series status."}
- **Purpose:** ${purpose || "Add the overall purpose for the series."}

## Intended Scope

### Variables
- **Independent:** ${independentVariables || "Add the controlled variables for this series."}
- **Dependent:** ${dependentVariables || "Add the measured outcomes for this series."}

### Parameter Ranges
- Minimum and maximum operating ranges:
- Planned step sizes:
- Measurement limits or restrictions:

### Emergency Stop Conditions
- List all non-interlock abort conditions here.
- Include leakage current, arcing, pressure spikes, or thermal excursions.

### Data Types Expected
- Oscilloscope traces
- Digital UI logging
- MCP images
- Raw MCP hit files
- Other:

## Planned Runs

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Run",
  run.run_id as "Run ID",
  run.mode as "Mode",
  specimen.id as "Specimen ID",
  run.status as "Status",
  file.mtime as "Modified"
FROM #experiment-run AND !"assets"
WHERE run.series_name = this.series.name
SORT file.mtime DESC
\`\`\`

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(tp, noteContent, seriesName, folder, return_type);
}

module.exports = new_experiment_series;
