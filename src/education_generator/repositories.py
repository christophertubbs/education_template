"""Acquire target repositories and initialize generated repositories."""

from __future__ import annotations

from pathlib import Path

from .configuration import ProjectConfiguration
from .processes import run_process


def acquire_target_repository(
    repository_root: Path,
    configuration: ProjectConfiguration,
) -> Path:
    """Clone or fetch the configured target repository."""

    repository_directory = repository_root / "repository"
    repository_directory.mkdir(exist_ok=True)
    target_path = repository_directory / configuration.name
    if target_path.exists():
        ensure_clean_repository(target_path)
        run_process(["git", "-C", str(target_path), "fetch", "--all"])
        return target_path

    run_process(["git", "clone", configuration.repository_url, str(target_path)])
    return target_path


def ensure_clean_repository(repository_path: Path) -> None:
    """Reject a target checkout containing local modifications."""

    status = run_process(
        ["git", "-C", str(repository_path), "status", "--short"],
        capture_output=True,
    )
    if status.stdout.strip():
        raise RuntimeError(
            f"Target repository has local modifications:\n{status.stdout}"
        )


def resolve_revision(repository_path: Path, revision: str) -> str:
    """Resolve a configured revision to an exact commit hash."""

    result = run_process(
        ["git", "-C", str(repository_path), "rev-parse", revision],
        capture_output=True,
    )
    return result.stdout.strip()


def initialize_generated_repository(repository_path: Path, message: str) -> None:
    """Initialize and commit a generated repository."""

    run_process(["git", "-C", str(repository_path), "init", "-b", "main"])
    run_process([
        "git",
        "-C",
        str(repository_path),
        "config",
        "user.name",
        "Education Generator",
    ])
    run_process(
        [
            "git",
            "-C",
            str(repository_path),
            "config",
            "user.email",
            "education-generator@example.invalid",
        ]
    )
    run_process(["git", "-C", str(repository_path), "add", "."])
    run_process(["git", "-C", str(repository_path), "commit", "-m", message])


def ignore_nested_curriculum_repository(
    host_repository_path: Path,
    curriculum_directory_name: str,
) -> None:
    """Locally exclude a new nested app without changing tracked host files."""

    exclude_path = host_repository_path / ".git" / "info" / "exclude"
    exclusion = f"/{curriculum_directory_name}/"
    existing_lines = exclude_path.read_text(encoding="utf-8").splitlines()
    if exclusion in existing_lines:
        return
    with exclude_path.open("a", encoding="utf-8") as exclude_file:
        if existing_lines and existing_lines[-1]:
            exclude_file.write("\n")
        exclude_file.write(f"{exclusion}\n")
