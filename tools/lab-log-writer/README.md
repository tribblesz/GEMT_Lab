# Lab Log Writer

Local GUI writer for the APT/FIM Obsidian vault.

## Purpose

This tool provides form-style data entry for:

- `experiment-series`
- `experiment-log`
- `mcp-image-log`
- `ion-column-image-log`
- `instrument-configuration`
- `specimen`
- `contact`
- `daily-note`
- `meeting`
- `note`
- `task-list`
- `startup-checklist`
- `shutdown-checklist`
- `resource-library` for PDF ingestion and LLM summaries

The writer stores the resulting notes directly in `ELN_vault` as markdown files with YAML frontmatter.

## Run

From the repository root:

```bash
python tools/lab-log-writer/server.py
```

If you want PDF extraction support, install the Python dependencies first:

```bash
python -m pip install -r tools/lab-log-writer/requirements.txt
```

Or on Windows:

```bat
tools\lab-log-writer\start_writer.bat
```

The tool serves the UI at:

`http://127.0.0.1:8765/`

## Notes

- No external dependencies are required.
- The writer is designed for local use on the same machine as the vault.
- Obsidian remains the reader/query/dashboard layer; this tool is the structured writer.
- The `Resources` panel scans PDFs from `ELN_vault/Resources/APT-FIM/PDFs` and writes markdown summaries into the vault.
