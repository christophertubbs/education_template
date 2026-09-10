Operating and changing the ecosystem
====================================

Local lifecycle
---------------

After installing the root package and one or more products, the normal order is:

.. code-block:: bash

   ./install.sh
   python manage.py check
   python manage.py runserver

``install.sh`` runs ``migrate --noinput``, ``load_curricula``, then
``collectstatic --noinput`` and stops on the first failure.  Set ``PYTHON_BIN``
to select an interpreter and use the runner's environment variables for the
database and deployment settings.

Generate a product
------------------

.. code-block:: bash

   education-generate --project project.json

The command may fetch Git remotes and checks out the target at a detached exact
commit.  It will refuse dirty target or generated repositories.  Reviewed
artifact authoring happens under ``curricula/<target>`` before this deterministic
assembly step.

Validation by change type
-------------------------

Use the smallest focused test while iterating, then the repository-required full
checks before completion.  A typical full pass is:

.. code-block:: bash

   ruff format --check src tests tools manage.py
   ruff check src tests tools manage.py
   python manage.py test
   python manage.py check
   python manage.py makemigrations --check --dry-run
   git diff --check

For generator changes, also validate representative canonical artifacts,
generate into staging, build the resulting package, install it in isolation,
run its tests, and migrate/load it into a clean database.  For model or importer
changes, cover clean migration, repeated refresh, baseline updates, human edits,
and conflict creation.  For templates, CSS, or JavaScript, render representative
routes and include keyboard, responsive, math, and progress behavior checks.

Operational invariants
----------------------

* Target repositories under ``repository/`` are read-only evidence.
* Generated products under ``generated/`` are separate Git repositories.
* The root Git repository does not track either boundary.
* Unknown required artifact state stays unresolved and blocks promotion.
* Stable identifiers survive product releases; changing one affects imports and
  browser progress compatibility.
* Runtime data refresh is explicit and separate from migration state.
* Deployment secrets and production debug/host choices come from environment.

Debugging sequence
------------------

When a product does not appear, inspect its provenance target name, matching
``curricula`` directory, ``pyproject.toml`` entry point, ``src`` directory, and
duplicate entry-point names.  When content is stale, run ``load_curricula`` and
inspect ``ImportConflict`` before assuming migrations failed.  When an
assessment fails to render, compare its selection count to the required concept,
contract, section, and outcome coverage.  When progress import fails, compare
all three compatibility keys: progress schema, curriculum ID, and curriculum
version.
