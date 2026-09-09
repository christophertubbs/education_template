"""Basic package and provenance checks for __DISPLAY_NAME__."""

import json
import unittest
from importlib.metadata import distribution
from importlib.resources import files


class ProductTests(unittest.TestCase):
    def test_packaged_curriculum_has_exact_source_revision(self):
        path = files("__APP_NAME__").joinpath("data/curriculum.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["metadata"]["resolved_target_commit"], "__RESOLVED_COMMIT__"
        )

    def test_package_advertises_curriculum_product(self):
        products = {
            entry_point.name: entry_point.value
            for entry_point in distribution("__APP_NAME__").entry_points
            if entry_point.group == "education_curriculum.products"
        }
        self.assertEqual(
            products,
            {"__APP_NAME__": "__APP_NAME__.apps:__APP_CONFIG_CLASS__"},
        )


if __name__ == "__main__":
    unittest.main()
