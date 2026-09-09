"""Discover installed Curriculum Product Django applications."""

from __future__ import annotations

import re
from importlib import metadata

from django.core.exceptions import ImproperlyConfigured

PRODUCT_ENTRY_POINT_GROUP = "education_curriculum.products"
_DOTTED_IDENTIFIER = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$"
)


def product_app_configuration(package_name: str) -> str:
    """Derive the conventional product AppConfig path for a legacy package."""

    if not _DOTTED_IDENTIFIER.fullmatch(package_name):
        raise ImproperlyConfigured(
            f"Invalid Curriculum Product package name: {package_name!r}"
        )
    class_name = "".join(word.capitalize() for word in package_name.split("_"))
    return f"{package_name}.apps.{class_name}Config"


def discover_product_apps(configured_products: str = "") -> list[str]:
    """Return every advertised product plus explicitly configured legacy products."""

    products: dict[str, str] = {}
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
        products.setdefault(package_name, product_app_configuration(package_name))

    return [products[name] for name in sorted(products)]


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
