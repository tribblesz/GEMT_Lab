import importlib.util
import tempfile
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
