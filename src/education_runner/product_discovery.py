"""Discover installed Curriculum Product Django applications."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from importlib import metadata
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

PRODUCT_ENTRY_POINT_GROUP = "education_curriculum.products"
_DOTTED_IDENTIFIER = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$"
)
_PROJECT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def product_app_configuration(package_name: str) -> str:
    """Derive the conventional product AppConfig path for a legacy package."""

    if not _DOTTED_IDENTIFIER.fullmatch(package_name):
        raise ImproperlyConfigured(
            f"Invalid Curriculum Product package name: {package_name!r}"
        )
    class_name = "".join(word.capitalize() for word in package_name.split("_"))
    return f"{package_name}.apps.{class_name}Config"


def discover_product_apps(
    configured_products: str = "", repository_root: Path | None = None
) -> list[str]:
    """Return local, installed, and explicitly configured product applications.

    Local products are selected by matching directories under ``curricula`` to
    the target project recorded by each product under ``generated``. Neither a
    product directory nor its curriculum identifier needs to contain the word
    ``"curriculum"``.
    """

    products: dict[str, str] = {}
    local_products = (
        _discover_local_products(repository_root) if repository_root is not None else {}
    )
    for name, (app_configuration, _source_root) in local_products.items():
        products[name] = app_configuration

    entry_points = metadata.entry_points(group=PRODUCT_ENTRY_POINT_GROUP)
    for entry_point in sorted(entry_points, key=lambda item: (item.name, item.value)):
        app_configuration = _app_configuration_from_entry_point(
            entry_point.name, entry_point.value
        )
        existing = products.get(entry_point.name)
        if existing is not None and existing != app_configuration:
            raise ImproperlyConfigured(
                f"Conflicting Curriculum Product entry points named "
                f"{entry_point.name!r}: {existing!r} and {app_configuration!r}"
            )
        products[entry_point.name] = app_configuration

    for package_name in configured_products.split(","):
        package_name = package_name.strip()
        if not package_name:
            continue
        app_configuration = product_app_configuration(package_name)
        existing = products.get(package_name)
        if existing is not None and existing != app_configuration:
            raise ImproperlyConfigured(
                f"Conflicting Curriculum Product named {package_name!r}: "
                f"{existing!r} and {app_configuration!r}"
            )
        products[package_name] = app_configuration

    # Modify the import path only after every candidate validates so a failed
    # discovery attempt cannot leave a partially activated local product set.
    for _, source_root in local_products.values():
        source_root_text = str(source_root)
        if source_root_text not in sys.path:
            sys.path.insert(0, source_root_text)

    return [products[name] for name in sorted(products)]


def _discover_local_products(repository_root: Path) -> dict[str, tuple[str, Path]]:
    """Cross-reference reviewed curricula with locally generated products."""

    curricula_root = repository_root / "curricula"
    generated_root = repository_root / "generated"
    if not curricula_root.is_dir() or not generated_root.is_dir():
        return {}

    curriculum_projects = {
        path.name
        for path in curricula_root.iterdir()
        if path.is_dir() and not path.is_symlink()
    }
    products: dict[str, tuple[str, Path]] = {}
    matched_projects: dict[str, Path] = {}
    for product_path in sorted(generated_root.iterdir()):
        if not product_path.is_dir() or product_path.is_symlink():
            continue
        target_project = _read_target_project(product_path)
        if target_project is None or target_project not in curriculum_projects:
            continue
        existing_path = matched_projects.get(target_project)
        if existing_path is not None:
            raise ImproperlyConfigured(
                f"Generated products {existing_path.name!r} and "
                f"{product_path.name!r} both match curriculum project "
                f"{target_project!r}"
            )
        matched_projects[target_project] = product_path
        name, app_configuration = _read_local_product_entry_point(product_path)
        candidate = (app_configuration, product_path / "src")
        existing = products.get(name)
        if existing is not None and existing != candidate:
            raise ImproperlyConfigured(
                f"Conflicting local Curriculum Products named {name!r}"
            )
        products[name] = candidate
    return products


def _read_target_project(product_path: Path) -> str | None:
    """Read the target project used to cross-reference a generated product."""

    metadata_path = product_path / "provenance" / "generation.json"
    if not metadata_path.is_file():
        return None
    try:
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        target_project = payload["target_repository_name"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise ImproperlyConfigured(
            f"Invalid generated product provenance in {metadata_path}"
        ) from error
    except OSError as error:
        raise ImproperlyConfigured(f"Cannot read {metadata_path}") from error
    if not isinstance(target_project, str) or not _PROJECT_NAME.fullmatch(
        target_project
    ):
        raise ImproperlyConfigured(
            f"Invalid target project in {metadata_path}: {target_project!r}"
        )
    return target_project


def _read_local_product_entry_point(product_path: Path) -> tuple[str, str]:
    """Read and validate one generated product's package entry point."""

    configuration_path = product_path / "pyproject.toml"
    try:
        with configuration_path.open("rb") as configuration_file:
            configuration = tomllib.load(configuration_file)
        entry_points = configuration["project"]["entry-points"][
            PRODUCT_ENTRY_POINT_GROUP
        ]
    except (OSError, KeyError, TypeError, tomllib.TOMLDecodeError) as error:
        raise ImproperlyConfigured(
            f"Invalid generated product metadata in {configuration_path}"
        ) from error
    if not isinstance(entry_points, dict) or len(entry_points) != 1:
        raise ImproperlyConfigured(
            f"Generated product {product_path.name!r} must advertise exactly one "
            f"{PRODUCT_ENTRY_POINT_GROUP!r} entry point"
        )
    name, value = next(iter(entry_points.items()))
    if not isinstance(name, str) or not isinstance(value, str):
        raise ImproperlyConfigured(
            f"Invalid generated product entry point in {configuration_path}"
        )
    source_root = product_path / "src"
    if not source_root.is_dir():
        raise ImproperlyConfigured(
            f"Generated product {product_path.name!r} has no src directory"
        )
    return name, _app_configuration_from_entry_point(name, value)


def _app_configuration_from_entry_point(name: str, value: str) -> str:
    """Validate and convert a package entry point into Django dotted notation."""

    if not _DOTTED_IDENTIFIER.fullmatch(name):
        raise ImproperlyConfigured(
            f"Invalid Curriculum Product entry-point name: {name!r}"
        )
    module_name, separator, attribute_name = value.partition(":")
    if (
        separator != ":"
        or ":" in attribute_name
        or not _DOTTED_IDENTIFIER.fullmatch(module_name)
        or not _DOTTED_IDENTIFIER.fullmatch(attribute_name)
    ):
        raise ImproperlyConfigured(
            f"Invalid Curriculum Product entry-point value for {name!r}: {value!r}"
        )
    if module_name.split(".", 1)[0] != name:
        raise ImproperlyConfigured(
            f"Curriculum Product {name!r} advertises an unrelated module: "
            f"{module_name!r}"
        )
    return f"{module_name}.{attribute_name}"
