"""Create host and curriculum repositories from reusable scaffold assets."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from .constants import PACKAGE_ROOT, TEMPLATE_ROOT
from .context import GenerationContext
from .curriculum import package_curriculum
from .metadata import write_metadata
from .processes import run_process
from .rendering import copy_agent_documents, render_tree, template_tokens


def recreate_generated_root(path: Path) -> None:
    """Recreate the configured generated-output directory."""

    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def create_host_project(context: GenerationContext) -> None:
    """Create a Django host, leaving ``manage.py`` owned by Django."""

    run_process(
        [
            sys.executable,
            "-m",
            "django",
            "startproject",
            "standalone",
            str(context.generated_root),
        ]
    )
    tokens = template_tokens(context, "Generated Host Project")
    render_tree(TEMPLATE_ROOT / "host", context.generated_root, tokens)
    shutil.copy2(PACKAGE_ROOT / "launch.sh", context.generated_root / "launch.sh")
    write_metadata(
        context.generated_root / "generation_metadata.json",
        context,
        "host",
    )
    copy_agent_documents(
        context.repository_root,
        context.generated_root,
        TEMPLATE_ROOT / "agent",
        tokens,
    )


def create_curriculum_app(context: GenerationContext) -> None:
    """Render the reusable, installable curriculum app scaffold."""

    app_name = context.configuration.curriculum_app_name
    app_root = context.curriculum_repository_path
    package_root = app_root / "src" / app_name
    package_root.mkdir(parents=True)

    tokens = template_tokens(context, "Curriculum App")
    render_tree(TEMPLATE_ROOT / "curriculum", app_root, tokens)
    package_curriculum(context, package_root)
    write_metadata(app_root / "generation_metadata.json", context, "curriculum_app")
    copy_agent_documents(
        context.repository_root,
        app_root,
        TEMPLATE_ROOT / "agent",
        tokens,
    )


def generate_migrations(context: GenerationContext) -> None:
    """Ask Django to derive migration files from the rendered models."""

    source_root = context.curriculum_repository_path / "src"
    existing_python_path = os.environ.get("PYTHONPATH")
    python_path_entries = [str(source_root), str(PACKAGE_ROOT.parent)]
    if existing_python_path:
        python_path_entries.append(existing_python_path)
    python_path = os.pathsep.join(python_path_entries)
    run_process(
        [
            sys.executable,
            "-m",
            "django",
            "makemigrations",
            context.configuration.curriculum_app_name,
            "--settings=education_generator.migration_settings",
        ],
        extra_environment={
            "EDUCATION_CURRICULUM_APP": context.configuration.curriculum_app_name,
            "PYTHONPATH": python_path,
        },
        working_directory=context.repository_root,
    )
