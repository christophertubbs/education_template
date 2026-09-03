"""Tests for reusable generated Django scaffold behavior."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from education_generator import generator


class GeneratorScaffoldTests(unittest.TestCase):
    """Verify generator helpers that support non-lstm projects."""

    def test_load_project_configuration_accepts_content_path(self) -> None:
        """Project configuration resolves optional curriculum content paths."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            configuration_path = temporary_directory / "project.json"
            content_path = temporary_directory / "curriculum.json"
            content_path.write_text("{}", encoding="utf-8")
            configuration_path.write_text(
                json.dumps(
                    {
                        "repository_url": "https://example.test/project.git",
                        "name": "example-project",
                        "revision": "main",
                        "curriculum_app_name": "example_project",
                        "display_name": "Example Project",
                        "curriculum_content_path": "curriculum.json",
                    }
                ),
                encoding="utf-8",
            )

            configuration = generator.load_project_configuration(configuration_path)

        self.assertEqual(configuration.curriculum_app_name, "example_project")
        self.assertEqual(configuration.curriculum_content_path, content_path.resolve())

    def test_app_config_class_uses_pascal_case(self) -> None:
        """Generated AppConfig class names are derived from package names."""

        self.assertEqual(
            generator.app_config_class("example_project"),
            "ExampleProjectConfig",
        )

    def test_migration_template_uses_configured_app_label(self) -> None:
        """Generated migrations do not hard-code the lstm app label."""

        migration_source = generator.migration_py("example_project")

        self.assertIn('to="example_project.assessment"', migration_source)
        self.assertIn('to="example_project.lesson"', migration_source)
        self.assertNotIn('to="lstm.', migration_source)

    def test_external_curriculum_content_gets_current_metadata(self) -> None:
        """External curriculum JSON keeps scaffold shape with fresh provenance."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            content_path = temporary_directory / "curriculum.json"
            content_path.write_text(
                json.dumps(
                    {
                        "metadata": {"stale": True},
                        "course": {"identifier": "course"},
                        "lessons": [],
                        "glossary": [],
                        "assessments": [],
                        "questions": [],
                        "coverage": [],
                    }
                ),
                encoding="utf-8",
            )
            configuration = generator.ProjectConfiguration(
                repository_url="https://example.test/project.git",
                name="example-project",
                revision="main",
                curriculum_app_name="example_project",
                display_name="Example Project",
                curriculum_content_path=content_path,
            )
            context = generator.GenerationContext(
                repository_root=temporary_directory,
                configuration=configuration,
                target_repository_path=temporary_directory / "repository",
                resolved_commit="abc123",
                generated_root=temporary_directory / "generated",
                curriculum_repository_path=temporary_directory / "generated" / "app",
                generated_at="2026-09-03T00:00:00+00:00",
            )

            curriculum = generator.load_curriculum_content(context)

        self.assertEqual(
            curriculum["metadata"]["resolved_target_commit"],
            "abc123",
        )
        self.assertNotIn("stale", curriculum["metadata"])


if __name__ == "__main__":
    unittest.main()
