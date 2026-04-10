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
        self.assertTrue(ollama["baseUrl"].startswith("http://"))

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


if __name__ == "__main__":
    unittest.main()
