"""Deterministic, non-executing Target Repository inventory."""

from __future__ import annotations

import json
from pathlib import Path

from .processes import run_process


def create_repository_inventory(repository_path: Path, destination: Path) -> None:
    """Record source layout without importing or executing target code."""

    files = []
    for path in sorted(repository_path.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(repository_path)
        files.append({"path": relative.as_posix(), "size_bytes": path.stat().st_size})
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps({"files": files}, indent=2) + "\n", encoding="utf-8"
    )


def create_regeneration_impact(
    repository_path: Path,
    prior_commit: str | None,
    resolved_commit: str,
    destination: Path,
) -> None:
    """Record source changes requiring curriculum re-audit."""

    changed_files: list[dict[str, str]] = []
    if prior_commit and prior_commit != resolved_commit:
        result = run_process(
            [
                "git",
                "-C",
                str(repository_path),
                "diff",
                "--name-status",
                prior_commit,
                resolved_commit,
            ],
            capture_output=True,
        )
        for line in result.stdout.splitlines():
            status, path = line.split("\t", maxsplit=1)
            changed_files.append({"status": status, "path": path})
    destination.write_text(
        json.dumps(
            {
                "prior_source_commit": prior_commit,
                "resolved_source_commit": resolved_commit,
                "changed_files": changed_files,
                "requires_reaudit": bool(changed_files),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
