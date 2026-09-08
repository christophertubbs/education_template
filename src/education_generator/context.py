"""Resolved state shared by generation phases."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .configuration import ProjectConfiguration


@dataclass(frozen=True)
class GenerationContext:
    """Paths and provenance for one generation run."""

    repository_root: Path
    configuration: ProjectConfiguration
    target_repository_path: Path
    resolved_commit: str
    workspace_path: Path
    product_repository_path: Path
    generated_at: str
    prior_source_commit: str | None = None
