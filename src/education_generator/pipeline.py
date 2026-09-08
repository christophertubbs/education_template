"""Multi-stage generation orchestration with durable completion state."""

from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .artifacts import load_artifacts
from .context import GenerationContext
from .inventory import create_regeneration_impact, create_repository_inventory
from .repositories import (
    commit_generated_update,
    ensure_clean_repository,
    initialize_generated_repository,
)
from .scaffold import assemble_product, promote_staged_product
from .source_validation import validate_source_references
from .validation import validate_artifacts


@dataclass
class PipelineState:
    """Durable execution state for resumable generation."""

    path: Path
    phases: dict[str, str]
    unresolved: list[str]

    @classmethod
    def create(cls, path: Path) -> PipelineState:
        return cls(path=path, phases={}, unresolved=[])

    def record(self, phase: str, status: str) -> None:
        self.phases[phase] = status
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"phases": self.phases, "unresolved": self.unresolved}, indent=2)
            + "\n",
            encoding="utf-8",
        )


def run_pipeline(context: GenerationContext) -> Path:
    """Validate, assemble, verify, and promote one Curriculum Product."""

    state = PipelineState.create(context.workspace_path / "state.json")
    state.record("configuration_validation", "complete")
    state.record("repository_acquisition", "complete")
    state.record("revision_resolution", "complete")
    create_repository_inventory(
        context.target_repository_path,
        context.workspace_path / "repository-inventory.json",
    )
    create_regeneration_impact(
        context.target_repository_path,
        context.prior_source_commit,
        context.resolved_commit,
        context.workspace_path / "regeneration-impact.json",
    )
    state.record("repository_inventory", "complete")

    artifacts = load_artifacts(context.configuration.curriculum_source_path)
    state.record("analysis_artifact_loading", "complete")
    report = validate_artifacts(artifacts)
    source_report = validate_source_references(
        artifacts,
        context.target_repository_path,
        context.resolved_commit,
    )
    report.errors.extend(source_report.errors)
    if not report.is_valid:
        state.unresolved.extend(report.errors)
        state.record("curriculum_validation", "failed")
        report.raise_for_errors()
    state.record("curriculum_validation", "complete")

    staging_path = context.workspace_path / "staging"
    if staging_path.exists():
        shutil.rmtree(staging_path)
    staging_path.mkdir(parents=True)
    assemble_product(context, artifacts, staging_path)
    state.record("product_assembly", "complete")
    validate_python_sources(staging_path)
    state.record("package_validation", "complete")

    destination = context.product_repository_path
    existing_repository = destination.exists() and (destination / ".git").exists()
    if existing_repository:
        ensure_clean_repository(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    promote_staged_product(staging_path, destination)
    state.record("release_promotion", "complete")
    if context.configuration.automated_commit:
        if existing_repository:
            commit_generated_update(destination, "Regenerate Curriculum Product")
        else:
            initialize_generated_repository(
                destination,
                "Initial generated Curriculum Product",
                context.configuration.initial_branch,
            )
    return destination


def validate_python_sources(root: Path) -> None:
    """Compile all generated Python without leaving bytecode in the product."""

    import py_compile

    with tempfile.TemporaryDirectory() as temporary_directory:
        cache_root = Path(temporary_directory)
        for index, path in enumerate(root.rglob("*.py")):
            py_compile.compile(
                path, cfile=str(cache_root / f"{index}.pyc"), doraise=True
            )
