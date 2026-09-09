"""Load current curriculum payloads from installed Django applications."""

from __future__ import annotations

import json
from collections.abc import Iterable
from importlib.resources import files

from django.apps import AppConfig

from .importing import import_product_payload


def load_installed_product_payloads(
    app_configs: Iterable[AppConfig], *, using: str = "default"
) -> list[str]:
    """Import every packaged curriculum payload and return its stable identifier.

    Products place their assembled payload at ``data/curriculum.json``. Reading
    that resource on every installation allows content-only product updates to
    reach the database even when no new Django migration was necessary.
    """

    loaded_curricula: list[str] = []
    for app_config in sorted(app_configs, key=lambda config: config.name):
        data_path = files(app_config.name).joinpath("data/curriculum.json")
        if not data_path.is_file():
            continue
        try:
            payload = json.loads(data_path.read_text(encoding="utf-8"))
            curriculum_identifier = payload["curriculum"]["identifier"]
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ValueError(
                f"Invalid packaged curriculum payload for {app_config.name!r}"
            ) from error
        if not isinstance(curriculum_identifier, str) or not curriculum_identifier:
            raise ValueError(f"Invalid curriculum identifier for {app_config.name!r}")
        import_product_payload(payload, using=using)
        loaded_curricula.append(curriculum_identifier)
    return loaded_curricula
