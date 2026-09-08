"""Basic package and provenance checks for __DISPLAY_NAME__."""

import json
import unittest
from importlib.resources import files


class ProductTests(unittest.TestCase):
    def test_packaged_curriculum_has_exact_source_revision(self):
        path = files("__APP_NAME__").joinpath("data/curriculum.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["metadata"]["resolved_target_commit"], "__RESOLVED_COMMIT__"
        )


if __name__ == "__main__":
    unittest.main()
