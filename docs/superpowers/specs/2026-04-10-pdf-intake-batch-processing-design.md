# PDF Intake Batch Processing Design

## Goal

Add an inbox-style PDF processing flow to the lab log writer so the user can drop many PDFs into the APT/FIM resource folder, click a single batch action, and have the system process each PDF safely, remember completion state, and move completed files out of the intake area.

## Scope

This design extends the existing resource pipeline in `tools/lab-log-writer` rather than introducing a new service. It covers:

- scanning the intake folder
- batch ingest + summarize processing
- completion tracking across restarts
- moving completed PDFs into a processed subfolder
- moving failed PDFs into a failed subfolder
- updating the resource UI and vault documentation

It does not add background workers, concurrent job execution, or automatic retry scheduling.

## User Workflow

1. The user drops PDFs into `ELN_vault/Resources/APT-FIM/PDFs`.
2. The user opens the writer `Resources` page.
3. The user clicks `Scan Intake Folder` to refresh what is waiting.
4. The user chooses provider settings and whether embeddings are enabled.
5. The user clicks `Process Intake Folder`.
6. The system processes every pending PDF in the intake folder.
7. A PDF is considered done only after:
   - the summary note is successfully written
   - and embeddings are also successfully generated when embeddings are enabled for that run
8. Completed PDFs are moved into `ELN_vault/Resources/APT-FIM/PDFs/Processed`.
9. Failed PDFs are moved into `ELN_vault/Resources/APT-FIM/PDFs/Failed`.
10. The UI shows a run summary with done and failed counts.

## Folder Layout

The existing folder remains the user-facing upload location:

- `ELN_vault/Resources/APT-FIM/PDFs`

Two operational subfolders are added beneath it:

- `ELN_vault/Resources/APT-FIM/PDFs/Processed`
- `ELN_vault/Resources/APT-FIM/PDFs/Failed`

Behavior rules:

- Only PDFs in the top-level `PDFs` intake folder are eligible for the new intake batch action.
- Files already in `Processed` or `Failed` are excluded from intake scans.
- Existing summary notes and topic notes stay where they are today.
- Existing index files stay in `Resources/APT-FIM/.index`.

## Recommended Architecture

Use the current `resources.py` and `server.py` modules as the orchestration layer.

### Resource State Model

Each PDF should have durable processing metadata stored in its index payload. The batch flow should record at least:

- `status`: `pending`, `processing`, `done`, or `failed`
- `processing_started_at`
- `processing_finished_at`
- `summary_path`
- `embeddings_generated`
- `original_pdf_rel_path`
- `current_pdf_rel_path`
- `error_message`

This state must survive server restarts. The index remains the source of truth for whether a PDF has already been completed.

### Batch Processor

Add a dedicated backend helper that:

- scans only top-level intake PDFs
- skips PDFs already marked `done`
- processes each PDF sequentially
- writes status updates before and after each stage
- moves the file only after the run outcome is known

Per-PDF processing pipeline:

1. Mark status `processing`
2. Extract text and build chunks
3. Write or update the PDF index JSON
4. Generate embeddings if enabled
5. Generate the summary note
6. If all required steps succeed, mark `done` and move the PDF to `Processed`
7. If any required step fails, mark `failed`, store the error, and move the PDF to `Failed`

Sequential processing is preferred here because it keeps failure handling simple, reduces API rate-limit complexity, and is easier to reason about for dozens of documents.

### Scan Semantics

The scan endpoint for intake mode should report:

- pending intake PDFs
- already processed count
- failed count
- per-file state from the index when available

The existing broader resource library scan can continue to show all PDFs across intake and subfolders, but the new intake batch action should act only on the upload folder.

## API Design

Extend the current resource API with explicit inbox-oriented operations.

### `GET /api/resources/status`

Keep the current broad resource status response, but include counts for:

- `pending`
- `processing`
- `done`
- `failed`

Also include folder paths for:

- `pdfs`
- `processed`
- `failed`
- `summaries`
- `topics`
- `index`

### `POST /api/resources/scan-intake`

Return the current intake queue and counts. This should only inspect the top-level intake folder plus stored status metadata.

### `POST /api/resources/process-intake`

Accept the same provider configuration already used for summarization:

- `provider`
- `baseUrl`
- `apiKey`
- `model`
- `embeddingModel`
- `generateEmbeddings`

Return:

- total PDFs discovered
- how many were processed this run
- how many succeeded
- how many failed
- per-file results
- updated resource status payload

No new endpoint is needed for manual single-file processing if the current actions remain available.

## File Movement Rules

Moving files must preserve uniqueness and traceability.

Rules:

- If a destination filename already exists in `Processed` or `Failed`, generate a safe unique filename rather than overwrite.
- The index must record both the original intake-relative path and the current location after moving.
- Summary notes should continue linking to the vault path of the moved PDF, so the summary renderer or post-move update step must refresh the stored PDF link to the final location.

Because summary notes currently link directly to the PDF vault path, the backend should generate the summary note after determining the final processed location, or rewrite the note link after the move.

## UI Design

Update the `resource-library` panel in `app.js` and `styles.css`.

### New Actions

Add:

- `Scan Intake Folder`
- `Process Intake Folder`

Retain the existing fine-grained actions:

- `Scan PDFs`
- `Ingest Selected`
- `Summarize Selected`
- `Summarize All Unsummarized`

This preserves both operational modes:

- inbox batch mode for large drops
- manual per-selection mode for targeted work

### UI Status

Show:

- pending count
- done count
- failed count
- selected count

Add a short explanation that the intake batch action only processes PDFs placed directly in the top-level intake folder.

### Results Display

Show a run result summary after `Process Intake Folder`:

- succeeded file names
- failed file names
- failure messages when present

The inline preview behavior should remain available for PDFs still visible in the library view.

## Error Handling

The system should fail one PDF without aborting the entire batch.

Per-file failure handling:

- catch exceptions at the per-file level
- record the error string in the index
- mark the PDF `failed`
- move the file to `Failed`
- continue with the next PDF

Batch-level failures should be reserved for malformed requests or unavailable configuration before any file work begins.

Examples of per-file failure causes:

- unreadable PDF
- missing `pypdf`
- provider API error
- missing hosted API key
- embedding model rejected by provider
- summary note write failure

## Testing Strategy

Add focused automated tests around the new behavior rather than broad end-to-end mocks.

### Unit Tests

Extend `tools/lab-log-writer/tests/test_resources.py` to cover:

- intake scan ignores `Processed` and `Failed`
- processed PDFs are moved only after summary success
- failed PDFs are moved to the failed folder
- duplicate destination names are made unique
- completion status persists in index metadata
- done means summary exists and embeddings exist when embeddings are enabled

### Syntax and Smoke Checks

Continue using:

- `python -m unittest`
- `python -m py_compile`
- `node --check`

Also run a local HTTP smoke check for the new intake endpoints.

## Files Expected To Change

### Backend

- `tools/lab-log-writer/resources.py`
  - add intake/processed/failed path helpers
  - add queue state helpers
  - add file move helpers
  - add batch processor orchestration
- `tools/lab-log-writer/server.py`
  - expose intake scan and process endpoints
  - include new counts and folder paths in status payload

### Frontend

- `tools/lab-log-writer/app.js`
  - add intake actions
  - add queue status rendering
  - surface per-run results
- `tools/lab-log-writer/styles.css`
  - style new intake status and result blocks

### Vault Docs

- `ELN_vault/Resources/APT-FIM/Library.md`
  - explain inbox processing flow
- `ELN_vault/Home.md`
  - optional short wording update if needed to mention batch intake flow

### Tests

- `tools/lab-log-writer/tests/test_resources.py`

## Open Design Decisions Resolved

These decisions are now fixed for implementation:

- The upload location remains `ELN_vault/Resources/APT-FIM/PDFs`
- Completed files move to `Processed`
- Failed files move to `Failed`
- The intake batch action scans only the top-level intake folder
- A PDF is only `done` after summary output exists, plus embeddings when embeddings are enabled
- Processing is sequential

## Non-Goals

This design intentionally does not include:

- background daemon processing
- automatic retries
- concurrent multi-file provider calls
- queue pause/resume controls
- topic synthesis as part of the automatic intake batch

These can be added later if the basic inbox pipeline proves useful.
