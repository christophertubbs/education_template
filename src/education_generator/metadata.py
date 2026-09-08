"""Build and write generated-repository provenance metadata."""

from __future__ import annotations

import json
from pathlib import Path

from .constants import (
    CURRICULUM_SCHEMA_VERSION,
    GENERATOR_NAME,
    GENERATOR_VERSION,
    TEMPLATE_VERSION,
)
from .context import GenerationContext


def build_metadata(
    context: GenerationContext,
    repository_type: str,
) -> dict[str, str]:
    """Build serializable generation metadata."""

    configuration = context.configuration
    return {
        "generator_name": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "template_name": "django-curriculum",
        "template_version": TEMPLATE_VERSION,
        "generation_timestamp": context.generated_at,
        "repository_type": repository_type,
        "target_repository_name": configuration.name,
        "target_repository_url": configuration.repository_url,
        "configured_target_revision": configuration.revision,
        "resolved_target_commit": context.resolved_commit,
        "generated_package_name": configuration.curriculum_app_name,
        "curriculum_schema_version": CURRICULUM_SCHEMA_VERSION,
    }


def write_metadata(
    destination: Path,
    context: GenerationContext,
    repository_type: str,
) -> None:
    """Write generation metadata as formatted JSON."""

    destination.write_text(
        json.dumps(build_metadata(context, repository_type), indent=2) + "\n",
        encoding="utf-8",
    )
