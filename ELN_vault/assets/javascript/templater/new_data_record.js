const common = require("./apt_fim_common");

async function new_data_record(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const dateCreated = common.getToday();

  const runNames = common.getDataviewPageNames("#experiment-run AND !\"assets\"");
  const runName = await common.chooseFromList(
    tp,
    runNames,
    "Select experiment run:",
    "Enter experiment run name:"
  );
  const recordName = await tp.system.prompt(
    "Enter data record name:",
    `${runName || "Experiment Run"} Data Record`
  );
  if (!recordName) {
    return "";
  }

  const rawDataLocation = await tp.system.prompt(
    "Enter the raw data folder or archive link:",
    ""
  );

  const folder = common.getFolder(settings, "data records", "Data Records");

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
cssclasses:
  - wide-page
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: data-record
tags:
  - "#data-record"
data:
  run_name: ${common.yamlString(runName, "Link this record to an experiment run")}
  raw_data_location: ${common.yamlString(
    rawDataLocation,
    "Add the primary raw data folder or archive link."
  )}
  formatting_status: "draft"
  data_types_recorded:
    - "oscilloscope traces"
    - "digital logging"
    - "MCP images"
    - "raw MCP hit files"
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Data Record Summary

- **Experiment run:** ${runName || "Link this data record to an experiment run."}
- **Raw data location:** ${
    rawDataLocation || "Add the primary raw data folder or archive link."
  }

## Raw Data Inventory

| File / Folder | Type | Link | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## Alignment Settings Archive

- Link to archived alignment settings file:
- Notes about which settings were active during this run:

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
| Aperture number or diameter | |
| Field of view | |
| Pixel dwell time | |
| Signal source | |

## Plot Formatting Checklist

- [ ] Two-axis data saved as CSV with column headings.
- [ ] Axes labeled with units.
- [ ] Major and minor ticks added as appropriate.
- [ ] Separate symbols and colors used for different data sets.
- [ ] No smoothing or unnecessary connecting lines.
- [ ] Error bars added where relevant.
- [ ] Log scale used when data spans more than two orders of magnitude.
- [ ] Separate plots used instead of multiple y-axes where practical.

## Photo Formatting Checklist

- [ ] Caption states the purpose of the image.
- [ ] Relevant details are called out.
- [ ] Photographer or operator is recorded.
- [ ] Conditions at capture are documented.
- [ ] Full-resolution signal-only image is embedded or linked where required.

## Notes

- Additional data-handling notes:
- Missing files or follow-up actions:

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(
    tp,
    noteContent,
    recordName,
    folder,
    return_type
  );
}

module.exports = new_data_record;
