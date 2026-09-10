Standalone Runner
=================

``education_runner`` is an optional Django host.  Applications may embed
``education_runtime`` in another Django project instead, provided they install
compatible Curriculum Products and mount the runtime URLs.

Discovery precedence and safety
-------------------------------

:func:`education_runner.product_discovery.discover_product_apps` merges three
sources by product entry-point name:

1. local products under ``generated/`` whose provenance target matches a real,
   non-symlink directory under ``curricula/``;
2. installed ``education_curriculum.products`` package entry points;
3. comma-separated legacy packages from ``EDUCATION_PRODUCTS``.

Results are deterministic.  Names and dotted Python paths are validated,
entry-point modules must be owned by the named package, each generated product
must advertise exactly one entry point, and conflicting advertisements fail
startup.  Local ``src`` paths are added to ``sys.path`` only after every local
candidate validates, preventing partial activation after an error.

Environment settings
--------------------

.. list-table::
   :header-rows: 1
   :widths: 28 30 42

   * - Variable
     - Default
     - Effect
   * - ``EDUCATION_SECRET_KEY``
     - ``unsafe-development-key``
     - Django signing key.  A deployment must override the development value.
   * - ``EDUCATION_DEBUG``
     - ``true``
     - Enables debug only when the lowercased value is exactly ``true``.
   * - ``EDUCATION_ALLOWED_HOSTS``
     - localhost, loopback, hostname
     - Comma-separated Django allowed hosts.
   * - ``EDUCATION_DATABASE``
     - ``education.sqlite3`` at repository root
     - SQLite database path.
   * - ``EDUCATION_PRODUCTS``
     - empty
     - Additive legacy package names; normal products use discovery.

``settings.py`` installs Django admin/auth/session/static applications, the
shared runtime, then discovered products.  WhiteNoise serves collected static
assets with manifest storage.  ``urls.py`` mounts admin at ``/admin/`` and the
runtime at the site root.  ``asgi.py`` and ``wsgi.py`` expose the two standard
deployment callables and select these settings by default.

Startup implications
--------------------

Discovery happens while settings are imported, before Django builds the app
registry.  Malformed product metadata is therefore a deliberate startup error.
After installing or regenerating products, run migration, explicit curriculum
refresh, and static collection before serving traffic; see :doc:`operations`.
