"""Load the latest packaged JSON for every installed Curriculum Product."""

from __future__ import annotations

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import DEFAULT_DB_ALIAS, connections

from education_runtime.product_loading import load_installed_product_payloads


class Command(BaseCommand):
    """Refresh generated curriculum baselines independently of migrations."""

    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        """Add the standard database selection option."""

        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            choices=tuple(connections),
            help="Database onto which the curricula will be loaded.",
        )

    def handle(self, *args: object, **options: object) -> None:
        """Import current product data and report the refreshed curricula."""

        database = str(options["database"])
        try:
            identifiers = load_installed_product_payloads(
                apps.get_app_configs(), using=database
            )
        except (OSError, ValueError) as error:
            raise CommandError(str(error)) from error
        if not identifiers:
            self.stdout.write(self.style.WARNING("No curriculum payloads found."))
            return
        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(identifiers)} curriculum payload(s): "
                f"{', '.join(identifiers)}"
            )
        )
