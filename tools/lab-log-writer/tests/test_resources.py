import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "resources.py"


def load_resources_module():
    spec = importlib.util.spec_from_file_location("lab_log_writer_resources", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResourcesTests(unittest.TestCase):
    def test_chunk_text_preserves_page_ranges(self):
        resources = load_resources_module()
        pages = [
            {"page": 1, "text": "A" * 1400},
            {"page": 2, "text": "B" * 1400},
            {"page": 3, "text": "C" * 600},
        ]

        chunks = resources.chunk_pages(pages, chunk_size=1800, overlap=200)

        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["page_start"], 1)
        self.assertEqual(chunks[0]["page_end"], 2)
        self.assertEqual(chunks[-1]["page_end"], 3)
        self.assertTrue(all(chunk["text"].strip() for chunk in chunks))

    def test_scan_pdf_library_marks_summary_status(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            summary_dir = root / "Summaries"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)

            (pdf_dir / "Field Ion Microscopy Primer.pdf").write_bytes(b"%PDF-1.4\n")
            (summary_dir / "Field Ion Microscopy Primer.md").write_text("# summary\n", encoding="utf-8")

            scanned = resources.scan_pdf_library(pdf_dir, summary_dir)

            self.assertEqual(len(scanned), 1)
            self.assertEqual(scanned[0]["pdf_name"], "Field Ion Microscopy Primer.pdf")
            self.assertEqual(scanned[0]["summary_name"], "Field Ion Microscopy Primer.md")
            self.assertTrue(scanned[0]["has_summary"])

    def test_render_summary_note_links_back_to_pdf(self):
        resources = load_resources_module()
        note = resources.render_pdf_summary_note(
            pdf_title="APT Imaging Review",
            pdf_rel_path="Resources/APT-FIM/PDFs/APT Imaging Review.pdf",
            provider_label="ollama",
            model_name="llama3.1",
            summary_text="A concise summary.",
            citations=[
                {"page_start": 3, "page_end": 4, "quote": "Field evaporation is central."},
                {"page_start": 7, "page_end": 7, "quote": "Detector efficiency shapes results."},
            ],
        )

        self.assertIn("note type: pdf-summary", note)
        self.assertIn("[[Resources/APT-FIM/PDFs/APT Imaging Review.pdf]]", note)
        self.assertIn("pages 3-4", note)
        self.assertIn("A concise summary.", note)

    def test_filter_unsummarized_pdfs(self):
        resources = load_resources_module()
        files = [
            {"pdf_rel_path": "one.pdf", "has_summary": False},
            {"pdf_rel_path": "two.pdf", "has_summary": True},
            {"pdf_rel_path": "three.pdf", "has_summary": False},
        ]

        selected = resources.unsummarized_pdf_rel_paths(files)

        self.assertEqual(selected, ["one.pdf", "three.pdf"])

    def test_provider_presets_include_expected_defaults(self):
        resources = load_resources_module()

        presets = resources.build_provider_presets()
        preset_ids = [preset["id"] for preset in presets]

        self.assertIn("ollama-local", preset_ids)
        self.assertIn("lmstudio-local", preset_ids)
        self.assertIn("openai-default", preset_ids)
        self.assertIn("anthropic-default", preset_ids)
        ollama = next(preset for preset in presets if preset["id"] == "ollama-local")
        self.assertEqual(ollama["provider"], "ollama")
        self.assertEqual(ollama["baseUrl"], "http://localhost:11434")
        lmstudio = next(preset for preset in presets if preset["id"] == "lmstudio-local")
        self.assertEqual(lmstudio["baseUrl"], "http://127.0.0.1:1234/v1")

    def test_read_resource_settings_returns_normalized_defaults(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = resources.read_resource_settings(Path(temp_dir) / "resource-settings.json")

        self.assertEqual(settings["defaultProvider"], "ollama")
        self.assertIn("ollama", settings["providers"])
        self.assertEqual(settings["providers"]["ollama"]["baseUrls"], [])
        self.assertEqual(settings["providers"]["ollama"]["models"], [])

    def test_write_resource_settings_round_trips_and_deduplicates(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = Path(temp_dir) / "resource-settings.json"
            saved = resources.write_resource_settings(
                {
                    "defaultProvider": "lmstudio",
                    "providers": {
                        "lmstudio": {
                            "defaultBaseUrl": "http://127.0.0.1:1234/v1",
                            "baseUrls": ["http://127.0.0.1:1234/v1", "http://127.0.0.1:1234/v1", ""],
                            "defaultModel": "gemma",
                            "models": ["gemma", "gemma", "llama"],
                            "defaultEmbeddingModel": "embedder",
                            "embeddingModels": ["embedder", "embedder"],
                        }
                    },
                },
                settings_path,
            )

            reloaded = resources.read_resource_settings(settings_path)

        self.assertEqual(saved["defaultProvider"], "lmstudio")
        self.assertEqual(reloaded["defaultProvider"], "lmstudio")
        self.assertEqual(reloaded["providers"]["lmstudio"]["baseUrls"], ["http://127.0.0.1:1234/v1"])
        self.assertEqual(reloaded["providers"]["lmstudio"]["models"], ["gemma", "llama"])
        self.assertEqual(reloaded["providers"]["lmstudio"]["embeddingModels"], ["embedder"])

    def test_scan_intake_pdf_library_ignores_processed_and_failed_subfolders(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            summary_dir = root / "Summaries"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            (pdf_dir / "Processed").mkdir()
            (pdf_dir / "Failed").mkdir()

            (pdf_dir / "intake.pdf").write_bytes(b"%PDF-1.4\n")
            (pdf_dir / "Processed" / "done.pdf").write_bytes(b"%PDF-1.4\n")
            (pdf_dir / "Failed" / "bad.pdf").write_bytes(b"%PDF-1.4\n")

            scanned = resources.scan_intake_pdf_library(pdf_dir, summary_dir)

            self.assertEqual(len(scanned), 1)
            self.assertEqual(scanned[0]["pdf_name"], "intake.pdf")

    def test_is_processing_complete_true_when_summary_and_embeddings_not_required(self):
        resources = load_resources_module()
        item = {"has_summary": True, "has_embeddings": False}
        self.assertTrue(resources.is_processing_complete(item, require_embeddings=False))

    def test_is_processing_complete_false_when_embeddings_required_but_missing(self):
        resources = load_resources_module()
        item = {"has_summary": True, "has_embeddings": False}
        self.assertFalse(resources.is_processing_complete(item, require_embeddings=True))

    def test_is_processing_complete_true_when_embeddings_required_and_present(self):
        resources = load_resources_module()
        item = {"has_summary": True, "has_embeddings": True}
        self.assertTrue(resources.is_processing_complete(item, require_embeddings=True))

    def test_should_skip_intake_scan_item_uses_durable_status_when_present(self):
        resources = load_resources_module()
        stale_summary = {"has_summary": True, "has_embeddings": True, "index_status": "failed"}
        self.assertFalse(resources.should_skip_intake_scan_item(stale_summary, require_embeddings=False))
        self.assertFalse(resources.should_skip_intake_scan_item(stale_summary, require_embeddings=True))

        processing = {"has_summary": True, "has_embeddings": False, "index_status": "processing"}
        self.assertFalse(resources.should_skip_intake_scan_item(processing, require_embeddings=True))

        done = {"has_summary": False, "has_embeddings": False, "index_status": "done"}
        self.assertTrue(resources.should_skip_intake_scan_item(done, require_embeddings=False))
        self.assertTrue(resources.should_skip_intake_scan_item(done, require_embeddings=True))

        no_status = {"has_summary": True, "has_embeddings": False, "index_status": None}
        self.assertTrue(resources.should_skip_intake_scan_item(no_status, require_embeddings=False))
        self.assertFalse(resources.should_skip_intake_scan_item(no_status, require_embeddings=True))

    def test_update_processing_state_persists_status_fields(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            index_path = base / "sample.json"
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
            started_at = payload["processing_started_at"]

            resources.update_processing_state(
                index_path,
                status="done",
                current_pdf_rel_path="Resources/APT-FIM/PDFs/Processed/sample.pdf",
            )
            payload = resources.read_json(index_path, {})
            self.assertEqual(payload["status"], "done")
            self.assertEqual(payload["processing_started_at"], started_at)
            self.assertIn("processing_finished_at", payload)
            self.assertEqual(payload["current_pdf_rel_path"], "Resources/APT-FIM/PDFs/Processed/sample.pdf")

            failed_index = base / "bad.json"
            resources.write_json(failed_index, {"pdf_name": "bad.pdf"})
            resources.update_processing_state(
                failed_index,
                status="processing",
                original_pdf_rel_path="Resources/APT-FIM/PDFs/bad.pdf",
                current_pdf_rel_path="Resources/APT-FIM/PDFs/bad.pdf",
            )
            resources.update_processing_state(
                failed_index,
                status="failed",
                error_message="extraction failed",
                current_pdf_rel_path="Resources/APT-FIM/PDFs/Failed/bad.pdf",
            )
            failed_payload = resources.read_json(failed_index, {})
            self.assertEqual(failed_payload["status"], "failed")
            self.assertIn("processing_finished_at", failed_payload)
            self.assertEqual(failed_payload["error_message"], "extraction failed")
            self.assertEqual(failed_payload["current_pdf_rel_path"], "Resources/APT-FIM/PDFs/Failed/bad.pdf")

    def test_processed_failed_dir_helpers_and_ensure_subdirectories(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_dir = Path(temp_dir) / "PDFs"
            pdf_dir.mkdir(parents=True)
            self.assertEqual(resources.processed_pdf_dir(pdf_dir), pdf_dir / "Processed")
            self.assertEqual(resources.failed_pdf_dir(pdf_dir), pdf_dir / "Failed")
            resources.ensure_resource_subdirectories(pdf_dir)
            self.assertTrue((pdf_dir / "Processed").is_dir())
            self.assertTrue((pdf_dir / "Failed").is_dir())

    def test_move_pdf_to_processed_avoids_duplicate_names(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_dir = Path(temp_dir) / "PDFs"
            pdf_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            processed = resources.processed_pdf_dir(pdf_dir)
            intake_pdf = pdf_dir / "paper.pdf"
            intake_pdf.write_bytes(b"%PDF-1.4\n")
            (processed / "paper.pdf").write_bytes(b"%PDF-1.4\nolder\n")

            moved = resources.move_pdf_to_bucket(intake_pdf, processed)

            self.assertEqual(moved, processed / "paper (1).pdf")
            self.assertTrue(moved.is_file())
            self.assertFalse(intake_pdf.exists())
            self.assertTrue((processed / "paper.pdf").is_file())

    def test_move_pdf_to_failed_removes_source(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_dir = Path(temp_dir) / "PDFs"
            pdf_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            failed = resources.failed_pdf_dir(pdf_dir)
            intake_pdf = pdf_dir / "broken.pdf"
            intake_pdf.write_bytes(b"%PDF-1.4\n")

            moved = resources.move_pdf_to_bucket(intake_pdf, failed)

            self.assertEqual(moved, failed / "broken.pdf")
            self.assertTrue(moved.is_file())
            self.assertFalse(intake_pdf.exists())

    def test_process_intake_pdf_success_end_to_end(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "BatchIntake.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )
            fake_pages = [{"page": 1, "text": "APT sample paragraph for testing."}]

            with patch.object(resources, "extract_pdf_pages", return_value=fake_pages), patch.object(
                resources,
                "summarize_pdf_chunks",
                return_value={"summary_text": "## Overview\nBatch OK.", "citations": []},
            ):
                result = resources.process_intake_pdf(
                    vault,
                    intake,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertTrue(result.get("success"), msg=str(result))
            processed_pdf = pdf_dir / "Processed" / "BatchIntake.pdf"
            self.assertTrue(processed_pdf.is_file())
            self.assertFalse(intake.exists())
            note_path = summary_dir / "BatchIntake.md"
            self.assertTrue(note_path.is_file())
            note_body = note_path.read_text(encoding="utf-8")
            self.assertIn("[[Resources/APT-FIM/PDFs/Processed/BatchIntake.pdf]]", note_body)
            idx_path = index_dir / f"{resources.pdf_index_key(processed_pdf)}.json"
            idx = resources.read_json(idx_path, {})
            self.assertEqual(idx.get("status"), "done")
            self.assertEqual(idx.get("current_pdf_rel_path"), "Resources/APT-FIM/PDFs/Processed/BatchIntake.pdf")
            self.assertTrue(idx.get("embeddings_generated") is False)
            scanned = resources.scan_pdf_library(pdf_dir, summary_dir, index_dir)
            match = next(item for item in scanned if item["pdf_name"] == "BatchIntake.pdf")
            self.assertTrue(resources.is_processing_complete(match, require_embeddings=False))

    def test_process_intake_pdf_when_ingest_fails_moves_to_failed_and_records_index(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "IngestFail.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )

            with patch.object(resources, "ingest_pdf", side_effect=RuntimeError("simulated ingest failure")):
                result = resources.process_intake_pdf(
                    vault,
                    intake,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertFalse(result.get("success"))
            self.assertEqual(result.get("status"), "failed")
            self.assertEqual(result.get("error"), "simulated ingest failure")
            failed_pdf = pdf_dir / "Failed" / "IngestFail.pdf"
            self.assertTrue(failed_pdf.is_file(), msg=f"expected PDF under Failed, got {result!r}")
            self.assertFalse(intake.exists())
            self.assertEqual(
                result.get("pdf_path"),
                str(failed_pdf.resolve()),
            )
            idx_path = index_dir / f"{resources.pdf_index_key(failed_pdf)}.json"
            self.assertTrue(idx_path.is_file(), msg="index should exist at key for failed PDF path")
            idx = resources.read_json(idx_path, {})
            self.assertEqual(idx.get("status"), "failed")
            self.assertEqual(idx.get("error_message"), "simulated ingest failure")
            self.assertEqual(
                idx.get("current_pdf_rel_path"),
                "Resources/APT-FIM/PDFs/Failed/IngestFail.pdf",
            )

    def test_process_intake_library_reports_failed_batch_status_when_ingest_fails(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            pending = pdf_dir / "BatchIngestFail.pdf"
            pending.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )

            with patch.object(resources, "ingest_pdf", side_effect=RuntimeError("batch ingest failure")):
                batch = resources.process_intake_library(
                    vault,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertEqual(batch["processed"], 1)
            self.assertEqual(batch["succeeded"], 0)
            self.assertEqual(batch["failed"], 1)
            self.assertEqual(len(batch["results"]), 1)
            entry = batch["results"][0]
            self.assertFalse(entry.get("success"))
            self.assertEqual(entry.get("status"), "failed")
            self.assertEqual(entry.get("error"), "batch ingest failure")

    def test_process_intake_library_processes_only_incomplete_intake_pdfs(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            done_pdf = pdf_dir / "AlreadyDone.pdf"
            pending_pdf = pdf_dir / "StillPending.pdf"
            done_pdf.write_bytes(b"%PDF-1.4\n")
            pending_pdf.write_bytes(b"%PDF-1.4\n")
            (summary_dir / "AlreadyDone.md").write_text("# ok\n", encoding="utf-8")
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )
            fake_pages = [{"page": 1, "text": "Body."}]

            with patch.object(resources, "extract_pdf_pages", return_value=fake_pages), patch.object(
                resources,
                "summarize_pdf_chunks",
                return_value={"summary_text": "## Overview\nOK", "citations": []},
            ):
                batch = resources.process_intake_library(
                    vault,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertEqual(batch["processed"], 1)
            self.assertEqual(batch["succeeded"], 1)
            self.assertEqual(batch["failed"], 0)
            self.assertTrue(done_pdf.is_file())
            self.assertTrue((pdf_dir / "Processed" / "StillPending.pdf").is_file())

    def test_process_intake_library_retries_stale_summary_when_index_status_failed(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "StaleSummary.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            (summary_dir / "StaleSummary.md").write_text("# stale\n", encoding="utf-8")
            key = resources.pdf_index_key(intake)
            resources.write_json(
                index_dir / f"{key}.json",
                {"status": "failed", "error_message": "prior run", "chunks": []},
            )
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )
            fake_pages = [{"page": 1, "text": "Retry body."}]

            with patch.object(resources, "extract_pdf_pages", return_value=fake_pages), patch.object(
                resources,
                "summarize_pdf_chunks",
                return_value={"summary_text": "## Overview\nRetried OK", "citations": []},
            ):
                batch = resources.process_intake_library(
                    vault,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertEqual(batch["processed"], 1, msg="failed durable status must not skip despite stale summary")
            self.assertEqual(batch["succeeded"], 1)
            self.assertTrue((pdf_dir / "Processed" / "StaleSummary.pdf").is_file())

    def test_scan_intake_resolves_failed_index_by_content_hash_when_path_key_differs(self):
        """After Failed→intake retry, index file name uses old path hash; scan must still see durable status."""
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pdf_dir = root / "PDFs"
            summary_dir = root / "Summaries"
            index_dir = root / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "RequeueSameName.pdf"
            intake.write_bytes(b"%PDF-1.4\nrequeue-bytes\n")
            (summary_dir / "RequeueSameName.md").write_text("# stale summary\n", encoding="utf-8")
            failed_path = pdf_dir / "Failed" / "RequeueSameName.pdf"
            failed_key = resources.pdf_index_key(failed_path)
            intake_key = resources.pdf_index_key(intake)
            self.assertNotEqual(
                failed_key,
                intake_key,
                "fixture requires distinct keys so direct path lookup misses the durable index",
            )
            resources.write_json(
                index_dir / f"{failed_key}.json",
                {
                    "status": "failed",
                    "error_message": "prior failure",
                    "hash": resources.file_sha256(intake),
                    "chunks": [],
                },
            )
            scanned = resources.scan_intake_pdf_library(pdf_dir, summary_dir, index_dir)
            self.assertEqual(len(scanned), 1)
            item = scanned[0]
            self.assertEqual(item["index_status"], "failed")
            self.assertTrue(item["has_summary"])
            self.assertFalse(
                resources.should_skip_intake_scan_item(item, require_embeddings=False),
                "stale summary must not skip when durable failed status is recovered via hash",
            )

    def test_process_intake_library_retries_requeued_pdf_when_index_key_is_failed_path_with_stale_summary(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "RequeueBatch.pdf"
            intake.write_bytes(b"%PDF-1.4\nbatch-requeue\n")
            (summary_dir / "RequeueBatch.md").write_text("# stale\n", encoding="utf-8")
            failed_path = pdf_dir / "Failed" / "RequeueBatch.pdf"
            failed_key = resources.pdf_index_key(failed_path)
            resources.write_json(
                index_dir / f"{failed_key}.json",
                {
                    "status": "failed",
                    "error_message": "moved to failed earlier",
                    "hash": resources.file_sha256(intake),
                    "chunks": [],
                },
            )
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )
            fake_pages = [{"page": 1, "text": "Requeued body."}]

            with patch.object(resources, "extract_pdf_pages", return_value=fake_pages), patch.object(
                resources,
                "summarize_pdf_chunks",
                return_value={"summary_text": "## Overview\nRequeue OK", "citations": []},
            ):
                batch = resources.process_intake_library(
                    vault,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertEqual(
                batch["processed"],
                1,
                msg="re-queued intake PDF must run despite stale summary and mismatched index filename",
            )
            self.assertEqual(batch["succeeded"], 1)
            self.assertTrue((pdf_dir / "Processed" / "RequeueBatch.pdf").is_file())

    def test_process_intake_library_retries_stale_summary_when_index_status_processing(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            resources.ensure_resource_subdirectories(pdf_dir)
            intake = pdf_dir / "OrphanProcessing.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            (summary_dir / "OrphanProcessing.md").write_text("# stale\n", encoding="utf-8")
            key = resources.pdf_index_key(intake)
            resources.write_json(
                index_dir / f"{key}.json",
                {"status": "processing", "processing_started_at": "2026-01-01 00:00", "chunks": []},
            )
            config = resources.prepare_provider_config(
                {"provider": "ollama", "baseUrl": "", "model": "llama3.1", "embeddingModel": ""}
            )
            fake_pages = [{"page": 1, "text": "Resume body."}]

            with patch.object(resources, "extract_pdf_pages", return_value=fake_pages), patch.object(
                resources,
                "summarize_pdf_chunks",
                return_value={"summary_text": "## Overview\nResumed OK", "citations": []},
            ):
                batch = resources.process_intake_library(
                    vault,
                    pdf_dir=pdf_dir,
                    summary_dir=summary_dir,
                    index_dir=index_dir,
                    config=config,
                    generate_embeddings=False,
                )

            self.assertEqual(batch["processed"], 1, msg="processing durable status must not skip despite stale summary")
            self.assertEqual(batch["succeeded"], 1)
            self.assertTrue((pdf_dir / "Processed" / "OrphanProcessing.pdf").is_file())

    def test_process_intake_library_rejects_openai_without_api_key_before_pdf_mutation(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            intake = pdf_dir / "ConfigBad.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {
                    "provider": "openai",
                    "baseUrl": "https://api.openai.com/v1",
                    "model": "gpt-4.1-mini",
                    "apiKey": "",
                    "embeddingModel": "",
                }
            )
            with patch.object(resources, "extract_pdf_pages") as mock_extract:
                with self.assertRaises(ValueError) as ctx:
                    resources.process_intake_library(
                        vault,
                        pdf_dir=pdf_dir,
                        summary_dir=summary_dir,
                        index_dir=index_dir,
                        config=config,
                        generate_embeddings=False,
                    )
                mock_extract.assert_not_called()
            self.assertIn("API key", str(ctx.exception))
            self.assertTrue(intake.is_file(), "intake PDF must not be moved when config is invalid")
            self.assertFalse((pdf_dir / "Failed" / "ConfigBad.pdf").exists())

    def test_process_intake_library_rejects_empty_text_model_before_pdf_mutation(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            intake = pdf_dir / "NoModel.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {
                    "provider": "ollama",
                    "baseUrl": "",
                    "model": "",
                    "embeddingModel": "",
                }
            )
            with patch.object(resources, "extract_pdf_pages") as mock_extract:
                with self.assertRaises(ValueError):
                    resources.process_intake_library(
                        vault,
                        pdf_dir=pdf_dir,
                        summary_dir=summary_dir,
                        index_dir=index_dir,
                        config=config,
                        generate_embeddings=False,
                    )
                mock_extract.assert_not_called()
            self.assertTrue(intake.is_file())

    def test_process_intake_library_rejects_embeddings_without_embedding_model_before_pdf_mutation(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            intake = pdf_dir / "NoEmbedModel.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {
                    "provider": "ollama",
                    "baseUrl": "",
                    "model": "llama3.1",
                    "embeddingModel": "",
                }
            )
            with patch.object(resources, "extract_pdf_pages") as mock_extract:
                with self.assertRaises(ValueError) as ctx:
                    resources.process_intake_library(
                        vault,
                        pdf_dir=pdf_dir,
                        summary_dir=summary_dir,
                        index_dir=index_dir,
                        config=config,
                        generate_embeddings=True,
                    )
                mock_extract.assert_not_called()
            self.assertIn("embedding", str(ctx.exception).lower())
            self.assertTrue(intake.is_file())

    def test_process_intake_library_rejects_anthropic_embeddings_before_pdf_mutation(self):
        resources = load_resources_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            pdf_dir = vault / "Resources" / "APT-FIM" / "PDFs"
            summary_dir = vault / "Resources" / "APT-FIM" / "Summaries"
            index_dir = vault / "Resources" / "APT-FIM" / ".index"
            pdf_dir.mkdir(parents=True)
            summary_dir.mkdir(parents=True)
            index_dir.mkdir(parents=True)
            intake = pdf_dir / "AnthropicEmbed.pdf"
            intake.write_bytes(b"%PDF-1.4\n")
            config = resources.prepare_provider_config(
                {
                    "provider": "anthropic",
                    "baseUrl": "",
                    "model": "claude-3-5-sonnet-latest",
                    "apiKey": "sk-ant-test",
                    "embeddingModel": "any",
                }
            )
            with patch.object(resources, "extract_pdf_pages") as mock_extract:
                with self.assertRaises(ValueError):
                    resources.process_intake_library(
                        vault,
                        pdf_dir=pdf_dir,
                        summary_dir=summary_dir,
                        index_dir=index_dir,
                        config=config,
                        generate_embeddings=True,
                    )
                mock_extract.assert_not_called()
            self.assertTrue(intake.is_file())


if __name__ == "__main__":
    unittest.main()
