"""Command-line orchestration for education application generation."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from .configuration import load_project_configuration, with_content_override
from .context import GenerationContext
from .repositories import (
    acquire_target_repository,
    initialize_generated_repository,
    ignore_nested_curriculum_repository,
    resolve_revision,
)
from .scaffold import (
    create_curriculum_app,
    create_host_project,
    generate_migrations,
    recreate_generated_root,
)


def main() -> None:
    """Generate the configured standalone host and curriculum app."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default="project.json")
    parser.add_argument(
        "--curriculum-content",
        type=Path,
        help="Upload curriculum JSON in place of the path configured by project.json.",
    )
    arguments = parser.parse_args()

    repository_root = Path.cwd()
    configuration = load_project_configuration(repository_root / arguments.project)
    configuration = with_content_override(
        configuration,
        arguments.curriculum_content,
    )
    target_path = acquire_target_repository(repository_root, configuration)
    generated_root = repository_root / "generated" / "education"
    context = GenerationContext(
        repository_root=repository_root,
        configuration=configuration,
        target_repository_path=target_path,
        resolved_commit=resolve_revision(target_path, configuration.revision),
        generated_root=generated_root,
        curriculum_repository_path=generated_root / configuration.name,
        generated_at=datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
    )

    generate(context)


def generate(context: GenerationContext) -> None:
    """Generate one Curriculum App while preserving an existing host."""

    generated_root = context.generated_root
    host_created = not generated_root.exists()
    if host_created:
        recreate_generated_root(generated_root)
        create_host_project(context)
    create_curriculum_app(context)
    generate_migrations(context)
    initialize_generated_repository(
        context.curriculum_repository_path,
        "Initial generated curriculum app",
    )
    if host_created:
        initialize_generated_repository(
            generated_root,
            "Initial generated host project",
        )
    else:
        ignore_nested_curriculum_repository(
            generated_root,
            context.configuration.name,
        )
