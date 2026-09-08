"""Render reusable scaffold trees from natural source files."""

from __future__ import annotations

import shutil
from pathlib import Path

from .configuration import app_config_class
from .context import GenerationContext


def template_tokens(
    context: GenerationContext,
    repository_label: str = "generated repository",
) -> dict[str, str]:
    """Return all supported scaffold substitution tokens."""

    configuration = context.configuration
    return {
        "__APP_CONFIG_CLASS__": app_config_class(configuration.curriculum_product_name),
        "__APP_NAME__": configuration.curriculum_product_name,
        "__CONFIGURED_REVISION__": configuration.revision,
        "__DISPLAY_NAME__": configuration.display_name,
        "__REPOSITORY_LABEL__": repository_label,
        "__REPOSITORY_NAME__": configuration.name,
        "__REPOSITORY_URL__": configuration.repository_url,
        "__RESOLVED_COMMIT__": context.resolved_commit,
        "__RUNTIME_COMPATIBILITY__": configuration.runtime_compatibility,
    }


def render_tree(
    source_root: Path,
    destination_root: Path,
    tokens: dict[str, str],
) -> None:
    """Render every text file in a scaffold tree, including tokenized paths."""

    for source_path in sorted(source_root.rglob("*")):
        if "__pycache__" in source_path.parts or source_path.suffix == ".pyc":
            continue
        relative_path = source_path.relative_to(source_root)
        rendered_relative = Path(
            *[_replace_tokens(part, tokens) for part in relative_path.parts]
        )
        destination_path = destination_root / rendered_relative
        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        rendered_content = _replace_tokens(
            source_path.read_text(encoding="utf-8"),
            tokens,
        )
        destination_path.write_text(rendered_content, encoding="utf-8")
        destination_path.chmod(source_path.stat().st_mode & 0o777)


def copy_agent_documents(
    repository_root: Path,
    destination: Path,
    agent_template_root: Path,
    tokens: dict[str, str],
) -> None:
    """Copy shared instructions and render generated agent state."""

    for filename in ("AGENTS.md", "SPEC.md", "STYLE.md"):
        shutil.copy2(repository_root / filename, destination / filename)
    render_tree(agent_template_root, destination / "docs" / "agent", tokens)


def _replace_tokens(value: str, tokens: dict[str, str]) -> str:
    """Replace known explicit tokens in a path component or file body."""

    rendered_value = value
    for token, replacement in tokens.items():
        rendered_value = rendered_value.replace(token, replacement)
    return rendered_value
