const state = {
  options: {},
  activeForm: "experiment-log",
  collapsedGroups: {},
  resourceFiles: [],
  selectedResourcePaths: {},
  resourceConfig: {
    provider: "ollama",
    baseUrl: "",
    apiKey: "",
    model: "",
    embeddingModel: "",
    generateEmbeddings: false,
  },
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
}

async function fetchOptions() {
  try {
    const response = await fetch("./api/options");
    const data = await response.json();
    state.options = data;
    serverStatus.textContent = "Connected";
    serverStatus.classList.add("status-ok");
    renderForm(state.activeForm);
  } catch (error) {
    serverStatus.textContent = "Connection failed";
    serverStatus.classList.remove("status-ok");
    showMessage("Could not load lookup data from the writer server.", "error");
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

function resourceConfigPayload() {
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
    pdfs: selectedPdfPaths(),
  };
}

function resourceRowMarkup(file) {
  return `
    <tr>
      <td><input type="checkbox" class="resource-checkbox" data-resource-path="${escapeHtml(file.pdf_rel_path)}" ${state.selectedResourcePaths[file.pdf_rel_path] ? "checked" : ""}></td>
      <td><code>${escapeHtml(file.pdf_rel_path)}</code></td>
      <td>${file.has_index ? "Yes" : "No"}</td>
      <td>${file.chunk_count || 0}</td>
      <td>${file.has_summary ? escapeHtml(file.summary_name) : "-"}</td>
      <td>${file.has_embeddings ? "Yes" : "No"}</td>
      <td>${escapeHtml(file.modified_at || "")}</td>
    </tr>
  `;
}

function renderResourcesPanel() {
  const rows = state.resourceFiles.length
    ? state.resourceFiles.map(resourceRowMarkup).join("")
    : '<tr><td colspan="7">No PDFs found. Put files into <code>ELN_vault/Resources/APT-FIM/PDFs</code>, then click Scan PDFs.</td></tr>';

  formSections.innerHTML = `
    <section class="form-section">
      <h3>PDF Library</h3>
      <p class="resource-help">Summaries are written into the vault so Obsidian can query them later.</p>

      <div class="resource-grid">
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
              <th>Modified</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </section>

    <section class="form-section">
      <h3>Topic Synthesis</h3>
      <div class="resource-grid">
        <label class="field field-wide">
          <span>Topic Title</span>
          <input id="resource-topic-title" type="text" placeholder="Example: FIM image interpretation" />
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
    });
  });

  ["resource-provider", "resource-base-url", "resource-api-key", "resource-model", "resource-embedding-model", "resource-generate-embeddings"].forEach((id) => {
    document.getElementById(id)?.addEventListener("change", () => {
      resourceConfigPayload();
    });
    document.getElementById(id)?.addEventListener("input", () => {
      resourceConfigPayload();
    });
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
  document.getElementById("resource-synthesize")?.addEventListener("click", () =>
    runResourceSynthesis()
  );
}

async function runResourceAction(endpoint, defaultError) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(resourceConfigPayload()),
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
    topicTitle: document.getElementById("resource-topic-title")?.value.trim() || "",
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
