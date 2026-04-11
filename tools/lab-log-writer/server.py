from __future__ import annotations

import json
import re
import sys
import textwrap
import webbrowser
from datetime import datetime, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

MODULE_ROOT = Path(__file__).resolve().parent
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from resources import (
    _resolve_index_paths_for_scan,
    build_provider_presets,
    ensure_directories,
    ensure_resource_subdirectories,
    failed_pdf_dir,
    ingest_pdf,
    is_processing_complete,
    pdf_index_key,
    prepare_provider_config,
    process_intake_library,
    processed_pdf_dir,
    read_json,
    render_pdf_summary_note,
    render_topic_summary_note,
    resolve_resource_paths,
    scan_intake_pdf_library,
    scan_pdf_library,
    summary_note_name,
    synthesize_topic_summary,
    summarize_pdf_chunks,
    topic_note_name,
    unsummarized_pdf_rel_paths,
)


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
VAULT_ROOT = REPO_ROOT / "ELN_vault"
SETTINGS_PATH = VAULT_ROOT / "assets" / "ELN Settings.md"
HOST = "127.0.0.1"
PORT = 8765


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def sanitize_file_name(value: str) -> str:
    safe = re.sub(r'[\\/:*?"<>|]+', "-", str(value or "").strip())
    safe = re.sub(r"\s+", " ", safe).strip()
    return safe or "Untitled"


def slugify(value: str) -> str:
    return re.sub(r"\s+", "_", sanitize_file_name(value))


def yaml_string(value: str, fallback: str = "") -> str:
    raw = fallback if value in (None, "") else str(value)
    escaped = raw.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()
    return f'"{escaped}"'


def yaml_list(items: list[str], indent: int = 2, fallback: str | None = None) -> str:
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values and fallback is not None:
        values = [fallback]
    if not values:
        return "[]"
    prefix = " " * indent
    return "\n".join(f"{prefix}- {yaml_string(item)}" for item in values)


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def current_year() -> str:
    return datetime.now().strftime("%Y")


def current_month_number() -> str:
    return datetime.now().strftime("%m")


def current_month_name() -> str:
    return datetime.now().strftime("%B")


def current_weekday_name() -> str:
    return datetime.now().strftime("%A")


def count_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def find_block(lines: list[str], key: str, indent: int = 0) -> list[str]:
    target = f"{' ' * indent}{key}:"
    for index, line in enumerate(lines):
        if line == target:
            base_indent = count_indent(line)
            block: list[str] = []
            for subline in lines[index + 1 :]:
                if subline.strip() == "":
                    block.append(subline)
                    continue
                if count_indent(subline) <= base_indent:
                    break
                block.append(subline)
            return block
    return []


def parse_mapping(block: list[str], indent: int) -> dict[str, str]:
    data: dict[str, str] = {}
    prefix = " " * indent
    for line in block:
        if not line.startswith(prefix) or count_indent(line) != indent:
            continue
        content = line[indent:]
        if ":" not in content:
            continue
        key, value = content.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def parse_list_from_block(block: list[str], key: str, indent: int) -> list[str]:
    target = f"{' ' * indent}{key}:"
    values: list[str] = []
    for index, line in enumerate(block):
        if line == target:
            base_indent = count_indent(line)
            for subline in block[index + 1 :]:
                stripped = subline.strip()
                if stripped == "":
                    continue
                if count_indent(subline) <= base_indent:
                    break
                item = subline.strip()
                if item.startswith("- "):
                    values.append(item[2:].strip())
            break
    return values


def parse_settings() -> dict[str, object]:
    text = read_file(SETTINGS_PATH)
    lines = text.splitlines()

    folders = parse_mapping(find_block(lines, "folder"), 2)
    series_block = find_block(lines, "experiment series")
    gas_block = find_block(lines, "gas")
    gauge_block = find_block(lines, "gauge")
    exp_log_block = find_block(lines, "experiment log")
    mcp_block = find_block(lines, "mcp image log")
    ion_block = find_block(lines, "ion column image log")
    inst_block = find_block(lines, "instrument configuration")
    specimen_block = find_block(lines, "specimen")

    settings = {
        "eln_version": "0.5.0",
        "folders": folders,
        "experiment_series_types": parse_list_from_block(series_block, "type", 2),
        "experiment_series_statuses": parse_list_from_block(series_block, "status", 2),
        "gases": parse_list_from_block(gas_block, "allowed", 2),
        "experiment_log_statuses": parse_list_from_block(exp_log_block, "status", 2),
        "experiment_log_data_types": parse_list_from_block(exp_log_block, "data types", 2),
        "mcp_statuses": parse_list_from_block(mcp_block, "status", 2),
        "mcp_formats": parse_list_from_block(mcp_block, "image format", 2),
        "ion_statuses": parse_list_from_block(ion_block, "status", 2),
        "ion_signal_sources": parse_list_from_block(ion_block, "signal source", 2),
        "ion_formats": parse_list_from_block(ion_block, "image format", 2),
        "instrument_config_types": parse_list_from_block(inst_block, "type", 2),
        "specimen_types": parse_list_from_block(specimen_block, "type", 2),
        "main_chamber_gauge": parse_mapping(find_block(gauge_block, "main chamber", 2), 4).get("name", "Ion Gauge"),
        "load_lock_gauge": parse_mapping(find_block(gauge_block, "load lock", 2), 4).get("name", "LL Wide Range Gauge"),
        "ion_column_gauge": parse_mapping(find_block(gauge_block, "ion column", 2), 4).get("name", "Ion Column Wide Range Gauge"),
    }
    return settings


def note_choices(folder_key: str) -> list[str]:
    settings = parse_settings()
    folder = settings["folders"].get(folder_key, "")
    if not folder:
        return []
    path = VAULT_ROOT / folder
    if not path.exists():
        return []
    return sorted(
        file.stem
        for file in path.rglob("*.md")
        if "assets" not in file.parts and not file.name.startswith(".")
    )


def frontmatter(content: str) -> str:
    return f"---\n{content.strip()}\n---"


def build_experiment_series(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    series_name = str(payload.get("seriesName", "")).strip() or "Experiment Series"
    abbreviation = str(payload.get("abbreviation", "")).strip() or slugify(series_name)[:12]
    folder = VAULT_ROOT / settings["folders"].get("experiment series", "Experiment Series") / sanitize_file_name(series_name)
    file_path = folder / f"{sanitize_file_name(series_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
  - dashboard
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: experiment-series
tags:
  - "#experiment-series"
series:
  name: {yaml_string(series_name)}
  abbreviation: {yaml_string(abbreviation, 'N/A')}
  type: {yaml_string(str(payload.get('seriesType', 'integration status')), 'integration status')}
  status: {yaml_string(str(payload.get('seriesStatus', 'planned')), 'planned')}
  purpose: {yaml_string(str(payload.get('purpose', '')))}
  independent_variables: {yaml_string(str(payload.get('independentVariables', '')))}
  dependent_variables: {yaml_string(str(payload.get('dependentVariables', '')))}
  data_types_recorded:
    - "oscilloscope traces"
    - "digital logging"
    - "MCP images"
    - "raw MCP hit files"
"""
    )

    body = textwrap.dedent(
        f"""
        # Experiment Series Summary

        | Field | Value |
        | --- | --- |
        | Series | {series_name} |
        | Abbreviation | {abbreviation} |
        | Type | {str(payload.get("seriesType", "")).strip()} |
        | Status | {str(payload.get("seriesStatus", "")).strip()} |
        | Purpose | {str(payload.get("purpose", "")).strip()} |

        ## Intended Scope

        ### Variables

        - **Independent:** {str(payload.get("independentVariables", "")).strip()}
        - **Dependent:** {str(payload.get("dependentVariables", "")).strip()}

        ### Parameter Ranges

        - Minimum and maximum operating ranges:
        - Planned step sizes:
        - Measurement limits or restrictions:

        ### Emergency Stop Conditions

        - List all non-interlock abort conditions here.
        - Include leakage current, arcing, pressure spikes, or thermal excursions.

        ### Data Types Expected

        - Oscilloscope traces
        - Digital UI logging
        - MCP images
        - Raw MCP hit files
        - Other:

        ## Planned Experiment Logs

        ```dataview
        TABLE WITHOUT ID
          file.link as "Experiment Log",
          experiment.log_id as "Log ID",
          specimen.id as "Specimen ID",
          experiment.status as "Status",
          experiment.date_time as "Date / Time",
          file.mtime as "Modified"
        FROM #experiment-log AND !"assets"
        WHERE experiment.series_name = this.series.name
        SORT file.mtime DESC
        ```

        ## Linked MCP Image Logs

        ```dataview
        TABLE WITHOUT ID
          file.link as "MCP Image Log",
          image.parent_experiment_log as "Experiment Log",
          image.sequence_number as "Sequence",
          image.date_time as "Date / Time",
          file.mtime as "Modified"
        FROM #mcp-image-log AND !"assets"
        WHERE contains(image.experiment_series_number, this.series.name) OR contains(image.parent_experiment_log, this.series.name)
        SORT file.mtime DESC
        ```

        ## Linked Ion Column Image Logs

        ```dataview
        TABLE WITHOUT ID
          file.link as "Ion Column Image Log",
          image.parent_experiment_log as "Experiment Log",
          image.sequence_number as "Sequence",
          image.date_time as "Date / Time",
          file.mtime as "Modified"
        FROM #ion-column-image-log AND !"assets"
        WHERE contains(image.experiment_series_number, this.series.name) OR contains(image.parent_experiment_log, this.series.name)
        SORT file.mtime DESC
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_experiment_log(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    date_time = payload.get("dateTime") or current_timestamp()
    series_name = str(payload.get("seriesName", "")).strip()
    series_number = str(payload.get("seriesNumber", "")).strip()
    operators = [value.strip() for value in payload.get("operators", []) if str(value).strip()]
    gases = [value.strip() for value in payload.get("gasesIntroduced", []) if str(value).strip()]
    data_types = [value.strip() for value in payload.get("dataTypesRecorded", []) if str(value).strip()]
    raw_files = payload.get("rawDataFiles", [])
    raw_rows = []
    for row in raw_files:
        raw_rows.append(
            f"| {row.get('fileName', '').strip()} | {row.get('fileType', '').strip()} | {row.get('link', '').strip()} |"
        )
    if not raw_rows:
        raw_rows.append("|  |  |  |")

    log_id = str(payload.get("logId", "")).strip() or f"{date_created}-{slugify(series_name or 'experiment')}-{series_number or 'log'}"
    folder = VAULT_ROOT / settings["folders"].get("experiment logs", "Experiment Logs")
    file_path = folder / f"{sanitize_file_name(log_id)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: experiment-log
tags:
  - "#experiment-log"
experiment:
  log_id: {yaml_string(log_id)}
  series_name: {yaml_string(series_name, 'Add experiment series name')}
  series_number: {yaml_string(series_number, 'Add experiment number in series')}
  date_time: {yaml_string(str(date_time))}
  operators:
{yaml_list(operators, indent=4, fallback='Add operator')}
  status: {yaml_string(str(payload.get('status', 'draft')), 'draft')}
  instrument_configuration: {yaml_string(str(payload.get('instrumentConfiguration', '')))}
  instrument_condition: {yaml_string(str(payload.get('instrumentCondition', '')))}
specimen:
  type: {yaml_string(str(payload.get('specimenType', '')))}
  id: {yaml_string(str(payload.get('specimenId', '')))}
run:
  ion_column_used: {yaml_string(str(payload.get('ionColumnUsed', '')))}
  load_lock_vented: {yaml_string(str(payload.get('loadLockVented', '')))}
gas:
  introduced:
{yaml_list(gases, indent=4, fallback='none')}
data:
  types_recorded:
{yaml_list(data_types, indent=4, fallback='oscilloscope traces')}
  alignment_settings_file_link: {yaml_string(str(payload.get('alignmentSettingsFileLink', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        # Experiment Log

        | Field | Value |
        | --- | --- |
        | Experiment Series Name | {series_name} |
        | Experiment Number in Series | {series_number} |
        | Date / Time / Operator(s) | {date_time} / {", ".join(operators)} |
        | Instrument Configuration | {str(payload.get("instrumentConfiguration", "")).strip()} |

        ## Instrument Condition

        | Instrument Parameter | Condition | Units / Notes |
        | --- | --- | --- |
        | Main Chamber Starting Pressure | {str(payload.get("mainChamberStartingPressure", "")).strip()} | #.#E-# mbar ({settings.get("main_chamber_gauge", "Ion Gauge")}) |
        | Main Chamber Ending Pressure | {str(payload.get("mainChamberEndingPressure", "")).strip()} | #.#E-# mbar ({settings.get("main_chamber_gauge", "Ion Gauge")}) |
        | Main Ion Pump Current | {str(payload.get("mainIonPumpCurrent", "")).strip()} | #.# A |
        | Main Ion Pump Pressure | {str(payload.get("mainIonPumpPressure", "")).strip()} | #.#E-# mbar |
        | Puck Nest Temperature | {str(payload.get("puckNestTemperature", "")).strip()} | # K |
        | Cryo Setpoint | {str(payload.get("cryoSetpoint", "")).strip()} | # K |
        | Load Lock Starting Pressure | {str(payload.get("loadLockStartingPressure", "")).strip()} | #.#E-# mbar ({settings.get("load_lock_gauge", "LL Wide Range Gauge")}) |
        | Load Lock Ending Pressure | {str(payload.get("loadLockEndingPressure", "")).strip()} | #.#E-# mbar ({settings.get("load_lock_gauge", "LL Wide Range Gauge")}) |
        | Ion Column Starting Pressure | {str(payload.get("ionColumnStartingPressure", "")).strip()} | #.#E-# mbar ({settings.get("ion_column_gauge", "Ion Column Wide Range Gauge")}) |
        | Ion Column Ending Pressure | {str(payload.get("ionColumnEndingPressure", "")).strip()} | #.#E-# mbar ({settings.get("ion_column_gauge", "Ion Column Wide Range Gauge")}) |
        | Ion Column Ion Pump Current | {str(payload.get("ionColumnIonPumpCurrent", "")).strip()} | #.# A |
        | Ion Column Ion Pump Pressure | {str(payload.get("ionColumnIonPumpPressure", "")).strip()} | #.#E-# mbar |
        | Ion Column Used? | {str(payload.get("ionColumnUsed", "")).strip()} | Yes / No |
        | Specimen Type | {str(payload.get("specimenType", "")).strip()} | |
        | Specimen ID | {str(payload.get("specimenId", "")).strip()} | |
        | Gasses Introduced into Main Chamber | {", ".join(gases)} | He, O, etc. |
        | Load Lock Vented | {str(payload.get("loadLockVented", "")).strip()} | Yes / No |

        ## Experiment Description

        {str(payload.get("experimentDescription", "")).strip()}

        ## Parameter Ranges

        | Parameter Type | Value | Notes |
        | --- | --- | --- |
        | Independent Variable Range | {str(payload.get("independentVariableRange", "")).strip()} | min to max, with step size |
        | Dependent Variable Measurement Range | {str(payload.get("dependentMeasurementRange", "")).strip()} | min to max detectable; restrictions |
        | Emergency Stop Parameters | {str(payload.get("emergencyStopParameters", "")).strip()} | besides interlock faults |

        ## Data Types Recorded

        {chr(10).join(f"- {item}" for item in data_types) if data_types else "- Add recorded data types"}

        ## Names of Raw Data Files And Links To Their Location

        | File Name | File Type | Link / Location |
        | --- | --- | --- |
        {chr(10).join(raw_rows)}

        ## IonOptika Column Alignment Settings

        {str(payload.get("alignmentSettingsFileLink", "")).strip()}

        ## Data

        Insert or link experimental data below. Refer to the Data Formatting Guide for conventions on graphs, photos, MCP images, and Ion Column images.

        ## Linked MCP Image Logs

        ```dataview
        TABLE WITHOUT ID
          file.link as "MCP Image Log",
          image.sequence_number as "Sequence",
          image.date_time as "Date / Time",
          file.mtime as "Modified"
        FROM #mcp-image-log AND !"assets"
        WHERE image.parent_experiment_log = this.file.name
        SORT image.sequence_number ASC
        ```

        ## Linked Ion Column Image Logs

        ```dataview
        TABLE WITHOUT ID
          file.link as "Ion Column Image Log",
          image.sequence_number as "Sequence",
          image.date_time as "Date / Time",
          file.mtime as "Modified"
        FROM #ion-column-image-log AND !"assets"
        WHERE image.parent_experiment_log = this.file.name
        SORT image.sequence_number ASC
        ```

        ## Experiment Notes

        {str(payload.get("experimentNotes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_mcp_image_log(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    date_time = payload.get("dateTime") or current_timestamp()
    sequence = str(payload.get("imageSequenceNumber", "")).strip() or "1"
    parent_log = str(payload.get("parentExperimentLog", "")).strip()
    file_name = str(payload.get("fileName", "")).strip() or f"{current_date()}-mcp-image-{sequence}"
    folder = VAULT_ROOT / settings["folders"].get("mcp image logs", "Image Logs/MCP")
    file_path = folder / f"{sanitize_file_name(file_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: mcp-image-log
tags:
  - "#mcp-image-log"
image:
  parent_experiment_log: {yaml_string(parent_log, 'Link parent experiment log')}
  experiment_series_number: {yaml_string(str(payload.get('experimentSeriesNumber', '')))}
  date_time: {yaml_string(str(date_time))}
  sequence_number: {yaml_string(sequence)}
  status: {yaml_string(str(payload.get('status', 'draft')), 'draft')}
  front_voltage: {yaml_string(str(payload.get('mcpFrontVoltage', '')))}
  back_voltage: {yaml_string(str(payload.get('mcpBackVoltage', '')))}
  integration_time: {yaml_string(str(payload.get('integrationTime', '')))}
  specimen_stage_hv: {yaml_string(str(payload.get('specimenStageHv', '')))}
  main_chamber_pressure: {yaml_string(str(payload.get('mainChamberPressure', '')))}
  ion_column_settings: {yaml_string(str(payload.get('ionColumnSettings', '')))}
  imaging_gas: {yaml_string(str(payload.get('imagingGasUsed', '')))}
  image_file_name: {yaml_string(str(payload.get('imageFileName', '')))}
  image_file_link: {yaml_string(str(payload.get('imageFileLink', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        # MCP Image Data Log

        | Field | Value |
        | --- | --- |
        | Experiment Log | {parent_log} |
        | Experiment Series / Number | {str(payload.get("experimentSeriesNumber", "")).strip()} |
        | Date / Time | {date_time} |
        | Image Sequence Number | {sequence} |

        ## MCP Image Parameters

        | Parameter | Condition | Units / Format |
        | --- | --- | --- |
        | MCP Front Voltage | {str(payload.get("mcpFrontVoltage", "")).strip()} | +/- #### V |
        | MCP Back Voltage | {str(payload.get("mcpBackVoltage", "")).strip()} | +/- #### V |
        | Integration Time | {str(payload.get("integrationTime", "")).strip()} | ## s |
        | Specimen Stage HV | {str(payload.get("specimenStageHv", "")).strip()} | #### V |
        | Main Chamber Pressure (on ion gauge) | {str(payload.get("mainChamberPressure", "")).strip()} | #.#E-# mbar |
        | Ion Column Settings | {str(payload.get("ionColumnSettings", "")).strip()} | Inactive, or settings summary |
        | Imaging Gas Used, if any | {str(payload.get("imagingGasUsed", "")).strip()} | Helium, or N/A |

        ## MCP Image

        Attach or embed the MCP image below.

        | Field | Value |
        | --- | --- |
        | Image File Name | {str(payload.get("imageFileName", "")).strip()} |
        | Image File Link / Location | {str(payload.get("imageFileLink", "")).strip()} |

        [Paste or insert MCP image here]

        ## Notes

        {str(payload.get("notes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_ion_column_image_log(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    date_time = payload.get("dateTime") or current_timestamp()
    sequence = str(payload.get("imageSequenceNumber", "")).strip() or "1"
    parent_log = str(payload.get("parentExperimentLog", "")).strip()
    file_name = str(payload.get("fileName", "")).strip() or f"{current_date()}-ion-column-image-{sequence}"
    folder = VAULT_ROOT / settings["folders"].get("ion column image logs", "Image Logs/Ion Column")
    file_path = folder / f"{sanitize_file_name(file_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: ion-column-image-log
tags:
  - "#ion-column-image-log"
image:
  parent_experiment_log: {yaml_string(parent_log, 'Link parent experiment log')}
  experiment_series_number: {yaml_string(str(payload.get('experimentSeriesNumber', '')))}
  date_time: {yaml_string(str(date_time))}
  sequence_number: {yaml_string(sequence)}
  status: {yaml_string(str(payload.get('status', 'draft')), 'draft')}
  accelerating_voltage: {yaml_string(str(payload.get('acceleratingVoltage', '')))}
  source_pressure: {yaml_string(str(payload.get('sourcePressure', '')))}
  aperture_number: {yaml_string(str(payload.get('apertureNumber', '')))}
  field_of_view: {yaml_string(str(payload.get('fieldOfView', '')))}
  pixel_dwell_time: {yaml_string(str(payload.get('pixelDwellTime', '')))}
  signal_source: {yaml_string(str(payload.get('signalSource', '')))}
  image_file_name: {yaml_string(str(payload.get('imageFileName', '')))}
  image_file_link: {yaml_string(str(payload.get('imageFileLink', '')))}
  signal_only_file_name: {yaml_string(str(payload.get('signalOnlyImageFileName', '')))}
  signal_only_file_link: {yaml_string(str(payload.get('signalOnlyImageFileLink', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        # Ion Column Image Data Log

        | Field | Value |
        | --- | --- |
        | Experiment Log | {parent_log} |
        | Experiment Series / Number | {str(payload.get("experimentSeriesNumber", "")).strip()} |
        | Date / Time | {date_time} |
        | Image Sequence Number | {sequence} |

        ## Ion Column Image Parameters

        | Parameter | Condition | Units / Format |
        | --- | --- | --- |
        | Ion Column Accelerating Voltage | {str(payload.get("acceleratingVoltage", "")).strip()} | # kV or V |
        | Ion Column Source Pressure | {str(payload.get("sourcePressure", "")).strip()} | #.#E-# mbar |
        | Aperture Number | {str(payload.get("apertureNumber", "")).strip()} | # or diameter in um |
        | Field of View | {str(payload.get("fieldOfView", "")).strip()} | ### um |
        | Pixel Dwell Time | {str(payload.get("pixelDwellTime", "")).strip()} | # ms or s |
        | Signal Source | {str(payload.get("signalSource", "")).strip()} | SED or current measurement |

        ## Ion Column Image

        | Field | Value |
        | --- | --- |
        | Image File Name | {str(payload.get("imageFileName", "")).strip()} |
        | Image File Link / Location | {str(payload.get("imageFileLink", "")).strip()} |

        [Paste or insert Ion Column image here]

        ## Full-Resolution Signal-Only Image

        | Field | Value |
        | --- | --- |
        | Signal-Only Image File Name | {str(payload.get("signalOnlyImageFileName", "")).strip()} |
        | Signal-Only Image Link / Location | {str(payload.get("signalOnlyImageFileLink", "")).strip()} |

        ## Notes

        {str(payload.get("notes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_instrument_configuration(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    name = str(payload.get("configurationName", "")).strip() or "Instrument Configuration"
    folder = VAULT_ROOT / settings["folders"].get("instrument configurations", "Instrument Configurations")
    file_path = folder / f"{sanitize_file_name(name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: instrument-configuration
tags:
  - "#instrument-config"
configuration:
  name: {yaml_string(name)}
  type: {yaml_string(str(payload.get('configurationType', 'Hybrid')), 'Hybrid')}
  status: {yaml_string(str(payload.get('configurationStatus', 'active')), 'active')}
  instrument_name: {yaml_string(str(payload.get('instrumentName', 'Hybrid FIM/APT Tool')))}
  alignment_settings_file: {yaml_string(str(payload.get('alignmentSettingsFile', '')))}
  main_chamber_gauge: {yaml_string(str(payload.get('mainChamberGauge', settings.get('main_chamber_gauge', 'Ion Gauge'))))}
  load_lock_gauge: {yaml_string(str(payload.get('loadLockGauge', settings.get('load_lock_gauge', 'LL Wide Range Gauge'))))}
  ion_column_gauge: {yaml_string(str(payload.get('ionColumnGauge', settings.get('ion_column_gauge', 'Ion Column Wide Range Gauge'))))}
"""
    )

    body = textwrap.dedent(
        f"""
        # Configuration Summary

        | Field | Value | Notes |
        | --- | --- | --- |
        | Configuration | {name} | |
        | Type | {str(payload.get("configurationType", "Hybrid")).strip()} | |
        | Status | {str(payload.get("configurationStatus", "active")).strip()} | |
        | Instrument | {str(payload.get("instrumentName", "Hybrid FIM/APT Tool")).strip()} | |
        | Alignment settings archive | {str(payload.get("alignmentSettingsFile", "")).strip()} | |

        ## Gauge Mapping

        | Location | Gauge / Readback | Notes |
        | --- | --- | --- |
        | Main chamber | {str(payload.get("mainChamberGauge", settings.get("main_chamber_gauge", "Ion Gauge"))).strip()} | |
        | Load lock | {str(payload.get("loadLockGauge", settings.get("load_lock_gauge", "LL Wide Range Gauge"))).strip()} | |
        | Ion column | {str(payload.get("ionColumnGauge", settings.get("ion_column_gauge", "Ion Column Wide Range Gauge"))).strip()} | |
        | Main pump | {str(payload.get("mainIonPumpLabel", "Main Ion Pump")).strip()} | |
        | Ion column pump | {str(payload.get("ionColumnIonPumpLabel", "Ion Column Ion Pump")).strip()} | |

        ## Interlocks And Safeties

        | Item | Configured State | Notes |
        | --- | --- | --- |
        | Vacuum interlocks active | {str(payload.get("vacuumInterlocksActive", "")).strip()} | |
        | High-voltage interlocks active | {str(payload.get("highVoltageInterlocksActive", "")).strip()} | |
        | MCP protection active | {str(payload.get("mcpProtectionActive", "")).strip()} | |
        | Ion column protection active | {str(payload.get("ionColumnProtectionActive", "")).strip()} | |
        | Safeties intentionally bypassed | {str(payload.get("safetiesBypassed", "")).strip()} | |
        | Required stop conditions beyond interlocks | {str(payload.get("requiredStopConditions", "")).strip()} | |

        ## Startup Targets

        | Parameter | Target | Units / Notes |
        | --- | --- | --- |
        | Main chamber target pressure | {str(payload.get("mainChamberTargetPressure", "")).strip()} | mbar |
        | Load lock target pressure | {str(payload.get("loadLockTargetPressure", "")).strip()} | mbar |
        | Ion column target pressure | {str(payload.get("ionColumnTargetPressure", "")).strip()} | mbar |
        | Main ion pump target current | {str(payload.get("mainIonPumpTargetCurrent", "")).strip()} | A |
        | Ion column ion pump target current | {str(payload.get("ionColumnIonPumpTargetCurrent", "")).strip()} | A |
        | Puck nest target temperature | {str(payload.get("puckNestTargetTemperature", "")).strip()} | K |
        | Cryo target | {str(payload.get("cryoTarget", "")).strip()} | K |

        ## Imaging Defaults

        | Parameter | Default | Units / Notes |
        | --- | --- | --- |
        | MCP front voltage | {str(payload.get("mcpFrontVoltageDefault", "")).strip()} | V |
        | MCP back voltage | {str(payload.get("mcpBackVoltageDefault", "")).strip()} | V |
        | Specimen stage HV | {str(payload.get("specimenStageHvDefault", "")).strip()} | V |
        | Ion column accelerating voltage | {str(payload.get("ionColumnAcceleratingVoltageDefault", "")).strip()} | V |
        | Ion column source pressure | {str(payload.get("ionColumnSourcePressureDefault", "")).strip()} | mbar |
        | Preferred image export format | {str(payload.get("preferredImageExportFormat", "")).strip()} | |
        | Preferred signal source | {str(payload.get("preferredSignalSource", "")).strip()} | |

        ## Operating Notes

        {str(payload.get("operatingNotes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_specimen(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    specimen_id = str(payload.get("specimenId", "")).strip() or "specimen"
    note_name = str(payload.get("specimenName", "")).strip() or specimen_id
    folder = VAULT_ROOT / settings["folders"].get("specimens", "Specimens")
    file_path = folder / f"{sanitize_file_name(note_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - wide-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: specimen
tags:
  - "#specimen"
specimen:
  name: {yaml_string(note_name)}
  id: {yaml_string(specimen_id)}
  type: {yaml_string(str(payload.get('specimenType', 'APT needle')), 'APT needle')}
  material: {yaml_string(str(payload.get('material', '')))}
  preparation_state: {yaml_string(str(payload.get('preparationState', '')))}
  storage_location: {yaml_string(str(payload.get('storageLocation', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        # Specimen Summary

        | Field | Value |
        | --- | --- |
        | Specimen ID | {specimen_id} |
        | Type | {str(payload.get("specimenType", "")).strip()} |
        | Material | {str(payload.get("material", "")).strip()} |
        | Preparation state | {str(payload.get("preparationState", "")).strip()} |
        | Storage location | {str(payload.get("storageLocation", "")).strip()} |

        ## Preparation Notes

        {str(payload.get("preparationNotes", "")).strip()}

        ## Handling Notes

        {str(payload.get("handlingNotes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_contact(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    given_name = str(payload.get("givenName", "")).strip()
    family_name = str(payload.get("familyName", "")).strip()
    note_name = str(payload.get("noteName", "")).strip() or " ".join(part for part in [given_name, family_name] if part).strip() or "Contact"
    folder = VAULT_ROOT / settings["folders"].get("contacts", "Contacts")
    file_path = folder / f"{sanitize_file_name(note_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclasses:
  - normal-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: contact
tags:
  - "#contact"
name:
  title: {yaml_string(str(payload.get('title', '')))}
  given name: {yaml_string(given_name)}
  family name: {yaml_string(family_name)}
contact:
  work:
    email: {yaml_string(str(payload.get('workEmail', '')))}
    phone: {yaml_string(str(payload.get('workPhone', '')))}
    mobile: {yaml_string(str(payload.get('mobile', '')))}
    fax: {yaml_string(str(payload.get('fax', '')))}
address:
  work:
    affiliation: {yaml_string(str(payload.get('affiliation', '')))}
    division: {yaml_string(str(payload.get('division', '')))}
    street: {yaml_string(str(payload.get('street', '')))}
    building: {yaml_string(str(payload.get('building', '')))}
    room: {yaml_string(str(payload.get('room', '')))}
    city: {yaml_string(str(payload.get('city', '')))}
    zip code: {yaml_string(str(payload.get('zipCode', '')))}
    country: {yaml_string(str(payload.get('country', '')))}
job position: {yaml_string(str(payload.get('jobPosition', '')))}
group: {yaml_string(str(payload.get('group', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/navbar", {{}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_header", {{}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/contact", {{obsidian: obsidian}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_footer", {{}});
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_daily_note(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    now = datetime.now()
    date_created = current_date()
    year = current_year()
    month_number = current_month_number()
    month_name = current_month_name()
    weekday_name = current_weekday_name()
    note_title = f"{date_created} - {weekday_name}, {now.day}. {month_name}"
    folder = VAULT_ROOT / settings["folders"].get("daily notes", "Daily Notes") / year / f"{month_number} {month_name}"
    file_path = folder / f"{sanitize_file_name(note_title)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclass: daily-note
banner: "![[obsidian-eln-banner.png]]"
banner_y: 0.336
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: daily-note
tag:
  - " #daily-note "
"""
    )

    body = textwrap.dedent(
        f"""
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/navbar", {{}});
        ```

        <div class="title" style="color:#edf">
          {note_title}
        </div>

        ```dataviewjs
          await dv.view("/assets/javascript/dataview/views/daily_note_nav", {{}});
        ```

        # Daily Note - {note_title}

          - ### Tasks
            - [ ] Today 1
            - [ ] Today 2
            - [ ] Today 3

        - ### 
          ```dataviewjs
          await dv.view("/assets/javascript/dataview/views/motivation_image", {{}});
          ```

        - ### Progress
          ```dataviewjs
          await dv.view("/assets/javascript/dataview/views/circular_progress", {{}});
          ```

        # Notes

        {str(payload.get("notes", "")).strip()}

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_footer", {{}});
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def add_minutes(time_string: str, minutes: int) -> str:
    base = datetime.strptime(time_string, "%H:%M")
    return (base.replace(year=1970, month=1, day=1) + timedelta(minutes=minutes)).strftime("%H:%M")


def build_meeting(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    now = datetime.now()
    date_created = current_date()
    year = current_year()
    month_number = current_month_number()
    month_name = current_month_name()
    rounded_minutes = round(now.minute / 15) * 15
    if rounded_minutes == 60:
      start_dt = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
      start_dt = now.replace(minute=rounded_minutes, second=0, microsecond=0)
    starting_time = start_dt.strftime("%H:%M")
    meeting_title = str(payload.get("meetingTitle", "")).strip() or "Meeting"
    folder = VAULT_ROOT / settings["folders"].get("meetings", "Meetings") / year / f"{month_number} {month_name}"
    file_path = folder / f"{sanitize_file_name(f'{date_created} - {meeting_title}')}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclass: meeting
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: meeting
tag:
  - " #meeting "
meeting:
   title: {yaml_string(meeting_title)}
   type: {yaml_string(str(payload.get('meetingType', '')))}
   date: {yaml_string(date_created)}
   time: {yaml_string(starting_time)}
   location: {yaml_string(str(payload.get('location', '')))}
   participants:
{yaml_list([item.strip() for item in str(payload.get('participants', '')).split(',') if item.strip()], indent=5, fallback='First Participant')}
project:
   name: {yaml_string(str(payload.get('projectName', '')))}
"""
    )

    body = textwrap.dedent(
        f"""
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/navbar", {{}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_header", {{}});
        ```

        ## Meeting Info

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/meeting", {{obsidian: obsidian}});
        ```

        ## Agenda & Minutes

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/meeting_topics", {{  }});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/meeting_topics", {{  }});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/meeting_topics", {{  }});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/meeting_topics", {{  }});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_footer", {{}});
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_note(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    note_name = str(payload.get("noteName", "")).strip() or "Untitled"
    folder = VAULT_ROOT / settings["folders"].get("notes", "Notes")
    file_path = folder / f"{sanitize_file_name(note_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclass: normal-page
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: note
tag:
  - " #note "
"""
    )

    body = textwrap.dedent(
        f"""
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/navbar", {{}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_header", {{}});
        ```

        {str(payload.get("body", "")).strip()}

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_footer", {{}});
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_task_list(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    task_list_name = str(payload.get("taskListName", "")).strip() or "My Tasks"
    folder = VAULT_ROOT / settings["folders"].get("tasks", "Tasks")
    file_path = folder / f"{sanitize_file_name(task_list_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
cssclass: task-list
author: {yaml_string('StarDustX')}
date created: {yaml_string(date_created)}
note type: task-list
tag:
  - " #task "
"""
    )

    body = textwrap.dedent(
        f"""
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/navbar", {{}});
        ```

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_header", {{}});
        ```

        ## Progress
        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/circular_progress", {{}});
        ```

        ## High Priority Tasks

        - [ ] High Priority Task

        ## Medium Priority Tasks

        - [ ] Medium Priority Task

        ## Low Priority Tasks

        - [ ] Low Priority Task

        ```dataviewjs
        await dv.view("/assets/javascript/dataview/views/note_footer", {{}});
        ```
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_startup_checklist(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    checklist_name = str(payload.get("checklistName", "")).strip() or "APT FIM Startup Checklist"
    folder = VAULT_ROOT / settings["folders"].get("startup checklists", "Checklists/Startup")
    file_path = folder / f"{sanitize_file_name(checklist_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: startup-checklist
tags:
  - "#startup-checklist"
checklist:
  name: {yaml_string(checklist_name)}
  phase: "startup"
  configuration_name: {yaml_string(str(payload.get('configurationName', '')), 'Add configuration link')}
  status: {yaml_string(str(payload.get('status', 'active')), 'active')}
"""
    )

    body = textwrap.dedent(
        f"""
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

        {str(payload.get("notes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


def build_shutdown_checklist(payload: dict[str, object], settings: dict[str, object]) -> tuple[Path, str]:
    date_created = current_date()
    checklist_name = str(payload.get("checklistName", "")).strip() or "APT FIM Shutdown Checklist"
    folder = VAULT_ROOT / settings["folders"].get("shutdown checklists", "Checklists/Shutdown")
    file_path = folder / f"{sanitize_file_name(checklist_name)}.md"

    fm = frontmatter(
        f"""
ELN version: {yaml_string(str(settings.get('eln_version', '0.5.0')))}
date created: {yaml_string(date_created)}
author: {yaml_string('StarDustX')}
note type: shutdown-checklist
tags:
  - "#shutdown-checklist"
checklist:
  name: {yaml_string(checklist_name)}
  phase: "shutdown"
  configuration_name: {yaml_string(str(payload.get('configurationName', '')), 'Add configuration link')}
  status: {yaml_string(str(payload.get('status', 'active')), 'active')}
"""
    )

    body = textwrap.dedent(
        f"""
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

        {str(payload.get("notes", "")).strip()}
        """
    ).strip()

    return file_path, f"{fm}\n\n{body}\n"


BUILDERS = {
    "experiment-series": build_experiment_series,
    "experiment-log": build_experiment_log,
    "mcp-image-log": build_mcp_image_log,
    "ion-column-image-log": build_ion_column_image_log,
    "instrument-configuration": build_instrument_configuration,
    "specimen": build_specimen,
    "contact": build_contact,
    "daily-note": build_daily_note,
    "meeting": build_meeting,
    "note": build_note,
    "task-list": build_task_list,
    "startup-checklist": build_startup_checklist,
    "shutdown-checklist": build_shutdown_checklist,
}


def get_options() -> dict[str, object]:
    settings = parse_settings()
    return {
        "seriesNames": note_choices("experiment series"),
        "specimenNames": note_choices("specimens"),
        "instrumentConfigurations": note_choices("instrument configurations"),
        "experimentLogs": note_choices("experiment logs"),
        "experimentSeriesTypes": settings["experiment_series_types"],
        "experimentSeriesStatuses": settings["experiment_series_statuses"],
        "gases": settings["gases"],
        "experimentLogStatuses": settings["experiment_log_statuses"],
        "experimentLogDataTypes": settings["experiment_log_data_types"],
        "mcpStatuses": settings["mcp_statuses"],
        "mcpFormats": settings["mcp_formats"],
        "ionStatuses": settings["ion_statuses"],
        "ionSignalSources": settings["ion_signal_sources"],
        "ionFormats": settings["ion_formats"],
        "instrumentConfigTypes": settings["instrument_config_types"],
        "specimenTypes": settings["specimen_types"],
        "gauges": {
            "mainChamber": settings["main_chamber_gauge"],
            "loadLock": settings["load_lock_gauge"],
            "ionColumn": settings["ion_column_gauge"],
        },
    }


def rel_to_posix(path: Path) -> str:
    return str(path).replace("\\", "/")


def resource_settings_and_paths() -> tuple[dict[str, object], dict[str, Path]]:
    settings = parse_settings()
    paths = resolve_resource_paths(VAULT_ROOT, settings)
    ensure_directories(paths)
    return settings, paths


def ensure_within(root: Path, relative_value: str) -> Path:
    base = root.resolve()
    candidate = (root / relative_value).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"Path escapes resource folder: {relative_value}") from exc
    return candidate


def selected_pdf_paths(payload: dict[str, object], pdf_dir: Path) -> list[Path]:
    requested = payload.get("pdfs") or []
    if payload.get("unsummarizedOnly"):
        _, paths = resource_settings_and_paths()
        files = scan_pdf_library(paths["pdfs"], paths["summaries"], paths["index"])
        requested = unsummarized_pdf_rel_paths(files)
    if not requested:
        return sorted(pdf_dir.rglob("*.pdf"))
    return [ensure_within(pdf_dir, str(item)) for item in requested]


def selected_summary_paths(payload: dict[str, object], summary_dir: Path) -> list[Path]:
    requested = payload.get("summaryNotes") or []
    return [ensure_within(summary_dir, str(item)) for item in requested]


def note_body(markdown: str) -> str:
    if markdown.startswith("---"):
        parts = markdown.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return markdown.strip()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _resource_folders(paths: dict[str, Path]) -> dict[str, str]:
    pdf_root = paths["pdfs"]
    ensure_resource_subdirectories(pdf_root)
    processed_root = processed_pdf_dir(pdf_root)
    failed_root = failed_pdf_dir(pdf_root)
    return {
        "pdfs": rel_to_posix(pdf_root.relative_to(VAULT_ROOT)),
        "processed": rel_to_posix(processed_root.relative_to(VAULT_ROOT)),
        "failed": rel_to_posix(failed_root.relative_to(VAULT_ROOT)),
        "summaries": rel_to_posix(paths["summaries"].relative_to(VAULT_ROOT)),
        "topics": rel_to_posix(paths["topics"].relative_to(VAULT_ROOT)),
        "index": rel_to_posix(paths["index"].relative_to(VAULT_ROOT)),
    }


def _workflow_status_token(value: object) -> str | None:
    if value is None:
        return None
    token = str(value).strip().lower()
    if token in {"pending", "processing", "done", "failed"}:
        return token
    return None


def _resource_item_state(
    item: dict[str, object],
    *,
    index_dir: Path,
    processed_root: Path,
    failed_root: Path,
) -> dict[str, object]:
    pdf_path = Path(str(item["pdf_path"]))
    _resolved_index_path, _resolved_emb_path, index_payload = _resolve_index_paths_for_scan(pdf_path, index_dir)

    # Prefer scan metadata (index_status) from the library scan, then the same
    # resolver used above — never let summary heuristics override a durable token.
    scan_token = _workflow_status_token(item.get("index_status"))
    index_token = _workflow_status_token(index_payload.get("status"))

    if scan_token is not None:
        status = scan_token
    elif index_token is not None:
        status = index_token
    elif _is_within(pdf_path, failed_root):
        status = "failed"
    elif _is_within(pdf_path, processed_root):
        status = "done"
    elif str(index_payload.get("error_message", "")).strip():
        status = "failed"
    elif is_processing_complete(item, require_embeddings=False):
        status = "done"
    else:
        status = "pending"

    enriched = dict(item)
    enriched["status"] = status
    if index_payload.get("processing_started_at"):
        enriched["processingStartedAt"] = index_payload["processing_started_at"]
    if index_payload.get("processing_finished_at"):
        enriched["processingFinishedAt"] = index_payload["processing_finished_at"]
    if index_payload.get("error_message"):
        enriched["errorMessage"] = index_payload["error_message"]
    if index_payload.get("original_pdf_rel_path"):
        enriched["originalPdfRelPath"] = index_payload["original_pdf_rel_path"]
    if index_payload.get("current_pdf_rel_path"):
        enriched["currentPdfRelPath"] = index_payload["current_pdf_rel_path"]
    return enriched


def _resource_counts(items: list[dict[str, object]], summary_count: int) -> dict[str, int]:
    return {
        "pdfs": len(items),
        "pending": sum(1 for item in items if item["status"] == "pending"),
        "processing": sum(1 for item in items if item["status"] == "processing"),
        "done": sum(1 for item in items if item["status"] == "done"),
        "failed": sum(1 for item in items if item["status"] == "failed"),
        "summaries": summary_count,
        "indexed": sum(1 for item in items if item["has_index"]),
        "embedded": sum(1 for item in items if item["has_embeddings"]),
    }


def get_resource_status() -> dict[str, object]:
    _, paths = resource_settings_and_paths()
    pdf_root = paths["pdfs"]
    processed_root = processed_pdf_dir(pdf_root)
    failed_root = failed_pdf_dir(pdf_root)
    summary_dir = paths["summaries"]
    index_dir = paths["index"]
    folders = _resource_folders(paths)

    files = [
        _resource_item_state(
            item,
            index_dir=index_dir,
            processed_root=processed_root,
            failed_root=failed_root,
        )
        for item in scan_pdf_library(pdf_root, summary_dir, index_dir)
    ]
    intake_files = [
        _resource_item_state(
            item,
            index_dir=index_dir,
            processed_root=processed_root,
            failed_root=failed_root,
        )
        for item in scan_intake_pdf_library(pdf_root, summary_dir, index_dir)
    ]
    summary_count = len(list(summary_dir.rglob("*.md"))) if summary_dir.exists() else 0

    return {
        "folders": folders,
        "counts": _resource_counts(files, summary_count),
        "files": files,
        "intakeFiles": intake_files,
    }


def get_resource_intake_status() -> dict[str, object]:
    _, paths = resource_settings_and_paths()
    pdf_root = paths["pdfs"]
    processed_root = processed_pdf_dir(pdf_root)
    failed_root = failed_pdf_dir(pdf_root)
    summary_dir = paths["summaries"]
    index_dir = paths["index"]
    folders = _resource_folders(paths)

    intake_files = [
        _resource_item_state(
            item,
            index_dir=index_dir,
            processed_root=processed_root,
            failed_root=failed_root,
        )
        for item in scan_intake_pdf_library(pdf_root, summary_dir, index_dir)
    ]
    summary_count = len(list(summary_dir.rglob("*.md"))) if summary_dir.exists() else 0
    counts = _resource_counts(intake_files, summary_count)
    counts["done"] = len(list(processed_root.rglob("*.pdf"))) if processed_root.exists() else 0
    counts["failed"] = len(list(failed_root.rglob("*.pdf"))) if failed_root.exists() else 0

    return {
        "folders": folders,
        "counts": counts,
        "intakeFiles": intake_files,
    }


def get_resource_presets() -> dict[str, object]:
    return {"presets": build_provider_presets()}


def get_resource_pdf(relative_value: str) -> tuple[Path, bytes]:
    _, paths = resource_settings_and_paths()
    pdf_path = ensure_within(paths["pdfs"], relative_value)
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        raise FileNotFoundError(relative_value)
    return pdf_path, pdf_path.read_bytes()


def run_resource_ingest(payload: dict[str, object]) -> dict[str, object]:
    _, paths = resource_settings_and_paths()
    pdf_paths = selected_pdf_paths(payload, paths["pdfs"])
    generate_embeddings = bool(payload.get("generateEmbeddings"))
    provider_config = prepare_provider_config(payload) if generate_embeddings else None

    results = []
    for pdf_path in pdf_paths:
        indexed = ingest_pdf(pdf_path, paths["index"], generate_embeddings, provider_config)
        results.append(
            {
                "pdf_name": pdf_path.name,
                "chunk_count": indexed["chunk_count"],
                "page_count": indexed["page_count"],
            }
        )

    return {
        "message": f"Ingested {len(results)} PDF(s).",
        "results": results,
        "status": get_resource_status(),
    }


def run_resource_summary(payload: dict[str, object]) -> dict[str, object]:
    provider_config = prepare_provider_config(payload)
    _, paths = resource_settings_and_paths()
    pdf_paths = selected_pdf_paths(payload, paths["pdfs"])
    results = []

    for pdf_path in pdf_paths:
        index_path = paths["index"] / f"{pdf_index_key(pdf_path)}.json"
        if not index_path.exists():
            ingest_pdf(pdf_path, paths["index"], False)
        indexed = read_json(index_path, {})
        if not indexed.get("chunks"):
            raise ValueError(f"No extracted chunks available for {pdf_path.name}.")

        summary_payload = summarize_pdf_chunks(pdf_path.stem, indexed["chunks"], provider_config)
        note_path = paths["summaries"] / summary_note_name(pdf_path)
        relative_pdf = rel_to_posix(pdf_path.relative_to(VAULT_ROOT))
        content = render_pdf_summary_note(
            pdf_title=pdf_path.stem,
            pdf_rel_path=relative_pdf,
            provider_label=provider_config["provider"],
            model_name=provider_config["model"],
            summary_text=summary_payload["summary_text"],
            citations=summary_payload["citations"],
        )
        write_file(note_path, content)
        results.append(
            {
                "pdf_name": pdf_path.name,
                "summary_name": note_path.name,
                "summary_path": rel_to_posix(note_path.relative_to(VAULT_ROOT)),
            }
        )

    return {
        "message": f"Summarized {len(results)} PDF(s).",
        "results": results,
        "status": get_resource_status(),
    }


def run_resource_process_intake(payload: dict[str, object]) -> dict[str, object]:
    _, paths = resource_settings_and_paths()
    generate_embeddings = bool(payload.get("generateEmbeddings"))
    config = prepare_provider_config(payload)
    intake_items = scan_intake_pdf_library(paths["pdfs"], paths["summaries"], paths["index"])
    discovered = len(intake_items)
    batch = process_intake_library(
        VAULT_ROOT,
        pdf_dir=paths["pdfs"],
        summary_dir=paths["summaries"],
        index_dir=paths["index"],
        config=config,
        generate_embeddings=generate_embeddings,
    )
    processed = int(batch.get("processed", 0))
    succeeded = int(batch.get("succeeded", 0))
    failed = int(batch.get("failed", 0))
    return {
        "discovered": discovered,
        "processed": processed,
        "succeeded": succeeded,
        "failed": failed,
        "results": batch.get("results", []),
        "status": get_resource_status(),
        "message": f"Discovered {discovered} intake PDF(s); processed {processed} this run ({succeeded} succeeded, {failed} failed).",
    }


def run_topic_synthesis(payload: dict[str, object]) -> dict[str, object]:
    provider_config = prepare_provider_config(payload)
    topic_title = str(payload.get("topicTitle", "")).strip() or "APT FIM Topic Summary"
    _, paths = resource_settings_and_paths()
    summary_paths = selected_summary_paths(payload, paths["summaries"])
    if not summary_paths:
        raise ValueError("Select at least one summary note to synthesize.")

    source_payloads = []
    for summary_path in summary_paths:
        markdown = read_file(summary_path)
        source_payloads.append(
            {
                "title": summary_path.stem,
                "summary": note_body(markdown),
                "summary_rel_path": rel_to_posix(summary_path.relative_to(VAULT_ROOT)),
            }
        )

    synthesized = synthesize_topic_summary(topic_title, source_payloads, provider_config)
    note_path = paths["topics"] / topic_note_name(topic_title)
    content = render_topic_summary_note(
        topic_title=topic_title,
        topic_summary=synthesized,
        sources=source_payloads,
        provider_name=provider_config["provider"],
        model_name=provider_config["model"],
    )
    write_file(note_path, content)
    return {
        "message": f"Created topic summary {note_path.name}.",
        "topic_path": rel_to_posix(note_path.relative_to(VAULT_ROOT)),
        "status": get_resource_status(),
    }


class LabLogRequestHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._send(HTTPStatus.OK, read_file(ROOT / "index.html").encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/app.js":
            self._send(HTTPStatus.OK, read_file(ROOT / "app.js").encode("utf-8"), "application/javascript; charset=utf-8")
            return
        if path == "/styles.css":
            self._send(HTTPStatus.OK, read_file(ROOT / "styles.css").encode("utf-8"), "text/css; charset=utf-8")
            return
        if path == "/api/options":
            payload = json.dumps(get_options()).encode("utf-8")
            self._send(HTTPStatus.OK, payload, "application/json; charset=utf-8")
            return
        if path == "/api/health":
            self._send(HTTPStatus.OK, b'{"status":"ok"}', "application/json; charset=utf-8")
            return
        if path == "/api/resources/status":
            payload = json.dumps(get_resource_status()).encode("utf-8")
            self._send(HTTPStatus.OK, payload, "application/json; charset=utf-8")
            return
        if path == "/api/resources/files":
            payload = json.dumps(get_resource_status()).encode("utf-8")
            self._send(HTTPStatus.OK, payload, "application/json; charset=utf-8")
            return
        if path == "/api/resources/presets":
            payload = json.dumps(get_resource_presets()).encode("utf-8")
            self._send(HTTPStatus.OK, payload, "application/json; charset=utf-8")
            return
        if path == "/api/resources/pdf":
            rel_path = parse_qs(parsed.query).get("path", [""])[0]
            try:
                pdf_path, content = get_resource_pdf(rel_path)
            except FileNotFoundError:
                self._send(HTTPStatus.NOT_FOUND, b"Not Found", "text/plain; charset=utf-8")
                return
            except Exception as exc:
                self._send(
                    HTTPStatus.BAD_REQUEST,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Content-Disposition", f'inline; filename="{pdf_path.name}"')
            self.end_headers()
            self.wfile.write(content)
            return

        self._send(HTTPStatus.NOT_FOUND, b"Not Found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(HTTPStatus.BAD_REQUEST, b'{"error":"Invalid JSON"}', "application/json; charset=utf-8")
            return

        if parsed.path == "/api/resources/scan":
            try:
                response = get_resource_status()
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
        if parsed.path == "/api/resources/scan-intake":
            try:
                response = get_resource_intake_status()
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
        if parsed.path == "/api/resources/process-intake":
            try:
                response = run_resource_process_intake(payload)
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
        if parsed.path == "/api/resources/ingest":
            try:
                response = run_resource_ingest(payload)
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
        if parsed.path == "/api/resources/summarize":
            try:
                response = run_resource_summary(payload)
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return
        if parsed.path == "/api/resources/synthesize-topic":
            try:
                response = run_topic_synthesis(payload)
                self._send(HTTPStatus.OK, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            except Exception as exc:  # pragma: no cover - local best effort
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    json.dumps({"error": str(exc)}).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
            return

        if parsed.path != "/api/create":
            self._send(HTTPStatus.NOT_FOUND, b"Not Found", "text/plain; charset=utf-8")
            return

        form_type = str(payload.get("formType", "")).strip()
        builder = BUILDERS.get(form_type)
        if builder is None:
            self._send(HTTPStatus.BAD_REQUEST, b'{"error":"Unknown form type"}', "application/json; charset=utf-8")
            return

        settings = parse_settings()
        try:
            path, content = builder(payload, settings)
            if path.exists():
                response = {"error": f"File already exists: {path.name}"}
                self._send(HTTPStatus.CONFLICT, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
                return
            write_file(path, content)
        except Exception as exc:  # pragma: no cover - best effort local tool
            response = {"error": str(exc)}
            self._send(HTTPStatus.INTERNAL_SERVER_ERROR, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")
            return

        response = {
            "path": str(path.relative_to(VAULT_ROOT)),
            "absolutePath": str(path),
            "fileName": path.name,
        }
        self._send(HTTPStatus.CREATED, json.dumps(response).encode("utf-8"), "application/json; charset=utf-8")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), LabLogRequestHandler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Lab log writer serving at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    server.serve_forever()


if __name__ == "__main__":
    main()
