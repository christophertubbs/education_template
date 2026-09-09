"""Tests for automatic installed Curriculum Product discovery."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured

from education_runner.product_discovery import discover_product_apps


@dataclass(frozen=True)
class FakeEntryPoint:
    """Minimal importlib.metadata entry-point test value."""

    name: str
    value: str


class ProductDiscoveryTests(unittest.TestCase):
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
