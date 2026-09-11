"""Assemble an installable Curriculum Product from validated artifacts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from .artifacts import CurriculumArtifacts
from .constants import TEMPLATE_ROOT
from .context import GenerationContext
from .metadata import build_metadata
from .rendering import copy_agent_documents, render_tree, template_tokens


def assemble_product(
    context: GenerationContext,
    artifacts: CurriculumArtifacts,
    destination: Path,
) -> None:
    """Render product packaging and persist content plus provenance."""

    package_name = context.configuration.curriculum_product_name
    package_root = destination / "src" / package_name
    render_tree(
        TEMPLATE_ROOT / "product",
        destination,
        template_tokens(context, "Curriculum Product"),
    )
    copy_agent_documents(
        context.repository_root,
        destination,
        TEMPLATE_ROOT / "agent",
        template_tokens(context, "Curriculum Product"),
    )
    product_payload = artifacts.as_product_payload()
    product_payload["metadata"] = build_metadata(context)
    data_path = package_root / "data" / "curriculum.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(product_payload, indent=2) + "\n", encoding="utf-8")
    provenance_path = destination / "provenance"
    provenance_path.mkdir(parents=True, exist_ok=True)
    _write_json(provenance_path / "generation.json", build_metadata(context))
    _write_json(provenance_path / "knowledge-map.json", artifacts.knowledge_map)
    _write_json(provenance_path / "mastery-contracts.json", artifacts.mastery_contracts)
    _write_json(provenance_path / "coverage.json", artifacts.coverage)
    _write_json(provenance_path / "completion.json", artifacts.completion)
    impact_path = context.workspace_path / "regeneration-impact.json"
    if impact_path.is_file():
        shutil.copy2(impact_path, provenance_path / "regeneration-impact.json")


def promote_staged_product(staging_path: Path, destination: Path) -> None:
    """Atomically promote staged files while preserving an existing Git directory."""

    if not destination.exists():
        staging_path.replace(destination)
        return
    for path in destination.iterdir():
        if path.name == ".git":
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    for path in staging_path.iterdir():
        shutil.move(str(path), destination / path.name)
    staging_path.rmdir()


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

