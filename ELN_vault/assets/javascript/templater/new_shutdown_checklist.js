const common = require("./apt_fim_common");

async function new_shutdown_checklist(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const dateCreated = common.getToday();

  const configurationNames = common.getDataviewPageNames("#instrument-config AND !\"assets\"");
  const checklistName = await tp.system.prompt(
    "Enter shutdown checklist name:",
    "APT FIM Shutdown Checklist"
  );
  if (!checklistName) {
    return "";
  }

  const configurationName = await common.chooseFromList(
    tp,
    configurationNames,
    "Select associated instrument configuration:",
    "Enter associated instrument configuration:"
  );
  const folder = common.getFolder(
    settings,
    "shutdown checklists",
    "Checklists/Shutdown"
  );

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: shutdown-checklist
tags:
  - "#shutdown-checklist"
checklist:
  name: ${common.yamlString(checklistName)}
  phase: "shutdown"
  configuration_name: ${common.yamlString(configurationName, "Add configuration link")}
  status: "active"
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Shutdown Checklist

- [ ] Confirm data files have finished writing before shutdown.
- [ ] Record main chamber ending pressure from the ion gauge.
- [ ] Record load lock ending pressure from the LL wide range gauge.
- [ ] Record ion column ending pressure from the ion column wide range gauge.
- [ ] Record main ion pump current and inferred pressure.
- [ ] Record ion column ion pump current and inferred pressure if the column was used.
- [ ] Confirm gas introduction is isolated or shut off as required.
- [ ] Confirm HV, MCP, and ion column states are returned to their shutdown condition.
- [ ] Archive alignment settings and operator notes for the run.
- [ ] Document any abnormal shutdown behavior or follow-up actions.

## Shutdown Monitoring Table

| Parameter | Condition | Notes |
| --- | --- | --- |
| Main chamber ending pressure | | |
| Main ion pump current and pressure | | |
| Load lock ending pressure | | |
| Ion column ending pressure | | |
| Ion column ion pump current and pressure | | |
| Gas state | | |
| HV / MCP safe state confirmed | | |

## Shutdown Notes

- Cleanup actions:
- Data archival confirmation:
- Issues to revisit at the next startup:

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/note_footer", {});
\`\`\`
`;

  return common.finalizeNote(
    tp,
    noteContent,
    checklistName,
    folder,
    return_type
  );
}

module.exports = new_shutdown_checklist;
