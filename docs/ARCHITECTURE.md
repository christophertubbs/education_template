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

The runner supplies settings, URLs, ASGI, WSGI, SQLite defaults, and
environment-driven product discovery. It contains no target knowledge.
