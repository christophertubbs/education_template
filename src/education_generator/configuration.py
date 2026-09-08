"""Load and validate untrusted generator configuration."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class ProjectConfiguration:
    """Validated values loaded from ``project.json``."""

    repository_url: str
    name: str
    revision: str
    curriculum_product_name: str
    display_name: str
    curriculum_source_path: Path
    runtime_compatibility: str
    assumed_learner_prerequisites: tuple[str, ...]
    required_topics: tuple[str, ...]
    initial_branch: str
    automated_commit: bool


def load_project_configuration(configuration_path: Path) -> ProjectConfiguration:
    """Load and validate a project configuration file."""

    raw_configuration = json.loads(configuration_path.read_text(encoding="utf-8"))
    required_fields = (
        "repository_url",
        "name",
        "revision",
        "curriculum_product_name",
        "display_name",
    )
    missing_fields = [
        field for field in required_fields if not raw_configuration.get(field)
    ]
    if missing_fields:
        raise ValueError(f"Missing required project fields: {missing_fields}")

    name = str(raw_configuration["name"])
    product_name = str(raw_configuration["curriculum_product_name"])
    display_name = str(raw_configuration["display_name"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        raise ValueError(f"Unsafe repository name: {name!r}")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", product_name):
        raise ValueError(f"Invalid Curriculum Product package: {product_name!r}")
    if any(character in display_name for character in ('"', "\n", "\r")):
        raise ValueError("display_name cannot contain quotes or line breaks")

    repository_url = str(raw_configuration["repository_url"])
    parsed_url = urlparse(repository_url)
    if parsed_url.scheme not in {"https", "ssh", "git", "file"}:
        raise ValueError("repository_url must use https, ssh, git, or file")

    source_path = _resolve_local_path(
        configuration_path.parent,
        raw_configuration.get("curriculum_source_path", f"curricula/{name}"),
        "curriculum_source_path",
    )
    prerequisites = _string_tuple(raw_configuration, "assumed_learner_prerequisites")
    required_topics = _string_tuple(raw_configuration, "required_topics")
    initial_branch = str(raw_configuration.get("initial_branch", "main"))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", initial_branch):
        raise ValueError(f"Invalid initial branch: {initial_branch!r}")
    return ProjectConfiguration(
        repository_url=repository_url,
        name=name,
        revision=str(raw_configuration["revision"]),
        curriculum_product_name=product_name,
        display_name=display_name,
        curriculum_source_path=source_path,
        runtime_compatibility=str(
            raw_configuration.get("runtime_compatibility", ">=1.0,<2.0")
        ),
        assumed_learner_prerequisites=prerequisites,
        required_topics=required_topics,
        initial_branch=initial_branch,
        automated_commit=bool(raw_configuration.get("automated_commit", True)),
    )


def _resolve_local_path(base_path: Path, raw_path: object, field_name: str) -> Path:
    """Resolve a configured path while preventing traversal outside the project."""

    if not isinstance(raw_path, str):
        raise ValueError(f"{field_name} must be a string")
    resolved_base = base_path.resolve()
    resolved_path = (resolved_base / raw_path).resolve()
    if not resolved_path.is_relative_to(resolved_base):
        raise ValueError(f"{field_name} must stay inside the repository")
    return resolved_path


def app_config_class(app_name: str) -> str:
    """Return a conventional Django ``AppConfig`` class name."""

    words = [word for word in app_name.split("_") if word]
    return "".join(word.capitalize() for word in words) + "Config"


def _string_tuple(configuration: dict[str, object], field_name: str) -> tuple[str, ...]:
    """Validate an optional JSON array containing non-empty strings."""

    raw_values = configuration.get(field_name, [])
    if not isinstance(raw_values, list) or not all(
        isinstance(value, str) and value.strip() for value in raw_values
    ):
        raise ValueError(f"{field_name} must be an array of non-empty strings")
    return tuple(raw_values)
