Education Curriculum System
===========================

This documentation is the shortest path from a fresh checkout to a working
mental model of the code under ``src/``.  It describes the implementation as it
exists; :doc:`specification-map` explains how that implementation relates to the
normative product contract in ``SPEC.md``.

Start here
----------

* Read :doc:`architecture` for the package boundaries and end-to-end flows.
* Read :doc:`generator` before changing generation, validation, or promotion.
* Read :doc:`runtime` before changing data, imports, assessments, or views.
* Read :doc:`runner` before changing startup or product discovery.
* Use :doc:`source-inventory` to find every authored asset under ``src/``.
* Use :doc:`api` for Python signatures and implementation docstrings.

.. toctree::
   :maxdepth: 2
   :caption: System guide

   architecture
   generator
   runtime
   runner
   frontend
   generated-products
   operations
   specification-map
   source-inventory
   api

Authority and boundaries
------------------------

``SPEC.md`` is authoritative for product behavior.  ``AGENTS.md`` defines the
repository workflow, and ``STYLE.md`` defines implementation conventions.  The
documentation here is explanatory: if it conflicts with the specification,
fix this documentation and follow the specification.

The central boundary is:

.. code-block:: text

   education_generator  --->  Curriculum Product  --->  education_runtime
                                                           ^
                                                           |
                                                   education_runner

The arrow means *supplies data to* or *depends on*.  The runtime owns generic
behavior and must not depend on a target-specific product.  A product contains
knowledge and deterministic loading logic, not its own views or models.  The
runner is an optional host, not a curriculum.
