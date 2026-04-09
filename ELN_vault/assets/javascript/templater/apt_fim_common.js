function getSettings() {
  const settingsPath = "assets/ELN Settings.md";
  const settingsFile = app.vault.getAbstractFileByPath(settingsPath);
  if (!settingsFile) {
    throw new Error(`Could not find settings file at ${settingsPath}.`);
  }

  return app.metadataCache.getFileCache(settingsFile).frontmatter || {};
}

function getNested(obj, ...keys) {
  let current = obj;

  for (const key of keys) {
    if (current == null || !Object.prototype.hasOwnProperty.call(current, key)) {
      return null;
    }

    current = current[key];
  }

  return current;
}

function getFolder(settings, key, fallback) {
  return getNested(settings, "folder", key) || fallback;
}

function getToday() {
  return new Date().toISOString().split("T")[0];
}

function sanitizeFileName(value) {
  return String(value || "")
    .replace(/[\\/:*?"<>|]/g, "-")
    .replace(/\s+/g, " ")
    .trim();
}

function slugify(value) {
  return sanitizeFileName(value).replace(/\s+/g, "_");
}

function yamlString(value, fallback = "") {
  const raw = value == null || value === "" ? fallback : String(value);
  return `"${raw
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/\r?\n/g, " ")
    .trim()}"`;
}

function getDataviewPageNames(query) {
  const dataview = app.plugins.plugins.dataview?.api;
  if (!dataview) {
    return [];
  }

  return dataview
    .pages(query)
    .sort((page) => page.file.name, "asc")
    .map((page) => String(page.file.name))
    .values;
}

async function chooseFromList(tp, list, prompt, manualPrompt) {
  const options = (list || []).filter(Boolean);
  const manualOption = "Enter manually...";

  if (options.length > 0) {
    const selection = await tp.system.suggester(
      [...options, manualOption],
      [...options, manualOption],
      false,
      prompt
    );

    if (selection && selection !== manualOption) {
      return selection;
    }
  }

  return (await tp.system.prompt(manualPrompt, "")) || "";
}

async function chooseYesNo(tp, prompt, defaultValue = "No") {
  return (
    (await tp.system.suggester(["Yes", "No"], ["Yes", "No"], false, prompt)) ||
    defaultValue
  );
}

async function ensureFolderPath(folderPath) {
  const parts = String(folderPath || "")
    .split("/")
    .filter(Boolean);

  let currentPath = "";
  for (const part of parts) {
    currentPath = currentPath ? `${currentPath}/${part}` : part;
    if (!app.vault.getAbstractFileByPath(currentPath)) {
      await app.vault.createFolder(currentPath);
    }
  }
}

async function finalizeNote(tp, noteContent, filename, folderPath, returnType) {
  await ensureFolderPath(folderPath);

  const safeFilename = sanitizeFileName(filename);
  const activeFile = app.workspace.getActiveFile();

  if (returnType === undefined && activeFile) {
    const activeContent = await app.vault.read(activeFile);
    returnType = activeContent === "" ? "insert" : "create";
  } else if (returnType === undefined) {
    returnType = "create";
  }

  if (returnType === "insert" && activeFile) {
    const newFilePath = `${folderPath}/${safeFilename}.md`;
    await app.vault.rename(activeFile, newFilePath);
    return noteContent;
  }

  const targetFolder = app.vault.getAbstractFileByPath(folderPath);
  await tp.file.create_new(noteContent, safeFilename, true, targetFolder);
  return "";
}

module.exports = {
  chooseFromList,
  chooseYesNo,
  finalizeNote,
  getDataviewPageNames,
  getFolder,
  getNested,
  getSettings,
  getToday,
  sanitizeFileName,
  slugify,
  yamlString,
};
