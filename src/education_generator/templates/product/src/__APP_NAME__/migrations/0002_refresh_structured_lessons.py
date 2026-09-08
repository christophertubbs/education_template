"""Refresh the generated baseline with structured lesson content."""

import json
from importlib.resources import files

from django.db import migrations


def refresh_curriculum(apps, schema_editor):
    """Import the new baseline while preserving administrative overrides."""

    from education_runtime.importing import import_product_payload

    data_path = files("__APP_NAME__").joinpath("data/curriculum.json")
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    import_product_payload(payload, apps=apps, using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [("__APP_NAME__", "0001_load_curriculum")]
    operations = [migrations.RunPython(refresh_curriculum, migrations.RunPython.noop)]
