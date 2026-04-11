const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function makeElement() {
  return {
    value: "",
    innerHTML: "",
    textContent: "",
    dataset: {},
    style: {},
    className: "",
    checked: false,
    appendChild() {},
    remove() {},
    setAttribute() {},
    getAttribute() {
      return null;
    },
    addEventListener() {},
    querySelector() {
      return null;
    },
    querySelectorAll() {
      return [];
    },
    closest() {
      return null;
    },
    cloneNode() {
      return makeElement();
    },
    classList: {
      add() {},
      remove() {},
      toggle() {},
    },
    content: {
      cloneNode() {
        return {
          querySelector() {
            return { addEventListener() {} };
          },
        };
      },
    },
  };
}

function loadAppContext() {
  const source = fs.readFileSync(path.join(__dirname, "..", "app.js"), "utf8");
  const documentStub = {
    getElementById() {
      return makeElement();
    },
    querySelector() {
      return makeElement();
    },
    querySelectorAll() {
      return [];
    },
    createElement() {
      return makeElement();
    },
  };
  const localStorageData = new Map();
  const context = {
    console,
    document: documentStub,
    window: {
      localStorage: {
        getItem(key) {
          return localStorageData.has(key) ? localStorageData.get(key) : null;
        },
        setItem(key, value) {
          localStorageData.set(key, value);
        },
      },
      location: { search: "", pathname: "/" },
      history: { replaceState() {} },
      requestAnimationFrame(callback) {
        callback();
      },
    },
    fetch: async () => {
      throw new Error("offline in tests");
    },
    URLSearchParams,
    Date,
    setTimeout,
    clearTimeout,
    HTMLInputElement: function HTMLInputElement() {},
    HTMLSelectElement: function HTMLSelectElement() {},
  };
  context.globalThis = context;
  vm.createContext(context);
  vm.runInContext(source, context, { filename: "app.js" });
  return context;
}

test("groupResourceFiles splits files into indexed and summarized buckets", () => {
  const context = loadAppContext();
  assert.equal(typeof context.groupResourceFiles, "function");

  const grouped = context.groupResourceFiles([
    { pdf_rel_path: "a.pdf", has_index: false, has_summary: false },
    { pdf_rel_path: "b.pdf", has_index: true, has_summary: false },
    { pdf_rel_path: "c.pdf", has_index: true, has_summary: true },
  ]);

  assert.deepEqual(
    Object.keys(grouped),
    ["notYetIndexed", "indexedNotSummarized", "indexedAndSummarized"]
  );
  assert.equal(grouped.notYetIndexed.length, 1);
  assert.equal(grouped.indexedNotSummarized.length, 1);
  assert.equal(grouped.indexedAndSummarized.length, 1);
});

test("normalize and resize resource column widths keep narrow select column and preserve width map", () => {
  const context = loadAppContext();
  assert.equal(typeof context.normalizeResourceColumnWidths, "function");
  assert.equal(typeof context.resizeResourceColumnWidths, "function");

  const normalized = context.normalizeResourceColumnWidths({
    select: 10,
    pdf: 150,
    indexed: 120,
    chunks: 110,
    summary: 200,
    embeddings: 120,
    preview: 170,
    modified: 160,
  });

  assert.ok(normalized.select >= 48);
  assert.ok(normalized.pdf >= 120);
  assert.ok(normalized.summary >= 120);

  const resized = context.resizeResourceColumnWidths(normalized, "pdf", 60);
  assert.ok(resized.pdf > normalized.pdf);
  assert.ok(resized.indexed < normalized.indexed || resized.chunks < normalized.chunks || resized.summary < normalized.summary);
});
