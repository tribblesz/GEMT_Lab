const common = require("./apt_fim_common");

async function new_startup_checklist(tp, return_type) {
  const settings = common.getSettings();
  const elnVersion = settings["ELN version"] || "0.5.0";
  const author = await tp.user.get_author(tp);
  const dateCreated = common.getToday();

  const configurationNames = common.getDataviewPageNames("#instrument-config AND !\"assets\"");
  const checklistName = await tp.system.prompt(
    "Enter startup checklist name:",
    "APT FIM Startup Checklist"
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
    "startup checklists",
    "Checklists/Startup"
  );

  const noteContent = `---
ELN version: ${common.yamlString(elnVersion)}
date created: ${common.yamlString(dateCreated)}
author: ${common.yamlString(author)}
note type: startup-checklist
tags:
  - "#startup-checklist"
checklist:
  name: ${common.yamlString(checklistName)}
  phase: "startup"
  configuration_name: ${common.yamlString(configurationName, "Add configuration link")}
  status: "active"
---

\`\`\`dataviewjs
await dv.view("/assets/javascript/dataview/views/navbar", {});
\`\`\`

# Startup Checklist

- [ ] Confirm the correct instrument configuration and alignment archive are selected.
- [ ] Verify all interlocks are in their expected state before pumpdown or HV enable.
- [ ] Record main chamber starting pressure from the ion gauge.
- [ ] Record load lock starting pressure from the LL wide range gauge.
- [ ] Record ion column starting pressure from the ion column wide range gauge.
- [ ] Record main ion pump current and inferred pressure.
- [ ] Record ion column ion pump current and inferred pressure if the column is active.
- [ ] Confirm puck nest temperature and cryo setpoint.
- [ ] Confirm gas lines and leak valves are in the expected pre-run state.
- [ ] Document any safeties bypassed for this startup.

## Startup Monitoring Table

| Parameter | Condition | Notes |
| --- | --- | --- |
| Main chamber starting pressure | | |
| Main ion pump current and pressure | | |
| Puck nest temperature | | |
| Cryo setpoint | | |
| Load lock starting pressure | | |
| Ion column starting pressure | | |
| Ion column ion pump current and pressure | | |
| Gases introduced into main chamber | | |

## Startup Notes

- Expected path to ready state:
- Known risks:
- Operator signoff:

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

module.exports = new_startup_checklist;
