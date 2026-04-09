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
- `startup-checklist`
- `shutdown-checklist`

The writer stores the resulting notes directly in `ELN_vault` as markdown files with YAML frontmatter.

## Run

From the repository root:

```bash
python tools/lab-log-writer/server.py
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
