"""Command-line interface for staged Curriculum Product generation."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from .configuration import load_project_configuration
from .context import GenerationContext
from .pipeline import run_pipeline
from .repositories import (
    acquire_target_repository,
    checkout_resolved_revision,
    resolve_revision,
)


def main() -> None:
    """Generate the configured Curriculum Product after complete validation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path("project.json"))
    arguments = parser.parse_args()
    repository_root = Path.cwd().resolve()
    configuration_path = (repository_root / arguments.project).resolve()
    if not configuration_path.is_relative_to(repository_root):
        raise ValueError("project configuration must be inside the repository")
    configuration = load_project_configuration(configuration_path)
    target_path = acquire_target_repository(repository_root, configuration)
    resolved_commit = resolve_revision(target_path, configuration.revision)
    checkout_resolved_revision(target_path, resolved_commit)
    product_slug = f"{configuration.name}-curriculum"
    product_path = repository_root / "generated" / product_slug
    prior_source_commit = _prior_source_commit(product_path)
    context = GenerationContext(
        repository_root=repository_root,
        configuration=configuration,
        target_repository_path=target_path,
        resolved_commit=resolved_commit,
        workspace_path=repository_root / ".work" / product_slug,
        product_repository_path=product_path,
        generated_at=datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        prior_source_commit=prior_source_commit,
    )
    run_pipeline(context)


def _prior_source_commit(product_path: Path) -> str | None:
    """Read the last successfully promoted source revision, if present."""

    metadata_path = product_path / "provenance" / "generation.json"
    if not metadata_path.is_file():
        return None
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    value = metadata.get("resolved_target_commit")
    return value if isinstance(value, str) else None

