"""Load the generated __DISPLAY_NAME__ baseline into runtime models."""

import json
from importlib.resources import files

from django.db import migrations


def load_curriculum(apps, schema_editor):
    """Import packaged data without overwriting administrative overrides."""

    from education_runtime.importing import import_product_payload

    data_path = files("__APP_NAME__").joinpath("data/curriculum.json")
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    import_product_payload(payload, apps=apps, using=schema_editor.connection.alias)


def unload_curriculum(apps, schema_editor):
    """Remove this product's baseline while leaving other products intact."""

    curriculum_model = apps.get_model("education_runtime", "Curriculum")
    curriculum_model.objects.using(schema_editor.connection.alias).filter(
        identifier="__REPOSITORY_NAME__-curriculum"
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("education_runtime", "0001_initial")]
    operations = [migrations.RunPython(load_curriculum, unload_curriculum)]
