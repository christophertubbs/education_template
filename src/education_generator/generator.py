"""Stable public API for generator integrations."""

from .artifacts import CurriculumArtifacts, load_artifacts
from .configuration import ProjectConfiguration, load_project_configuration
from .context import GenerationContext
from .pipeline import PipelineState, run_pipeline
from .validation import ValidationReport, validate_artifacts

__all__ = [
    "CurriculumArtifacts",
    "GenerationContext",
    "PipelineState",
    "ProjectConfiguration",
    "ValidationReport",
    "load_artifacts",
    "load_project_configuration",
    "run_pipeline",
    "validate_artifacts",
]
