const common = require("./apt_fim_common");

function getSpecimenFrontmatter(specimenMeta) {
  return specimenMeta?.specimen || {};
}

async function new_specimen(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const operator = await tp.user.get_operator(tp);
  const dateCreated = common.getToday();

  const specimenTypes =
    common.getNested(settings, "specimen", "type") || [
      "APT needle",
      "FIM tip",
      "reference specimen",
      "calibration specimen",
    ];

  const specimenId = await tp.system.prompt("Enter specimen ID:", "");
  if (!specimenId) {
    return "";
  }

  const specimenType = await common.chooseFromList(
    tp,
    specimenTypes,
    "Select specimen type:",
    "Enter specimen type:"
  );
  const specimenName = await tp.system.prompt(
    "Enter specimen note name:",
    specimenId
  );
  const material = await tp.system.prompt(
    "Enter the specimen material or material system:",
    ""
  );
  const preparationState = await tp.system.prompt(
    "Enter the specimen preparation state:",
    "ready for loading"
  );
  const storageLocation = await tp.system.prompt(
    "Enter the storage location:",
    ""
  );

  const folder = common.getFolder(settings, "specimens", "Specimens");

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
cssclasses:
  - wide-page
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: specimen
tags:
  - "#specimen"
specimen:
  name: ${common.yamlString(specimenName)}
  id: ${common.yamlString(specimenId)}
  type: ${common.yamlString(specimenType, "APT needle")}
  material: ${common.yamlString(material, "Add the material system or specimen composition.")}
  preparation_state: ${common.yamlString(preparationState, "ready for loading")}
  operator: ${common.yamlString(operator.name)}
  storage_location: ${common.yamlString(
    storageLocation,
    "Document where the specimen is stored between runs."
  )}
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Specimen Summary

- **Specimen ID:** ${specimenId}
- **Type:** ${specimenType || "Add a specimen type."}
- **Material:** ${material || "Add the specimen material or material system."}
- **Preparation state:** ${preparationState || "Describe the current preparation state."}

## Preparation Notes

- Geometry and mounting details:
- Sharpening or preparation history:
- Transfer or storage constraints:

## Handling Notes

- Vacuum compatibility notes:
- Special precautions:
- Damage or contamination history:

## Linked Experiment Runs

\`\`\`dataview
TABLE WITHOUT ID
  file.link as "Run",
  run.series_name as "Series",
  run.mode as "Mode",
  run.status as "Status",
  file.mtime as "Modified"
FROM #experiment-run AND !"assets"
WHERE specimen.id = this.specimen.id
SORT file.mtime DESC
\`\`\`

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(
    tp,
    noteContent,
    specimenName,
    folder,
    return_type
  );
}

module.exports = new_specimen;
