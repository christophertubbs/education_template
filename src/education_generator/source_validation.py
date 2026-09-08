"""Verify Target Repository source references against the resolved checkout."""

from __future__ import annotations

from pathlib import Path

from .artifacts import CurriculumArtifacts
from .validation import ValidationReport


def validate_source_references(
    artifacts: CurriculumArtifacts,
    repository_path: Path,
    resolved_commit: str,
) -> ValidationReport:
    """Check local paths, line bounds, and commit-pinned repository URLs."""

    report = ValidationReport()
    for source in artifacts.curriculum.get("sources", []):
        if source.get("evidence_kind") != "target_source":
            continue
        identifier = source.get("identifier")
        file_path = source.get("file_path")
        if not isinstance(file_path, str):
            report.errors.append(f"{identifier} lacks a target file path")
            continue
        candidate = (repository_path / file_path).resolve()
        if not candidate.is_relative_to(repository_path.resolve()):
            report.errors.append(f"{identifier} escapes the Target Repository")
            continue
        if not candidate.is_file():
            report.errors.append(f"{identifier} references missing file {file_path}")
            continue
        line_count = sum(1 for _ in candidate.open(encoding="utf-8", errors="replace"))
        start_line = source.get("start_line")
        end_line = source.get("end_line")
        if not isinstance(start_line, int) or start_line < 1:
            report.errors.append(f"{identifier} has an invalid start line")
        if (
            not isinstance(end_line, int)
            or end_line < start_line
            or end_line > line_count
        ):
            report.errors.append(f"{identifier} has an invalid end line")
        url = source.get("url", "")
        if url and resolved_commit not in url:
            report.errors.append(f"{identifier} URL is not pinned to {resolved_commit}")
    return report
