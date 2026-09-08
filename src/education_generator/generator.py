"""Compatibility imports for the modular education generator API."""

from .cli import main
from .configuration import (
    ProjectConfiguration,
    app_config_class,
    load_project_configuration,
)
from .context import GenerationContext
from .curriculum import load_curriculum_content
from .scaffold import create_curriculum_app, create_host_project, generate_migrations


__all__ = [
    "GenerationContext",
    "ProjectConfiguration",
    "app_config_class",
    "create_curriculum_app",
    "create_host_project",
    "generate_migrations",
    "load_curriculum_content",
    "load_project_configuration",
    "main",
]
