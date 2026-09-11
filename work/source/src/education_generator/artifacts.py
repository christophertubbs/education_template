"""Load and validate persistent curriculum-analysis artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ARTIFACT_FILENAMES = {
    "knowledge_map": "knowledge-map.json",
    "mastery_contracts": "mastery-contracts.json",
    "curriculum": "curriculum.json",
    "coverage": "coverage.json",
    "completion": "completion.json",
}


@dataclass(frozen=True)
class CurriculumArtifacts:
    """Validated input artifacts used to assemble one Curriculum Product."""

    knowledge_map: dict[str, Any]
    mastery_contracts: dict[str, Any]
    curriculum: dict[str, Any]
    coverage: dict[str, Any]
    completion: dict[str, Any]

    def as_product_payload(self) -> dict[str, Any]:
        """Combine analysis artifacts into the runtime import representation."""

        return {
            "knowledge_map": self.knowledge_map,
            "mastery_contracts": self.mastery_contracts["mastery_contracts"],
            **self.curriculum,
            "coverage": self.coverage["concepts"],
            "completion": self.completion,
        }


def load_artifacts(source_path: Path) -> CurriculumArtifacts:
    """Load every required JSON artifact from a curriculum source directory."""

    if not source_path.is_dir():
        raise ValueError(f"Curriculum source directory does not exist: {source_path}")
    loaded: dict[str, dict[str, Any]] = {}
    for artifact_name, filename in ARTIFACT_FILENAMES.items():
        artifact_path = source_path / filename
        if not artifact_path.is_file():
            raise ValueError(f"Missing required artifact: {artifact_path}")
        try:
            value = json.loads(artifact_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in {artifact_path}: {error}") from error
        if not isinstance(value, dict):
            raise ValueError(f"Artifact must contain a JSON object: {artifact_path}")
        loaded[artifact_name] = value
    return CurriculumArtifacts(**loaded)

