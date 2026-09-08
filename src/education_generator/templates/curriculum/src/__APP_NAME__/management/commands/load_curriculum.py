"""Load packaged generated curriculum data into the configured database."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from __APP_NAME__ import services


class Command(BaseCommand):
    """Load generated curriculum into Django models."""

    help = "Load packaged generated curriculum into the database."

    def handle(self, *args, **options) -> None:
        """Execute the curriculum load command."""

        counts = services.load_packaged_curriculum()
        self.stdout.write(self.style.SUCCESS(f"Loaded curriculum: {counts}"))
