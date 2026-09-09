"""Tests for the repository installation workflow."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class InstallScriptTests(unittest.TestCase):
    """Verify that installation performs every required preparation step."""

    def test_runs_migration_refresh_and_static_collection_in_order(self) -> None:
        """The script must refresh JSON even when migration state is current."""

        with tempfile.TemporaryDirectory() as directory_name:
            temporary_root = Path(directory_name)
            invocation_log = temporary_root / "invocations.txt"
            fake_python = temporary_root / "python"
            fake_python.write_text(
                '#!/usr/bin/env bash\nprintf \'%s\\n\' "$*" >> "${INSTALL_TEST_LOG}"\n',
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            environment = os.environ.copy()
            environment.update(
                {
                    "INSTALL_TEST_LOG": str(invocation_log),
                    "PYTHON_BIN": str(fake_python),
                }
            )

            subprocess.run(["bash", "install.sh"], check=True, env=environment)

            self.assertEqual(
                invocation_log.read_text(encoding="utf-8").splitlines(),
                [
                    "manage.py migrate --noinput",
                    "manage.py load_curricula",
                    "manage.py collectstatic --noinput",
                ],
            )


if __name__ == "__main__":
    unittest.main()
