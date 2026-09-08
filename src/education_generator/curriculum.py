"""Validate and package uploaded curriculum data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .context import GenerationContext
from .metadata import build_metadata


REQUIRED_SECTIONS = (
    "course",
    "lessons",
    "glossary",
    "assessments",
    "questions",
    "coverage",
)


def load_curriculum_content(context: GenerationContext) -> dict[str, Any]:
    """Load uploaded curriculum data and inject current provenance metadata."""

    content_path = context.configuration.curriculum_content_path
    if not content_path.is_file():
        raise ValueError(f"Curriculum content file does not exist: {content_path}")
    curriculum = json.loads(content_path.read_text(encoding="utf-8"))
    if not isinstance(curriculum, dict):
        raise ValueError("Curriculum content must be a JSON object")
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in curriculum
    ]
    if missing_sections:
        raise ValueError(f"Missing curriculum sections: {missing_sections}")
    if not isinstance(curriculum["course"], dict):
        raise ValueError("Curriculum course must be a JSON object")
    for section in REQUIRED_SECTIONS[1:]:
        if not isinstance(curriculum[section], list):
            raise ValueError(f"Curriculum {section} must be a JSON array")

    curriculum["metadata"] = build_metadata(context, "curriculum_data")
    return curriculum


def package_curriculum(context: GenerationContext, package_root: Path) -> None:
    """Write uploaded curriculum into the generated installable package."""

    destination = package_root / "data" / "curriculum.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(load_curriculum_content(context), indent=2) + "\n",
        encoding="utf-8",
    )
