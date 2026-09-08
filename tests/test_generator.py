"""Tests for configuration, artifacts, and generation gates."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from education_generator.artifacts import load_artifacts
from education_generator.configuration import load_project_configuration
from education_generator.repositories import resolve_revision
from education_generator.validation import validate_artifacts


class ConfigurationTests(unittest.TestCase):
    def test_rejects_curriculum_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory_name:
            root = Path(directory_name)
            path = root / "project.json"
            path.write_text(
                json.dumps(
                    {
                        "name": "safe",
                        "repository_url": "https://example.test/safe.git",
                        "revision": "main",
                        "curriculum_product_name": "safe_curriculum",
                        "display_name": "Safe",
                        "curriculum_source_path": "../escape",
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "stay inside"):
                load_project_configuration(path)

    def test_current_configuration_is_valid(self) -> None:
        configuration = load_project_configuration(Path("project.json"))
        self.assertEqual(configuration.curriculum_product_name, "cfe_curriculum")

    @patch("education_generator.repositories.run_process")
    def test_remote_tracking_branch_is_resolved_after_fetch(self, run_process) -> None:
        run_process.side_effect = [
            CompletedProcess([], 0, stdout="  origin/main\n", stderr=""),
            CompletedProcess([], 0, stdout="abc123\n", stderr=""),
        ]
        resolved = resolve_revision(Path("repository/example"), "main")
        self.assertEqual(resolved, "abc123")
        self.assertIn("origin/main^{commit}", run_process.call_args_list[1].args[0])


class ArtifactValidationTests(unittest.TestCase):
    def test_cfe_artifacts_pass_structural_completion_gate(self) -> None:
        report = validate_artifacts(load_artifacts(Path("curricula/cfe")))
        self.assertEqual(report.errors, [])

    def test_unresolved_item_prevents_completion(self) -> None:
        artifacts = load_artifacts(Path("curricula/cfe"))
        artifacts.completion["unresolved_required_items"] = ["missing evidence"]
        report = validate_artifacts(artifacts)
        self.assertIn("required items remain unresolved", report.errors)

    def test_paragraph_only_lesson_fails_presentation_validation(self) -> None:
        artifacts = load_artifacts(Path("curricula/cfe"))
        artifacts.curriculum["lessons"][0]["content"] = [
            {"type": "paragraph", "inline": [{"type": "text", "text": "Flat"}]}
        ]
        report = validate_artifacts(artifacts)
        self.assertTrue(any("flattens all content" in error for error in report.errors))

    def test_equation_requires_accessible_text(self) -> None:
        artifacts = load_artifacts(Path("curricula/cfe"))
        artifacts.curriculum["lessons"][0]["content"] = [
            {"type": "equation", "latex": "x=1"}
        ]
        report = validate_artifacts(artifacts)
        self.assertTrue(
            any("lacks accessible equation text" in error for error in report.errors)
        )

    def test_glossary_mentions_require_a_lesson_definition(self) -> None:
        artifacts = load_artifacts(Path("curricula/cfe"))
        schaake = next(
            item
            for item in artifacts.curriculum["glossary"]
            if item["identifier"] == "schaake"
        )
        schaake["lesson_identifiers"].remove("partitioning-and-et")
        report = validate_artifacts(artifacts)
        self.assertTrue(
            any("mentions glossary entry schaake" in error for error in report.errors)
        )


if __name__ == "__main__":
    unittest.main()
