"""Acquire source repositories and manage independent generated repositories."""

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
        run_process(["git", "-C", str(target_path), "fetch", "--all", "--prune"])
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

    remote_branch = run_process(
        [
            "git",
            "-C",
            str(repository_path),
            "branch",
            "--remotes",
            "--list",
            f"origin/{revision}",
        ],
        capture_output=True,
    )
    revision_expression = (
        f"origin/{revision}" if remote_branch.stdout.strip() else revision
    )
    result = run_process(
        [
            "git",
            "-C",
            str(repository_path),
            "rev-parse",
            "--verify",
            f"{revision_expression}^{{commit}}",
        ],
        capture_output=True,
    )
    return result.stdout.strip()


def checkout_resolved_revision(repository_path: Path, resolved_commit: str) -> None:
    """Put a clean Target Repository at the exact revision being analyzed."""

    ensure_clean_repository(repository_path)
    run_process(
        ["git", "-C", str(repository_path), "checkout", "--detach", resolved_commit]
    )


def initialize_generated_repository(
    repository_path: Path,
    message: str,
    branch: str = "main",
) -> None:
    """Initialize and commit a generated repository."""

    run_process(["git", "-C", str(repository_path), "init", "-b", branch])
    run_process(
        [
            "git",
            "-C",
            str(repository_path),
            "config",
            "user.name",
            "Education Generator",
        ]
    )
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


def commit_generated_update(repository_path: Path, message: str) -> None:
    """Commit a validated update using repository-local identity."""

    status = run_process(
        ["git", "-C", str(repository_path), "status", "--short"],
        capture_output=True,
    )
    if not status.stdout.strip():
        return
    run_process(["git", "-C", str(repository_path), "add", "."])
    run_process(["git", "-C", str(repository_path), "commit", "-m", message])
