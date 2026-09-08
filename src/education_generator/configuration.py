"""Load and validate generator configuration."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfiguration:
    """Validated values loaded from ``project.json``."""

    repository_url: str
    name: str
    revision: str
    curriculum_app_name: str
    display_name: str
    curriculum_content_path: Path


def load_project_configuration(configuration_path: Path) -> ProjectConfiguration:
    """Load and validate a project configuration file."""

    raw_configuration = json.loads(configuration_path.read_text(encoding="utf-8"))
    required_fields = (
        "repository_url",
        "name",
        "revision",
        "curriculum_app_name",
        "display_name",
    )
    missing_fields = [
        field for field in required_fields if not raw_configuration.get(field)
    ]
    if missing_fields:
        raise ValueError(f"Missing required project fields: {missing_fields}")

    name = str(raw_configuration["name"])
    app_name = str(raw_configuration["curriculum_app_name"])
    display_name = str(raw_configuration["display_name"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        raise ValueError(f"Unsafe repository name: {name!r}")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", app_name):
        raise ValueError(f"Invalid Python package name: {app_name!r}")
    if any(character in display_name for character in ('"', "\n", "\r")):
        raise ValueError("display_name cannot contain quotes or line breaks")

    raw_content_path = raw_configuration.get(
        "curriculum_content_path",
        f"curricula/{name}/curriculum.json",
    )
    content_path = _resolve_content_path(configuration_path.parent, raw_content_path)
    return ProjectConfiguration(
        repository_url=str(raw_configuration["repository_url"]),
        name=name,
        revision=str(raw_configuration["revision"]),
        curriculum_app_name=app_name,
        display_name=display_name,
        curriculum_content_path=content_path,
    )


def with_content_override(
    configuration: ProjectConfiguration,
    content_path: Path | None,
) -> ProjectConfiguration:
    """Return configuration using an optional command-line content upload."""

    if content_path is None:
        return configuration
    resolved_path = content_path.resolve()
    if not resolved_path.is_file():
        raise ValueError(f"Curriculum content file does not exist: {resolved_path}")
    return replace(configuration, curriculum_content_path=resolved_path)


def _resolve_content_path(base_path: Path, raw_path: object) -> Path:
    """Resolve and verify a configured curriculum content path."""

    if not isinstance(raw_path, str):
        raise ValueError("curriculum_content_path must be a string")
    content_path = (base_path / raw_path).resolve()
    return content_path


def app_config_class(app_name: str) -> str:
    """Return a conventional Django ``AppConfig`` class name."""

    words = [word for word in app_name.split("_") if word]
    return "".join(word.capitalize() for word in words) + "Config"
