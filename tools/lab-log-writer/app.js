const state = {
  options: {},
  activeForm: "experiment-log",
  collapsedGroups: {},
  resourceFiles: [],
  resourcePresets: [],
  selectedResourcePaths: {},
  resourcePreviewPath: "",
  resourceTopicTitle: "",
  resourceConfig: {
    provider: "ollama",
    baseUrl: "",
    apiKey: "",
    model: "",
    embeddingModel: "",
    generateEmbeddings: false,
  },
  intakeScanLoading: false,
  intakeProcessLoading: false,
  intakeScanError: "",
  intakeProcessError: "",
  intakeLastScan: null,
  intakeLastProcess: null,
};

const SIDEBAR_STATE_KEY = "lab-log-writer-sidebar";
const DEFAULT_GROUP_STATE = {
  daily: false,
  experiment: false,
  reference: false,
  operations: false,
};

const formConfigs = {
  "experiment-series": {
    title: "Experiment Series",
    description: "Create the planning record for an integration campaign or test program.",
    sections: [
      {
        title: "Series Details",
        fields: [
          { name: "seriesName", label: "Experiment Series Name", type: "text" },
          { name: "abbreviation", label: "Series Abbreviation", type: "text" },
          { name: "seriesType", label: "Series Type", type: "select", optionsKey: "experimentSeriesTypes" },
          { name: "seriesStatus", label: "Series Status", type: "select", optionsKey: "experimentSeriesStatuses" },
          { name: "purpose", label: "Purpose", type: "textarea", rows: 4 },
          { name: "independentVariables", label: "Independent Variables", type: "textarea", rows: 3 },
          { name: "dependentVariables", label: "Dependent Variables", type: "textarea", rows: 3 },
        ],
      },
    ],
  },
  "experiment-log": {
    title: "Experiment Log",
    description: "Create the main experiment/session record that links specimens, configurations, and image logs.",
    sections: [
      {
        title: "Core Record",
        fields: [
          { name: "logId", label: "Log ID (optional)", type: "text", placeholder: "Auto-generated if left blank" },
          { name: "seriesName", label: "Experiment Series Name", type: "datalist", optionsKey: "seriesNames" },
          { name: "seriesNumber", label: "Experiment Number in Series", type: "text" },
          { name: "dateTime", label: "Date / Time", type: "datetime-local" },
          { name: "operators", label: "Operators", type: "comma-list", placeholder: "StarDustX, Operator 2" },
          { name: "status", label: "Status", type: "select", optionsKey: "experimentLogStatuses" },
          { name: "instrumentConfiguration", label: "Instrument Configuration", type: "datalist", optionsKey: "instrumentConfigurations" },
          { name: "instrumentCondition", label: "Instrument Condition Summary", type: "text" },
          { name: "specimenType", label: "Specimen Type", type: "text", placeholder: "APT needle, FIM tip, etc." },
          { name: "specimenId", label: "Specimen ID", type: "text" },
          { name: "ionColumnUsed", label: "Ion Column Used?", type: "select", options: ["Yes", "No"] },
          { name: "loadLockVented", label: "Load Lock Vented?", type: "select", options: ["Yes", "No"] },
        ],
      },
      {
        title: "Instrument Condition",
        fields: [
          { name: "mainChamberStartingPressure", label: "Main Chamber Starting Pressure", type: "text" },
          { name: "mainChamberEndingPressure", label: "Main Chamber Ending Pressure", type: "text" },
          { name: "mainIonPumpCurrent", label: "Main Ion Pump Current", type: "text" },
          { name: "mainIonPumpPressure", label: "Main Ion Pump Pressure", type: "text" },
          { name: "puckNestTemperature", label: "Puck Nest Temperature", type: "text" },
          { name: "cryoSetpoint", label: "Cryo Setpoint", type: "text" },
          { name: "loadLockStartingPressure", label: "Load Lock Starting Pressure", type: "text" },
          { name: "loadLockEndingPressure", label: "Load Lock Ending Pressure", type: "text" },
          { name: "ionColumnStartingPressure", label: "Ion Column Starting Pressure", type: "text" },
          { name: "ionColumnEndingPressure", label: "Ion Column Ending Pressure", type: "text" },
          { name: "ionColumnIonPumpCurrent", label: "Ion Column Ion Pump Current", type: "text" },
          { name: "ionColumnIonPumpPressure", label: "Ion Column Ion Pump Pressure", type: "text" },
          { name: "gasesIntroduced", label: "Gasses Introduced into Main Chamber", type: "multi-checkbox", optionsKey: "gases" },
        ],
      },
      {
        title: "Experiment Description",
        fields: [
          { name: "experimentDescription", label: "Description", type: "textarea", rows: 5 },
          { name: "independentVariableRange", label: "Independent Variable Range", type: "text" },
          { name: "dependentMeasurementRange", label: "Dependent Variable Measurement Range", type: "text" },
          { name: "emergencyStopParameters", label: "Emergency Stop Parameters", type: "text" },
          { name: "dataTypesRecorded", label: "Data Types Recorded", type: "multi-checkbox", optionsKey: "experimentLogDataTypes" },
          { name: "alignmentSettingsFileLink", label: "Alignment Settings File Link", type: "text" },
        ],
      },
      {
        title: "Raw Data Files",
        fields: [
          {
            name: "rawDataFiles",
            label: "Raw Data File Table",
            type: "repeatable-table",
            columns: ["File Name", "File Type", "Link / Location"],
          },
          { name: "experimentNotes", label: "Experiment Notes", type: "textarea", rows: 6 },
        ],
      },
    ],
  },
  "mcp-image-log": {
    title: "MCP Image Log",
    description: "Use one note per MCP image captured.",
    sections: [
      {
        title: "Core Record",
        fields: [
          { name: "fileName", label: "Note File Name (optional)", type: "text", placeholder: "Auto-generated if left blank" },
          { name: "parentExperimentLog", label: "Parent Experiment Log", type: "datalist", optionsKey: "experimentLogs" },
          { name: "experimentSeriesNumber", label: "Experiment Series / Number", type: "text" },
          { name: "dateTime", label: "Date / Time", type: "datetime-local" },
          { name: "imageSequenceNumber", label: "Image Sequence Number", type: "text" },
          { name: "status", label: "Status", type: "select", optionsKey: "mcpStatuses" },
        ],
      },
      {
        title: "MCP Image Parameters",
        fields: [
          { name: "mcpFrontVoltage", label: "MCP Front Voltage", type: "text" },
          { name: "mcpBackVoltage", label: "MCP Back Voltage", type: "text" },
          { name: "integrationTime", label: "Integration Time", type: "text" },
          { name: "specimenStageHv", label: "Specimen Stage HV", type: "text" },
          { name: "mainChamberPressure", label: "Main Chamber Pressure", type: "text" },
          { name: "ionColumnSettings", label: "Ion Column Settings", type: "text" },
          { name: "imagingGasUsed", label: "Imaging Gas Used", type: "select", optionsKey: "gases" },
          { name: "imageFileName", label: "Image File Name", type: "text" },
          { name: "imageFileLink", label: "Image File Link / Location", type: "text" },
          { name: "notes", label: "Notes", type: "textarea", rows: 5 },
        ],
      },
    ],
  },
  "ion-column-image-log": {
    title: "Ion Column Image Log",
    description: "Use one note per ion column image captured.",
    sections: [
      {
        title: "Core Record",
        fields: [
          { name: "fileName", label: "Note File Name (optional)", type: "text", placeholder: "Auto-generated if left blank" },
          { name: "parentExperimentLog", label: "Parent Experiment Log", type: "datalist", optionsKey: "experimentLogs" },
          { name: "experimentSeriesNumber", label: "Experiment Series / Number", type: "text" },
          { name: "dateTime", label: "Date / Time", type: "datetime-local" },
          { name: "imageSequenceNumber", label: "Image Sequence Number", type: "text" },
          { name: "status", label: "Status", type: "select", optionsKey: "ionStatuses" },
        ],
      },
      {
        title: "Ion Column Image Parameters",
        fields: [
          { name: "acceleratingVoltage", label: "Accelerating Voltage", type: "text" },
          { name: "sourcePressure", label: "Source Pressure", type: "text" },
          { name: "apertureNumber", label: "Aperture Number / Diameter", type: "text" },
          { name: "fieldOfView", label: "Field of View", type: "text" },
          { name: "pixelDwellTime", label: "Pixel Dwell Time", type: "text" },
          { name: "signalSource", label: "Signal Source", type: "select", optionsKey: "ionSignalSources" },
          { name: "imageFileName", label: "Image File Name", type: "text" },
          { name: "imageFileLink", label: "Image File Link / Location", type: "text" },
          { name: "signalOnlyImageFileName", label: "Signal-Only Image File Name", type: "text" },
          { name: "signalOnlyImageFileLink", label: "Signal-Only Image Link / Location", type: "text" },
          { name: "notes", label: "Notes", type: "textarea", rows: 5 },
        ],
      },
    ],
  },
  "instrument-configuration": {
    title: "Instrument Configuration",
    description: "Create a reusable configuration note from the same GUI.",
    sections: [
      {
        title: "Core Record",
        fields: [
          { name: "configurationName", label: "Configuration Name", type: "text" },
          { name: "configurationType", label: "Configuration Type", type: "select", optionsKey: "instrumentConfigTypes" },
          { name: "configurationStatus", label: "Status", type: "text", placeholder: "active" },
          { name: "instrumentName", label: "Instrument Name", type: "text", placeholder: "Hybrid FIM/APT Tool" },
          { name: "alignmentSettingsFile", label: "Alignment Settings File", type: "text" },
        ],
      },
      {
        title: "Gauge Mapping And Targets",
        fields: [
          { name: "mainChamberGauge", label: "Main Chamber Gauge", type: "text", optionValue: "gauges.mainChamber" },
          { name: "loadLockGauge", label: "Load Lock Gauge", type: "text", optionValue: "gauges.loadLock" },
          { name: "ionColumnGauge", label: "Ion Column Gauge", type: "text", optionValue: "gauges.ionColumn" },
          { name: "mainIonPumpLabel", label: "Main Ion Pump Label", type: "text", placeholder: "Main Ion Pump" },
          { name: "ionColumnIonPumpLabel", label: "Ion Column Ion Pump Label", type: "text", placeholder: "Ion Column Ion Pump" },
          { name: "mainChamberTargetPressure", label: "Main Chamber Target Pressure", type: "text" },
          { name: "loadLockTargetPressure", label: "Load Lock Target Pressure", type: "text" },
          { name: "ionColumnTargetPressure", label: "Ion Column Target Pressure", type: "text" },
          { name: "mainIonPumpTargetCurrent", label: "Main Ion Pump Target Current", type: "text" },
          { name: "ionColumnIonPumpTargetCurrent", label: "Ion Column Ion Pump Target Current", type: "text" },
          { name: "puckNestTargetTemperature", label: "Puck Nest Target Temperature", type: "text" },
          { name: "cryoTarget", label: "Cryo Target", type: "text" },
        ],
      },
      {
        title: "Interlocks And Imaging",
        fields: [
          { name: "vacuumInterlocksActive", label: "Vacuum Interlocks Active", type: "text" },
          { name: "highVoltageInterlocksActive", label: "High-Voltage Interlocks Active", type: "text" },
          { name: "mcpProtectionActive", label: "MCP Protection Active", type: "text" },
          { name: "ionColumnProtectionActive", label: "Ion Column Protection Active", type: "text" },
          { name: "safetiesBypassed", label: "Safeties Intentionally Bypassed", type: "text" },
          { name: "requiredStopConditions", label: "Required Stop Conditions", type: "text" },
          { name: "mcpFrontVoltageDefault", label: "MCP Front Voltage Default", type: "text" },
          { name: "mcpBackVoltageDefault", label: "MCP Back Voltage Default", type: "text" },
          { name: "specimenStageHvDefault", label: "Specimen Stage HV Default", type: "text" },
          { name: "ionColumnAcceleratingVoltageDefault", label: "Ion Column Accelerating Voltage Default", type: "text" },
          { name: "ionColumnSourcePressureDefault", label: "Ion Column Source Pressure Default", type: "text" },
          { name: "preferredImageExportFormat", label: "Preferred Image Export Format", type: "text" },
          { name: "preferredSignalSource", label: "Preferred Signal Source", type: "text" },
          { name: "operatingNotes", label: "Operating Notes", type: "textarea", rows: 5 },
        ],
      },
    ],
  },
  specimen: {
    title: "Specimen",
    description: "Create a specimen note from the GUI writer.",
    sections: [
      {
        title: "Specimen Details",
        fields: [
          { name: "specimenId", label: "Specimen ID", type: "text" },
          { name: "specimenName", label: "Specimen Note Name", type: "text" },
          { name: "specimenType", label: "Specimen Type", type: "select", optionsKey: "specimenTypes" },
          { name: "material", label: "Material", type: "text" },
          { name: "preparationState", label: "Preparation State", type: "text" },
          { name: "storageLocation", label: "Storage Location", type: "text" },
          { name: "preparationNotes", label: "Preparation Notes", type: "textarea", rows: 4 },
          { name: "handlingNotes", label: "Handling Notes", type: "textarea", rows: 4 },
        ],
      },
    ],
  },
  contact: {
    title: "Contact",
    description: "Create a contact note from the GUI writer.",
    sections: [
      {
        title: "Contact Details",
        fields: [
          { name: "noteName", label: "Note Name (optional)", type: "text", placeholder: "Defaults to Given + Family name" },
          { name: "title", label: "Title", type: "text" },
          { name: "givenName", label: "Given Name", type: "text" },
          { name: "familyName", label: "Family Name", type: "text" },
          { name: "workEmail", label: "Work Email", type: "text" },
          { name: "workPhone", label: "Work Phone", type: "text" },
          { name: "mobile", label: "Mobile", type: "text" },
          { name: "fax", label: "Fax", type: "text" },
          { name: "affiliation", label: "Affiliation", type: "text" },
          { name: "division", label: "Division", type: "text" },
          { name: "street", label: "Street", type: "text" },
          { name: "building", label: "Building", type: "text" },
          { name: "room", label: "Room", type: "text" },
          { name: "city", label: "City", type: "text" },
          { name: "zipCode", label: "Zip Code", type: "text" },
          { name: "country", label: "Country", type: "text" },
          { name: "jobPosition", label: "Job Position", type: "text" },
          { name: "group", label: "Group", type: "text" },
        ],
      },
    ],
  },
  "resource-library": {
    title: "Resources",
    description: "Scan APT/FIM PDFs, extract text, generate summaries, and synthesize topic notes into the vault.",
    customRenderer: "resources",
    sections: [],
  },
  "daily-note": {
    title: "Daily Note",
    description: "Create a daily note in the dated daily-notes folder structure.",
    sections: [
      {
        title: "Daily Note",
        fields: [
          { name: "notes", label: "Starting Notes (optional)", type: "textarea", rows: 8, placeholder: "Optional notes to seed today's entry." },
        ],
      },
    ],
  },
  meeting: {
    title: "Meeting",
    description: "Create a dated meeting note in the meetings archive.",
    sections: [
      {
        title: "Meeting Details",
        fields: [
          { name: "meetingTitle", label: "Meeting Title", type: "text" },
          { name: "meetingType", label: "Meeting Type", type: "text", placeholder: "Group meeting, review, planning..." },
          { name: "location", label: "Location", type: "text" },
          { name: "participants", label: "Participants", type: "comma-list", placeholder: "StarDustX, Participant 2" },
          { name: "projectName", label: "Project / Series", type: "text" },
        ],
      },
    ],
  },
  note: {
    title: "Note",
    description: "Create a general note in the Notes folder.",
    sections: [
      {
        title: "Note Details",
        fields: [
          { name: "noteName", label: "Note Name", type: "text", placeholder: "Untitled" },
          { name: "body", label: "Initial Body (optional)", type: "textarea", rows: 10 },
        ],
      },
    ],
  },
  "task-list": {
    title: "Task List",
    description: "Create a reusable task list note in the Tasks folder.",
    sections: [
      {
        title: "Task List Details",
        fields: [
          { name: "taskListName", label: "Task List Name", type: "text", placeholder: "My Tasks" },
        ],
      },
    ],
  },
  "startup-checklist": {
    title: "Startup Checklist",
    description: "Create a reusable startup checklist note.",
    sections: [
      {
        title: "Checklist Details",
        fields: [
          { name: "checklistName", label: "Checklist Name", type: "text", placeholder: "APT FIM Startup Checklist" },
          { name: "configurationName", label: "Associated Instrument Configuration", type: "datalist", optionsKey: "instrumentConfigurations" },
          { name: "status", label: "Status", type: "text", placeholder: "active" },
          { name: "notes", label: "Startup Notes", type: "textarea", rows: 5 },
        ],
      },
    ],
  },
  "shutdown-checklist": {
    title: "Shutdown Checklist",
    description: "Create a reusable shutdown checklist note.",
    sections: [
      {
        title: "Checklist Details",
        fields: [
          { name: "checklistName", label: "Checklist Name", type: "text", placeholder: "APT FIM Shutdown Checklist" },
          { name: "configurationName", label: "Associated Instrument Configuration", type: "datalist", optionsKey: "instrumentConfigurations" },
          { name: "status", label: "Status", type: "text", placeholder: "active" },
          { name: "notes", label: "Shutdown Notes", type: "textarea", rows: 5 },
        ],
      },
    ],
  },
};

const formSections = document.getElementById("form-sections");
const formTitle = document.getElementById("form-title");
const formDescription = document.getElementById("form-description");
const form = document.getElementById("entry-form");
const message = document.getElementById("message");
const serverStatus = document.getElementById("server-status");
const formActions = document.querySelector(".form-actions");

function loadSidebarState() {
  try {
    const raw = window.localStorage.getItem(SIDEBAR_STATE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return { ...DEFAULT_GROUP_STATE, ...parsed };
  } catch (error) {
    return { ...DEFAULT_GROUP_STATE };
  }
}

function saveSidebarState() {
  window.localStorage.setItem(SIDEBAR_STATE_KEY, JSON.stringify(state.collapsedGroups));
}

function applySidebarState() {
  document.querySelectorAll(".nav-group").forEach((group) => {
    const groupKey = group.dataset.group;
    const collapsed = Boolean(state.collapsedGroups[groupKey]);
    group.classList.toggle("collapsed", collapsed);

    const toggle = group.querySelector(".nav-group-toggle");
    if (toggle) {
      toggle.setAttribute("aria-expanded", String(!collapsed));
    }
  });
}

function expandActiveGroup() {
  const activeButton = document.querySelector(`.nav-button[data-form="${state.activeForm}"]`);
  if (!activeButton) return;

  const group = activeButton.closest(".nav-group");
  if (!group) return;

  const groupKey = group.dataset.group;
  if (!groupKey) return;

  state.collapsedGroups[groupKey] = false;
  saveSidebarState();
  applySidebarState();
}

function toggleGroup(groupKey) {
  state.collapsedGroups[groupKey] = !state.collapsedGroups[groupKey];
  saveSidebarState();
  applySidebarState();
}

function currentLocalDateTimeValue() {
  const now = new Date();
  const offset = now.getTimezoneOffset();
  const local = new Date(now.getTime() - offset * 60 * 1000);
  return local.toISOString().slice(0, 16);
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function syncResourceSelections() {
  for (const file of state.resourceFiles) {
    if (!(file.pdf_rel_path in state.selectedResourcePaths)) {
      state.selectedResourcePaths[file.pdf_rel_path] = false;
    }
  }
  if (
    state.resourcePreviewPath &&
    !state.resourceFiles.some((file) => file.pdf_rel_path === state.resourcePreviewPath)
  ) {
    state.resourcePreviewPath = "";
  }
  if (!state.resourcePreviewPath && state.resourceFiles.length) {
    state.resourcePreviewPath = state.resourceFiles[0].pdf_rel_path;
  }
}

function intakeQueueStatusCounts(intakeFiles) {
  const tallies = { pending: 0, processing: 0, done: 0, failed: 0 };
  for (const file of intakeFiles || []) {
    const key = String(file.status || "pending").toLowerCase();
    if (key in tallies) {
      tallies[key] += 1;
    } else {
      tallies.pending += 1;
    }
  }
  return tallies;
}

function intakeScanSummaryMarkup() {
  const scan = state.intakeLastScan;
  if (!scan) {
    return '<p class="resource-help">Click <strong>Scan Intake Folder</strong> to load the intake queue and folder totals.</p>';
  }
  const folders = scan.folders || {};
  const counts = scan.counts || {};
  const intakeFiles = scan.intakeFiles || [];
  const qc = intakeQueueStatusCounts(intakeFiles);
  const folderLines = [
    folders.pdfs && `<li>Intake / library root: <code>${escapeHtml(folders.pdfs)}</code></li>`,
    folders.processed && `<li>Processed bucket: <code>${escapeHtml(folders.processed)}</code></li>`,
    folders.failed && `<li>Failed bucket: <code>${escapeHtml(folders.failed)}</code></li>`,
  ]
    .filter(Boolean)
    .join("");

  const queueRows = intakeFiles.length
    ? intakeFiles
        .map((file) => {
          const err = file.errorMessage ? `<div class="resource-help">${escapeHtml(file.errorMessage)}</div>` : "";
          return `
            <tr>
              <td><code>${escapeHtml(file.pdf_rel_path || file.pdf_name || "")}</code></td>
              <td>${escapeHtml(file.status || "")}</td>
              <td>${file.has_summary ? escapeHtml(file.summary_name || "Yes") : "—"}</td>
              <td>${file.has_index ? "Yes" : "No"}</td>
              <td>${err || "—"}</td>
            </tr>
          `;
        })
        .join("")
    : '<tr><td colspan="5">No PDFs at the intake root (queue is empty).</td></tr>';

  return `
    <p class="resource-help">
      <strong>Scope note:</strong> Queue counts apply only to PDFs sitting in the library root.
      The processed/failed numbers below count <em>every</em> PDF under those bucket folders (recursive), including files from earlier runs or manual moves — they are not the same as the queue length.
    </p>
    ${folderLines ? `<ul class="resource-help">${folderLines}</ul>` : ""}
    <div class="resource-stats">
      <span class="resource-stat">Queue at root: ${intakeFiles.length}</span>
      <span class="resource-stat">Pending: ${qc.pending}</span>
      <span class="resource-stat">Processing: ${qc.processing}</span>
      <span class="resource-stat">Indexed (queue): ${counts.indexed ?? 0}</span>
      <span class="resource-stat">Embeddings (queue): ${counts.embedded ?? 0}</span>
    </div>
    <div class="resource-stats">
      <span class="resource-stat">PDFs in processed folder (recursive): ${counts.done ?? 0}</span>
      <span class="resource-stat">PDFs in failed folder (recursive): ${counts.failed ?? 0}</span>
      <span class="resource-stat">Summary notes (vault, all): ${counts.summaries ?? 0}</span>
    </div>
    <div class="resource-table-wrap">
      <table class="editable-table resource-table">
        <thead>
          <tr>
            <th>PDF (queue)</th>
            <th>Status</th>
            <th>Summary</th>
            <th>Indexed</th>
            <th>Error / detail</th>
          </tr>
        </thead>
        <tbody>${queueRows}</tbody>
      </table>
    </div>
  `;
}

function intakeProcessResultMarkup() {
  const run = state.intakeLastProcess;
  if (!run) {
    return "";
  }
  const resultRows = (run.results || []).length
    ? run.results
        .map((entry) => {
          const ok = entry.success;
          const pathCell = escapeHtml(entry.pdf_path || "");
          const errCell = entry.error ? escapeHtml(entry.error) : "—";
          return `
            <tr>
              <td>${ok ? "OK" : "Failed"}</td>
              <td><code>${pathCell}</code></td>
              <td>${errCell}</td>
            </tr>
          `;
        })
        .join("")
    : '<tr><td colspan="3">No PDFs were attempted in this run (queue may have been empty or already complete).</td></tr>';

  return `
    <div class="resource-stats">
      <span class="resource-stat">Last run — discovered: ${run.discovered ?? "—"}</span>
      <span class="resource-stat">Attempted: ${run.processed ?? "—"}</span>
      <span class="resource-stat">Succeeded: ${run.succeeded ?? "—"}</span>
      <span class="resource-stat">Failed: ${run.failed ?? "—"}</span>
    </div>
    <p class="resource-help">${escapeHtml(run.message || "")}</p>
    <p class="resource-help"><strong>Per-file results (this run only)</strong></p>
    <div class="resource-table-wrap">
      <table class="editable-table resource-table">
        <thead>
          <tr>
            <th>Outcome</th>
            <th>PDF path</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>${resultRows}</tbody>
      </table>
    </div>
  `;
}

async function fetchOptions() {
  try {
    const response = await fetch("./api/options");
    const data = await response.json();
    state.options = data;
    fetchResourcePresets();
    serverStatus.textContent = "Connected";
    serverStatus.classList.add("status-ok");
    renderForm(state.activeForm);
  } catch (error) {
    serverStatus.textContent = "Connection failed";
    serverStatus.classList.remove("status-ok");
    showMessage("Could not load lookup data from the writer server.", "error");
  }
}

async function fetchResourcePresets() {
  try {
    const response = await fetch("./api/resources/presets");
    const data = await response.json();
    state.resourcePresets = data.presets || [];
    if (state.activeForm === "resource-library") {
      renderResourcesPanel();
    }
  } catch (error) {
    state.resourcePresets = [];
  }
}

async function fetchResourceFiles(showErrors = true) {
  try {
    const response = await fetch("./api/resources/files");
    const data = await response.json();
    state.resourceFiles = data.files || [];
    syncResourceSelections();
    if (state.activeForm === "resource-library") {
      renderResourcesPanel();
    }
  } catch (error) {
    if (showErrors) {
      showMessage("Could not load PDF resource data from the writer server.", "error");
    }
  }
}

function getOptionValues(field) {
  if (field.options) return field.options;
  if (field.optionsKey) return state.options[field.optionsKey] || [];
  if (field.optionValue) {
    return field.optionValue.split(".").reduce((value, key) => (value ? value[key] : ""), state.options);
  }
  return [];
}

function createField(field) {
  const wrapper = document.createElement("div");
  wrapper.className = field.type === "textarea" || field.type === "repeatable-table" ? "field field-wide" : "field";

  const label = document.createElement("label");
  label.textContent = field.label;
  label.htmlFor = field.name;
  wrapper.appendChild(label);

  if (field.type === "textarea") {
    const input = document.createElement("textarea");
    input.name = field.name;
    input.id = field.name;
    input.rows = field.rows || 4;
    input.placeholder = field.placeholder || "";
    wrapper.appendChild(input);
    return wrapper;
  }

  if (field.type === "select") {
    const input = document.createElement("select");
    input.name = field.name;
    input.id = field.name;
    const blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "Select...";
    input.appendChild(blank);
    for (const option of getOptionValues(field)) {
      const optionEl = document.createElement("option");
      optionEl.value = option;
      optionEl.textContent = option;
      input.appendChild(optionEl);
    }
    wrapper.appendChild(input);
    return wrapper;
  }

  if (field.type === "datalist") {
    const input = document.createElement("input");
    const listId = `${field.name}-list`;
    input.type = "text";
    input.name = field.name;
    input.id = field.name;
    input.setAttribute("list", listId);
    input.placeholder = field.placeholder || "";
    const datalist = document.createElement("datalist");
    datalist.id = listId;
    for (const option of getOptionValues(field)) {
      const optionEl = document.createElement("option");
      optionEl.value = option;
      datalist.appendChild(optionEl);
    }
    wrapper.appendChild(input);
    wrapper.appendChild(datalist);
    return wrapper;
  }

  if (field.type === "multi-checkbox") {
    const container = document.createElement("div");
    container.className = "checkbox-group";
    for (const option of getOptionValues(field)) {
      const item = document.createElement("label");
      item.className = "checkbox-item";
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = field.name;
      checkbox.value = option;
      item.appendChild(checkbox);
      item.append(option);
      container.appendChild(item);
    }
    wrapper.appendChild(container);
    return wrapper;
  }

  if (field.type === "comma-list") {
    const input = document.createElement("input");
    input.type = "text";
    input.name = field.name;
    input.id = field.name;
    input.placeholder = field.placeholder || "";
    wrapper.appendChild(input);
    return wrapper;
  }

  if (field.type === "repeatable-table") {
    const tableContainer = document.createElement("div");
    tableContainer.className = "table-editor";
    tableContainer.dataset.name = field.name;

    const table = document.createElement("table");
    table.className = "editable-table";
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    field.columns.forEach((column) => {
      const th = document.createElement("th");
      th.textContent = column;
      headerRow.appendChild(th);
    });
    const actionsTh = document.createElement("th");
    actionsTh.textContent = "Actions";
    headerRow.appendChild(actionsTh);
    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    table.appendChild(tbody);
    tableContainer.appendChild(table);

    const addRow = document.createElement("button");
    addRow.type = "button";
    addRow.className = "secondary-button";
    addRow.textContent = "Add row";
    addRow.addEventListener("click", () => appendRepeatableRow(tbody));
    tableContainer.appendChild(addRow);

    wrapper.appendChild(tableContainer);
    appendRepeatableRow(tbody);
    return wrapper;
  }

  const input = document.createElement("input");
  input.type = field.type || "text";
  input.name = field.name;
  input.id = field.name;
  input.placeholder = field.placeholder || "";
  if (field.type === "datetime-local") {
    input.value = currentLocalDateTimeValue();
  }
  const optionValue = getOptionValues(field);
  if (typeof optionValue === "string" && optionValue) {
    input.value = optionValue;
  }
  wrapper.appendChild(input);
  return wrapper;
}

function appendRepeatableRow(tbody) {
  const template = document.getElementById("repeatable-row-template");
  const clone = template.content.cloneNode(true);
  clone.querySelector(".remove-row").addEventListener("click", (event) => {
    const row = event.target.closest("tr");
    row.remove();
    if (!tbody.querySelector("tr")) {
      appendRepeatableRow(tbody);
    }
  });
  tbody.appendChild(clone);
}

function selectedPdfPaths() {
  return state.resourceFiles
    .filter((file) => state.selectedResourcePaths[file.pdf_rel_path])
    .map((file) => file.pdf_rel_path);
}

function unsummarizedPdfPaths() {
  return state.resourceFiles.filter((file) => !file.has_summary).map((file) => file.pdf_rel_path);
}

function resourcePdfUrl(relativePath) {
  return `./api/resources/pdf?path=${encodeURIComponent(relativePath)}`;
}

function resourceConfigPayload(pdfsOverride = null) {
  state.resourceConfig = {
    provider: document.getElementById("resource-provider")?.value || "ollama",
    baseUrl: document.getElementById("resource-base-url")?.value.trim() || "",
    apiKey: document.getElementById("resource-api-key")?.value.trim() || "",
    model: document.getElementById("resource-model")?.value.trim() || "",
    embeddingModel: document.getElementById("resource-embedding-model")?.value.trim() || "",
    generateEmbeddings: Boolean(document.getElementById("resource-generate-embeddings")?.checked),
  };
  return {
    ...state.resourceConfig,
    pdfs: pdfsOverride || selectedPdfPaths(),
  };
}

function resourceRowMarkup(file) {
  const previewUrl = resourcePdfUrl(file.pdf_rel_path);
  return `
    <tr>
      <td><input type="checkbox" class="resource-checkbox" data-resource-path="${escapeHtml(file.pdf_rel_path)}" ${state.selectedResourcePaths[file.pdf_rel_path] ? "checked" : ""}></td>
      <td><code>${escapeHtml(file.pdf_rel_path)}</code></td>
      <td>${file.has_index ? "Yes" : "No"}</td>
      <td>${file.chunk_count || 0}</td>
      <td>${file.has_summary ? escapeHtml(file.summary_name) : "-"}</td>
      <td>${file.has_embeddings ? "Yes" : "No"}</td>
      <td>
        <button type="button" class="secondary-button resource-preview-button" data-resource-preview="${escapeHtml(file.pdf_rel_path)}">Preview</button>
        <a class="resource-open-link" href="${previewUrl}" target="_blank" rel="noreferrer">Open PDF</a>
      </td>
      <td>${escapeHtml(file.modified_at || "")}</td>
    </tr>
  `;
}

function renderResourcesPanel() {
  const summaryCount = state.resourceFiles.filter((file) => file.has_summary).length;
  const unsummarizedCount = state.resourceFiles.length - summaryCount;
  const selectedCount = selectedPdfPaths().length;
  const rows = state.resourceFiles.length
    ? state.resourceFiles.map(resourceRowMarkup).join("")
    : '<tr><td colspan="8">No PDFs found. Put files into <code>ELN_vault/Resources/APT-FIM/PDFs</code>, then click Scan PDFs.</td></tr>';
  const presetOptions = [
    '<option value="">Manual configuration</option>',
    ...state.resourcePresets.map(
      (preset) =>
        `<option value="${escapeHtml(preset.id)}">${escapeHtml(preset.label)}</option>`
    ),
  ].join("");
  const activePreset = state.resourcePresets.find(
    (preset) =>
      preset.provider === state.resourceConfig.provider &&
      preset.baseUrl === state.resourceConfig.baseUrl &&
      preset.model === state.resourceConfig.model &&
      preset.embeddingModel === state.resourceConfig.embeddingModel
  );
  const previewMarkup = state.resourcePreviewPath
    ? `
      <div class="resource-preview-shell">
        <div class="resource-preview-header">
          <div>
            <strong>Inline preview</strong>
            <div class="resource-preview-caption"><code>${escapeHtml(state.resourcePreviewPath)}</code></div>
          </div>
          <a class="resource-open-link" href="${resourcePdfUrl(state.resourcePreviewPath)}" target="_blank" rel="noreferrer">Open in new tab</a>
        </div>
        <iframe class="resource-preview-frame" src="${resourcePdfUrl(state.resourcePreviewPath)}" title="PDF preview"></iframe>
      </div>
    `
    : '<p class="resource-help">Choose a PDF preview to inspect it inline here.</p>';

  formSections.innerHTML = `
    <section class="form-section">
      <h3>PDF Library</h3>
      <p class="resource-help">Summaries are written into the vault so Obsidian can query them later.</p>
      <div class="resource-stats">
        <span class="resource-stat">PDFs: ${state.resourceFiles.length}</span>
        <span class="resource-stat">Summaries: ${summaryCount}</span>
        <span class="resource-stat">Unsummarized: ${unsummarizedCount}</span>
        <span class="resource-stat">Selected: ${selectedCount}</span>
      </div>

      <section class="form-section">
        <h3>Intake folder (batch)</h3>
        <p class="resource-help">
          Drop new PDFs in the library root. <strong>Scan Intake Folder</strong> refreshes the queue and bucket totals.
          <strong>Process Intake Folder</strong> ingests, summarizes, and moves each incomplete queue file using the provider settings below (same as manual ingest/summarize).
        </p>
        <div class="resource-actions">
          <button id="resource-intake-scan" type="button" class="secondary-button" ${state.intakeScanLoading || state.intakeProcessLoading ? "disabled" : ""}>
            ${state.intakeScanLoading ? "Scanning…" : "Scan Intake Folder"}
          </button>
          <button id="resource-intake-process" type="button" class="secondary-button" ${state.intakeScanLoading || state.intakeProcessLoading ? "disabled" : ""}>
            ${state.intakeProcessLoading ? "Processing…" : "Process Intake Folder"}
          </button>
        </div>
        ${state.intakeScanError ? `<p class="resource-help" role="alert"><strong>Intake scan error:</strong> ${escapeHtml(state.intakeScanError)}</p>` : ""}
        ${state.intakeProcessError ? `<p class="resource-help" role="alert"><strong>Intake process error:</strong> ${escapeHtml(state.intakeProcessError)}</p>` : ""}
        ${intakeScanSummaryMarkup()}
        ${intakeProcessResultMarkup()}
      </section>

      <div class="resource-grid">
        <label class="field">
          <span>Provider Preset</span>
          <select id="resource-preset">
            ${presetOptions}
          </select>
        </label>
        <label class="field">
          <span>Provider</span>
          <select id="resource-provider">
            <option value="ollama" ${state.resourceConfig.provider === "ollama" ? "selected" : ""}>Ollama</option>
            <option value="lmstudio" ${state.resourceConfig.provider === "lmstudio" ? "selected" : ""}>LM Studio</option>
            <option value="openai" ${state.resourceConfig.provider === "openai" ? "selected" : ""}>OpenAI</option>
            <option value="anthropic" ${state.resourceConfig.provider === "anthropic" ? "selected" : ""}>Anthropic</option>
          </select>
        </label>
        <label class="field">
          <span>Base URL</span>
          <input id="resource-base-url" type="text" placeholder="Optional custom API base URL" value="${escapeHtml(state.resourceConfig.baseUrl)}" />
        </label>
        <label class="field">
          <span>Model</span>
          <input id="resource-model" type="text" placeholder="Required for summaries and synthesis" value="${escapeHtml(state.resourceConfig.model)}" />
        </label>
        <label class="field">
          <span>Embedding Model</span>
          <input id="resource-embedding-model" type="text" placeholder="Optional unless embeddings are enabled" value="${escapeHtml(state.resourceConfig.embeddingModel)}" />
        </label>
        <label class="field field-wide">
          <span>API Key</span>
          <input id="resource-api-key" type="password" placeholder="Required for hosted providers" value="${escapeHtml(state.resourceConfig.apiKey)}" />
        </label>
      </div>

      <label class="resource-checkbox-inline">
        <input id="resource-generate-embeddings" type="checkbox" ${state.resourceConfig.generateEmbeddings ? "checked" : ""} />
        Generate embeddings during ingest
      </label>

      <div class="resource-actions">
        <button id="resource-scan" type="button" class="secondary-button">Scan PDFs</button>
        <button id="resource-ingest" type="button" class="secondary-button">Ingest Selected</button>
        <button id="resource-summarize" type="button" class="primary-button">Summarize Selected</button>
        <button id="resource-summarize-unsummarized" type="button" class="secondary-button">Summarize All Unsummarized</button>
      </div>

      <div class="resource-table-wrap">
        <table class="editable-table resource-table">
          <thead>
            <tr>
              <th>Select</th>
              <th>PDF</th>
              <th>Indexed</th>
              <th>Chunks</th>
              <th>Summary Note</th>
              <th>Embeddings</th>
              <th>Preview</th>
              <th>Modified</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </section>

    <section class="form-section">
      <h3>PDF Preview</h3>
      ${previewMarkup}
    </section>

    <section class="form-section">
      <h3>Topic Synthesis</h3>
      <div class="resource-grid">
        <label class="field field-wide">
          <span>Topic Title</span>
          <input id="resource-topic-title" type="text" placeholder="Example: FIM image interpretation" value="${escapeHtml(state.resourceTopicTitle)}" />
        </label>
      </div>
      <p class="resource-help">Use the selected PDFs' generated summary notes as synthesis sources.</p>
      <div class="resource-actions">
        <button id="resource-synthesize" type="button" class="primary-button">Synthesize Topic From Selected</button>
      </div>
    </section>
  `;

  document.querySelectorAll(".resource-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", (event) => {
      state.selectedResourcePaths[event.target.dataset.resourcePath] = event.target.checked;
      renderResourcesPanel();
    });
  });

  document.querySelectorAll(".resource-preview-button").forEach((button) => {
    button.addEventListener("click", (event) => {
      state.resourcePreviewPath = event.currentTarget.dataset.resourcePreview || "";
      renderResourcesPanel();
    });
  });

  document.getElementById("resource-preset")?.addEventListener("change", (event) => {
    const preset = state.resourcePresets.find((item) => item.id === event.target.value);
    if (!preset) {
      return;
    }
    state.resourceConfig = {
      ...state.resourceConfig,
      provider: preset.provider,
      baseUrl: preset.baseUrl || "",
      model: preset.model || "",
      embeddingModel: preset.embeddingModel || "",
    };
    renderResourcesPanel();
  });

  ["resource-provider", "resource-base-url", "resource-api-key", "resource-model", "resource-embedding-model", "resource-generate-embeddings"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", () => {
      resourceConfigPayload();
    });
    document.getElementById(id)?.addEventListener("input", () => {
      resourceConfigPayload();
    });
  });

  document.getElementById("resource-intake-scan")?.addEventListener("click", async () => {
    state.intakeScanLoading = true;
    state.intakeScanError = "";
    renderResourcesPanel();
    try {
      const response = await fetch("./api/resources/scan-intake", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await response.json();
      if (!response.ok) {
        state.intakeScanError = data.error || "Could not scan intake folder.";
        state.intakeLastScan = null;
        showMessage(state.intakeScanError, "error");
      } else {
        state.intakeLastScan = data;
        showMessage("Scanned the intake folder.", "success");
      }
    } catch {
      state.intakeScanError = "Could not scan intake folder.";
      state.intakeLastScan = null;
      showMessage(state.intakeScanError, "error");
    } finally {
      state.intakeScanLoading = false;
      renderResourcesPanel();
    }
  });

  document.getElementById("resource-intake-process")?.addEventListener("click", async () => {
    const payload = resourceConfigPayload();
    state.intakeProcessLoading = true;
    state.intakeProcessError = "";
    renderResourcesPanel();
    try {
      const response = await fetch("./api/resources/process-intake", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        state.intakeProcessError = data.error || "Could not process intake folder.";
        state.intakeLastProcess = null;
        showMessage(state.intakeProcessError, "error");
      } else {
        state.intakeLastProcess = {
          discovered: data.discovered,
          processed: data.processed,
          succeeded: data.succeeded,
          failed: data.failed,
          results: data.results || [],
          message: data.message || "",
        };
        if (data.status?.files) {
          state.resourceFiles = data.status.files;
          syncResourceSelections();
        }
        showMessage(data.message || "Intake processing completed.", "success");
        try {
          const scanResponse = await fetch("./api/resources/scan-intake", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({}),
          });
          const scanData = await scanResponse.json();
          if (scanResponse.ok) {
            state.intakeLastScan = scanData;
          }
        } catch {
          // leave prior intake scan snapshot
        }
      }
    } catch {
      state.intakeProcessError = "Could not process intake folder.";
      state.intakeLastProcess = null;
      showMessage(state.intakeProcessError, "error");
    } finally {
      state.intakeProcessLoading = false;
      renderResourcesPanel();
    }
  });

  document.getElementById("resource-scan")?.addEventListener("click", async () => {
    try {
      const response = await fetch("./api/resources/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await response.json();
      if (!response.ok) {
        showMessage(data.error || "Could not scan PDFs.", "error");
        return;
      }
      state.resourceFiles = data.files || data.status?.files || [];
      syncResourceSelections();
      renderResourcesPanel();
      showMessage("Scanned the PDF library.", "success");
    } catch (error) {
      showMessage("Could not scan the PDF library.", "error");
    }
  });

  document.getElementById("resource-ingest")?.addEventListener("click", () =>
    runResourceAction("./api/resources/ingest", "Could not ingest selected PDFs.")
  );
  document.getElementById("resource-summarize")?.addEventListener("click", () =>
    runResourceAction("./api/resources/summarize", "Could not summarize selected PDFs.")
  );
  document.getElementById("resource-summarize-unsummarized")?.addEventListener("click", () => {
    const pdfs = unsummarizedPdfPaths();
    if (!pdfs.length) {
      showMessage("Every discovered PDF already has a summary note.", "success");
      return;
    }
    runResourceAction(
      "./api/resources/summarize",
      "Could not summarize unsummarized PDFs.",
      resourceConfigPayload(pdfs)
    );
  });
  document.getElementById("resource-synthesize")?.addEventListener("click", () =>
    runResourceSynthesis()
  );
  document.getElementById("resource-topic-title")?.addEventListener("input", (event) => {
    state.resourceTopicTitle = event.target.value;
  });
  if (activePreset) {
    document.getElementById("resource-preset").value = activePreset.id;
  }
}

async function runResourceAction(endpoint, defaultError, payloadOverride = null) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payloadOverride || resourceConfigPayload()),
    });
    const data = await response.json();
    if (!response.ok) {
      showMessage(data.error || defaultError, "error");
      return;
    }
    if (data.status?.files) {
      state.resourceFiles = data.status.files;
      syncResourceSelections();
      renderResourcesPanel();
    }
    showMessage(data.message || "Resource action completed.", "success");
  } catch (error) {
    showMessage(defaultError, "error");
  }
}

async function runResourceSynthesis() {
  const selected = state.resourceFiles.filter((file) => state.selectedResourcePaths[file.pdf_rel_path] && file.has_summary);
  const payload = {
    ...resourceConfigPayload(),
    topicTitle: document.getElementById("resource-topic-title")?.value.trim() || state.resourceTopicTitle.trim() || "",
    summaryNotes: selected.map((file) => file.summary_name),
  };

  try {
    const response = await fetch("./api/resources/synthesize-topic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      showMessage(data.error || "Could not synthesize a topic note.", "error");
      return;
    }
    if (data.status?.files) {
      state.resourceFiles = data.status.files;
      syncResourceSelections();
      renderResourcesPanel();
    }
    showMessage(data.message || "Created topic synthesis note.", "success");
  } catch (error) {
    showMessage("Could not synthesize a topic note.", "error");
  }
}

function renderForm(formKey) {
  state.activeForm = formKey;
  const config = formConfigs[formKey];
  if (!config) return;

  document.querySelectorAll(".nav-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.form === formKey);
  });

  expandActiveGroup();

  formTitle.textContent = config.title;
  formDescription.textContent = config.description;
  formSections.innerHTML = "";

  if (config.customRenderer === "resources") {
    formActions.classList.add("hidden");
    renderResourcesPanel();
    fetchResourceFiles(false);

    const params = new URLSearchParams(window.location.search);
    if (params.get("form") !== formKey) {
      params.set("form", formKey);
      const nextUrl = `${window.location.pathname}?${params.toString()}`;
      window.history.replaceState({}, "", nextUrl);
    }
    return;
  }

  formActions.classList.remove("hidden");

  for (const section of config.sections) {
    const sectionEl = document.createElement("section");
    sectionEl.className = "form-section";

    const heading = document.createElement("h3");
    heading.textContent = section.title;
    sectionEl.appendChild(heading);

    const grid = document.createElement("div");
    grid.className = "form-grid";

    for (const field of section.fields) {
      grid.appendChild(createField(field));
    }

    sectionEl.appendChild(grid);
    formSections.appendChild(sectionEl);
  }

  const params = new URLSearchParams(window.location.search);
  if (params.get("form") !== formKey) {
    params.set("form", formKey);
    const nextUrl = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState({}, "", nextUrl);
  }
}

function collectFormData() {
  const config = formConfigs[state.activeForm];
  const payload = { formType: state.activeForm };

  for (const section of config.sections) {
    for (const field of section.fields) {
      if (field.type === "multi-checkbox") {
        payload[field.name] = Array.from(document.querySelectorAll(`input[name="${field.name}"]:checked`)).map(
          (input) => input.value
        );
        continue;
      }
      if (field.type === "comma-list") {
        const value = document.getElementById(field.name).value.trim();
        payload[field.name] = value ? value.split(",").map((item) => item.trim()).filter(Boolean) : [];
        continue;
      }
      if (field.type === "repeatable-table") {
        payload[field.name] = Array.from(document.querySelectorAll(`[data-name="${field.name}"] tbody tr`)).map((row) => {
          const inputs = row.querySelectorAll("input");
          return {
            fileName: inputs[0].value.trim(),
            fileType: inputs[1].value.trim(),
            link: inputs[2].value.trim(),
          };
        });
        continue;
      }
      const input = document.getElementById(field.name);
      if (!input) continue;
      payload[field.name] = input.value.trim();
    }
  }

  return payload;
}

async function handleSubmit(event) {
  event.preventDefault();
  const payload = collectFormData();

  try {
    const response = await fetch("./api/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      showMessage(data.error || "Could not create the note.", "error");
      return;
    }
    showMessage(`Created ${data.fileName} in ${data.path}`, "success");
    form.reset();
    renderForm(state.activeForm);
    fetchOptions();
  } catch (error) {
    showMessage("Could not send note data to the writer server.", "error");
  }
}

function showMessage(text, type) {
  message.textContent = text;
  message.className = `message ${type}`;
}

document.querySelectorAll(".nav-button").forEach((button) => {
  button.addEventListener("click", () => renderForm(button.dataset.form));
});

document.querySelectorAll(".nav-group-toggle").forEach((button) => {
  button.addEventListener("click", () => toggleGroup(button.closest(".nav-group").dataset.group));
});

document.getElementById("refresh-options").addEventListener("click", fetchOptions);
form.addEventListener("submit", handleSubmit);

const params = new URLSearchParams(window.location.search);
state.activeForm = params.get("form") || "experiment-log";
state.collapsedGroups = loadSidebarState();
applySidebarState();
fetchOptions();
