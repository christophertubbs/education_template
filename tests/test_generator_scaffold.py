"""Tests for reusable generated Django scaffold behavior."""

from __future__ import annotations

import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from education_generator import generator
from education_generator import cli
from education_generator.constants import PACKAGE_ROOT, TEMPLATE_ROOT
from education_generator.rendering import render_tree


class GeneratorScaffoldTests(unittest.TestCase):
    """Verify generator helpers that support non-lstm projects."""

    def test_load_project_configuration_accepts_explicit_content_path(self) -> None:
        """Project configuration resolves an explicit curriculum data path."""

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

    def test_load_project_configuration_defaults_content_path_by_name(self) -> None:
        """A project can use the conventional repository curriculum path."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            configuration_path = temporary_directory / "project.json"
            configuration_path.write_text(
                json.dumps(
                    {
                        "repository_url": "https://example.test/cfe.git",
                        "name": "cfe",
                        "revision": "main",
                        "curriculum_app_name": "cfe",
                        "display_name": "CFE",
                    }
                ),
                encoding="utf-8",
            )

            configuration = generator.load_project_configuration(configuration_path)

        self.assertEqual(
            configuration.curriculum_content_path,
            (temporary_directory / "curricula" / "cfe" / "curriculum.json").resolve(),
        )

    def test_app_config_class_uses_pascal_case(self) -> None:
        """Generated AppConfig class names are derived from package names."""

        self.assertEqual(
            generator.app_config_class("example_project"),
            "ExampleProjectConfig",
        )

    def test_no_migration_or_manage_script_is_stored_as_a_template(self) -> None:
        """Django owns generated migrations and the host management script."""

        template_files = {
            path.relative_to(TEMPLATE_ROOT).as_posix()
            for path in TEMPLATE_ROOT.rglob("*")
            if path.is_file()
        }

        self.assertNotIn("host/manage.py", template_files)
        self.assertFalse(
            any(path.endswith("0001_initial.py") for path in template_files)
        )
        launch_script = PACKAGE_ROOT / "launch.sh"
        self.assertTrue(launch_script.is_file())
        self.assertTrue(launch_script.stat().st_mode & stat.S_IXUSR)

    def test_template_renderer_ignores_python_cache_files(self) -> None:
        """Compiled cache artifacts cannot break text scaffold rendering."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            source = temporary_directory / "source"
            destination = temporary_directory / "destination"
            cache_directory = source / "__pycache__"
            cache_directory.mkdir(parents=True)
            (source / "module.py").write_text("NAME = '__NAME__'\n", encoding="utf-8")
            script_path = source / "launch.sh"
            script_path.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
            script_path.chmod(0o755)
            (cache_directory / "module.pyc").write_bytes(b"\xcb\x00")

            render_tree(source, destination, {"__NAME__": "rendered"})

            self.assertEqual(
                (destination / "module.py").read_text(encoding="utf-8"),
                "NAME = 'rendered'\n",
            )
            self.assertFalse((destination / "__pycache__").exists())
            self.assertTrue((destination / "launch.sh").stat().st_mode & stat.S_IXUSR)

    @patch("education_generator.scaffold.run_process")
    def test_generate_migrations_invokes_django(self, run_process_mock) -> None:
        """Migration creation delegates to the generated Django project."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            content_path = temporary_directory / "curriculum.json"
            content_path.write_text("{}", encoding="utf-8")
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

            generator.generate_migrations(context)

        command = run_process_mock.call_args.args[0]
        self.assertIn("makemigrations", command)
        self.assertIn("example_project", command)
        self.assertIn("--settings=education_generator.migration_settings", command)

    @patch("education_generator.cli.ignore_nested_curriculum_repository")
    @patch("education_generator.cli.initialize_generated_repository")
    @patch("education_generator.cli.generate_migrations")
    @patch("education_generator.cli.create_curriculum_app")
    @patch("education_generator.cli.create_host_project")
    @patch("education_generator.cli.recreate_generated_root")
    def test_existing_host_is_preserved(
        self,
        recreate_root_mock,
        create_host_mock,
        create_app_mock,
        migrations_mock,
        initialize_repository_mock,
        ignore_nested_mock,
    ) -> None:
        """Adding a curriculum does not regenerate an existing host."""

        with tempfile.TemporaryDirectory() as temporary_directory_name:
            temporary_directory = Path(temporary_directory_name)
            generated_root = temporary_directory / "generated"
            generated_root.mkdir()
            configuration = generator.ProjectConfiguration(
                repository_url="https://example.test/cfe.git",
                name="cfe",
                revision="main",
                curriculum_app_name="cfe",
                display_name="CFE",
                curriculum_content_path=temporary_directory / "curriculum.json",
            )
            context = generator.GenerationContext(
                repository_root=temporary_directory,
                configuration=configuration,
                target_repository_path=temporary_directory / "repository",
                resolved_commit="abc123",
                generated_root=generated_root,
                curriculum_repository_path=generated_root / "cfe",
                generated_at="2026-09-03T00:00:00+00:00",
            )

            cli.generate(context)

        recreate_root_mock.assert_not_called()
        create_host_mock.assert_not_called()
        create_app_mock.assert_called_once_with(context)
        migrations_mock.assert_called_once_with(context)
        initialize_repository_mock.assert_called_once()
        ignore_nested_mock.assert_called_once_with(generated_root, "cfe")

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
