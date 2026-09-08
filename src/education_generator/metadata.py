"""Build and write generated-repository provenance metadata."""

from __future__ import annotations

import json
from pathlib import Path

from .constants import (
    CURRICULUM_SCHEMA_VERSION,
    GENERATOR_NAME,
    GENERATOR_VERSION,
    RUNTIME_VERSION,
)
from .context import GenerationContext


def build_metadata(
    context: GenerationContext,
    repository_type: str = "curriculum_product",
) -> dict[str, str]:
    """Build serializable generation metadata."""

    configuration = context.configuration
    metadata = {
        "generator_name": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "generation_timestamp": context.generated_at,
        "repository_type": repository_type,
        "target_repository_name": configuration.name,
        "target_repository_url": configuration.repository_url,
        "configured_target_revision": configuration.revision,
        "resolved_target_commit": context.resolved_commit,
        "curriculum_product_name": configuration.curriculum_product_name,
        "curriculum_product_version": "1.0.0",
        "curriculum_schema_version": CURRICULUM_SCHEMA_VERSION,
        "compatible_education_runtime": configuration.runtime_compatibility,
        "education_runtime_version_at_generation": RUNTIME_VERSION,
        "analysis_methodology": "staged-artifacts-v1",
    }
    if context.prior_source_commit:
        metadata["prior_source_revision"] = context.prior_source_commit
    return metadata


def write_metadata(
    destination: Path,
    context: GenerationContext,
    repository_type: str = "curriculum_product",
) -> None:
    """Write generation metadata as formatted JSON."""

    destination.write_text(
        json.dumps(build_metadata(context, repository_type), indent=2) + "\n",
        encoding="utf-8",
    )
