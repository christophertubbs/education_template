"""Generate the standalone education project and reusable curriculum app."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from textwrap import dedent
from typing import Final


GENERATOR_NAME: Final[str] = "education_template"
GENERATOR_VERSION: Final[str] = "0.1.0"
CURRICULUM_SCHEMA_VERSION: Final[str] = "1.0"
TEMPLATE_VERSION: Final[str] = "0.1.0"


@dataclass(frozen=True)
class ProjectConfiguration:
    """Validated project configuration loaded from ``project.json``."""

    repository_url: str
    """Git URL for the target repository."""

    name: str
    """Filesystem-safe target repository name."""

    revision: str
    """Configured target repository revision."""

    curriculum_app_name: str
    """Python package name for the generated curriculum app."""

    display_name: str
    """Human-readable curriculum display name."""

    curriculum_content_path: Path | None
    """Optional path to repository-specific curriculum content JSON."""


@dataclass(frozen=True)
class GenerationContext:
    """Resolved paths and provenance used during generation."""

    repository_root: Path
    """Root of the generator repository."""

    configuration: ProjectConfiguration
    """Validated project configuration."""

    target_repository_path: Path
    """Local checkout path for the target repository."""

    resolved_commit: str
    """Exact target repository commit used as curriculum provenance."""

    generated_root: Path
    """Path to the generated standalone Django host project."""

    curriculum_repository_path: Path
    """Path to the generated independent curriculum app repository."""

    generated_at: str
    """UTC generation timestamp in ISO 8601 format."""


def main() -> None:
    """Run the command-line generator."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        default="project.json",
        help="Path to the project configuration JSON file.",
    )
    arguments = parser.parse_args()

    repository_root = Path.cwd()
    configuration = load_project_configuration(repository_root / arguments.project)
    target_repository_path = acquire_target_repository(repository_root, configuration)
    resolved_commit = resolve_revision(target_repository_path, configuration.revision)
    generated_root = repository_root / "generated" / "education"
    curriculum_repository_path = generated_root / configuration.name
    context = GenerationContext(
        repository_root=repository_root,
        configuration=configuration,
        target_repository_path=target_repository_path,
        resolved_commit=resolved_commit,
        generated_root=generated_root,
        curriculum_repository_path=curriculum_repository_path,
        generated_at=datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
    )

    recreate_directory(generated_root)
    create_host_project(context)
    create_curriculum_app(context)
    initialize_generated_repository(
        curriculum_repository_path,
        "Initial generated curriculum app",
    )
    initialize_generated_repository(generated_root, "Initial generated host project")


def load_project_configuration(configuration_path: Path) -> ProjectConfiguration:
    """Load and validate project configuration.

    :param configuration_path: Path to ``project.json``.
    :return: Validated configuration values.
    :raises ValueError: If required values are absent or unsafe.
    """

    raw_configuration = json.loads(configuration_path.read_text())
    required_fields = (
        "repository_url",
        "name",
        "revision",
        "curriculum_app_name",
        "display_name",
    )
    missing_fields = [
        field for field in required_fields if not raw_configuration.get(field)
    ]
    if missing_fields:
        raise ValueError(f"Missing required project fields: {missing_fields}")

    name = str(raw_configuration["name"])
    curriculum_app_name = str(raw_configuration["curriculum_app_name"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        raise ValueError(f"Unsafe repository name: {name!r}")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", curriculum_app_name):
        raise ValueError(f"Invalid Python package name: {curriculum_app_name!r}")

    return ProjectConfiguration(
        repository_url=str(raw_configuration["repository_url"]),
        name=name,
        revision=str(raw_configuration["revision"]),
        curriculum_app_name=curriculum_app_name,
        display_name=str(raw_configuration["display_name"]),
        curriculum_content_path=optional_path(
            configuration_path.parent,
            raw_configuration.get("curriculum_content_path"),
        ),
    )


def optional_path(base_path: Path, raw_path: object) -> Path | None:
    """Resolve an optional configuration path relative to ``project.json``.

    :param base_path: Directory containing the project configuration file.
    :param raw_path: Optional path value from configuration.
    :return: Resolved path, or ``None`` when not configured.
    :raises ValueError: If the configured path is not a string.
    """

    if raw_path in (None, ""):
        return None
    if not isinstance(raw_path, str):
        raise ValueError("curriculum_content_path must be a string when provided")
    return (base_path / raw_path).resolve()


def app_config_class(app_name: str) -> str:
    """Return a conventional Django ``AppConfig`` class name.

    :param app_name: Valid Python package name for the generated app.
    :return: PascalCase application configuration class name.
    """

    words = [word for word in app_name.split("_") if word]
    return "".join(word.capitalize() for word in words) + "Config"


def acquire_target_repository(
    repository_root: Path,
    configuration: ProjectConfiguration,
) -> Path:
    """Clone or update the configured target repository.

    :param repository_root: Generator repository root.
    :param configuration: Validated project configuration.
    :return: Local target repository checkout path.
    :raises RuntimeError: If the checkout has local modifications.
    """

    repository_directory = repository_root / "repository"
    repository_directory.mkdir(exist_ok=True)
    target_repository_path = repository_directory / configuration.name

    if target_repository_path.exists():
        ensure_clean_repository(target_repository_path)
        run_process(["git", "-C", str(target_repository_path), "fetch", "--all"])
        return target_repository_path

    run_process(
        [
            "git",
            "clone",
            configuration.repository_url,
            str(target_repository_path),
        ]
    )
    return target_repository_path


def ensure_clean_repository(repository_path: Path) -> None:
    """Raise an error when the target checkout has local modifications.

    :param repository_path: Git checkout to inspect.
    :raises RuntimeError: If tracked or untracked changes are present.
    """

    status = run_process(
        ["git", "-C", str(repository_path), "status", "--short"],
        capture_output=True,
    )
    if status.stdout.strip():
        raise RuntimeError(
            f"Target repository has local modifications:\n{status.stdout}"
        )


def resolve_revision(repository_path: Path, revision: str) -> str:
    """Resolve a configured revision to an exact commit hash.

    :param repository_path: Target repository checkout.
    :param revision: Configured branch, tag, or commit.
    :return: Exact commit hash.
    """

    result = run_process(
        ["git", "-C", str(repository_path), "rev-parse", revision],
        capture_output=True,
    )
    return result.stdout.strip()


def create_host_project(context: GenerationContext) -> None:
    """Create the standalone Django host project.

    :param context: Generation context and provenance.
    """

    configuration = context.configuration
    generated_root = context.generated_root
    write_file(
        generated_root / ".gitignore",
        f"/db.sqlite3\n/staticfiles/\n/{configuration.name}/\n",
    )
    write_file(
        generated_root / "pyproject.toml",
        f"""
        [build-system]
        requires = ["setuptools>=70"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "education-host"
        version = "0.1.0"
        description = "Standalone Django host for generated curriculum apps"
        requires-python = ">=3.12"
        dependencies = [
            "Django>=5.0,<6.0",
        ]

        [tool.setuptools.packages.find]
        include = ["standalone*"]
        """,
    )
    write_file(
        generated_root / "manage.py",
        f"""
        #!/usr/bin/env python
        \"\"\"Run Django administrative commands for the generated host.\"\"\"

        from __future__ import annotations

        import os
        import sys
        from pathlib import Path


        def main() -> None:
            \"\"\"Execute Django's command-line utility.\"\"\"

            host_root = Path(__file__).resolve().parent
            app_source = host_root / "{configuration.name}" / "src"
            if app_source.exists():
                sys.path.insert(0, str(app_source))

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "standalone.settings")
            from django.core.management import execute_from_command_line

            execute_from_command_line(sys.argv)


        if __name__ == "__main__":
            main()
        """,
    )
    os.chmod(generated_root / "manage.py", 0o755)
    write_file(generated_root / "standalone" / "__init__.py", "")
    write_file(
        generated_root / "standalone" / "settings.py",
        f"""
        \"\"\"Django settings for the generated standalone education host.\"\"\"

        from __future__ import annotations

        from pathlib import Path


        BASE_DIR = Path(__file__).resolve().parent.parent
        SECRET_KEY = "generated-development-only-secret-key"
        DEBUG = True
        ALLOWED_HOSTS = ["*"]

        INSTALLED_APPS = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "{configuration.curriculum_app_name}",
        ]

        MIDDLEWARE = [
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]

        ROOT_URLCONF = "standalone.urls"
        TEMPLATES = [
            {{
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR / "templates"],
                "APP_DIRS": True,
                "OPTIONS": {{
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                }},
            }}
        ]
        WSGI_APPLICATION = "standalone.wsgi.application"

        DATABASES = {{
            "default": {{
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }}
        }}

        LANGUAGE_CODE = "en-us"
        TIME_ZONE = "UTC"
        USE_I18N = True
        USE_TZ = True
        STATIC_URL = "static/"
        STATIC_ROOT = BASE_DIR / "staticfiles"
        DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
        """,
    )
    write_file(
        generated_root / "standalone" / "urls.py",
        f"""
        \"\"\"Root URL configuration for the generated standalone host.\"\"\"

        from __future__ import annotations

        from django.contrib import admin
        from django.shortcuts import redirect
        from django.urls import include, path


        urlpatterns = [
            path("", lambda request: redirect("{configuration.curriculum_app_name}:index")),
            path("admin/", admin.site.urls),
            path("{configuration.name}/", include("{configuration.curriculum_app_name}.urls")),
        ]
        """,
    )
    write_file(
        generated_root / "standalone" / "asgi.py",
        """
        \"\"\"ASGI entry point for the generated standalone host.\"\"\"

        from __future__ import annotations

        import os

        from django.core.asgi import get_asgi_application


        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "standalone.settings")
        application = get_asgi_application()
        """,
    )
    write_file(
        generated_root / "standalone" / "wsgi.py",
        """
        \"\"\"WSGI entry point for the generated standalone host.\"\"\"

        from __future__ import annotations

        import os

        from django.core.wsgi import get_wsgi_application


        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "standalone.settings")
        application = get_wsgi_application()
        """,
    )
    write_file(
        generated_root / "templates" / "base.html",
        f"""
        {{% load static %}}
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{{% block title %}}Education{{% endblock %}}</title>
            <link rel="stylesheet" href="{{% static '{configuration.curriculum_app_name}/css/curriculum.css' %}}">
            <script defer src="{{% static '{configuration.curriculum_app_name}/js/progress.js' %}}"></script>
        </head>
        <body>
            <header class="site-header">
                <a class="brand" href="{{% url '{configuration.curriculum_app_name}:index' %}}">{configuration.display_name} Curriculum</a>
                <nav aria-label="Primary">
                    <a href="{{% url '{configuration.curriculum_app_name}:index' %}}">Lessons</a>
                    <a href="{{% url '{configuration.curriculum_app_name}:glossary' %}}">Glossary</a>
                    <a href="{{% url '{configuration.curriculum_app_name}:progress' %}}">Progress</a>
                    <a href="/admin/">Admin</a>
                </nav>
            </header>
            <main class="page-shell">
                {{% block content %}}{{% endblock %}}
            </main>
        </body>
        </html>
        """,
    )
    write_file(generated_root / "generation_metadata.json", metadata_json(context, "host"))
    write_file(generated_root / "README.md", host_readme(context))
    copy_agent_docs(context.repository_root, generated_root, "Generated Host Project")


def create_curriculum_app(context: GenerationContext) -> None:
    """Create the reusable curriculum app repository.

    :param context: Generation context and provenance.
    """

    app_name = context.configuration.curriculum_app_name
    app_root = context.curriculum_repository_path
    package_root = app_root / "src" / app_name
    app_config_class_name = app_config_class(app_name)
    write_file(
        app_root / "pyproject.toml",
        f"""
        [build-system]
        requires = ["setuptools>=70"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "{app_name}-education"
        version = "0.1.0"
        description = "Reusable Django curriculum app for {context.configuration.display_name}"
        requires-python = ">=3.12"
        dependencies = [
            "Django>=5.0,<6.0",
        ]

        [tool.setuptools.packages.find]
        where = ["src"]

        [tool.setuptools.package-data]
        "{app_name}" = [
            "data/*.json",
            "templates/{app_name}/*.html",
            "static/{app_name}/css/*.css",
            "static/{app_name}/js/*.js",
        ]
        """,
    )
    write_file(package_root / "__init__.py", "")
    write_file(
        package_root / "apps.py",
        f"""
        \"\"\"Django application configuration for the generated curriculum.\"\"\"

        from __future__ import annotations

        from django.apps import AppConfig


        class {app_config_class_name}(AppConfig):
            \"\"\"Configure the {context.configuration.display_name} curriculum Django application.\"\"\"

            default_auto_field = "django.db.models.BigAutoField"
            name = "{app_name}"
            verbose_name = "{context.configuration.display_name} Curriculum"
        """,
    )
    write_file(package_root / "models.py", models_py())
    write_file(package_root / "admin.py", admin_py())
    write_file(package_root / "services.py", services_py(app_name))
    write_file(package_root / "views.py", views_py(app_name))
    write_file(package_root / "urls.py", urls_py(app_name))
    write_file(
        package_root / "management" / "__init__.py",
        "",
    )
    write_file(
        package_root / "management" / "commands" / "__init__.py",
        "",
    )
    write_file(
        package_root / "management" / "commands" / "load_curriculum.py",
        load_curriculum_py(app_name),
    )
    write_file(package_root / "migrations" / "__init__.py", "")
    write_file(package_root / "migrations" / "0001_initial.py", migration_py(app_name))
    write_file(
        package_root / "data" / "curriculum.json",
        json.dumps(build_curriculum(context), indent=2) + "\n",
    )
    write_file(
        package_root / "templates" / app_name / "index.html",
        template_index(app_name, context.configuration.display_name),
    )
    write_file(
        package_root / "templates" / app_name / "lesson.html",
        template_lesson(app_name),
    )
    write_file(
        package_root / "templates" / app_name / "assessment.html",
        template_assessment(),
    )
    write_file(
        package_root / "templates" / app_name / "glossary.html",
        template_glossary(),
    )
    write_file(
        package_root / "templates" / app_name / "progress.html",
        template_progress(),
    )
    write_file(
        package_root / "static" / app_name / "css" / "curriculum.css",
        curriculum_css(),
    )
    write_file(
        package_root / "static" / app_name / "js" / "progress.js",
        progress_js(app_name),
    )
    write_file(app_root / "generation_metadata.json", metadata_json(context, "curriculum_app"))
    write_file(app_root / "README.md", curriculum_readme(context))
    copy_agent_docs(context.repository_root, app_root, "Curriculum App")


def build_curriculum(context: GenerationContext) -> dict[str, object]:
    """Build deterministic curriculum content for the target repository.

    :param context: Generation context and provenance.
    :return: Structured curriculum data suitable for database loading.
    """

    if context.configuration.curriculum_content_path is not None:
        return load_curriculum_content(context)

    commit = context.resolved_commit
    repository_url = context.configuration.repository_url
    source_repository_url = repository_url.removesuffix(".git")
    source_prefix = f"{source_repository_url}/blob/{commit}"
    lessons = [
        lesson(
            "lstm-purpose",
            "1",
            "Purpose, Scope, and Evidence",
            "The repository packages a Long Short-Term Memory hydrologic model behind BMI so NextGen can drive it like another model component.",
            [
                "The `lstm` repository is a Python package for streamflow prediction with a Long Short-Term Memory neural network. Its README identifies the model as a BMI-enabled component developed for the Next Generation Water Resources Modeling Framework. That means the package is not only a standalone Python model; it is meant to be driven by an external model framework that calls a standard set of lifecycle, time, variable, and grid methods.",
                "The package metadata in `pyproject.toml` names the distribution `lstm`, describes it as a hydrologic model based on the Long Short-Term Memory algorithm, and declares runtime dependencies on `bmipy`, `numpy`, `pandas`, `pyyml`, and `torch`. Those dependencies reveal the major implementation concerns: BMI interoperability, array-based variable exchange, tabular/time handling, YAML configuration, and PyTorch inference.",
                "The repository includes example data and trained model artifacts. The README names forcing data in `data/usgs-streamflow-nldas_hourly.nc`, basin attributes under `data/camels_attributes_v2.0`, BMI YAML examples under `bmi_config_files`, and trained NeuralHydrology model files under `trained_neuralhydrology_models`. A developer changing or diagnosing the package needs to distinguish source code from these runtime inputs because an apparently code-level failure may actually be caused by a missing or mismatched configuration, scaler, weight file, or forcing variable.",
                "The repository is scoped to inference and coupling, not general LSTM training. The README explains that the forward pass in `nextgen_cuda_lstm.py` is based on NeuralHydrology's `CudaLSTM`, and `bmi_lstm.py` is responsible for loading the trained model into the BMI component. If a different model class is used, the BMI wrapper would need to be changed to load it.",
            ],
            [
                source("README.md", 1, 27, f"{source_prefix}/README.md"),
                source("README.md", 29, 64, f"{source_prefix}/README.md"),
                source("pyproject.toml", 1, 36, f"{source_prefix}/pyproject.toml"),
            ],
        ),
        lesson(
            "bmi-contract",
            "2",
            "BMI as the Integration Boundary",
            "BMI gives the LSTM a stable model-control and variable-access interface for frameworks such as NextGen.",
            [
                "`BmiBase` subclasses `bmipy.Bmi` and provides placeholder implementations for BMI grid methods that this component does not specialize. The decorator `raise_not_implemented` wraps a BMI method so calling an unsupported method raises `NotImplementedError` with the wrapped function's name. A caller therefore gets a clear failure such as `get_grid_shape` rather than a silent placeholder result.",
                "`bmi_LSTM` is the concrete BMI component. Its model-control methods are `initialize`, `update`, `update_until`, and `finalize`. `get_component_name` returns the string `LSTM`. `get_input_item_count` returns the number of dynamic input variables, while `get_output_item_count` returns the number of output variables. These are framework-facing answers, so they must describe what the BMI exposes rather than every internal tensor in the PyTorch model.",
                "The input variable names exposed over BMI are the eight dynamic forcing names in `_dynamic_input_vars`: longwave radiation, air pressure, relative saturation, precipitation rate, shortwave radiation, air temperature, wind x velocity, and wind y velocity. The output variable names exposed over BMI are `land_surface_water__runoff_volume_flux` and `land_surface_water__runoff_depth`.",
                "The repository keeps two name maps. `INTERNAL_NAME_CROSSWALK` maps trained-model feature names such as `APCP_surface` and `TMP_2maboveground` to BMI names such as `atmosphere_water__liquid_equivalent_precipitation_rate` and `land_surface_air__temperature`. `EXTERNAL_NAME_CROSSWALK` reverses that map. `crosswalk_to_external(name)` returns the BMI name for an internal name; `crosswalk_to_interal(name)` returns the internal name for a BMI name. The misspelling in `crosswalk_to_interal` is present in the source and matters when searching or calling it.",
                "The variable metadata methods are deliberately small. `get_var_grid(name)` validates the name and returns grid id `0`. `get_var_type(name)` returns the dtype name from `get_value_ptr(name)`. `get_var_units(name)` returns the stored unit from the first state container that contains the name. `get_var_itemsize(name)` returns the numpy element size, and `get_var_nbytes(name)` multiplies item size by array length. `get_var_location(name)` returns `node` after validating that the variable exists.",
                "The grid methods implemented by `bmi_LSTM` describe scalar behavior. `get_grid_rank(0)` returns `1`, `get_grid_size(0)` returns `1`, and `get_grid_type(0)` returns `scalar`. Passing a grid id other than `0` raises a runtime error that says only grid `0` is supported.",
            ],
            [
                source("lstm/base.py", 1, 44, f"{source_prefix}/lstm/base.py"),
                source("lstm/bmi_lstm.py", 44, 96, f"{source_prefix}/lstm/bmi_lstm.py"),
                source("lstm/bmi_lstm.py", 342, 487, f"{source_prefix}/lstm/bmi_lstm.py"),
            ],
        ),
        lesson(
            "state-containers",
            "3",
            "State, Variables, and In-Place Mutation",
            "The BMI wrapper uses small state containers to hold named numpy arrays for dynamic inputs, static attributes, and outputs.",
            [
                "`Var` is the smallest state unit in `model_state.py`. It is a dataclass with three fields: `name`, `unit`, and `value`. The value is a numpy array, not a Python scalar, because BMI getter and setter operations work with caller-provided arrays and references.",
                "`State.__init__` receives an iterable of `Var` objects and builds `_name_mapping`, a dictionary from variable name to `Var`. `unit(name)` returns the stored unit string. `value(name)` returns the actual numpy array object stored in the `Var`. The tests verify that `state.value(var.name)` is the same object as `var.value`, so code that receives that reference must understand it is working with live BMI state.",
                "`value_at_indices(name, dest, indices)` copies selected values from the stored source array into `dest` and returns `dest`. The source and destination arrays should not share memory after that operation. `set_value(name, value)` mutates the stored array in place by assigning into `[:]`. `set_value_at_indices(name, inds, src)` mutates selected stored positions from `src`.",
                "`names()` yields variable names, `vars()` yields `Var` instances, `__contains__` checks whether a name exists, `__iter__` iterates over variables, and `__len__` returns the number of mapped variables. These container methods are covered by `tests/test_model_state.py` because framework code depends on predictable container behavior.",
                "`StateFacade` accepts multiple `State` instances and presents them through the same `unit`, `value`, `value_at_indices`, setter, `names`, and `vars` methods. In `bmi_LSTM.update`, it combines dynamic inputs and static attributes so an `EnsembleMember` can request all required model features without caring which state container owns them.",
                "`state_proxy` is the helper behind `StateFacade`. It attempts the requested `State` method against each contained state until one succeeds. If every state raises an exception, it raises a `RuntimeError` containing the collected errors. This behavior is useful for missing variable names, but it also means broad exceptions inside a state method can be wrapped, so debugging should inspect the original collected errors.",
            ],
            [
                source("lstm/model_state.py", 19, 131, f"{source_prefix}/lstm/model_state.py"),
                source("tests/test_model_state.py", 29, 88, f"{source_prefix}/tests/test_model_state.py"),
            ],
        ),
        lesson(
            "configuration-and-scaling",
            "4",
            "Configuration, Feature Scaling, and Units",
            "Configuration files connect basin attributes, forcing variables, trained model metadata, and unit conversions.",
            [
                "`bmi_LSTM.initialize(config_file)` opens the supplied YAML configuration file, loads it with PyYAML's safe loader, and calls `coerce_config`. The `coerce_config` function converts `train_cfg_file` into a list of `Path` objects, converts other keys ending in `_dir`, `_path`, `_file`, or `_files` to paths, and parses keys ending in `_date` as pandas datetimes using day/month/year formatting.",
                "After configuration coercion, `initialize` computes `output_factor_cms`. The formula applies millimeters-to-meters, basin area in square kilometers to square meters, and hours to seconds: `(1 / 1000) * (area_sqkm * 1000 * 1000) * (1 / 3600)`. That factor is later used to convert a depth-like runoff prediction into a volume flux in cubic meters per second.",
                "For each configured training file, `initialize` loads the training configuration and creates an `EnsembleMember`. The `EnsembleMember` loads `train_data/train_data_scaler.yml`, calls `load_training_scalars`, initializes a PyTorch LSTM, and records `input_names` as dynamic inputs followed by static attributes. That order matters because it must match the feature order used during training.",
                "`load_training_scalars(cfg, train_data_scalar)` returns a `TrainingScalars` dataclass with four values: `input_mean`, `input_std`, `output_mean`, and `output_std`. `input_mean` and `input_std` are built by reading configured dynamic input variables from xarray scaler metadata and configured static attributes from attribute scaler metadata. `output_mean` and `output_std` come from the configured target variable.",
                "`gather_inputs(state, internal_input_names)` walks the configured internal names, converts each to a BMI name with `crosswalk_to_external`, reads the state value, asserts that the value is a single scalar in a one-dimensional array, and returns a float64 numpy array. `scale_inputs(input, mean, std)` then computes `(input - mean) / std` so the inference tensor is on the scale expected by the trained network.",
                "`scale_outputs(cfg, output, output_mean, output_std, output_scale_factor_cms)` reverses output normalization. If the target variable is hourly runoff in millimeters, it applies standard deviation and mean directly. If the target variable is daily runoff, it divides by 24 to produce an hourly value. It clamps negative runoff to zero, creates runoff depth in meters, and yields two `Var` objects: runoff depth in `m` and runoff volume flux in `m3 s-1`.",
            ],
            [
                source("bmi_config_files/README.md", 1, 44, f"{source_prefix}/bmi_config_files/README.md"),
                source("lstm/bmi_lstm.py", 178, 259, f"{source_prefix}/lstm/bmi_lstm.py"),
                source("lstm/bmi_lstm.py", 282, 340, f"{source_prefix}/lstm/bmi_lstm.py"),
            ],
        ),
        lesson(
            "lstm-inference",
            "5",
            "PyTorch LSTM Inference",
            "The repository reuses trained NeuralHydrology-style weights for one-step forward prediction, not training.",
            [
                "`Nextgen_CudaLSTM` is a small PyTorch module. Its constructor receives `input_size`, `hidden_layer_size`, `output_size`, `batch_size`, and `seq_length`. It stores those values, creates `self.lstm = nn.LSTM(self.input_size, self.hidden_layer_size)`, and creates `self.head = nn.Linear(self.hidden_layer_size, self.output_size)`.",
                "`Nextgen_CudaLSTM.forward(input_layer, h_t, c_t)` casts the hidden state, cell state, and input layer to float tensors. It reshapes `input_layer` with `view(self.seq_length, self.batch_size, self.input_size)`, runs `self.lstm(input_view, (h_t, c_t))`, sends the LSTM output through the linear head, and returns a three-item tuple: `prediction`, updated `h_t`, and updated `c_t`.",
                "`initialize_lstm(cfg)` calculates `input_size` as the number of dynamic inputs plus static attributes, uses `cfg['hidden_size']` as the hidden layer size, and sets `output_size` to the number of configured target variables. It constructs `Nextgen_CudaLSTM` with `batch_size=1` and `seq_length=1`, so the BMI wrapper is doing stepwise inference for one catchment state at a time.",
                "The trained model path is built as `cfg['run_dir'] / 'model_epochNNN.pt'`, where `NNN` is the configured epoch padded to three digits. The function loads that PyTorch state dictionary on CPU. Because NeuralHydrology names the head weights differently, it renames `head.net.0.weight` to `head.weight` and `head.net.0.bias` to `head.bias` before loading the state into the local model.",
                "`EnsembleMember.__init__` initializes `h_t` and `c_t` as zero float tensors with shape `(1, batch_size, hidden_layer_size)`. `EnsembleMember.update(state)` gathers and scales inputs, runs `self.lstm.forward(input_tensor, self.h_t, self.c_t)`, stores the returned hidden and cell tensors back on the ensemble member, and yields scaled output variables. The preserved hidden and cell tensors are what make repeated `update` calls recurrent instead of independent.",
            ],
            [
                source("lstm/nextgen_cuda_lstm.py", 1, 26, f"{source_prefix}/lstm/nextgen_cuda_lstm.py"),
                source("lstm/bmi_lstm.py", 121, 176, f"{source_prefix}/lstm/bmi_lstm.py"),
                source("lstm/bmi_lstm.py", 248, 280, f"{source_prefix}/lstm/bmi_lstm.py"),
            ],
        ),
        lesson(
            "runtime-lifecycle",
            "6",
            "Runtime Lifecycle and NextGen Use",
            "A host framework initializes the component, sets forcing values, advances timesteps, reads runoff outputs, and finalizes the component.",
            [
                "The README's BMI usage sequence is: create `model = lstm.bmi_LSTM()`, read or provide the BMI configuration file, call `model.initialize(...)`, call `model.update()` for one timestep or `model.update_until(model.iend)` for multiple timesteps, and finally call `model.finalize()`. In the current source, `finalize` is an empty method, so cleanup is effectively a no-op.",
                "`bmi_LSTM.update()` creates a `StateFacade` over dynamic inputs and static inputs. It then loops over each `EnsembleMember`, collects each yielded output `Var`, checks that each output array has length one, groups output values by output name, averages them with `np.mean(..., dtype='float64')`, writes the average into `_outputs`, and increments `_timestep` by one.",
                "Time methods are fixed around an hourly timestep. `_timestep_size_s` is `3600`. `get_current_time()` returns `_timestep * _timestep_size_s`. `get_start_time()` returns `0`. `get_end_time()` returns the maximum float64 value. `get_time_units()` returns `s`, and `get_time_step()` returns `3600`.",
                "`update_until(time)` compares the requested time with `get_current_time()`. If the requested time is not greater than the current time, it logs a warning and returns without updating. Otherwise it divides the remaining time by `get_time_step()`. If the requested time is not an exact multiple of the timestep, it logs a warning and advances only the whole number of timesteps.",
                "The NextGen documentation in `doc/How_to_Run_LSTM_in_NextGen.txt` describes a realization file that uses formulation name `bmi_python`, sets `python_type` to the BMI class path, sets `model_type_name` to `bmi_LSTM`, points `init_config` at an LSTM YAML file, and sets `main_output_variable` to `land_surface_water__runoff_volume_flux`.",
                "The repository examples distinguish forcing data from BMI state. The test code maps NetCDF forcing variable names such as `total_precipitation`, `temperature`, `pressure`, and `wind_u` onto BMI variable names before each call to `update`. A framework integration problem often comes down to one of those names, units, or timesteps not matching the trained model and BMI configuration.",
            ],
            [
                source("README.md", 85, 120, f"{source_prefix}/README.md"),
                source("lstm/bmi_lstm.py", 352, 390, f"{source_prefix}/lstm/bmi_lstm.py"),
                source("doc/How_to_Run_LSTM_in_NextGen.txt", 80, 123, f"{source_prefix}/doc/How_to_Run_LSTM_in_NextGen.txt"),
            ],
        ),
        lesson(
            "testing-debugging-limitations",
            "7",
            "Testing, Debugging, and Known Limits",
            "The test suite verifies state semantics and a one-member NLDAS configuration, while repository docs call out dependency and path assumptions.",
            [
                "`tests/test_model_state.py` is focused on the reusable state container semantics. It constructs `Var` records, checks `State` length and iteration order, verifies that `State.value` returns a reference, verifies that `value_at_indices` copies into the destination array, and verifies that both setter methods mutate the stored array. These tests protect BMI data exchange behavior without loading PyTorch weights.",
                "`tests/integration_test.py` exercises a one-member NLDAS configuration for basin `02064000`. It opens `bmi_config_files/02064000_nh_NLDAS_hourly.yml`, reads `data/usgs-streamflow-nldas_hourly.nc` with netCDF4, finds the basin index, sets eight forcing variables on the model for each timestep, calls `update`, reads `land_surface_water__runoff_depth`, converts meters to millimeters per hour, and compares 24 expected values.",
                "The integration test's forcing map is operationally important. It maps `total_precipitation` to `atmosphere_water__liquid_equivalent_precipitation_rate`, `temperature` to `land_surface_air__temperature`, `longwave_radiation` to longwave flux, `shortwave_radiation` to shortwave flux, `pressure` to air pressure, `specific_humidity` to relative saturation, and `wind_u`/`wind_v` to the x and y wind components.",
                "The README documents dependency-sensitive behavior. It says the environment uses libraries listed in `environment.yml`, calls out an `xarray` version constraint because newer versions are incompatible with current example files, and notes an OpenMP issue on some Mac Anaconda releases involving `libiomp5.dylib` and `libomp.dylib`.",
                "`PACKAGE.md` adds another important packaging note: the package uses files from `bmi_config_files`, `data`, and `trained_neuralhydrology_models`, but those were not placed inside the `lstm` package directory at that time. A packaging or deployment change must account for these runtime resources instead of assuming `import lstm` is enough.",
                "The NextGen run notes document path assumptions for model configuration. If LSTM is run from the top level of an `ngen` checkout, YAML paths such as `./trained_neuralhydrology_models/.../config.yml` may need to be rewritten or supported with a symlink from the `ngen` working directory. A failure to load scaler or weight files can therefore be caused by current working directory, not by the neural-network code itself.",
            ],
            [
                source("tests/integration_test.py", 16, 88, f"{source_prefix}/tests/integration_test.py"),
                source("README.md", 65, 84, f"{source_prefix}/README.md"),
                source("PACKAGE.md", 80, 116, f"{source_prefix}/PACKAGE.md"),
                source("doc/How_to_Run_LSTM_in_NextGen.txt", 24, 47, f"{source_prefix}/doc/How_to_Run_LSTM_in_NextGen.txt"),
            ],
        ),
    ]
    glossary = [
        glossary_entry("bmi", "Basic Model Interface", "A standardized API that lets a framework initialize, update, inspect, and exchange variables with a model component."),
        glossary_entry("nextgen", "NextGen", "NOAA's Next Generation Water Resources Modeling Framework, which can drive BMI-enabled model formulations."),
        glossary_entry("lstm", "Long Short-Term Memory", "A recurrent neural-network architecture that keeps hidden and cell state across sequential inputs."),
        glossary_entry("forcing", "Forcing Data", "Time-varying environmental inputs, such as precipitation, temperature, radiation, pressure, humidity, and wind."),
        glossary_entry("static-attributes", "Static Basin Attributes", "Catchment properties such as area, mean elevation, and slope that do not vary each timestep."),
        glossary_entry("camels", "CAMELS", "A hydrology dataset used for catchment attributes and meteorology in the repository examples."),
        glossary_entry("runoff-volume-flux", "Runoff Volume Flux", "The BMI output `land_surface_water__runoff_volume_flux`, expressed in cubic meters per second."),
        glossary_entry("runoff-depth", "Runoff Depth", "The BMI output `land_surface_water__runoff_depth`, expressed in meters after millimeter-to-meter conversion."),
        glossary_entry("ensemble-member", "Ensemble Member", "A wrapper around one trained LSTM model, its scalers, and recurrent hidden/cell tensors."),
        glossary_entry("source-provenance", "Source Provenance", "The exact commit, file, and line evidence supporting a curriculum claim."),
    ]
    assessments = [
        assessment("quiz-lstm-purpose", "section", "Purpose and Package Quiz", ["lstm-purpose"], 0, 3),
        assessment("quiz-bmi-contract", "section", "BMI Contract Quiz", ["bmi-contract"], 0, 3),
        assessment("quiz-state-containers", "section", "State Container Quiz", ["state-containers"], 0, 3),
        assessment("quiz-configuration-and-scaling", "section", "Configuration and Scaling Quiz", ["configuration-and-scaling"], 0, 3),
        assessment("quiz-lstm-inference", "section", "PyTorch LSTM Inference Quiz", ["lstm-inference"], 0, 3),
        assessment("quiz-runtime-lifecycle", "section", "Runtime Lifecycle Quiz", ["runtime-lifecycle"], 0, 3),
        assessment("quiz-testing-debugging-limitations", "section", "Testing and Debugging Quiz", ["testing-debugging-limitations"], 0, 3),
        assessment("midterm", "midterm", "Mid-Curriculum Examination", ["lstm-purpose", "bmi-contract", "state-containers", "configuration-and-scaling"], 0, 6),
        assessment("final", "final", "Final Examination", [lesson_data["identifier"] for lesson_data in lessons], 0, 8),
        assessment("pop-review", "pop", "Timed Review Pop Quiz", ["lstm-purpose", "bmi-contract", "state-containers"], 180, 4),
    ]
    questions = build_questions()
    coverage = [
        {"concept": "Repository purpose and runtime artifacts", "lessons": ["lstm-purpose"], "assessments": ["quiz-lstm-purpose", "midterm", "final"]},
        {"concept": "BMI interface", "lessons": ["bmi-contract", "runtime-lifecycle"], "assessments": ["quiz-bmi-contract", "quiz-runtime-lifecycle", "midterm", "final", "pop-review"]},
        {"concept": "State containers", "lessons": ["state-containers"], "assessments": ["quiz-state-containers", "midterm", "final"]},
        {"concept": "Configuration and scaling", "lessons": ["configuration-and-scaling"], "assessments": ["quiz-configuration-and-scaling", "midterm", "final"]},
        {"concept": "LSTM inference", "lessons": ["lstm-inference"], "assessments": ["quiz-lstm-inference", "final"]},
        {"concept": "NextGen lifecycle", "lessons": ["runtime-lifecycle"], "assessments": ["quiz-runtime-lifecycle", "final"]},
        {"concept": "Testing and limitations", "lessons": ["testing-debugging-limitations"], "assessments": ["quiz-testing-debugging-limitations", "final"]},
    ]
    return {
        "metadata": json.loads(metadata_json(context, "curriculum_data")),
        "course": {
            "identifier": "lstm-course",
            "title": "lstm Repository Curriculum",
            "description": "A source-traceable curriculum for the NOAA-OWP/lstm BMI hydrologic model package.",
            "passing_score": 0.8,
        },
        "lessons": lessons,
        "glossary": glossary,
        "assessments": assessments,
        "questions": questions,
        "coverage": coverage,
    }


def load_curriculum_content(context: GenerationContext) -> dict[str, object]:
    """Load repository-specific curriculum content from JSON configuration.

    The content file uses the same structure as the packaged
    ``curriculum.json`` file. The generator owns provenance metadata and
    replaces any provided ``metadata`` object so generated output always records
    the current target revision.

    :param context: Generation context and provenance.
    :return: Curriculum data ready to package in the generated app.
    :raises FileNotFoundError: If the configured content file is missing.
    :raises ValueError: If required top-level curriculum sections are absent.
    """

    content_path = context.configuration.curriculum_content_path
    if content_path is None:
        raise ValueError("curriculum_content_path is not configured")
    curriculum = json.loads(content_path.read_text())
    required_sections = (
        "course",
        "lessons",
        "glossary",
        "assessments",
        "questions",
        "coverage",
    )
    missing_sections = [
        section for section in required_sections if section not in curriculum
    ]
    if missing_sections:
        raise ValueError(
            f"Curriculum content is missing sections: {missing_sections}"
        )
    curriculum["metadata"] = json.loads(metadata_json(context, "curriculum_data"))
    return curriculum


def build_questions() -> list[dict[str, object]]:
    """Create the deterministic assessment question pool.

    :return: Question data records.
    """

    section_questions = [
        question("q-purpose-role", "quiz-lstm-purpose", "What is the `lstm` repository's primary role?", ["Expose a trained LSTM streamflow model through BMI for use by frameworks such as NextGen.", "Provide CAMELS basin attributes without any executable model interface.", "Train NeuralHydrology models from scratch inside the NextGen runtime.", "Route streamflow between NextGen nexus objects after another model computes runoff."], 0, "The README describes a streamflow LSTM developed for NextGen and exposed through BMI.", "lstm-purpose"),
        question("q-purpose-dependencies", "quiz-lstm-purpose", "Which dependency set best matches the repository metadata?", ["bmipy, numpy, pandas, YAML handling, and torch.", "netCDF4 only, with no BMI or PyTorch dependency.", "neuralhydrology, xarray, netCDF4, and pytest as required runtime dependencies.", "scikit-learn, rasterio, pyproj, and shapely only."], 0, "`pyproject.toml` declares BMI, array/data handling, YAML, and PyTorch dependencies.", "lstm-purpose"),
        question("q-purpose-artifacts", "quiz-lstm-purpose", "Which repository paths contain important runtime inputs rather than BMI wrapper source code?", ["`bmi_config_files`, `data`, and `trained_neuralhydrology_models`.", "`lstm/base.py`, `lstm/model_state.py`, and `lstm/bmi_lstm.py` only.", "`tests`, `.github`, and `doc` only.", "`LICENSE`, `TERMS.md`, and `SECURITY.md` only."], 0, "The README and packaging notes identify configuration, sample data, and trained model directories as runtime resources.", "lstm-purpose"),
        question("q-bmi-base", "quiz-bmi-contract", "What does the `raise_not_implemented` decorator in `lstm/base.py` do?", ["Wrap a BMI method so calling it raises `NotImplementedError` with that method's name.", "Convert BMI variable names into internal NeuralHydrology feature names.", "Allocate the hidden and cell state tensors for inference.", "Load the training scaler from `train_data_scaler.yml`."], 0, "`BmiBase` uses the decorator for unsupported BMI grid methods.", "bmi-contract"),
        question("q-bmi-component-name", "quiz-bmi-contract", "What does `bmi_LSTM.get_component_name()` return?", ["`LSTM`", "`bmi_LSTM`", "`Nextgen_CudaLSTM`", "`land_surface_water__runoff_volume_flux`"], 0, "The BMI component-name method returns the short component label `LSTM`.", "bmi-contract"),
        question("q-bmi-crosswalk-function", "quiz-bmi-contract", "What does `crosswalk_to_external('TMP_2maboveground')` return?", ["`land_surface_air__temperature`", "`TMP_2maboveground`", "`atmosphere_water__liquid_equivalent_precipitation_rate`", "`land_surface_water__runoff_depth`"], 0, "`TMP_2maboveground` is the internal temperature feature and maps to the BMI air-temperature name.", "bmi-contract"),
        question("q-state-value", "quiz-state-containers", "What is important about `State.value(name)` in `model_state.py`?", ["It returns the stored numpy array reference for the named variable.", "It returns a copy of selected indices in a caller-provided array.", "It returns the variable's unit string.", "It returns all variable names as a tuple."], 0, "The state tests assert that `State.value` returns the same object stored on the `Var`.", "state-containers"),
        question("q-state-index-copy", "quiz-state-containers", "Which `State` method copies selected values into a destination array?", ["`value_at_indices(name, dest, indices)`", "`value(name)`", "`unit(name)`", "`names()`"], 0, "`value_at_indices` reads selected positions and writes them into `dest`.", "state-containers"),
        question("q-state-facade", "quiz-state-containers", "Why does `bmi_LSTM.update()` use `StateFacade`?", ["It lets an ensemble member read dynamic inputs and static attributes through one value interface.", "It averages each ensemble member's runoff outputs into one scalar grid id.", "It converts target-variable dates from strings into pandas datetime values.", "It renames NeuralHydrology linear-head weights before loading."], 0, "`StateFacade` combines dynamic and static state access without merging their storage.", "state-containers"),
        question("q-config-coerce", "quiz-configuration-and-scaling", "What does `coerce_config` do for keys such as `train_cfg_file` and keys ending in `_date`?", ["It converts training config paths to `Path` lists and parses date fields with pandas.", "It loads PyTorch weights and renames linear-head parameters.", "It creates BMI output variables with zero-valued numpy arrays.", "It compares model predictions against expected runoff values."], 0, "`coerce_config` normalizes path-like and date-like YAML values before runtime use.", "configuration-and-scaling"),
        question("q-config-scaling", "quiz-configuration-and-scaling", "Where does `load_training_scalars` get input normalization values?", ["Dynamic inputs come from xarray feature scaler metadata, and static attributes come from attribute scaler metadata.", "All values come from the BMI configuration's `area_sqkm` setting.", "Values are recomputed from the current timestep's forcing file before every update.", "Values are loaded from the PyTorch model's hidden and cell state tensors."], 0, "The function builds input mean/std arrays from the training scaler data referenced by the training run.", "configuration-and-scaling"),
        question("q-config-output-units", "quiz-configuration-and-scaling", "How does `scale_outputs` produce `land_surface_water__runoff_volume_flux`?", ["It unscales runoff, clamps it at zero, and applies an area and time conversion factor to produce `m3 s-1`.", "It averages all dynamic input variables and stores the result directly as `m3 s-1`.", "It reads observed streamflow from NetCDF and bypasses the LSTM prediction.", "It returns the linear head weights without converting units."], 0, "`scale_outputs` converts the network output into runoff depth and volume flux using configured basin area.", "configuration-and-scaling"),
        question("q-lstm-forward", "quiz-lstm-inference", "What does `Nextgen_CudaLSTM.forward(input_layer, h_t, c_t)` return?", ["A prediction tensor plus updated hidden and cell tensors.", "Only the updated hidden tensor.", "A pair of runoff `Var` objects with BMI units.", "The loaded YAML configuration dictionary."], 0, "The PyTorch module returns `prediction, h_t, c_t` after the LSTM and linear head.", "lstm-inference"),
        question("q-lstm-initialize", "quiz-lstm-inference", "How does `initialize_lstm` adapt NeuralHydrology-trained weights for this local PyTorch module?", ["It renames `head.net.0.weight` and `head.net.0.bias` to `head.weight` and `head.bias` before loading.", "It converts all LSTM weights into CAMELS static attributes before inference.", "It discards the linear head and uses only observed streamflow from the forcing file.", "It changes the BMI output names to match NeuralHydrology's original target names."], 0, "The source explicitly renames the NeuralHydrology head keys to match `Nextgen_CudaLSTM`.", "lstm-inference"),
        question("q-lstm-ensemble-state", "quiz-lstm-inference", "Why do repeated `EnsembleMember.update` calls carry recurrent information forward?", ["The member stores the returned `h_t` and `c_t` tensors back on itself after each forward pass.", "The BMI configuration file is rewritten with every predicted runoff value.", "The `StateFacade` permanently merges dynamic and static state into one dictionary.", "The grid id increments every time `get_grid_size` is called."], 0, "`EnsembleMember.update` assigns the updated hidden and cell tensors returned by the LSTM.", "lstm-inference"),
        question("q-runtime-update-until", "quiz-runtime-lifecycle", "What does `update_until` do when the requested time is not aligned to the 3600-second timestep?", ["It logs a warning and advances only through the whole number of timesteps.", "It changes `_timestep_size_s` to match the requested time.", "It calls `finalize` before updating the model.", "It raises `NotImplementedError` from `BmiBase`."], 0, "`update_until` uses `divmod` with `get_time_step()` and warns on remainders.", "runtime-lifecycle"),
        question("q-runtime-time-methods", "quiz-runtime-lifecycle", "Which pair correctly describes `bmi_LSTM` time methods?", ["`get_current_time()` returns `_timestep * 3600`; `get_time_units()` returns `s`.", "`get_current_time()` returns a pandas datetime; `get_time_units()` returns `hours since start`.", "`get_start_time()` returns the first forcing timestamp; `get_end_time()` returns the last NetCDF timestamp.", "`get_time_step()` reads `time_step` from YAML every update; `get_time_units()` returns `hour`."], 0, "The source uses a fixed 3600-second timestep and simple scalar time values.", "runtime-lifecycle"),
        question("q-runtime-nextgen-config", "quiz-runtime-lifecycle", "In the NextGen run notes, which realization setting identifies the BMI Python class?", ["`python_type`", "`model_type_name`", "`init_config`", "`main_output_variable`"], 0, "The notes describe `python_type` as the package/module/class path for the BMI component.", "runtime-lifecycle"),
        question("q-testing-integration", "quiz-testing-debugging-limitations", "What does `tests/integration_test.py` compare after running the NLDAS example?", ["Runoff depth converted from meters to millimeters per hour against expected values.", "Runoff volume flux directly against basin area in square kilometers.", "The final hidden tensor against the initial zero tensor.", "The YAML training configuration against `pyproject.toml` dependencies."], 0, "The test reads runoff depth, converts it to millimeters per hour, and asserts expected values.", "testing-debugging-limitations"),
        question("q-testing-forcing-map", "quiz-testing-debugging-limitations", "Which mapping from the integration test is correct?", ["`total_precipitation` maps to `atmosphere_water__liquid_equivalent_precipitation_rate`.", "`temperature` maps to `land_surface_water__runoff_depth`.", "`pressure` maps to `land_surface_wind__x_component_of_velocity`.", "`wind_v` maps to `land_surface_radiation~incoming~shortwave__energy_flux`."], 0, "The integration test maps NetCDF forcing variable names to the BMI names set before each update.", "testing-debugging-limitations"),
        question("q-testing-nextgen-paths", "quiz-testing-debugging-limitations", "Why can running LSTM from the top level of an `ngen` checkout cause path problems?", ["Some YAML and pickle-file paths assume a working directory where `trained_neuralhydrology_models` is reachable.", "BMI forbids relative paths in `init_config` for all Python models.", "The PyTorch linear head only runs when the current directory is named `lstm`.", "The NetCDF basin id must match the name of the current directory."], 0, "The NextGen notes describe path rewrites or a symlink for `trained_neuralhydrology_models`.", "testing-debugging-limitations"),
    ]
    review_questions = [
        duplicate_question(record, "midterm", "midterm")
        for record in section_questions[:12]
    ]
    final_questions = [
        duplicate_question(record, "final", "final")
        for record in section_questions
    ]
    pop_questions = [
        duplicate_question(record, "pop-review", "pop")
        for record in section_questions[:9]
    ]
    return section_questions + review_questions + final_questions + pop_questions


def duplicate_question(
    original_question: dict[str, object],
    assessment_identifier: str,
    identifier_prefix: str,
) -> dict[str, object]:
    """Copy a question record for another assessment.

    :param original_question: Existing question data record.
    :param assessment_identifier: Assessment that should own the duplicate.
    :param identifier_prefix: Prefix used to keep question identifiers stable.
    :return: Duplicated question data record.
    """

    duplicate = dict(original_question)
    duplicate["identifier"] = f"{identifier_prefix}-{original_question['identifier']}"
    duplicate["assessment_identifier"] = assessment_identifier
    return duplicate


def lesson(
    identifier: str,
    sequence: str,
    title: str,
    summary: str,
    body: list[str],
    sources: list[dict[str, object]],
) -> dict[str, object]:
    """Create a lesson data record."""

    return {
        "identifier": identifier,
        "sequence": sequence,
        "title": title,
        "summary": summary,
        "body": body,
        "sources": sources,
    }


def source(file_path: str, start_line: int, end_line: int, url: str) -> dict[str, object]:
    """Create a source-reference data record."""

    return {
        "file_path": file_path,
        "start_line": start_line,
        "end_line": end_line,
        "url": url,
    }


def glossary_entry(identifier: str, term: str, definition: str) -> dict[str, str]:
    """Create a glossary data record."""

    return {
        "identifier": identifier,
        "term": term,
        "definition": definition,
    }


def assessment(
    identifier: str,
    assessment_type: str,
    title: str,
    lesson_identifiers: list[str],
    time_limit_seconds: int,
    question_count: int,
) -> dict[str, object]:
    """Create an assessment data record."""

    return {
        "identifier": identifier,
        "assessment_type": assessment_type,
        "title": title,
        "lesson_identifiers": lesson_identifiers,
        "time_limit_seconds": time_limit_seconds,
        "question_count": question_count,
        "passing_score": 0.8,
    }


def question(
    identifier: str,
    assessment_identifier: str,
    prompt: str,
    answers: list[str],
    correct_index: int,
    feedback: str,
    lesson_identifier: str,
) -> dict[str, object]:
    """Create a multiple-choice question data record."""

    return {
        "identifier": identifier,
        "assessment_identifier": assessment_identifier,
        "prompt": prompt,
        "answers": answers,
        "correct_index": correct_index,
        "feedback": feedback,
        "lesson_identifier": lesson_identifier,
    }


def metadata_json(context: GenerationContext, repository_type: str) -> str:
    """Return generation metadata as formatted JSON.

    :param context: Generation context and provenance.
    :param repository_type: Type of generated artifact.
    :return: JSON document.
    """

    metadata = {
        "generator_name": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "template_version": TEMPLATE_VERSION,
        "generation_timestamp": context.generated_at,
        "repository_type": repository_type,
        "target_repository_name": context.configuration.name,
        "target_repository_url": context.configuration.repository_url,
        "configured_revision": context.configuration.revision,
        "resolved_target_commit": context.resolved_commit,
        "generated_package_name": context.configuration.curriculum_app_name,
        "curriculum_schema_version": CURRICULUM_SCHEMA_VERSION,
    }
    return json.dumps(metadata, indent=2) + "\n"


def models_py() -> str:
    """Return Django model source for curriculum storage."""

    return """
    \"\"\"Database models for editable generated curriculum content.\"\"\"

    from __future__ import annotations

    from django.db import models


    class GeneratedContentModel(models.Model):
        \"\"\"Base model for generated content with modification tracking.\"\"\"

        identifier = models.SlugField(max_length=120, unique=True)
        baseline_fingerprint = models.CharField(max_length=64, blank=True)
        is_human_modified = models.BooleanField(default=False)
        generated_at = models.DateTimeField()
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            abstract = True


    class Course(GeneratedContentModel):
        \"\"\"Represent the generated course as a whole.\"\"\"

        title = models.CharField(max_length=200)
        description = models.TextField()
        passing_score = models.FloatField(default=0.8)

        def __str__(self) -> str:
            \"\"\"Return a readable course label.\"\"\"

            return self.title


    class Lesson(GeneratedContentModel):
        \"\"\"Represent an editable curriculum lesson.\"\"\"

        sequence = models.PositiveIntegerField()
        title = models.CharField(max_length=200)
        summary = models.TextField()
        body = models.JSONField(default=list)

        class Meta:
            ordering = ["sequence", "identifier"]

        def __str__(self) -> str:
            \"\"\"Return a readable lesson label.\"\"\"

            return f"{self.sequence}. {self.title}"


    class SourceReference(models.Model):
        \"\"\"Record source evidence for a lesson claim.\"\"\"

        lesson = models.ForeignKey(
            Lesson,
            related_name="sources",
            on_delete=models.CASCADE,
        )
        file_path = models.CharField(max_length=300)
        start_line = models.PositiveIntegerField()
        end_line = models.PositiveIntegerField()
        url = models.URLField(max_length=500, blank=True)

        class Meta:
            ordering = ["lesson__sequence", "file_path", "start_line"]

        def __str__(self) -> str:
            \"\"\"Return a readable source label.\"\"\"

            return f"{self.file_path}:{self.start_line}-{self.end_line}"


    class GlossaryEntry(GeneratedContentModel):
        \"\"\"Define an editable glossary term.\"\"\"

        term = models.CharField(max_length=120)
        definition = models.TextField()

        class Meta:
            ordering = ["term"]

        def __str__(self) -> str:
            \"\"\"Return the glossary term.\"\"\"

            return self.term


    class Assessment(GeneratedContentModel):
        \"\"\"Represent a quiz or examination.\"\"\"

        SECTION = "section"
        MIDTERM = "midterm"
        FINAL = "final"
        POP = "pop"
        ASSESSMENT_TYPES = [
            (SECTION, "Section quiz"),
            (MIDTERM, "Mid-curriculum examination"),
            (FINAL, "Final examination"),
            (POP, "Pop quiz"),
        ]

        title = models.CharField(max_length=200)
        assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
        lessons = models.ManyToManyField(Lesson, related_name="assessments", blank=True)
        time_limit_seconds = models.PositiveIntegerField(default=0)
        question_count = models.PositiveIntegerField(default=0)
        passing_score = models.FloatField(default=0.8)

        class Meta:
            ordering = ["assessment_type", "title"]

        def __str__(self) -> str:
            \"\"\"Return a readable assessment label.\"\"\"

            return self.title


    class Question(GeneratedContentModel):
        \"\"\"Represent an editable multiple-choice assessment question.\"\"\"

        assessment = models.ForeignKey(
            Assessment,
            related_name="questions",
            on_delete=models.CASCADE,
        )
        lesson = models.ForeignKey(
            Lesson,
            related_name="questions",
            on_delete=models.PROTECT,
        )
        prompt = models.TextField()
        answers = models.JSONField(default=list)
        correct_index = models.PositiveIntegerField(default=0)
        feedback = models.TextField()

        def __str__(self) -> str:
            \"\"\"Return a short question label.\"\"\"

            return self.prompt[:80]


    class CoverageRecord(models.Model):
        \"\"\"Map significant target repository concepts to lessons and assessments.\"\"\"

        concept = models.CharField(max_length=160, unique=True)
        lessons = models.ManyToManyField(Lesson, related_name="coverage_records")
        assessments = models.ManyToManyField(
            Assessment,
            related_name="coverage_records",
            blank=True,
        )

        class Meta:
            ordering = ["concept"]

        def __str__(self) -> str:
            \"\"\"Return the covered concept.\"\"\"

            return self.concept
    """


def admin_py() -> str:
    """Return Django admin source for generated models."""

    return """
    \"\"\"Administrative editing configuration for curriculum models.\"\"\"

    from __future__ import annotations

    from django.contrib import admin

    from . import models


    class SourceReferenceInline(admin.TabularInline):
        \"\"\"Edit lesson source references inline.\"\"\"

        model = models.SourceReference
        extra = 0


    @admin.register(models.Course)
    class CourseAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for courses.\"\"\"

        list_display = ("identifier", "title", "is_human_modified", "updated_at")
        list_filter = ("is_human_modified",)


    @admin.register(models.Lesson)
    class LessonAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for lessons.\"\"\"

        list_display = ("sequence", "identifier", "title", "is_human_modified")
        list_filter = ("is_human_modified",)
        inlines = [SourceReferenceInline]


    @admin.register(models.GlossaryEntry)
    class GlossaryEntryAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for glossary entries.\"\"\"

        list_display = ("term", "identifier", "is_human_modified")
        search_fields = ("term", "definition")


    @admin.register(models.Assessment)
    class AssessmentAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for assessments.\"\"\"

        list_display = ("title", "assessment_type", "question_count", "time_limit_seconds")
        filter_horizontal = ("lessons",)


    @admin.register(models.Question)
    class QuestionAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for questions.\"\"\"

        list_display = ("identifier", "assessment", "lesson", "is_human_modified")
        list_filter = ("assessment", "lesson", "is_human_modified")


    @admin.register(models.CoverageRecord)
    class CoverageRecordAdmin(admin.ModelAdmin):
        \"\"\"Admin configuration for coverage records.\"\"\"

        list_display = ("concept",)
        filter_horizontal = ("lessons", "assessments")
    """


def services_py(app_name: str) -> str:
    """Return curriculum loading service source."""

    return f"""
    \"\"\"Services for loading packaged curriculum data into the database.\"\"\"

    from __future__ import annotations

    import hashlib
    import json
    from importlib import resources
    from typing import Any

    from django.utils import timezone

    from . import models


    def load_packaged_curriculum() -> dict[str, int]:
        \"\"\"Load deterministic packaged curriculum records into the database.

        Existing records marked as human modified are preserved. Generated
        records are updated when their baseline fingerprint still matches
        generated ownership.

        :return: Counts of loaded record types.
        \"\"\"

        data = read_curriculum_data()
        generated_at = timezone.now()
        course_count = upsert_course(data["course"], generated_at)
        lesson_count = upsert_lessons(data["lessons"], generated_at)
        glossary_count = upsert_glossary(data["glossary"], generated_at)
        assessment_count = upsert_assessments(data["assessments"], generated_at)
        question_count = upsert_questions(data["questions"], generated_at)
        coverage_count = upsert_coverage(data["coverage"])
        return {{
            "courses": course_count,
            "lessons": lesson_count,
            "glossary_entries": glossary_count,
            "assessments": assessment_count,
            "questions": question_count,
            "coverage_records": coverage_count,
        }}


    def read_curriculum_data() -> dict[str, Any]:
        \"\"\"Read packaged curriculum JSON data.

        :return: Parsed curriculum data.
        \"\"\"

        curriculum_file = resources.files("{app_name}") / "data" / "curriculum.json"
        return json.loads(curriculum_file.read_text())


    def fingerprint(record: dict[str, Any]) -> str:
        \"\"\"Create a stable content fingerprint for a generated record.

        :param record: Structured record content.
        :return: SHA-256 hexadecimal fingerprint.
        \"\"\"

        payload = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


    def should_update(instance: models.GeneratedContentModel) -> bool:
        \"\"\"Return whether generated loading may update a model instance.\"\"\"

        return not instance.is_human_modified


    def upsert_generated_model(
        model_class: type[models.GeneratedContentModel],
        identifier: str,
        defaults: dict[str, Any],
        generated_at,
    ) -> tuple[models.GeneratedContentModel, bool]:
        \"\"\"Create or update a generated content model while preserving edits.\"\"\"

        record_fingerprint = fingerprint({{"identifier": identifier, **defaults}})
        instance, was_created = model_class.objects.get_or_create(
            identifier=identifier,
            defaults={{
                **defaults,
                "baseline_fingerprint": record_fingerprint,
                "generated_at": generated_at,
            }},
        )
        if not was_created and should_update(instance):
            for field_name, field_value in defaults.items():
                setattr(instance, field_name, field_value)
            instance.baseline_fingerprint = record_fingerprint
            instance.generated_at = generated_at
            instance.save()
        return instance, was_created


    def upsert_course(course: dict[str, Any], generated_at) -> int:
        \"\"\"Load the generated course record.\"\"\"

        upsert_generated_model(
            models.Course,
            course["identifier"],
            {{
                "title": course["title"],
                "description": course["description"],
                "passing_score": course["passing_score"],
            }},
            generated_at,
        )
        return 1


    def upsert_lessons(lessons: list[dict[str, Any]], generated_at) -> int:
        \"\"\"Load generated lesson and source-reference records.\"\"\"

        for lesson in lessons:
            lesson_instance, _ = upsert_generated_model(
                models.Lesson,
                lesson["identifier"],
                {{
                    "sequence": int(lesson["sequence"]),
                    "title": lesson["title"],
                    "summary": lesson["summary"],
                    "body": lesson["body"],
                }},
                generated_at,
            )
            if should_update(lesson_instance):
                lesson_instance.sources.all().delete()
                for source in lesson["sources"]:
                    models.SourceReference.objects.create(
                        lesson=lesson_instance,
                        file_path=source["file_path"],
                        start_line=source["start_line"],
                        end_line=source["end_line"],
                        url=source["url"],
                    )
        return len(lessons)


    def upsert_glossary(entries: list[dict[str, Any]], generated_at) -> int:
        \"\"\"Load generated glossary entries.\"\"\"

        for entry in entries:
            upsert_generated_model(
                models.GlossaryEntry,
                entry["identifier"],
                {{"term": entry["term"], "definition": entry["definition"]}},
                generated_at,
            )
        return len(entries)


    def upsert_assessments(assessments: list[dict[str, Any]], generated_at) -> int:
        \"\"\"Load generated assessment records.\"\"\"

        for assessment in assessments:
            assessment_instance, _ = upsert_generated_model(
                models.Assessment,
                assessment["identifier"],
                {{
                    "title": assessment["title"],
                    "assessment_type": assessment["assessment_type"],
                    "time_limit_seconds": assessment["time_limit_seconds"],
                    "question_count": assessment["question_count"],
                    "passing_score": assessment["passing_score"],
                }},
                generated_at,
            )
            lesson_instances = models.Lesson.objects.filter(
                identifier__in=assessment["lesson_identifiers"]
            )
            assessment_instance.lessons.set(lesson_instances)
        return len(assessments)


    def upsert_questions(questions: list[dict[str, Any]], generated_at) -> int:
        \"\"\"Load generated assessment question records.\"\"\"

        for question in questions:
            upsert_generated_model(
                models.Question,
                question["identifier"],
                {{
                    "assessment": models.Assessment.objects.get(
                        identifier=question["assessment_identifier"]
                    ),
                    "lesson": models.Lesson.objects.get(
                        identifier=question["lesson_identifier"]
                    ),
                    "prompt": question["prompt"],
                    "answers": question["answers"],
                    "correct_index": question["correct_index"],
                    "feedback": question["feedback"],
                }},
                generated_at,
            )
        return len(questions)


    def upsert_coverage(records: list[dict[str, Any]]) -> int:
        \"\"\"Load concept-to-curriculum coverage records.\"\"\"

        for record in records:
            coverage, _ = models.CoverageRecord.objects.get_or_create(
                concept=record["concept"]
            )
            coverage.lessons.set(
                models.Lesson.objects.filter(identifier__in=record["lessons"])
            )
            coverage.assessments.set(
                models.Assessment.objects.filter(identifier__in=record["assessments"])
            )
        return len(records)
    """


def views_py(app_name: str) -> str:
    """Return Django view source for learner pages."""

    return f"""
    \"\"\"HTTP views for the generated curriculum application.\"\"\"

    from __future__ import annotations

    import random

    from django.shortcuts import get_object_or_404, render
    from django.urls import reverse

    from . import models


    def index(request):
        \"\"\"Render the curriculum lesson index.\"\"\"

        lessons = models.Lesson.objects.prefetch_related("assessments").all()
        assessments = models.Assessment.objects.all()
        return render(
            request,
            "{app_name}/index.html",
            {{"lessons": lessons, "assessments": assessments}},
        )


    def lesson_detail(request, identifier: str):
        \"\"\"Render a lesson with source references.\"\"\"

        lesson = get_object_or_404(
            models.Lesson.objects.prefetch_related("sources"),
            identifier=identifier,
        )
        next_lesson = models.Lesson.objects.filter(
            sequence__gt=lesson.sequence
        ).order_by("sequence").first()
        related_assessments = list(lesson.assessments.all())
        assessment_priority = {{"section": 0, "midterm": 1, "final": 2, "pop": 3}}
        related_assessments.sort(
            key=lambda assessment: assessment_priority.get(
                assessment.assessment_type,
                99,
            )
        )
        next_assessment = related_assessments[0] if related_assessments else None
        next_assessment_url = (
            reverse(
                "{app_name}:assessment",
                kwargs={{"identifier": next_assessment.identifier}},
            )
            if next_assessment
            else ""
        )
        return render(
            request,
            "{app_name}/lesson.html",
            {{
                "lesson": lesson,
                "next_lesson": next_lesson,
                "next_assessment": next_assessment,
                "next_assessment_url": next_assessment_url,
            }},
        )


    def assessment_detail(request, identifier: str):
        \"\"\"Render an assessment with client-side answer checking.\"\"\"

        assessment = get_object_or_404(
            models.Assessment.objects.prefetch_related("questions", "lessons"),
            identifier=identifier,
        )
        lesson_sequences = [lesson.sequence for lesson in assessment.lessons.all()]
        next_lesson = None
        if lesson_sequences:
            next_lesson = models.Lesson.objects.filter(
                sequence__gt=max(lesson_sequences)
            ).order_by("sequence").first()
        next_url = (
            reverse("{app_name}:lesson", kwargs={{"identifier": next_lesson.identifier}})
            if next_lesson
            else reverse("{app_name}:index")
        )
        questions = list(assessment.questions.select_related("lesson"))
        random.shuffle(questions)
        if assessment.question_count:
            questions = questions[: assessment.question_count]
        for question in questions:
            question.answer_pairs = list(enumerate(question.answers))
            random.shuffle(question.answer_pairs)
        return render(
            request,
            "{app_name}/assessment.html",
            {{"assessment": assessment, "questions": questions, "next_url": next_url}},
        )


    def glossary(request):
        \"\"\"Render glossary entries.\"\"\"

        entries = models.GlossaryEntry.objects.all()
        return render(request, "{app_name}/glossary.html", {{"entries": entries}})


    def progress(request):
        \"\"\"Render client-side progress controls.\"\"\"

        return render(request, "{app_name}/progress.html")
    """


def urls_py(app_name: str) -> str:
    """Return URL configuration source for the curriculum app."""

    return f"""
    \"\"\"URL routes for the generated curriculum application.\"\"\"

    from __future__ import annotations

    from django.urls import path

    from . import views


    app_name = "{app_name}"

    urlpatterns = [
        path("", views.index, name="index"),
        path("lessons/<slug:identifier>/", views.lesson_detail, name="lesson"),
        path("assessments/<slug:identifier>/", views.assessment_detail, name="assessment"),
        path("glossary/", views.glossary, name="glossary"),
        path("progress/", views.progress, name="progress"),
    ]
    """


def load_curriculum_py(app_name: str) -> str:
    """Return management command source for loading curriculum data."""

    return f"""
    \"\"\"Load packaged generated curriculum data into the configured database.\"\"\"

    from __future__ import annotations

    from django.core.management.base import BaseCommand

    from {app_name} import services


    class Command(BaseCommand):
        \"\"\"Load generated curriculum into Django models.\"\"\"

        help = "Load packaged generated curriculum into the database."

        def handle(self, *args, **options) -> None:
            \"\"\"Execute the curriculum load command.\"\"\"

            counts = services.load_packaged_curriculum()
            self.stdout.write(self.style.SUCCESS(f"Loaded curriculum: {{counts}}"))
    """


def migration_py(app_name: str) -> str:
    """Return initial Django migration source."""

    return (
        """
    \"\"\"Initial database schema for generated curriculum content.\"\"\"

    from __future__ import annotations

    import django.db.models.deletion
    from django.db import migrations, models


    class Migration(migrations.Migration):
        \"\"\"Create curriculum, assessment, glossary, and provenance tables.\"\"\"

        initial = True

        dependencies = []

        operations = [
            migrations.CreateModel(
                name="Assessment",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("identifier", models.SlugField(max_length=120, unique=True)),
                    ("baseline_fingerprint", models.CharField(blank=True, max_length=64)),
                    ("is_human_modified", models.BooleanField(default=False)),
                    ("generated_at", models.DateTimeField()),
                    ("updated_at", models.DateTimeField(auto_now=True)),
                    ("title", models.CharField(max_length=200)),
                    ("assessment_type", models.CharField(choices=[("section", "Section quiz"), ("midterm", "Mid-curriculum examination"), ("final", "Final examination"), ("pop", "Pop quiz")], max_length=20)),
                    ("time_limit_seconds", models.PositiveIntegerField(default=0)),
                    ("question_count", models.PositiveIntegerField(default=0)),
                    ("passing_score", models.FloatField(default=0.8)),
                ],
                options={"ordering": ["assessment_type", "title"]},
            ),
            migrations.CreateModel(
                name="Course",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("identifier", models.SlugField(max_length=120, unique=True)),
                    ("baseline_fingerprint", models.CharField(blank=True, max_length=64)),
                    ("is_human_modified", models.BooleanField(default=False)),
                    ("generated_at", models.DateTimeField()),
                    ("updated_at", models.DateTimeField(auto_now=True)),
                    ("title", models.CharField(max_length=200)),
                    ("description", models.TextField()),
                    ("passing_score", models.FloatField(default=0.8)),
                ],
                options={"abstract": False},
            ),
            migrations.CreateModel(
                name="GlossaryEntry",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("identifier", models.SlugField(max_length=120, unique=True)),
                    ("baseline_fingerprint", models.CharField(blank=True, max_length=64)),
                    ("is_human_modified", models.BooleanField(default=False)),
                    ("generated_at", models.DateTimeField()),
                    ("updated_at", models.DateTimeField(auto_now=True)),
                    ("term", models.CharField(max_length=120)),
                    ("definition", models.TextField()),
                ],
                options={"ordering": ["term"]},
            ),
            migrations.CreateModel(
                name="Lesson",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("identifier", models.SlugField(max_length=120, unique=True)),
                    ("baseline_fingerprint", models.CharField(blank=True, max_length=64)),
                    ("is_human_modified", models.BooleanField(default=False)),
                    ("generated_at", models.DateTimeField()),
                    ("updated_at", models.DateTimeField(auto_now=True)),
                    ("sequence", models.PositiveIntegerField()),
                    ("title", models.CharField(max_length=200)),
                    ("summary", models.TextField()),
                    ("body", models.JSONField(default=list)),
                ],
                options={"ordering": ["sequence", "identifier"]},
            ),
            migrations.CreateModel(
                name="CoverageRecord",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("concept", models.CharField(max_length=160, unique=True)),
                    ("assessments", models.ManyToManyField(blank=True, related_name="coverage_records", to="__APP_NAME__.assessment")),
                    ("lessons", models.ManyToManyField(related_name="coverage_records", to="__APP_NAME__.lesson")),
                ],
                options={"ordering": ["concept"]},
            ),
            migrations.CreateModel(
                name="Question",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("identifier", models.SlugField(max_length=120, unique=True)),
                    ("baseline_fingerprint", models.CharField(blank=True, max_length=64)),
                    ("is_human_modified", models.BooleanField(default=False)),
                    ("generated_at", models.DateTimeField()),
                    ("updated_at", models.DateTimeField(auto_now=True)),
                    ("prompt", models.TextField()),
                    ("answers", models.JSONField(default=list)),
                    ("correct_index", models.PositiveIntegerField(default=0)),
                    ("feedback", models.TextField()),
                    ("assessment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="__APP_NAME__.assessment")),
                    ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="questions", to="__APP_NAME__.lesson")),
                ],
                options={"abstract": False},
            ),
            migrations.CreateModel(
                name="SourceReference",
                fields=[
                    ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("file_path", models.CharField(max_length=300)),
                    ("start_line", models.PositiveIntegerField()),
                    ("end_line", models.PositiveIntegerField()),
                    ("url", models.URLField(blank=True, max_length=500)),
                    ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sources", to="__APP_NAME__.lesson")),
                ],
                options={"ordering": ["lesson__sequence", "file_path", "start_line"]},
            ),
            migrations.AddField(
                model_name="assessment",
                name="lessons",
                field=models.ManyToManyField(blank=True, related_name="assessments", to="__APP_NAME__.lesson"),
            ),
        ]
    """).replace("__APP_NAME__", app_name)


def template_index(app_name: str, display_name: str) -> str:
    """Return the lesson index template."""

    return (
        """
    {% extends "base.html" %}
    {% block title %}__DISPLAY_NAME__ Curriculum{% endblock %}
    {% block content %}
    <section class="hero-band">
        <div>
            <p class="eyebrow">Source-traceable course</p>
            <h1>__DISPLAY_NAME__ Repository Curriculum</h1>
            <p>Learn the target repository from prerequisites through source-level contribution work.</p>
        </div>
        <div class="progress-card" data-progress-summary></div>
    </section>
    <section class="content-grid">
        <div>
            <h2>Lessons</h2>
            <ol class="lesson-list">
                {% for lesson in lessons %}
                    <li>
                        <a href="{% url '__APP_NAME__:lesson' lesson.identifier %}">{{ lesson.title }}</a>
                        <p>{{ lesson.summary }}</p>
                    </li>
                {% endfor %}
            </ol>
        </div>
        <aside>
            <h2>Assessments</h2>
            {% for assessment in assessments %}
                <a class="assessment-link" href="{% url '__APP_NAME__:assessment' assessment.identifier %}">
                    <span>{{ assessment.title }}</span>
                    <small>{{ assessment.get_assessment_type_display }}</small>
                </a>
            {% endfor %}
        </aside>
    </section>
    {% endblock %}
    """
    ).replace("__APP_NAME__", app_name).replace("__DISPLAY_NAME__", display_name)


def template_lesson(app_name: str) -> str:
    """Return the lesson detail template."""

    return (
        """
    {% extends "base.html" %}
    {% block title %}{{ lesson.title }}{% endblock %}
    {% block content %}
    <article class="lesson-page" data-lesson-id="{{ lesson.identifier }}">
        <p class="eyebrow">Lesson {{ lesson.sequence }}</p>
        <h1>{{ lesson.title }}</h1>
        <p class="lede">{{ lesson.summary }}</p>
        {% for paragraph in lesson.body %}
            <p>{{ paragraph }}</p>
        {% endfor %}
        <h2>Source Evidence</h2>
        <ul class="source-list">
            {% for source in lesson.sources.all %}
                <li>
                    <a href="{{ source.url }}">{{ source.file_path }}:{{ source.start_line }}-{{ source.end_line }}</a>
                </li>
            {% endfor %}
        </ul>
        <button
            class="primary-button"
            data-complete-lesson="{{ lesson.identifier }}"
            data-next-assessment-url="{{ next_assessment_url }}"
        >
            Mark Complete
        </button>
        <p class="completion-feedback" data-completion-feedback aria-live="polite"></p>
        {% if next_assessment %}
            <p class="assessment-trigger">
                Next check: <a href="{{ next_assessment_url }}">{{ next_assessment.title }}</a>
            </p>
        {% endif %}
        {% if next_lesson %}
            <a class="next-link" href="{% url '__APP_NAME__:lesson' next_lesson.identifier %}">Next lesson</a>
        {% endif %}
    </article>
    {% endblock %}
    """
    ).replace("__APP_NAME__", app_name)


def template_assessment() -> str:
    """Return the assessment template."""

    return """
    {% extends "base.html" %}
    {% block title %}{{ assessment.title }}{% endblock %}
    {% block content %}
    <section
        class="assessment-page"
        data-assessment-id="{{ assessment.identifier }}"
        data-time-limit="{{ assessment.time_limit_seconds }}"
        data-next-url="{{ next_url }}"
    >
        <p class="eyebrow">{{ assessment.get_assessment_type_display }}</p>
        <h1>{{ assessment.title }}</h1>
        <div class="timer" data-assessment-timer></div>
        {% for question in questions %}
            <fieldset class="question" data-question-id="{{ question.identifier }}" data-correct-index="{{ question.correct_index }}" data-feedback="{{ question.feedback }}">
                <legend>{{ question.prompt }}</legend>
                {% for answer_index, answer in question.answer_pairs %}
                    <label>
                        <input type="radio" name="{{ question.identifier }}" value="{{ answer_index }}">
                        <span>{{ answer }}</span>
                    </label>
                {% endfor %}
                <p class="feedback" aria-live="polite"></p>
            </fieldset>
        {% endfor %}
        <button class="primary-button" data-grade-assessment>Submit</button>
        <div class="score" data-assessment-score aria-live="polite"></div>
    </section>
    {% endblock %}
    """


def template_glossary() -> str:
    """Return the glossary template."""

    return """
    {% extends "base.html" %}
    {% block title %}Glossary{% endblock %}
    {% block content %}
    <section>
        <h1>Glossary</h1>
        <dl class="glossary-list">
            {% for entry in entries %}
                <dt id="{{ entry.identifier }}">{{ entry.term }}</dt>
                <dd>{{ entry.definition }}</dd>
            {% endfor %}
        </dl>
    </section>
    {% endblock %}
    """


def template_progress() -> str:
    """Return the progress template."""

    return """
    {% extends "base.html" %}
    {% block title %}Progress{% endblock %}
    {% block content %}
    <section class="progress-page">
        <h1>Progress</h1>
        <div data-progress-summary></div>
        <div class="button-row">
            <button class="primary-button" data-export-progress>Export</button>
            <label class="file-button">
                Import
                <input type="file" accept="application/json" data-import-progress>
            </label>
            <button class="secondary-button" data-reset-progress>Reset</button>
        </div>
        <pre data-progress-json></pre>
    </section>
    {% endblock %}
    """


def curriculum_css() -> str:
    """Return generated curriculum stylesheet."""

    return """
    :root {
        color-scheme: light;
        --ink: #18212f;
        --muted: #5d697a;
        --line: #d9e0ea;
        --surface: #ffffff;
        --band: #eef5f2;
        --accent: #116466;
        --accent-dark: #0b484a;
        --warning: #9f4c00;
        --success: #1f7a3f;
    }

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        color: var(--ink);
        background: #f7f8fa;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.55;
    }

    a {
        color: var(--accent-dark);
    }

    .site-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.9rem clamp(1rem, 4vw, 3rem);
        background: var(--surface);
        border-bottom: 1px solid var(--line);
    }

    .brand {
        font-weight: 700;
        text-decoration: none;
    }

    nav {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    nav a {
        text-decoration: none;
        font-size: 0.95rem;
    }

    .page-shell {
        max-width: 1120px;
        margin: 0 auto;
        padding: clamp(1rem, 4vw, 3rem);
    }

    .hero-band {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(16rem, 22rem);
        gap: 2rem;
        align-items: center;
        padding: clamp(1.5rem, 5vw, 3rem);
        background: var(--band);
        border: 1px solid var(--line);
        border-radius: 8px;
    }

    h1 {
        margin: 0 0 0.75rem;
        font-size: clamp(2rem, 6vw, 3.5rem);
        line-height: 1.05;
        letter-spacing: 0;
    }

    h2 {
        margin-top: 2rem;
        font-size: 1.35rem;
        letter-spacing: 0;
    }

    .eyebrow {
        margin: 0 0 0.5rem;
        color: var(--accent-dark);
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .content-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(16rem, 20rem);
        gap: 2rem;
        margin-top: 2rem;
    }

    .lesson-list {
        padding-left: 1.25rem;
    }

    .lesson-list li,
    .assessment-link,
    .question,
    .progress-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
    }

    .lesson-list li {
        margin-bottom: 1rem;
        padding: 1rem;
    }

    .assessment-link {
        display: block;
        margin-bottom: 0.75rem;
        padding: 0.85rem;
        text-decoration: none;
    }

    .assessment-link span {
        display: block;
        font-weight: 700;
    }

    .assessment-link small {
        color: var(--muted);
    }

    .lesson-page,
    .assessment-page,
    .progress-page {
        max-width: 780px;
    }

    .lede {
        color: var(--muted);
        font-size: 1.12rem;
    }

    .source-list {
        padding-left: 1.1rem;
    }

    .primary-button,
    .secondary-button,
    .file-button {
        display: inline-flex;
        align-items: center;
        min-height: 2.5rem;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        border: 1px solid var(--accent-dark);
        font: inherit;
        cursor: pointer;
    }

    .primary-button {
        color: #ffffff;
        background: var(--accent);
    }

    .secondary-button,
    .file-button {
        color: var(--accent-dark);
        background: #ffffff;
    }

    .file-button input {
        display: none;
    }

    .next-link {
        display: inline-block;
        margin-left: 1rem;
    }

    .question {
        margin: 1rem 0;
        padding: 1rem;
    }

    .question label {
        display: block;
        margin: 0.5rem 0;
    }

    .feedback {
        color: var(--warning);
        font-weight: 600;
    }

    .feedback.correct {
        color: var(--success);
    }

    .completion-feedback {
        min-height: 1.6rem;
        color: var(--success);
        font-weight: 700;
    }

    .assessment-trigger {
        margin-top: 0.75rem;
    }

    .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin: 1rem 0;
    }

    pre {
        overflow: auto;
        padding: 1rem;
        background: #202631;
        color: #eef5f2;
        border-radius: 8px;
    }

    @media (max-width: 760px) {
        .site-header,
        .hero-band,
        .content-grid {
            display: block;
        }

        nav {
            margin-top: 0.75rem;
        }

        .progress-card {
            margin-top: 1rem;
        }
    }
    """


def progress_js(app_name: str) -> str:
    """Return client-side progress and assessment JavaScript."""

    return (
        """
    (() => {
        const storageKey = "__APP_NAME__-curriculum-progress-v1";
        const initialProgress = {
            schemaVersion: 1,
            completedLessons: [],
            assessmentAttempts: {},
            preferences: {timersEnabled: true}
        };

        function loadProgress() {
            const stored = window.localStorage.getItem(storageKey);
            if (!stored) {
                return structuredClone(initialProgress);
            }
            try {
                const parsed = JSON.parse(stored);
                if (parsed.schemaVersion !== 1) {
                    return structuredClone(initialProgress);
                }
                return parsed;
            } catch {
                return structuredClone(initialProgress);
            }
        }

        function saveProgress(progress) {
            window.localStorage.setItem(storageKey, JSON.stringify(progress, null, 2));
            renderProgress();
        }

        function completeLesson(identifier) {
            const progress = loadProgress();
            if (!progress.completedLessons.includes(identifier)) {
                progress.completedLessons.push(identifier);
            }
            saveProgress(progress);
        }

        function showLessonCompletion(button) {
            const feedback = document.querySelector("[data-completion-feedback]");
            const nextAssessmentUrl = button.dataset.nextAssessmentUrl;
            if (feedback) {
                feedback.textContent = nextAssessmentUrl
                    ? "Lesson complete. Starting the related repository check."
                    : "Lesson complete.";
                feedback.classList.add("correct");
            }
            if (nextAssessmentUrl) {
                window.setTimeout(() => {
                    window.location.assign(nextAssessmentUrl);
                }, 900);
            }
        }

        function gradeAssessment(section) {
            const questions = [...section.querySelectorAll("[data-question-id]")];
            let correctCount = 0;
            questions.forEach((question) => {
                const selected = question.querySelector("input:checked");
                const feedback = question.querySelector(".feedback");
                const isCorrect = selected && selected.value === question.dataset.correctIndex;
                if (isCorrect) {
                    correctCount += 1;
                    feedback.textContent = "Correct. " + question.dataset.feedback;
                    feedback.classList.add("correct");
                } else {
                    feedback.textContent = "Review this concept. " + question.dataset.feedback;
                    feedback.classList.remove("correct");
                }
            });
            const score = questions.length ? correctCount / questions.length : 0;
            const progress = loadProgress();
            const identifier = section.dataset.assessmentId;
            progress.assessmentAttempts[identifier] = progress.assessmentAttempts[identifier] || [];
            progress.assessmentAttempts[identifier].push({
                score,
                correctCount,
                questionCount: questions.length,
                completedAt: new Date().toISOString()
            });
            saveProgress(progress);
            const scoreElement = section.querySelector("[data-assessment-score]");
            scoreElement.textContent = `Score: ${correctCount}/${questions.length} (${Math.round(score * 100)}%). Moving to the next lesson.`;
            if (section.dataset.nextUrl) {
                window.setTimeout(() => {
                    window.location.assign(section.dataset.nextUrl);
                }, 1200);
            }
        }

        function renderProgress() {
            const progress = loadProgress();
            document.querySelectorAll("[data-progress-summary]").forEach((element) => {
                const attemptCount = Object.values(progress.assessmentAttempts)
                    .reduce((total, attempts) => total + attempts.length, 0);
                element.innerHTML = `
                    <strong>${progress.completedLessons.length}</strong> lessons completed<br>
                    <strong>${attemptCount}</strong> assessment attempts saved
                `;
            });
            document.querySelectorAll("[data-progress-json]").forEach((element) => {
                element.textContent = JSON.stringify(progress, null, 2);
            });
        }

        function exportProgress() {
            const blob = new Blob([JSON.stringify(loadProgress(), null, 2)], {
                type: "application/json"
            });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "__APP_NAME__-curriculum-progress.json";
            link.click();
            URL.revokeObjectURL(link.href);
        }

        function importProgress(file) {
            file.text().then((text) => {
                const parsed = JSON.parse(text);
                if (parsed.schemaVersion !== 1) {
                    throw new Error("Unsupported progress schema version.");
                }
                saveProgress(parsed);
            }).catch((error) => {
                window.alert(error.message);
            });
        }

        function startTimer(section) {
            const timer = section.querySelector("[data-assessment-timer]");
            const seconds = Number(section.dataset.timeLimit || 0);
            if (!timer || seconds <= 0 || !loadProgress().preferences.timersEnabled) {
                if (timer) {
                    timer.textContent = "Timer disabled";
                }
                return;
            }
            const endsAt = Date.now() + seconds * 1000;
            window.setInterval(() => {
                const remaining = Math.max(0, Math.ceil((endsAt - Date.now()) / 1000));
                timer.textContent = `Time remaining: ${remaining}s`;
            }, 1000);
        }

        document.addEventListener("click", (event) => {
            const completeButton = event.target.closest("[data-complete-lesson]");
            if (completeButton) {
                completeLesson(completeButton.dataset.completeLesson);
                showLessonCompletion(completeButton);
            }
            if (event.target.closest("[data-grade-assessment]")) {
                gradeAssessment(event.target.closest("[data-assessment-id]"));
            }
            if (event.target.closest("[data-export-progress]")) {
                exportProgress();
            }
            if (event.target.closest("[data-reset-progress]")) {
                saveProgress(structuredClone(initialProgress));
            }
        });

        document.addEventListener("change", (event) => {
            if (event.target.matches("[data-import-progress]") && event.target.files[0]) {
                importProgress(event.target.files[0]);
            }
        });

        document.querySelectorAll("[data-assessment-id]").forEach(startTimer);
        renderProgress();
    })();
    """
    ).replace("__APP_NAME__", app_name)


def host_readme(context: GenerationContext) -> str:
    """Return generated host README content."""

    return f"""# Generated Education Host

This standalone Django project hosts generated curriculum apps.

## Provenance

* Target repository: `{context.configuration.repository_url}`
* Configured revision: `{context.configuration.revision}`
* Resolved commit: `{context.resolved_commit}`
* Generated package: `{context.configuration.curriculum_app_name}`

## Run

```bash
python -m pip install -e ./{context.configuration.name}
python -m pip install -e .
python manage.py migrate
python manage.py load_curriculum
python manage.py runserver 0.0.0.0:8000
```

The curriculum app is an independent Git repository at
`./{context.configuration.name}`. The host keeps that path ignored so it does
not absorb curriculum app history.
"""


def curriculum_readme(context: GenerationContext) -> str:
    """Return generated curriculum app README content."""

    return f"""# {context.configuration.display_name} Curriculum App

This is a reusable Django app containing source-traceable curriculum for
`{context.configuration.repository_url}` at commit `{context.resolved_commit}`.

## Install in a Django Project

```bash
python -m pip install -e .
```

Add `{context.configuration.curriculum_app_name}` to `INSTALLED_APPS`, include
`{context.configuration.curriculum_app_name}.urls`, run migrations, and load the
packaged curriculum:

```bash
python manage.py migrate
python manage.py load_curriculum
```

Packaged data lives in `src/{context.configuration.curriculum_app_name}/data/curriculum.json`.
Administrative edits are tracked with `is_human_modified` and generated
fingerprints so later regeneration can detect preservation requirements.
"""


def copy_agent_docs(repository_root: Path, destination: Path, repository_label: str) -> None:
    """Copy repository agent-state documents into a generated repository."""

    for filename in ("AGENTS.md", "SPEC.md", "STYLE.md"):
        shutil.copy2(repository_root / filename, destination / filename)
    agent_directory = destination / "docs" / "agent"
    agent_directory.mkdir(parents=True, exist_ok=True)
    write_file(
        agent_directory / "STATUS.md",
        f"""# STATUS

Current objective: maintain the generated {repository_label}.

The repository was generated from the parent generator state. Use local
`generation_metadata.json` and packaged curriculum data as the source of
generation provenance.
""",
    )
    write_file(
        agent_directory / "TASKS.md",
        f"""# TASKS

## Ready

* Review generated curriculum for technical accuracy against recorded source
  references.
* Add more lessons and assessment questions where maintainers need deeper
  coverage.
""",
    )
    write_file(
        agent_directory / "DECISIONS.md",
        """# DECISIONS

## Generated Repository Boundaries

This generated repository is intended to be maintained independently from the
generator after creation. Preserve generation metadata and source provenance
when making curriculum changes.
""",
    )


def initialize_generated_repository(repository_path: Path, message: str) -> None:
    """Initialize a generated repository and create an initial commit."""

    run_process(["git", "-C", str(repository_path), "init", "-b", "main"])
    run_process(["git", "-C", str(repository_path), "config", "user.name", "Education Generator"])
    run_process(["git", "-C", str(repository_path), "config", "user.email", "education-generator@example.invalid"])
    run_process(["git", "-C", str(repository_path), "add", "."])
    run_process(["git", "-C", str(repository_path), "commit", "-m", message])


def recreate_directory(path: Path) -> None:
    """Remove and recreate a generated directory inside the workspace."""

    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def write_file(path: Path, content: str) -> None:
    """Write normalized text content to a file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")


def run_process(
    command: list[str],
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run an external command with argument-list subprocess handling."""

    return subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=capture_output,
    )


if __name__ == "__main__":
    main()
