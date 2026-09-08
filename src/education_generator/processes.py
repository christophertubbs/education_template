"""Subprocess helpers for explicit external tool invocation."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_process(
    command: list[str],
    *,
    capture_output: bool = False,
    extra_environment: dict[str, str] | None = None,
    working_directory: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command and raise when it fails."""

    environment = os.environ.copy()
    if extra_environment:
        environment.update(extra_environment)
    return subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=capture_output,
        cwd=working_directory,
        env=environment,
    )
