from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - optional dependency at runtime
    PdfReader = None


DEFAULT_RESOURCE_FOLDERS = {
    "pdfs": "Resources/APT-FIM/PDFs",
    "summaries": "Resources/APT-FIM/Summaries",
    "topics": "Resources/APT-FIM/Topics",
    "index": "Resources/APT-FIM/.index",
}

PROVIDER_PRESETS = [
    {
        "id": "ollama-local",
        "label": "Ollama local",
        "provider": "ollama",
        "baseUrl": "http://127.0.0.1:11434",
        "model": "llama3.1",
        "embeddingModel": "nomic-embed-text",
        "notes": "Offline/local workflow through the Ollama API.",
    },
    {
        "id": "lmstudio-local",
        "label": "LM Studio local",
        "provider": "lmstudio",
        "baseUrl": "http://127.0.0.1:1234/v1",
        "model": "local-model",
        "embeddingModel": "text-embedding-model",
        "notes": "OpenAI-compatible local endpoint exposed by LM Studio.",
    },
    {
        "id": "openai-default",
        "label": "OpenAI hosted",
        "provider": "openai",
        "baseUrl": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
        "embeddingModel": "text-embedding-3-small",
        "notes": "Hosted workflow that requires an OpenAI API key.",
    },
    {
        "id": "anthropic-default",
        "label": "Anthropic hosted",
        "provider": "anthropic",
        "baseUrl": "https://api.anthropic.com/v1",
        "model": "claude-3-5-sonnet-latest",
        "embeddingModel": "",
        "notes": "Hosted workflow for summaries and topic synthesis.",
    },
]


def sanitize_file_name(value: str) -> str:
    safe = re.sub(r'[\\/:*?"<>|]+', "-", str(value or "").strip())
    safe = re.sub(r"\s+", " ", safe).strip()
    return safe or "Untitled"


def slugify(value: str) -> str:
    return re.sub(r"\s+", "_", sanitize_file_name(value))


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def yaml_string(value: str) -> str:
    escaped = str(value or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()
    return f'"{escaped}"'


def strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def ensure_directories(paths: dict[str, Path]) -> None:
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)


def processed_pdf_dir(pdf_dir: Path) -> Path:
    return pdf_dir / "Processed"


def failed_pdf_dir(pdf_dir: Path) -> Path:
    return pdf_dir / "Failed"


def ensure_resource_subdirectories(pdf_dir: Path) -> None:
    processed_pdf_dir(pdf_dir).mkdir(parents=True, exist_ok=True)
    failed_pdf_dir(pdf_dir).mkdir(parents=True, exist_ok=True)


def unique_destination_path(directory: Path, file_name: str) -> Path:
    directory = Path(directory)
    base_name = Path(file_name).name
    candidate = directory / base_name
    if not candidate.exists():
        return candidate
    stem = Path(base_name).stem
    suffix = Path(base_name).suffix
    n = 1
    while True:
        candidate = directory / f"{stem} ({n}){suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def move_pdf_to_bucket(source: Path, destination_dir: Path) -> Path:
    source = Path(source)
    destination_dir = Path(destination_dir)
    if not source.is_file():
        raise ValueError(f"Source PDF does not exist or is not a file: {source}")
    if source.suffix.lower() != ".pdf":
        raise ValueError(f"Source must be a PDF file: {source}")
    destination_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_destination_path(destination_dir, source.name)
    shutil.move(str(source), str(dest))
    return dest


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


def vault_relative_path(absolute_path: Path, vault_root: Path) -> str:
    return str(Path(absolute_path).resolve().relative_to(Path(vault_root).resolve())).replace("\\", "/")


def rekey_resource_index_files(index_dir: Path, old_pdf_path: Path, new_pdf_path: Path) -> None:
    index_dir = Path(index_dir)
    old_key = pdf_index_key(Path(old_pdf_path))
    new_key = pdf_index_key(Path(new_pdf_path))
    if old_key == new_key:
        return
    for src_name in (f"{old_key}.json", f"{old_key}.embeddings.json"):
        src = index_dir / src_name
        if not src.is_file():
            continue
        dest_name = src_name.replace(old_key, new_key, 1)
        dest = index_dir / dest_name
        if dest.is_file():
            dest.unlink()
        src.rename(dest)


def _restore_processing_after_ingest(
    index_path: Path,
    *,
    processing_started_at: str,
    original_pdf_rel_path: str,
    current_pdf_rel_path: str,
    summary_path: str,
) -> None:
    data = read_json(index_path, {})
    data["status"] = "processing"
    data["processing_started_at"] = processing_started_at
    data["original_pdf_rel_path"] = original_pdf_rel_path
    data["current_pdf_rel_path"] = current_pdf_rel_path
    data["summary_path"] = summary_path
    data["error_message"] = ""
    write_json(index_path, data)


def resolve_resource_paths(vault_root: Path, settings: dict[str, object]) -> dict[str, Path]:
    folders = settings.get("folders", {})
    return {
        "pdfs": vault_root / str(folders.get("resources apt fim pdfs", DEFAULT_RESOURCE_FOLDERS["pdfs"])),
        "summaries": vault_root / str(folders.get("resources apt fim summaries", DEFAULT_RESOURCE_FOLDERS["summaries"])),
        "topics": vault_root / str(folders.get("resources apt fim topics", DEFAULT_RESOURCE_FOLDERS["topics"])),
        "index": vault_root / str(folders.get("resources apt fim index", DEFAULT_RESOURCE_FOLDERS["index"])),
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_index_key(pdf_path: Path) -> str:
    stem = slugify(pdf_path.stem).lower()
    suffix = hashlib.sha1(str(pdf_path).encode("utf-8")).hexdigest()[:10]
    return f"{stem}-{suffix}"


def _index_status_priority_for_scan_resolution(status: str | None) -> int:
    """Higher is preferred when multiple index JSON files match the same PDF content hash."""
    if status is None:
        return 0
    s = str(status).strip().lower()
    if s == "failed":
        return 3
    if s == "processing":
        return 2
    if s == "done":
        return 1
    return 0


def _resolve_index_paths_for_scan(
    pdf_path: Path,
    index_dir: Path,
) -> tuple[Path, Path, dict[str, Any]]:
    """Resolve index and embeddings paths, and loaded index payload.

    The path-based key can change when a PDF is moved (e.g. Failed → intake retry).
    If the direct key file is missing, fall back to an index JSON in the same stem
    family whose stored content hash matches the file on disk.
    """
    pdf_path = Path(pdf_path)
    index_dir = Path(index_dir)
    direct_key = pdf_index_key(pdf_path)
    direct_index = index_dir / f"{direct_key}.json"
    if direct_index.is_file():
        cached = read_json(direct_index, {})
        emb = index_dir / f"{direct_key}.embeddings.json"
        return direct_index, emb, cached

    stem_slug = slugify(pdf_path.stem).lower()
    try:
        content_hash = file_sha256(pdf_path)
    except OSError:
        content_hash = ""

    best_path: Path | None = None
    best_cached: dict[str, Any] = {}
    best_pri = -1
    best_mtime = 0.0

    for candidate in sorted(index_dir.glob(f"{stem_slug}-*.json")):
        name = candidate.name
        if name.endswith(".embeddings.json"):
            continue
        cached = read_json(candidate, {})
        if not content_hash or cached.get("hash") != content_hash:
            continue
        pri = _index_status_priority_for_scan_resolution(cached.get("status"))
        mtime = candidate.stat().st_mtime
        if pri > best_pri or (pri == best_pri and mtime >= best_mtime):
            best_pri = pri
            best_mtime = mtime
            best_path = candidate
            best_cached = cached

    if best_path is not None:
        key = Path(best_path.name).stem
        return best_path, index_dir / f"{key}.embeddings.json", best_cached

    return direct_index, index_dir / f"{direct_key}.embeddings.json", {}


def summary_note_name(pdf_path: Path) -> str:
    return f"{sanitize_file_name(pdf_path.stem)}.md"


def topic_note_name(topic_title: str) -> str:
    return f"{sanitize_file_name(topic_title)}.md"


def build_provider_presets() -> list[dict[str, str]]:
    return [dict(preset) for preset in PROVIDER_PRESETS]


def unsummarized_pdf_rel_paths(files: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("pdf_rel_path", "")).strip() for item in files if item.get("pdf_rel_path") and not item.get("has_summary")]


def is_processing_complete(item: dict[str, Any], require_embeddings: bool) -> bool:
    if not item.get("has_summary"):
        return False
    if not require_embeddings:
        return True
    return bool(item.get("has_embeddings"))


def should_skip_intake_scan_item(item: dict[str, Any], require_embeddings: bool) -> bool:
    """Skip intake processing only when durable index status is done; otherwise fall back to on-disk summary/embeddings."""
    raw_status = item.get("index_status")
    if raw_status is not None:
        return str(raw_status).strip().lower() == "done"
    return is_processing_complete(item, require_embeddings)


def _scan_pdf_paths(
    pdf_paths: list[Path],
    pdf_dir: Path,
    summary_dir: Path,
    index_dir: Path | None = None,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for pdf_path in pdf_paths:
        summary_name = summary_note_name(pdf_path)
        summary_path = summary_dir / summary_name
        index_path = None
        embeddings_path = None
        has_index = False
        has_embeddings = False
        chunk_count = 0
        index_status: str | None = None
        if index_dir is not None:
            index_path, embeddings_path, cached = _resolve_index_paths_for_scan(pdf_path, index_dir)
            has_index = index_path.is_file()
            has_embeddings = embeddings_path.is_file()
            if has_index:
                chunk_count = len(cached.get("chunks", []))
                if "status" in cached:
                    index_status = str(cached.get("status", "")).strip() or None

        items.append(
            {
                "pdf_name": pdf_path.name,
                "pdf_path": str(pdf_path),
                "pdf_rel_path": pdf_path.name if pdf_path.parent == pdf_dir else str(pdf_path.relative_to(pdf_dir)).replace("\\", "/"),
                "summary_name": summary_name,
                "summary_path": str(summary_path),
                "has_summary": summary_path.exists(),
                "has_index": has_index,
                "has_embeddings": has_embeddings,
                "chunk_count": chunk_count,
                "index_status": index_status,
                "modified_at": datetime.fromtimestamp(pdf_path.stat().st_mtime).isoformat(timespec="seconds"),
                "size_bytes": pdf_path.stat().st_size,
            }
        )

    return items


def scan_pdf_library(pdf_dir: Path, summary_dir: Path, index_dir: Path | None = None) -> list[dict[str, Any]]:
    if not pdf_dir.exists():
        return []
    return _scan_pdf_paths(sorted(pdf_dir.rglob("*.pdf")), pdf_dir, summary_dir, index_dir)


def scan_intake_pdf_library(pdf_dir: Path, summary_dir: Path, index_dir: Path | None = None) -> list[dict[str, Any]]:
    if not pdf_dir.exists():
        return []
    return _scan_pdf_paths(sorted(pdf_dir.glob("*.pdf")), pdf_dir, summary_dir, index_dir)


def extract_pdf_pages(pdf_path: Path) -> list[dict[str, Any]]:
    if PdfReader is None:
        raise RuntimeError("PDF extraction requires the `pypdf` package. Install it with `python -m pip install pypdf`.")

    reader = PdfReader(str(pdf_path))
    pages: list[dict[str, Any]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        pages.append({"page": index, "text": text})
    return pages


def chunk_pages(pages: list[dict[str, Any]], chunk_size: int = 2200, overlap: int = 250) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    current_parts: list[str] = []
    current_length = 0
    page_start = None
    last_page = None

    def flush() -> None:
        nonlocal current_parts, current_length, page_start, last_page
        text = "\n\n".join(part for part in current_parts if part.strip()).strip()
        if not text:
            current_parts = []
            current_length = 0
            page_start = None
            last_page = None
            return

        chunks.append(
            {
                "chunk_id": len(chunks) + 1,
                "page_start": page_start,
                "page_end": last_page,
                "text": text,
                "char_count": len(text),
            }
        )

        if overlap > 0 and text:
            overlap_text = text[-overlap:]
            current_parts = [overlap_text]
            current_length = len(overlap_text)
            page_start = last_page
        else:
            current_parts = []
            current_length = 0
            page_start = None
        last_page = None

    for page in pages:
        page_text = str(page.get("text", "")).strip()
        if not page_text:
            continue

        annotated = f"[Page {page['page']}]\n{page_text}"
        if page_start is None:
            page_start = page["page"]
        last_page = page["page"]

        if current_length and current_length + len(annotated) + 2 > chunk_size:
            flush()
            if page_start is None:
                page_start = page["page"]

        current_parts.append(annotated)
        current_length += len(annotated) + 2
        last_page = page["page"]

    flush()
    return chunks


def build_resource_index(pdf_path: Path, pages: list[dict[str, Any]], chunks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "pdf_name": pdf_path.name,
        "pdf_stem": pdf_path.stem,
        "hash": file_sha256(pdf_path),
        "indexed_at": current_timestamp(),
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "pages": pages,
        "chunks": chunks,
    }


def prepare_provider_config(payload: dict[str, Any]) -> dict[str, str]:
    provider = str(payload.get("provider", "ollama")).strip().lower()
    config = {
        "provider": provider,
        "base_url": str(payload.get("baseUrl", "")).strip(),
        "api_key": str(payload.get("apiKey", "")).strip(),
        "model": str(payload.get("model", "")).strip(),
        "embedding_model": str(payload.get("embeddingModel", "")).strip(),
    }
    if provider == "ollama":
        config["base_url"] = config["base_url"] or "http://127.0.0.1:11434"
    elif provider == "lmstudio":
        config["base_url"] = config["base_url"] or "http://127.0.0.1:1234/v1"
    elif provider == "openai":
        config["base_url"] = config["base_url"] or "https://api.openai.com/v1"
    elif provider == "anthropic":
        config["base_url"] = config["base_url"] or "https://api.anthropic.com/v1"
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return config


def validate_provider_config_for_intake(config: dict[str, str], *, generate_embeddings: bool) -> None:
    """Raise ValueError if config cannot satisfy intake processing (summarize + optional embeddings).

    Call before any per-PDF intake work so batch-level misconfiguration does not move PDFs to Failed.
    """
    if not (config.get("model") or "").strip():
        raise ValueError("A text model is required.")

    provider = (config.get("provider") or "").strip().lower()
    if provider == "openai" and not (config.get("api_key") or "").strip():
        raise ValueError("An OpenAI API key is required.")
    if provider == "anthropic" and not (config.get("api_key") or "").strip():
        raise ValueError("An Anthropic API key is required.")

    if generate_embeddings:
        if not (config.get("embedding_model") or "").strip():
            raise ValueError("An embedding model is required when embeddings are enabled.")
        if provider == "anthropic":
            raise ValueError("Embeddings are not supported for provider: anthropic")


def provider_label(config: dict[str, str]) -> str:
    if config["provider"] == "lmstudio":
        return "lmstudio"
    return config["provider"]


def call_text_model(config: dict[str, str], system_prompt: str, user_prompt: str) -> str:
    provider = config["provider"]
    timeout = 120

    if not config.get("model"):
        raise ValueError("A text model is required.")

    if provider == "ollama":
        response = requests.post(
            f"{config['base_url'].rstrip('/')}/api/chat",
            json={
                "model": config["model"],
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    if provider in {"lmstudio", "openai"}:
        headers = {"Content-Type": "application/json"}
        if provider == "openai":
            if not config.get("api_key"):
                raise ValueError("An OpenAI API key is required.")
            headers["Authorization"] = f"Bearer {config['api_key']}"
        response = requests.post(
            f"{config['base_url'].rstrip('/')}/chat/completions",
            headers=headers,
            json={
                "model": config["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.2,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    if provider == "anthropic":
        if not config.get("api_key"):
            raise ValueError("An Anthropic API key is required.")
        response = requests.post(
            f"{config['base_url'].rstrip('/')}/messages",
            headers={
                "x-api-key": config["api_key"],
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": config["model"],
                "max_tokens": 1400,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
            },
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        text_parts = [part.get("text", "") for part in data.get("content", []) if part.get("type") == "text"]
        return "\n".join(text_parts).strip()

    raise ValueError(f"Unsupported provider: {provider}")


def call_embedding_model(config: dict[str, str], texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    provider = config["provider"]
    model_name = config.get("embedding_model")
    if not model_name:
        raise ValueError("An embedding model is required when embeddings are enabled.")

    if provider == "ollama":
        response = requests.post(
            f"{config['base_url'].rstrip('/')}/api/embed",
            json={"model": model_name, "input": texts},
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("embeddings", [])

    if provider in {"lmstudio", "openai"}:
        headers = {"Content-Type": "application/json"}
        if provider == "openai":
            if not config.get("api_key"):
                raise ValueError("An OpenAI API key is required.")
            headers["Authorization"] = f"Bearer {config['api_key']}"
        response = requests.post(
            f"{config['base_url'].rstrip('/')}/embeddings",
            headers=headers,
            json={"model": model_name, "input": texts},
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        return [item["embedding"] for item in payload.get("data", [])]

    raise ValueError(f"Embeddings are not supported for provider: {provider}")


def summarize_pdf_chunks(pdf_title: str, chunks: list[dict[str, Any]], config: dict[str, str]) -> dict[str, Any]:
    system_prompt = (
        "You summarize atom probe tomography and field ion microscopy literature for a lab notebook. "
        "Be accurate, concise, and preserve important experimental context."
    )

    chunk_summaries: list[dict[str, Any]] = []
    for chunk in chunks:
        pages_label = (
            f"pages {chunk['page_start']}-{chunk['page_end']}"
            if chunk["page_start"] != chunk["page_end"]
            else f"page {chunk['page_start']}"
        )
        user_prompt = (
            f"Summarize the following excerpt from '{pdf_title}' in 3-5 bullet points. "
            f"Focus on APT/FIM relevance, methods, instrumentation details, and important caveats.\n\n"
            f"Excerpt location: {pages_label}\n\n"
            f"{chunk['text']}"
        )
        chunk_summary = strip_code_fences(call_text_model(config, system_prompt, user_prompt))
        chunk_summaries.append(
            {
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "summary": chunk_summary,
            }
        )

    combined = "\n\n".join(
        (
            f"Source pages {entry['page_start']}-{entry['page_end'] if entry['page_end'] != entry['page_start'] else entry['page_start']}:\n"
            f"{entry['summary']}"
        )
        for entry in chunk_summaries
    )
    final_prompt = (
        f"Using the chunk summaries for '{pdf_title}', write a concise markdown summary with these sections:\n"
        f"## Overview\n## Key Findings\n## Methods And Instrumentation Notes\n## Relevance To APT/FIM\n## Open Questions\n\n"
        f"Do not invent facts. Only use the supplied summaries.\n\n{combined}"
    )
    final_summary = strip_code_fences(call_text_model(config, system_prompt, final_prompt))
    return {"summary_text": final_summary, "citations": chunk_summaries}


def synthesize_topic_summary(topic_title: str, source_payloads: list[dict[str, Any]], config: dict[str, str]) -> str:
    system_prompt = (
        "You synthesize literature notes for an atom probe tomography and field ion microscopy notebook. "
        "Compare sources carefully and call out disagreements or uncertainty."
    )
    combined_sources = "\n\n".join(
        f"Source: {item['title']}\nSummary:\n{item['summary']}" for item in source_payloads
    )
    user_prompt = (
        f"Create a markdown topic synthesis titled '{topic_title}' with these sections:\n"
        f"## Topic Overview\n## Consensus Findings\n## Differences Between Sources\n## Key Papers\n## Practical Relevance To GEMT Work\n\n"
        f"Use only the source summaries below.\n\n{combined_sources}"
    )
    return strip_code_fences(call_text_model(config, system_prompt, user_prompt))


def render_pdf_summary_note(
    pdf_title: str,
    pdf_rel_path: str,
    provider_label: str,
    model_name: str,
    summary_text: str,
    citations: list[dict[str, Any]],
) -> str:
    citation_lines = []
    for citation in citations:
        page_label = (
            f"pages {citation['page_start']}-{citation['page_end']}"
            if citation["page_start"] != citation["page_end"]
            else f"page {citation['page_start']}"
        )
        summary_excerpt = citation.get("quote") or citation.get("summary", "")
        citation_lines.append(f"- {page_label}: {summary_excerpt.strip()}")

    citations_block = "\n".join(citation_lines) if citation_lines else "- No citation summaries recorded."
    source_link = f"[[{pdf_rel_path.replace('\\', '/')}]]"
    return (
        "---\n"
        f"date created: {current_date()}\n"
        f"author: {yaml_string('StarDustX')}\n"
        'note type: pdf-summary\n'
        'resource type: apt-fim-literature\n'
        f"source pdf: {yaml_string(source_link)}\n"
        f"provider: {yaml_string(provider_label)}\n"
        f"model: {yaml_string(model_name)}\n"
        "tags:\n"
        '  - "#resource/pdf-summary"\n'
        '  - "#apt"\n'
        '  - "#fim"\n'
        "---\n\n"
        f"# {pdf_title}\n\n"
        f"## Source PDF\n\n{source_link}\n\n"
        f"{summary_text.strip()}\n\n"
        "## Citation Trail\n\n"
        f"{citations_block}\n"
    )


def render_topic_summary_note(topic_title: str, topic_summary: str, sources: list[dict[str, str]], provider_name: str, model_name: str) -> str:
    source_lines = "\n".join(
        f"- [[{item['summary_rel_path'].replace('\\', '/')}|{item['title']}]]" for item in sources
    )
    return (
        "---\n"
        f"date created: {current_date()}\n"
        f"author: {yaml_string('StarDustX')}\n"
        'note type: topic-summary\n'
        'resource type: apt-fim-literature-topic\n'
        f"provider: {yaml_string(provider_name)}\n"
        f"model: {yaml_string(model_name)}\n"
        "tags:\n"
        '  - "#resource/topic-summary"\n'
        '  - "#apt"\n'
        '  - "#fim"\n'
        "---\n\n"
        f"# {topic_title}\n\n"
        f"{topic_summary.strip()}\n\n"
        "## Source Summary Notes\n\n"
        f"{source_lines or '- No source summaries selected.'}\n"
    )


def ingest_pdf(
    pdf_path: Path,
    index_dir: Path,
    generate_embeddings: bool,
    config: dict[str, str] | None = None,
) -> dict[str, Any]:
    pages = extract_pdf_pages(pdf_path)
    chunks = chunk_pages(pages)
    payload = build_resource_index(pdf_path, pages, chunks)

    key = pdf_index_key(pdf_path)
    index_path = index_dir / f"{key}.json"
    write_json(index_path, payload)

    embeddings_path = index_dir / f"{key}.embeddings.json"
    if generate_embeddings:
        if config is None:
            raise ValueError("Provider configuration is required to generate embeddings.")
        vectors = call_embedding_model(config, [chunk["text"] for chunk in chunks])
        write_json(
            embeddings_path,
            {
                "pdf_name": pdf_path.name,
                "model": config.get("embedding_model", ""),
                "generated_at": current_timestamp(),
                "embeddings": [
                    {
                        "chunk_id": chunk["chunk_id"],
                        "page_start": chunk["page_start"],
                        "page_end": chunk["page_end"],
                        "vector": vector,
                    }
                    for chunk, vector in zip(chunks, vectors)
                ],
            },
        )
    elif embeddings_path.exists():
        embeddings_path.unlink()

    return payload


def process_intake_pdf(
    vault_root: Path,
    pdf_path: Path,
    *,
    pdf_dir: Path,
    summary_dir: Path,
    index_dir: Path,
    config: dict[str, str],
    generate_embeddings: bool = False,
) -> dict[str, Any]:
    vault_root = Path(vault_root).resolve()
    source_pdf = Path(pdf_path).resolve()
    pdf_dir = Path(pdf_dir).resolve()
    summary_dir = Path(summary_dir).resolve()
    index_dir = Path(index_dir).resolve()

    if source_pdf.parent.resolve() != pdf_dir.resolve():
        raise ValueError("Intake processing only supports PDFs in the top-level intake folder.")

    validate_provider_config_for_intake(config, generate_embeddings=generate_embeddings)

    ensure_resource_subdirectories(pdf_dir)
    index_path_intake = index_dir / f"{pdf_index_key(source_pdf)}.json"
    current_path = source_pdf
    orig_rel = vault_relative_path(source_pdf, vault_root)
    planned_summary = summary_dir / summary_note_name(source_pdf)

    try:
        started = update_processing_state(
            index_path_intake,
            status="processing",
            original_pdf_rel_path=orig_rel,
            current_pdf_rel_path=orig_rel,
            summary_path=str(planned_summary),
        )
        started_at = started["processing_started_at"]

        ingest_pdf(source_pdf, index_dir, generate_embeddings, config if generate_embeddings else None)
        _restore_processing_after_ingest(
            index_path_intake,
            processing_started_at=started_at,
            original_pdf_rel_path=orig_rel,
            current_pdf_rel_path=orig_rel,
            summary_path=str(planned_summary),
        )

        payload = read_json(index_path_intake, {})
        chunks = payload.get("chunks") or []
        summary_result = summarize_pdf_chunks(source_pdf.name, chunks, config)

        current_path = move_pdf_to_bucket(current_path, processed_pdf_dir(pdf_dir))
        rekey_resource_index_files(index_dir, source_pdf, current_path)

        final_path = current_path
        final_rel = vault_relative_path(final_path, vault_root)
        summary_file = summary_dir / summary_note_name(final_path)
        note_body = render_pdf_summary_note(
            pdf_title=sanitize_file_name(final_path.stem),
            pdf_rel_path=final_rel,
            provider_label=provider_label(config),
            model_name=config["model"],
            summary_text=summary_result["summary_text"],
            citations=summary_result["citations"],
        )
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(note_body, encoding="utf-8")

        new_index = index_dir / f"{pdf_index_key(final_path)}.json"
        embeddings_ok = not generate_embeddings or (index_dir / f"{pdf_index_key(final_path)}.embeddings.json").is_file()
        completion_item = {
            "has_summary": summary_file.is_file(),
            "has_embeddings": embeddings_ok if generate_embeddings else False,
        }
        if not is_processing_complete(completion_item, generate_embeddings):
            raise RuntimeError("Processing finished but completion criteria were not met.")

        update_processing_state(
            new_index,
            status="done",
            current_pdf_rel_path=final_rel,
            summary_path=str(summary_file),
            embeddings_generated=bool(generate_embeddings),
        )

        return {"success": True, "pdf_path": str(final_path), "error": ""}

    except Exception as exc:
        err = str(exc)
        failed_bucket = failed_pdf_dir(pdf_dir)
        report_path = current_path
        try:
            if current_path.exists() and current_path.parent.resolve() != failed_bucket.resolve():
                pre_move = current_path
                failed_dest = move_pdf_to_bucket(current_path, failed_bucket)
                report_path = failed_dest
                rekey_resource_index_files(index_dir, pre_move, failed_dest)
                update_processing_state(
                    index_dir / f"{pdf_index_key(failed_dest)}.json",
                    status="failed",
                    error_message=err,
                    current_pdf_rel_path=vault_relative_path(failed_dest, vault_root),
                )
            elif index_path_intake.exists():
                update_processing_state(
                    index_path_intake,
                    status="failed",
                    error_message=err,
                    current_pdf_rel_path=vault_relative_path(current_path, vault_root)
                    if current_path.exists()
                    else vault_relative_path(source_pdf, vault_root),
                )
        except Exception as cleanup_exc:
            if index_path_intake.exists():
                update_processing_state(
                    index_path_intake,
                    status="failed",
                    error_message=f"{err}; cleanup error: {cleanup_exc}",
                    current_pdf_rel_path=vault_relative_path(source_pdf, vault_root),
                )
        return {
            "success": False,
            "status": "failed",
            "pdf_path": str(report_path.resolve()),
            "error": err,
        }


def process_intake_library(
    vault_root: Path,
    *,
    pdf_dir: Path,
    summary_dir: Path,
    index_dir: Path,
    config: dict[str, str],
    generate_embeddings: bool = False,
) -> dict[str, Any]:
    validate_provider_config_for_intake(config, generate_embeddings=generate_embeddings)
    ensure_resource_subdirectories(Path(pdf_dir))
    items = scan_intake_pdf_library(Path(pdf_dir), Path(summary_dir), Path(index_dir))
    results: list[dict[str, Any]] = []
    for item in items:
        if should_skip_intake_scan_item(item, generate_embeddings):
            continue
        results.append(
            process_intake_pdf(
                vault_root,
                Path(item["pdf_path"]),
                pdf_dir=Path(pdf_dir),
                summary_dir=Path(summary_dir),
                index_dir=Path(index_dir),
                config=config,
                generate_embeddings=generate_embeddings,
            )
        )
    succeeded = sum(1 for entry in results if entry.get("success"))
    return {
        "processed": len(results),
        "succeeded": succeeded,
        "failed": len(results) - succeeded,
        "results": results,
    }
