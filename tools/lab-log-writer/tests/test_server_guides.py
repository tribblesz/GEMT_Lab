import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "server.py"


def load_server_module():
    spec = importlib.util.spec_from_file_location("lab_log_writer_server", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GuideInventoryTests(unittest.TestCase):
    def test_build_guide_inventory_includes_curated_docs_and_excludes_non_guides(self):
        server = load_server_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            vault_root = repo_root / "ELN_vault"
            (vault_root / "Notes" / "HowTos" / "Obsidian ELN").mkdir(parents=True)
            (vault_root / "Notes" / "HowTos" / "Getting started with Obsidian").mkdir(parents=True)
            (vault_root / "Lists" / "Operations").mkdir(parents=True)
            (vault_root / "Resources" / "APT-FIM").mkdir(parents=True)
            (vault_root / "Resources" / "APT-FIM" / "Summaries").mkdir(parents=True)
            (vault_root / "Daily Notes" / "2025").mkdir(parents=True)
            (repo_root / "tools" / "lab-log-writer").mkdir(parents=True)

            (vault_root / "Quick Start Guide.md").write_text("# Quick Start Guide\n\nFast onboarding.\n", encoding="utf-8")
            (vault_root / "Lab Log Writer.md").write_text("# Lab Log Writer\n\nWriter help.\n", encoding="utf-8")
            (vault_root / "Notes" / "HowTos" / "Obsidian ELN" / "Embeddings.md").write_text(
                "# Embeddings\n\nEmbeddings explain semantic indexing.\n", encoding="utf-8"
            )
            (vault_root / "Notes" / "HowTos" / "Getting started with Obsidian" / "Markdown Formatting Guide.md").write_text(
                "# Markdown Formatting Guide\n\nMarkdown basics.\n", encoding="utf-8"
            )
            (vault_root / "Lists" / "Operations" / "Startup Checklists.md").write_text(
                "# Startup Checklists\n\nStartup documentation.\n", encoding="utf-8"
            )
            (vault_root / "Resources" / "APT-FIM" / "Library.md").write_text(
                "# APT/FIM Resources\n\nResource workflow.\n", encoding="utf-8"
            )
            (vault_root / "Resources" / "APT-FIM" / "Summaries" / "Paper.md").write_text(
                "# Summary\n\nShould not be included.\n", encoding="utf-8"
            )
            (vault_root / "Daily Notes" / "2025" / "Today.md").write_text(
                "# Daily Note\n\nShould not be included.\n", encoding="utf-8"
            )
            (repo_root / "tools" / "lab-log-writer" / "README.md").write_text(
                "# Writer README\n\nTool explanation.\n", encoding="utf-8"
            )

            guides = server.build_guide_inventory(repo_root=repo_root, vault_root=vault_root)
            guide_paths = {item["relative_path"] for item in guides}

        self.assertIn("ELN_vault/Quick Start Guide.md", guide_paths)
        self.assertIn("ELN_vault/Lab Log Writer.md", guide_paths)
        self.assertIn("ELN_vault/Notes/HowTos/Obsidian ELN/Embeddings.md", guide_paths)
        self.assertIn("ELN_vault/Notes/HowTos/Getting started with Obsidian/Markdown Formatting Guide.md", guide_paths)
        self.assertIn("ELN_vault/Lists/Operations/Startup Checklists.md", guide_paths)
        self.assertIn("ELN_vault/Resources/APT-FIM/Library.md", guide_paths)
        self.assertIn("tools/lab-log-writer/README.md", guide_paths)
        self.assertNotIn("ELN_vault/Resources/APT-FIM/Summaries/Paper.md", guide_paths)
        self.assertNotIn("ELN_vault/Daily Notes/2025/Today.md", guide_paths)

    def test_build_guide_inventory_adds_description_preview_and_help_link(self):
        server = load_server_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            vault_root = repo_root / "ELN_vault"
            vault_root.mkdir(parents=True)
            (vault_root / "Quick Start Guide.md").write_text(
                "# Quick Start Guide\n\nFast onboarding for the current workflow.\n\nMore detail here.\n",
                encoding="utf-8",
            )

            guides = server.build_guide_inventory(repo_root=repo_root, vault_root=vault_root)

        quick_start = next(item for item in guides if item["relative_path"] == "ELN_vault/Quick Start Guide.md")
        self.assertEqual(quick_start["title"], "Quick Start Guide")
        self.assertTrue(quick_start["description"])
        self.assertIn("Fast onboarding", quick_start["preview"])
        self.assertIn("?form=help-and-guides&guide=", quick_start["help_url"])

    def test_build_guide_inventory_adds_functional_grouping_metadata(self):
        server = load_server_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            vault_root = repo_root / "ELN_vault"
            (vault_root / "Lists" / "Operations").mkdir(parents=True)
            (vault_root / "Notes" / "HowTos" / "Getting started with Obsidian").mkdir(parents=True)
            (vault_root / "Resources" / "APT-FIM").mkdir(parents=True)

            (vault_root / "Lists" / "Operations" / "Startup Checklists.md").write_text("# Startup Checklists\n\nStartup docs.\n", encoding="utf-8")
            (vault_root / "Notes" / "HowTos" / "Getting started with Obsidian" / "Markdown Formatting Guide.md").write_text(
                "# Markdown Formatting Guide\n\nMarkdown basics.\n", encoding="utf-8"
            )
            (vault_root / "Resources" / "APT-FIM" / "Library.md").write_text("# APT/FIM Resources\n\nResource workflow.\n", encoding="utf-8")

            guides = server.build_guide_inventory(repo_root=repo_root, vault_root=vault_root)

        startup = next(item for item in guides if item["relative_path"] == "ELN_vault/Lists/Operations/Startup Checklists.md")
        markdown = next(
            item
            for item in guides
            if item["relative_path"] == "ELN_vault/Notes/HowTos/Getting started with Obsidian/Markdown Formatting Guide.md"
        )
        library = next(item for item in guides if item["relative_path"] == "ELN_vault/Resources/APT-FIM/Library.md")

        self.assertEqual(startup["group"], "Operations")
        self.assertEqual(startup["subgroup"], "Checklists")
        self.assertEqual(markdown["group"], "Obsidian Reference")
        self.assertEqual(markdown["subgroup"], "Writing And Basics")
        self.assertEqual(library["group"], "Writer And Resources")
        self.assertEqual(library["subgroup"], "Literature Workflow")

    def test_plain_language_description_strips_code_like_markdown_from_fallback_summary(self):
        server = load_server_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            vault_root = repo_root / "ELN_vault"
            target_dir = vault_root / "Notes" / "HowTos" / "Getting started with Obsidian"
            target_dir.mkdir(parents=True)
            markdown_path = target_dir / "Custom Guide.md"
            markdown_path.write_text(
                "# Custom Guide\n\n"
                ">{!ignore me}\n"
                "> [!info] GUI writer entry\n"
                "> Start the local writer with `python tools/lab-log-writer/server.py`.\n\n"
                "{: .no_toc }\n"
                "![image](https://example.com/test.png)\n"
                "CSS snippet file: [MCL Multi Column.css](https://example.com/mcl.css)\n"
                "This note explains the actual workflow for experts.\n",
                encoding="utf-8",
            )

            guides = server.build_guide_inventory(repo_root=repo_root, vault_root=vault_root)

        custom = next(item for item in guides if item["relative_path"] == "ELN_vault/Notes/HowTos/Getting started with Obsidian/Custom Guide.md")
        self.assertNotIn("[!info]", custom["description"])
        self.assertNotIn("{: .no_toc", custom["description"])
        self.assertNotIn("![image]", custom["description"])
        self.assertNotIn("`python tools/lab-log-writer/server.py`", custom["description"])
        self.assertNotIn("CSS snippet file", custom["description"])
        self.assertIn("actual workflow", custom["description"].lower())


if __name__ == "__main__":
    unittest.main()
