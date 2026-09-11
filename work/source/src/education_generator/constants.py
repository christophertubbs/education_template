"""Constants shared by generator phases."""

from pathlib import Path
from typing import Final

GENERATOR_NAME: Final[str] = "education_template"
GENERATOR_VERSION: Final[str] = "1.1.0"
CURRICULUM_SCHEMA_VERSION: Final[str] = "2.1"
RUNTIME_VERSION: Final[str] = "1.1.0"
TEMPLATE_VERSION: Final[str] = "1.1.0"
PRODUCT_VERSION: Final[str] = "1.1.0"
PACKAGE_ROOT: Final[Path] = Path(__file__).resolve().parent
TEMPLATE_ROOT: Final[Path] = PACKAGE_ROOT / "templates"

