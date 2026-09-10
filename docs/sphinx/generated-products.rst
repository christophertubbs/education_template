Generated product scaffold
==========================

Everything under ``education_generator/templates`` is source code for future
independent repositories.  It is not runtime code for this repository until
rendered by the generator.

Product template
----------------

Token replacement supplies package/AppConfig names, repository identity, exact
commit, display name, runtime constraint, version, and branch context.  The
rendered tree contains:

.. code-block:: text

   pyproject.toml
   README.md
   AGENTS.md, SPEC.md, STYLE.md
   docs/agent/{STATUS,TASKS,DECISIONS}.md
   provenance/*.json
   src/<product>/
      apps.py
      data/curriculum.json
      migrations/{0001_load_curriculum,0002_refresh_structured_lessons}.py
   tests/test_product.py

``pyproject.toml`` declares an independently distributable package, its runtime
dependency, package data, and exactly one ``education_curriculum.products``
entry point.  ``apps.py`` makes its migrations and resources visible to Django.

The first migration imports the packaged baseline and deletes only that
curriculum on reverse migration.  The second migration refreshes structured
lesson content for databases that already ran the first migration.  Both call
the runtime importer so human edits receive the same protection as an explicit
``load_curricula`` refresh.  Future content-only changes still require the
explicit refresh command because an already-applied migration does not rerun.

The product test checks that packaged provenance contains the exact target
commit and that installed distribution metadata advertises the expected entry
point.  It therefore needs to run against an installed package, not merely a
directory placed on ``PYTHONPATH``.

Agent-state template
--------------------

The ``templates/agent`` files seed durable context inside each generated
repository.  ``STATUS`` records the pinned source and current release state;
``TASKS`` records completed generation and regeneration work; ``DECISIONS``
preserves the shared-runtime and semantic-content boundaries.  The root
``AGENTS.md``, ``SPEC.md``, and ``STYLE.md`` are copied verbatim during assembly.

Propagation rule
----------------

Editing these templates has no retroactive effect.  Regenerate and revalidate
each product that should receive the change.  Conversely, editing a rendered
product does not update this template and may make the destination dirty,
causing the next generator run to refuse promotion.
