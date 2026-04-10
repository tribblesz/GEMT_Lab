# PDF Intake Batch Processing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an inbox-style PDF processing workflow that scans the top-level APT/FIM PDF folder, batch-processes every pending PDF, persists completion state, and moves finished files into `Processed` or `Failed` subfolders.

**Architecture:** Extend the existing `tools/lab-log-writer` resource pipeline rather than adding a new service. Keep state in the existing PDF index JSON files, add explicit intake scan/process endpoints in `server.py`, and surface the new actions and queue status in the `resource-library` UI.

**Tech Stack:** Python standard library HTTP server, Python resource helpers, `requests`, `pypdf`, vanilla JavaScript, CSS, markdown vault docs, `unittest`

---

## File Structure

### Existing files to modify

- `tools/lab-log-writer/resources.py`
  - resource folder resolution
  - status metadata helpers
  - intake scan helpers
  - file move helpers
  - batch processing orchestration
- `tools/lab-log-writer/server.py`
  - new intake-oriented API routes
  - status payload expansion
- `tools/lab-log-writer/app.js`
  - intake scan button
  - process-intake button
  - queue counts and run result rendering
- `tools/lab-log-writer/styles.css`
  - queue summary and result panel styling
- `tools/lab-log-writer/tests/test_resources.py`
  - new unit coverage for intake behavior
- `ELN_vault/Resources/APT-FIM/Library.md`
  - user-facing intake workflow documentation

### No new subsystem files required

This feature fits cleanly into the existing writer modules. Keep the change focused and avoid introducing background jobs or extra config files.

## Task 1: Add failing tests for intake scanning and completion rules

**Files:**
- Modify: `tools/lab-log-writer/tests/test_resources.py`
- Modify: `tools/lab-log-writer/resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Write the failing intake scan tests**

```python
    def test_scan_intake_only_uses_top_level_pdf_folder(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            processed_dir = pdf_dir / "Processed"
            failed_dir = pdf_dir / "Failed"
            summary_dir = root / "Summaries"
            index_dir = root / ".index"
            processed_dir.mkdir(parents=True)
            failed_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)

            (pdf_dir / "pending.pdf").write_bytes(b"%PDF-1.4\n")
            (processed_dir / "done.pdf").write_bytes(b"%PDF-1.4\n")
            (failed_dir / "bad.pdf").write_bytes(b"%PDF-1.4\n")

            items = resources.scan_intake_pdf_library(pdf_dir, summary_dir, index_dir)

            self.assertEqual([item["pdf_name"] for item in items], ["pending.pdf"])

    def test_done_requires_summary_and_embeddings_when_enabled(self):
        resources = load_resources_module()

        done_without_embeddings = resources.is_processing_complete(
            has_summary=True,
            generate_embeddings=False,
            has_embeddings=False,
        )
        not_done_with_missing_embeddings = resources.is_processing_complete(
            has_summary=True,
            generate_embeddings=True,
            has_embeddings=False,
        )
        done_with_embeddings = resources.is_processing_complete(
            has_summary=True,
            generate_embeddings=True,
            has_embeddings=True,
        )

        self.assertTrue(done_without_embeddings)
        self.assertFalse(not_done_with_missing_embeddings)
        self.assertTrue(done_with_embeddings)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: FAIL with missing helper errors such as `AttributeError: module 'lab_log_writer_resources' has no attribute 'scan_intake_pdf_library'`

- [ ] **Step 3: Write minimal helper implementations**

```python
def scan_intake_pdf_library(pdf_dir: Path, summary_dir: Path, index_dir: Path | None = None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not pdf_dir.exists():
        return items

    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        items.extend(scan_pdf_library_for_paths([pdf_path], pdf_dir, summary_dir, index_dir))
    return items


def is_processing_complete(*, has_summary: bool, generate_embeddings: bool, has_embeddings: bool) -> bool:
    if not has_summary:
        return False
    if generate_embeddings and not has_embeddings:
        return False
    return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS for the new tests, with existing tests still green

- [ ] **Step 5: Commit**

```bash
git add tools/lab-log-writer/tests/test_resources.py tools/lab-log-writer/resources.py
git commit -m "test: define intake scan and completion rules"
```

## Task 2: Add resource path helpers and durable processing metadata

**Files:**
- Modify: `tools/lab-log-writer/resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Add a failing metadata persistence test**

```python
    def test_update_processing_state_persists_status_fields(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            index_path = Path(temp_dir) / "sample.json"
            resources.write_json(index_path, {"pdf_name": "sample.pdf"})

            resources.update_processing_state(
                index_path,
                status="processing",
                original_pdf_rel_path="Resources/APT-FIM/PDFs/sample.pdf",
                current_pdf_rel_path="Resources/APT-FIM/PDFs/sample.pdf",
            )

            payload = resources.read_json(index_path, {})
            self.assertEqual(payload["status"], "processing")
            self.assertEqual(payload["original_pdf_rel_path"], "Resources/APT-FIM/PDFs/sample.pdf")
            self.assertEqual(payload["current_pdf_rel_path"], "Resources/APT-FIM/PDFs/sample.pdf")
            self.assertIn("processing_started_at", payload)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: FAIL with `AttributeError` for `update_processing_state`

- [ ] **Step 3: Implement processing metadata and folder helpers**

```python
def processed_pdf_dir(pdf_dir: Path) -> Path:
    return pdf_dir / "Processed"


def failed_pdf_dir(pdf_dir: Path) -> Path:
    return pdf_dir / "Failed"


def ensure_resource_subdirectories(pdf_dir: Path) -> None:
    processed_pdf_dir(pdf_dir).mkdir(parents=True, exist_ok=True)
    failed_pdf_dir(pdf_dir).mkdir(parents=True, exist_ok=True)


def update_processing_state(index_path: Path, *, status: str, **fields: Any) -> dict[str, Any]:
    payload = read_json(index_path, {})
    payload["status"] = status
    if status == "processing":
        payload["processing_started_at"] = current_timestamp()
        payload["error_message"] = ""
    if status in {"done", "failed"}:
        payload["processing_finished_at"] = current_timestamp()
    payload.update(fields)
    write_json(index_path, payload)
    return payload
```

- [ ] **Step 4: Run tests to verify metadata persistence**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS for the new metadata test and earlier tests

- [ ] **Step 5: Commit**

```bash
git add tools/lab-log-writer/resources.py tools/lab-log-writer/tests/test_resources.py
git commit -m "feat: persist PDF processing state"
```

## Task 3: Implement safe move helpers for processed and failed PDFs

**Files:**
- Modify: `tools/lab-log-writer/resources.py`
- Modify: `tools/lab-log-writer/tests/test_resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Add failing move helper tests**

```python
    def test_move_pdf_to_processed_makes_name_unique(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_dir = Path(temp_dir) / "PDFs"
            processed_dir = pdf_dir / "Processed"
            pdf_dir.mkdir(parents=True)
            processed_dir.mkdir(parents=True)

            source = pdf_dir / "paper.pdf"
            source.write_bytes(b"%PDF-1.4\n")
            (processed_dir / "paper.pdf").write_bytes(b"%PDF-1.4\n")

            moved = resources.move_pdf_to_bucket(source, processed_dir)

            self.assertTrue(moved.exists())
            self.assertNotEqual(moved.name, "paper.pdf")

    def test_move_pdf_to_failed_keeps_file_available(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_dir = Path(temp_dir) / "PDFs"
            failed_dir = pdf_dir / "Failed"
            pdf_dir.mkdir(parents=True)
            failed_dir.mkdir(parents=True)

            source = pdf_dir / "broken.pdf"
            source.write_bytes(b"%PDF-1.4\n")

            moved = resources.move_pdf_to_bucket(source, failed_dir)

            self.assertTrue(moved.exists())
            self.assertFalse(source.exists())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: FAIL with missing `move_pdf_to_bucket`

- [ ] **Step 3: Implement safe file move logic**

```python
def unique_destination_path(directory: Path, file_name: str) -> Path:
    candidate = directory / sanitize_file_name(file_name)
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        alt = directory / f"{stem}-{counter}{suffix}"
        if not alt.exists():
            return alt
        counter += 1


def move_pdf_to_bucket(source: Path, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_destination_path(destination_dir, source.name)
    source.replace(destination)
    return destination
```

- [ ] **Step 4: Run tests to verify move behavior**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS for unique naming and move tests

- [ ] **Step 5: Commit**

```bash
git add tools/lab-log-writer/resources.py tools/lab-log-writer/tests/test_resources.py
git commit -m "feat: add safe PDF bucket moves"
```

## Task 4: Build the batch intake processor in `resources.py`

**Files:**
- Modify: `tools/lab-log-writer/resources.py`
- Modify: `tools/lab-log-writer/tests/test_resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Add a failing batch processing success test**

```python
    def test_process_intake_pdf_marks_done_and_moves_to_processed(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            summary_dir = root / "Summaries"
            index_dir = root / ".index"
            pdf_dir.mkdir()
            summary_dir.mkdir()
            index_dir.mkdir()
            source = pdf_dir / "paper.pdf"
            source.write_bytes(b"%PDF-1.4\n")

            def fake_ingest(pdf_path, index_dir_arg, generate_embeddings, config=None):
                key = resources.pdf_index_key(pdf_path)
                payload = {
                    "pdf_name": pdf_path.name,
                    "chunks": [{"chunk_id": 1, "page_start": 1, "page_end": 1, "text": "APT text"}],
                    "chunk_count": 1,
                    "page_count": 1,
                }
                resources.write_json(index_dir_arg / f"{key}.json", payload)
                if generate_embeddings:
                    resources.write_json(index_dir_arg / f"{key}.embeddings.json", {"embeddings": [1]})
                return payload

            def fake_summarize(pdf_title, chunks, config):
                return {"summary_text": "## Overview\nDone", "citations": []}

            result = resources.process_intake_pdf(
                pdf_path=source,
                pdf_dir=pdf_dir,
                summary_dir=summary_dir,
                index_dir=index_dir,
                provider_config={"provider": "ollama", "model": "llama3.1"},
                generate_embeddings=True,
                ingest_fn=fake_ingest,
                summarize_fn=fake_summarize,
            )

            self.assertEqual(result["status"], "done")
            self.assertIn("/Processed/", result["pdf_rel_path"].replace("\\\\", "/"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: FAIL with missing `process_intake_pdf`

- [ ] **Step 3: Implement per-file batch orchestration**

```python
def process_intake_pdf(
    *,
    pdf_path: Path,
    pdf_dir: Path,
    summary_dir: Path,
    index_dir: Path,
    provider_config: dict[str, str],
    generate_embeddings: bool,
    vault_root: Path,
    ingest_fn=ingest_pdf,
    summarize_fn=summarize_pdf_chunks,
) -> dict[str, Any]:
    key = pdf_index_key(pdf_path)
    index_path = index_dir / f"{key}.json"
    original_rel = rel_path_from_root(pdf_path, vault_root)
    update_processing_state(
        index_path,
        status="processing",
        original_pdf_rel_path=original_rel,
        current_pdf_rel_path=original_rel,
        embeddings_generated=False,
    )
    try:
        indexed = ingest_fn(pdf_path, index_dir, generate_embeddings, provider_config if generate_embeddings else None)
        embeddings_path = index_dir / f"{key}.embeddings.json"
        has_embeddings = embeddings_path.exists()
        processed_path = move_pdf_to_bucket(pdf_path, processed_pdf_dir(pdf_dir))
        final_rel = rel_path_from_root(processed_path, vault_root)
        summary_payload = summarize_fn(processed_path.stem, indexed["chunks"], provider_config)
        note_path = summary_dir / summary_note_name(processed_path)
        content = render_pdf_summary_note(
            pdf_title=processed_path.stem,
            pdf_rel_path=final_rel,
            provider_label=provider_config["provider"],
            model_name=provider_config["model"],
            summary_text=summary_payload["summary_text"],
            citations=summary_payload["citations"],
        )
        note_path.write_text(content, encoding="utf-8")
        done = is_processing_complete(
            has_summary=note_path.exists(),
            generate_embeddings=generate_embeddings,
            has_embeddings=has_embeddings,
        )
        update_processing_state(
            index_path,
            status="done" if done else "failed",
            summary_path=str(note_path),
            current_pdf_rel_path=final_rel,
            embeddings_generated=has_embeddings,
        )
        return {"status": "done" if done else "failed", "pdf_rel_path": final_rel, "summary_path": str(note_path)}
    except Exception as exc:
        failed_path = move_pdf_to_bucket(pdf_path, failed_pdf_dir(pdf_dir)) if pdf_path.exists() else pdf_path
        update_processing_state(
            index_path,
            status="failed",
            current_pdf_rel_path=str(failed_path),
            error_message=str(exc),
        )
        return {"status": "failed", "pdf_rel_path": str(failed_path), "error": str(exc)}
```

- [ ] **Step 4: Add the batch loop helper**

```python
def process_intake_library(
    pdf_dir: Path,
    summary_dir: Path,
    index_dir: Path,
    vault_root: Path,
    provider_config: dict[str, str],
    generate_embeddings: bool,
) -> dict[str, Any]:
    ensure_resource_subdirectories(pdf_dir)
    files = scan_intake_pdf_library(pdf_dir, summary_dir, index_dir)
    results = []
    for item in files:
        pdf_path = pdf_dir / item["pdf_rel_path"]
        if item.get("status") == "done":
            continue
        results.append(
            process_intake_pdf(
                pdf_path=pdf_path,
                pdf_dir=pdf_dir,
                summary_dir=summary_dir,
                index_dir=index_dir,
                vault_root=vault_root,
                provider_config=provider_config,
                generate_embeddings=generate_embeddings,
            )
        )
    return {
        "total": len(files),
        "processed": len(results),
        "succeeded": sum(1 for item in results if item["status"] == "done"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "results": results,
    }
```

- [ ] **Step 5: Run tests to verify the new processor**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS for the new success-path batch test

- [ ] **Step 6: Commit**

```bash
git add tools/lab-log-writer/resources.py tools/lab-log-writer/tests/test_resources.py
git commit -m "feat: add batch intake PDF processing"
```

## Task 5: Cover the batch failure path and status reporting

**Files:**
- Modify: `tools/lab-log-writer/tests/test_resources.py`
- Modify: `tools/lab-log-writer/resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Add a failing batch failure test**

```python
    def test_process_intake_pdf_moves_failed_files_and_records_error(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            summary_dir = root / "Summaries"
            index_dir = root / ".index"
            pdf_dir.mkdir()
            summary_dir.mkdir()
            index_dir.mkdir()
            source = pdf_dir / "broken.pdf"
            source.write_bytes(b"%PDF-1.4\n")

            def failing_ingest(*args, **kwargs):
                raise RuntimeError("provider unavailable")

            result = resources.process_intake_pdf(
                pdf_path=source,
                pdf_dir=pdf_dir,
                summary_dir=summary_dir,
                index_dir=index_dir,
                vault_root=root,
                provider_config={"provider": "ollama", "model": "llama3.1"},
                generate_embeddings=False,
                ingest_fn=failing_ingest,
            )

            self.assertEqual(result["status"], "failed")
            self.assertIn("provider unavailable", result["error"])
            self.assertTrue((pdf_dir / "Failed").exists())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: FAIL if failure path does not yet move the PDF or persist the error

- [ ] **Step 3: Tighten the failure path**

```python
    except Exception as exc:
        failed_path = pdf_path
        if pdf_path.exists():
            failed_path = move_pdf_to_bucket(pdf_path, failed_pdf_dir(pdf_dir))
        failed_rel = rel_path_from_root(failed_path, vault_root) if failed_path.exists() else original_rel
        update_processing_state(
            index_path,
            status="failed",
            current_pdf_rel_path=failed_rel,
            error_message=str(exc),
        )
        return {
            "status": "failed",
            "pdf_name": failed_path.name if failed_path else pdf_path.name,
            "pdf_rel_path": failed_rel,
            "error": str(exc),
        }
```

- [ ] **Step 4: Run tests to verify the failure path**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS for the failure-path assertions

- [ ] **Step 5: Commit**

```bash
git add tools/lab-log-writer/resources.py tools/lab-log-writer/tests/test_resources.py
git commit -m "fix: record failed PDF intake processing"
```

## Task 6: Expose intake scan and process routes in `server.py`

**Files:**
- Modify: `tools/lab-log-writer/server.py`
- Modify: `tools/lab-log-writer/resources.py`
- Test: `tools/lab-log-writer/tests/test_resources.py`

- [ ] **Step 1: Add route wiring in `server.py`**

```python
from resources import (
    ...
    process_intake_library,
    scan_intake_pdf_library,
)
```

```python
def get_resource_status() -> dict[str, object]:
    _, paths = resource_settings_and_paths()
    files = scan_pdf_library(paths["pdfs"], paths["summaries"], paths["index"])
    intake_files = scan_intake_pdf_library(paths["pdfs"], paths["summaries"], paths["index"])
    return {
        "folders": {
            "pdfs": rel_to_posix(paths["pdfs"].relative_to(VAULT_ROOT)),
            "processed": rel_to_posix((paths["pdfs"] / "Processed").relative_to(VAULT_ROOT)),
            "failed": rel_to_posix((paths["pdfs"] / "Failed").relative_to(VAULT_ROOT)),
            "summaries": rel_to_posix(paths["summaries"].relative_to(VAULT_ROOT)),
            "topics": rel_to_posix(paths["topics"].relative_to(VAULT_ROOT)),
            "index": rel_to_posix(paths["index"].relative_to(VAULT_ROOT)),
        },
        "counts": {
            "pdfs": len(files),
            "pending": sum(1 for item in intake_files if item.get("status") != "done"),
            "done": sum(1 for item in files if item.get("status") == "done"),
            "failed": sum(1 for item in files if item.get("status") == "failed"),
            "summaries": sum(1 for item in files if item["has_summary"]),
        },
        "files": files,
        "intakeFiles": intake_files,
    }
```

- [ ] **Step 2: Add the two new endpoints**

```python
        if path == "/api/resources/scan-intake":
            payload = json.dumps({"status": get_resource_status()}).encode("utf-8")
            self._send(HTTPStatus.OK, payload, "application/json; charset=utf-8")
            return
```

```python
        if parsed.path == "/api/resources/process-intake":
            try:
                provider_config = prepare_provider_config(payload)
                _, paths = resource_settings_and_paths()
                response = process_intake_library(
                    pdf_dir=paths["pdfs"],
                    summary_dir=paths["summaries"],
                    index_dir=paths["index"],
                    vault_root=VAULT_ROOT,
                    provider_config=provider_config,
                    generate_embeddings=bool(payload.get("generateEmbeddings")),
                )
                response["status"] = get_resource_status()
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
```

- [ ] **Step 3: Run Python syntax verification**

Run: `python -m py_compile "tools/lab-log-writer/server.py" "tools/lab-log-writer/resources.py"`

Expected: no output

- [ ] **Step 4: Run resource tests**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/lab-log-writer/server.py tools/lab-log-writer/resources.py tools/lab-log-writer/tests/test_resources.py
git commit -m "feat: add intake batch resource routes"
```

## Task 7: Add intake controls and batch result rendering in `app.js`

**Files:**
- Modify: `tools/lab-log-writer/app.js`
- Modify: `tools/lab-log-writer/styles.css`
- Test: `tools/lab-log-writer/app.js`

- [ ] **Step 1: Add new state fields for intake results**

```javascript
const state = {
  ...,
  intakeRunResults: [],
  intakeSummary: null,
};
```

- [ ] **Step 2: Add intake buttons and status copy in `renderResourcesPanel()`**

```javascript
      <div class="resource-actions">
        <button id="resource-scan-intake" type="button" class="secondary-button">Scan Intake Folder</button>
        <button id="resource-process-intake" type="button" class="primary-button">Process Intake Folder</button>
        <button id="resource-scan" type="button" class="secondary-button">Scan PDFs</button>
        <button id="resource-ingest" type="button" class="secondary-button">Ingest Selected</button>
        <button id="resource-summarize" type="button" class="primary-button">Summarize Selected</button>
        <button id="resource-summarize-unsummarized" type="button" class="secondary-button">Summarize All Unsummarized</button>
      </div>
```

```javascript
      <p class="resource-help">
        Intake processing only works on PDFs placed directly in the top-level
        <code>Resources/APT-FIM/PDFs</code> folder. Completed files are moved into
        <code>Processed</code>. Failures are moved into <code>Failed</code>.
      </p>
```

- [ ] **Step 3: Add event handlers for scan/process intake**

```javascript
  document.getElementById("resource-scan-intake")?.addEventListener("click", async () => {
    const response = await fetch("./api/resources/scan-intake", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    const data = await response.json();
    if (!response.ok) {
      showMessage(data.error || "Could not scan intake folder.", "error");
      return;
    }
    if (data.status) {
      state.resourceFiles = data.status.files || [];
      state.intakeSummary = data.status.counts || null;
      syncResourceSelections();
      renderResourcesPanel();
    }
    showMessage("Scanned the intake folder.", "success");
  });
```

```javascript
  document.getElementById("resource-process-intake")?.addEventListener("click", async () => {
    const response = await fetch("./api/resources/process-intake", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(resourceConfigPayload([])),
    });
    const data = await response.json();
    if (!response.ok) {
      showMessage(data.error || "Could not process intake folder.", "error");
      return;
    }
    state.intakeRunResults = data.results || [];
    state.intakeSummary = data.status?.counts || null;
    state.resourceFiles = data.status?.files || [];
    syncResourceSelections();
    renderResourcesPanel();
    showMessage(data.message || "Processed the intake folder.", "success");
  });
```

- [ ] **Step 4: Render the intake result panel**

```javascript
  const intakeResultsMarkup = state.intakeRunResults.length
    ? `
      <section class="form-section">
        <h3>Last Intake Run</h3>
        <div class="resource-result-list">
          ${state.intakeRunResults
            .map(
              (item) => `
                <div class="resource-result ${item.status}">
                  <strong>${escapeHtml(item.pdf_name || item.pdf_rel_path || "PDF")}</strong>
                  <span>${escapeHtml(item.status)}</span>
                  ${item.error ? `<code>${escapeHtml(item.error)}</code>` : ""}
                </div>
              `
            )
            .join("")}
        </div>
      </section>
    `
    : "";
```

- [ ] **Step 5: Run JavaScript syntax verification**

Run: `node --check "tools/lab-log-writer/app.js"`

Expected: no output

- [ ] **Step 6: Commit**

```bash
git add tools/lab-log-writer/app.js tools/lab-log-writer/styles.css
git commit -m "feat: add intake batch controls to resource UI"
```

## Task 8: Style intake summary and results in `styles.css`

**Files:**
- Modify: `tools/lab-log-writer/styles.css`
- Test: `tools/lab-log-writer/app.js`

- [ ] **Step 1: Add CSS for queue results**

```css
.resource-result-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.resource-result {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 0.9rem;
  border-radius: 0.6rem;
  background: rgba(255, 255, 255, 0.05);
}

.resource-result.done {
  border-left: 4px solid #5fbf77;
}

.resource-result.failed {
  border-left: 4px solid #d96a6a;
}

.resource-intake-help code {
  white-space: nowrap;
}
```

- [ ] **Step 2: Run JavaScript syntax check again**

Run: `node --check "tools/lab-log-writer/app.js"`

Expected: no output

- [ ] **Step 3: Run lints on touched files**

Run: use IDE lint diagnostics for:
- `tools/lab-log-writer/app.js`
- `tools/lab-log-writer/styles.css`

Expected: no new linter errors

- [ ] **Step 4: Commit**

```bash
git add tools/lab-log-writer/styles.css tools/lab-log-writer/app.js
git commit -m "style: add intake batch result styling"
```

## Task 9: Update vault documentation for the intake workflow

**Files:**
- Modify: `ELN_vault/Resources/APT-FIM/Library.md`
- Modify: `ELN_vault/Home.md`

- [ ] **Step 1: Update the library page instructions**

```md
Drop PDFs directly into `Resources/APT-FIM/PDFs`, then use the local writer `Resources` panel.

Batch intake workflow:

- Click `Scan Intake Folder` to see what is waiting.
- Click `Process Intake Folder` to process every pending PDF in the top-level intake folder.
- Completed PDFs move into `Resources/APT-FIM/PDFs/Processed`.
- Failed PDFs move into `Resources/APT-FIM/PDFs/Failed`.
```

- [ ] **Step 2: Add a brief Home page note if needed**

```md
- Resource intake is now batch-oriented: drop PDFs into `Resources/APT-FIM/PDFs` and process them from the writer `Resources` panel.
```

- [ ] **Step 3: Verify markdown syntax and links manually**

Run: inspect the updated markdown files in the editor

Expected: links point to `[[Resources/APT-FIM/Library|APT/FIM Resources]]` and text matches the implemented workflow

- [ ] **Step 4: Commit**

```bash
git add ELN_vault/Resources/APT-FIM/Library.md ELN_vault/Home.md
git commit -m "docs: describe batch PDF intake workflow"
```

## Task 10: Run final verification and smoke checks

**Files:**
- Modify: none
- Test: `tools/lab-log-writer/tests/test_resources.py`
- Test: `tools/lab-log-writer/server.py`
- Test: `tools/lab-log-writer/app.js`

- [ ] **Step 1: Run the full resource unit test suite**

Run: `python -m unittest "tools/lab-log-writer/tests/test_resources.py" -v`

Expected: all tests PASS

- [ ] **Step 2: Run Python syntax verification**

Run: `python -m py_compile "tools/lab-log-writer/server.py" "tools/lab-log-writer/resources.py"`

Expected: no output

- [ ] **Step 3: Run JavaScript syntax verification**

Run: `node --check "tools/lab-log-writer/app.js"`

Expected: no output

- [ ] **Step 4: Run a local HTTP smoke check**

Run:

```bash
python -c "import json, urllib.request; print(json.loads(urllib.request.urlopen('http://127.0.0.1:8766/api/resources/presets').read().decode('utf-8'))['presets'][0]['id'])"
python -c "import json, urllib.request; data=json.loads(urllib.request.urlopen('http://127.0.0.1:8766/api/resources/scan-intake').read().decode('utf-8')); print(sorted(data['status'].keys()))"
python -c "import json, urllib.request; data=json.loads(urllib.request.urlopen('http://127.0.0.1:8766/api/resources/files').read().decode('utf-8')); print(sorted(data['counts'].keys()))"
```

Expected:

- first command prints a preset id such as `ollama-local`
- second command prints keys including `counts`, `files`, `folders`
- third command prints counts including `pending`, `done`, and `failed`

- [ ] **Step 5: Check IDE diagnostics for touched files**

Run: inspect lint diagnostics for:
- `tools/lab-log-writer/resources.py`
- `tools/lab-log-writer/server.py`
- `tools/lab-log-writer/app.js`
- `tools/lab-log-writer/styles.css`
- `ELN_vault/Resources/APT-FIM/Library.md`
- `ELN_vault/Home.md`

Expected: no new diagnostics introduced by this feature

- [ ] **Step 6: Commit**

```bash
git add tools/lab-log-writer/resources.py tools/lab-log-writer/server.py tools/lab-log-writer/app.js tools/lab-log-writer/styles.css tools/lab-log-writer/tests/test_resources.py ELN_vault/Resources/APT-FIM/Library.md ELN_vault/Home.md
git commit -m "feat: add inbox-style PDF batch processing"
```

## Self-Review

### Spec coverage

- Intake folder scanning: covered in Tasks 1, 4, and 6
- Done rule with embeddings: covered in Tasks 1 and 4
- Processed and failed moves: covered in Tasks 3, 4, and 5
- Durable state tracking: covered in Task 2
- UI workflow and run summary: covered in Tasks 7 and 8
- Vault documentation: covered in Task 9
- Verification: covered in Task 10

### Placeholder scan

No `TODO`, `TBD`, or deferred implementation placeholders remain. Every task includes explicit code or exact commands.

### Type consistency

Helper names are used consistently across tasks:

- `scan_intake_pdf_library`
- `is_processing_complete`
- `update_processing_state`
- `move_pdf_to_bucket`
- `process_intake_pdf`
- `process_intake_library`

The server endpoints are consistently named:

- `/api/resources/scan-intake`
- `/api/resources/process-intake`
