"""Tests for automatic installed Curriculum Product discovery."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured

from education_runner.product_discovery import discover_product_apps


@dataclass(frozen=True)
class FakeEntryPoint:
    """Minimal importlib.metadata entry-point test value."""

    name: str
    value: str


class ProductDiscoveryTests(unittest.TestCase):
    def test_discovers_local_product_without_curriculum_in_its_name(self) -> None:
        """Local project metadata is authoritative instead of name conventions."""

        with tempfile.TemporaryDirectory() as directory_name:
            root = Path(directory_name)
            curriculum_path = root / "curricula" / "rain-model"
            product_path = root / "generated" / "learning-material"
            curriculum_path.mkdir(parents=True)
            (product_path / "src").mkdir(parents=True)
            (product_path / "provenance").mkdir()
            (product_path / "provenance" / "generation.json").write_text(
                json.dumps({"target_repository_name": "rain-model"}),
                encoding="utf-8",
            )
            (product_path / "pyproject.toml").write_text(
                """[project]
name = "water_lessons"
[project.entry-points."education_curriculum.products"]
water_lessons = "water_lessons.apps:WaterLessonsConfig"
""",
                encoding="utf-8",
            )

            with (
                patch.object(sys, "path", list(sys.path)),
                patch(
                    "education_runner.product_discovery.metadata.entry_points",
                    return_value=[],
                ),
            ):
                discovered = discover_product_apps(repository_root=root)
                self.assertEqual(discovered, ["water_lessons.apps.WaterLessonsConfig"])
                self.assertIn(str(product_path / "src"), sys.path)

    def test_ignores_generated_directory_without_matching_curriculum(self) -> None:
        """Unreviewed generated directories are not activated by themselves."""

        with tempfile.TemporaryDirectory() as directory_name:
            root = Path(directory_name)
            (root / "curricula").mkdir()
            product_path = root / "generated" / "unreviewed"
            (product_path / "src").mkdir(parents=True)
            (product_path / "provenance").mkdir()
            (product_path / "provenance" / "generation.json").write_text(
                json.dumps({"target_repository_name": "unreviewed"}),
                encoding="utf-8",
            )

            with patch(
                "education_runner.product_discovery.metadata.entry_points",
                return_value=[],
            ):
                self.assertEqual(discover_product_apps(repository_root=root), [])

    @patch("education_runner.product_discovery.metadata.entry_points")
    def test_discovers_all_advertised_products(self, entry_points) -> None:
        entry_points.return_value = [
            FakeEntryPoint(
                "sacsma_curriculum", "sacsma_curriculum.apps:SacsmaCurriculumConfig"
            ),
            FakeEntryPoint("cfe_curriculum", "cfe_curriculum.apps:CfeCurriculumConfig"),
        ]

        self.assertEqual(
            discover_product_apps(),
            [
                "cfe_curriculum.apps.CfeCurriculumConfig",
                "sacsma_curriculum.apps.SacsmaCurriculumConfig",
            ],
        )
        entry_points.assert_called_once_with(group="education_curriculum.products")

    @patch("education_runner.product_discovery.metadata.entry_points")
    def test_legacy_configuration_is_additive_and_deduplicated(
        self, entry_points
    ) -> None:
        entry_points.return_value = [
            FakeEntryPoint("cfe_curriculum", "cfe_curriculum.apps:CfeCurriculumConfig")
        ]

        self.assertEqual(
            discover_product_apps("legacy_curriculum, cfe_curriculum"),
            [
                "cfe_curriculum.apps.CfeCurriculumConfig",
                "legacy_curriculum.apps.LegacyCurriculumConfig",
            ],
        )

    @patch("education_runner.product_discovery.metadata.entry_points")
    def test_conflicting_advertisements_fail_closed(self, entry_points) -> None:
        entry_points.return_value = [
            FakeEntryPoint("example", "example.apps:FirstConfig"),
            FakeEntryPoint("example", "example.apps:SecondConfig"),
        ]

        with self.assertRaisesRegex(ImproperlyConfigured, "Conflicting"):
            discover_product_apps()

    @patch("education_runner.product_discovery.metadata.entry_points")
    def test_unrelated_entry_point_module_is_rejected(self, entry_points) -> None:
        entry_points.return_value = [
            FakeEntryPoint("example", "unrelated.apps:ExampleConfig")
        ]

        with self.assertRaisesRegex(ImproperlyConfigured, "unrelated module"):
            discover_product_apps()


if __name__ == "__main__":
    unittest.main()
