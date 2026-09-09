# Architecture

```text
project.json + Target Repository + reviewed analysis artifacts
                           |
                           v
                  education_generator
                           |
                           v
             independent Curriculum Product
                           |
                           v
education_runner ---> education_runtime <--- other Django services
```

The generator records state under `.work/<target>-curriculum`, inventories the
resolved checkout, validates knowledge, prerequisites, mastery, curriculum,
coverage, assessment, evidence, audits, and unresolved state, assembles in
staging, compiles, then promotes. Failure leaves diagnostics and no release.

The runtime owns target-independent models and rendering. Products populate
those models through deterministic data migrations. Baseline rows have a
fingerprint and human-modification flag. Changed incoming baselines do not
overwrite human edits; they create an `ImportConflict`.

Lesson data is semantic rather than presentation-oriented HTML. Products store
typed blocks and inline spans for equations, code, callouts, definitions,
examples, diagnostics, tables, variables, and references. The runtime converts
them to accessible HTML, uses MathJax for LaTeX, and exposes lesson-linked
glossary definitions. Curriculum validation rejects unsupported, inaccessible,
or paragraph-only technical content before promotion.

Assessment definitions are data. The runtime chooses from oversized pools and
evaluates supported items deterministically in the browser. Progress is
versioned in IndexedDB, survives restarts and offline periods, and supports JSON
export/import without identity or accounts.

The runner supplies settings, URLs, ASGI, WSGI, SQLite defaults, and product
discovery. In this checkout it cross-references `curricula/<project>` with each
generated repository's target-project provenance, then reads the product's
declared package entry point. It also discovers installed products through
package metadata. No discovery path infers meaning from a `curriculum` suffix.
The runner contains no target knowledge.

Deployment preparation runs migrations and then imports each discovered
product's current packaged `data/curriculum.json`. This separates schema history
from content refreshes: a JSON-only change reaches the database without a dummy
migration, while the baseline importer continues to preserve human edits. The
same installation workflow collects Django static assets.
