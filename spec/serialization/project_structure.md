# Project Structure

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 23. Curriculum Product Representation

Curriculum Products must be independently versioned and reproducibly installable into the Education Runtime.

The canonical content representation may use:

* Django data migrations;
* packaged structured data;
* generated Python modules;
* fixtures;
* management-command inputs;
* or another deterministic representation.

Django data migrations are explicitly supported as a first-class mechanism for producing independently versioned curriculum products.

A Curriculum Product should avoid defining its own generic education models. It should populate models owned by the Education Runtime unless a concrete target-specific requirement makes additional models necessary.

A fresh installation must be able to reconstruct the intended generated curriculum deterministically from the Curriculum Product repository alone plus its declared Education Runtime dependency.

---

# 24. Curriculum Product Repository Structure

Each Curriculum Product must be capable of existing as an independent Git repository.

A conceptual product may resemble:

```text
<target>-curriculum/
├── pyproject.toml
├── README.md
├── SPEC.md
├── AGENTS.md
├── curriculum_product/
│   ├── __init__.py
│   ├── apps.py
│   ├── migrations/
│   └── data/
├── provenance/
│   ├── generation.json
│   ├── coverage.json
│   └── source-map.json
└── tests/
```

The exact layout may differ according to packaging needs.

A Curriculum Product must not require access to the Generator repository after generation.

---

# 37. Generated Documentation

Every Curriculum Product must contain enough documentation to install, load, validate, update, and continue development without access to the Generator repository.

Documentation should include, where applicable:

* `README.md`;
* `SPEC.md` describing product-specific scope where useful;
* `AGENTS.md` for continued agent-assisted maintenance;
* installation instructions;
* migration instructions;
* testing instructions;
* Education Runtime compatibility;
* Target Repository provenance;
* regeneration provenance;
* known unresolved curriculum issues.

The Education Runtime and Standalone Runner must maintain their own independent documentation.

---

# 38. Git and Product Independence

Each Curriculum Product must be independently versionable and distributable.

Curriculum Products may be maintained as independent Git repositories.

A Standalone Runner or deployment repository may reference Curriculum Products using Python dependencies, Git submodules, package releases, or another documented mechanism.

A Curriculum Product's internal Git history must not be silently absorbed into an unrelated host repository.

After successful initial generation, a newly created Curriculum Product repository should:

1. use a configured initial branch, defaulting to `main`;
2. stage generated files;
3. record generation metadata;
4. create an initial generation commit where automated commit behavior is enabled;
5. remain independently cloneable and usable with a compatible Education Runtime.

The Generator must not modify global Git configuration merely to make automated commits possible.

---

## Current assembly procedure and required handoff retention

Keep configuration `project.json` separate from authored Markdown, reviewed five
JSON artifacts and generated packages. With the current default paths, authoring
lives in `authored/<target>/`, reviewed JSON in `curricula/<target>/`, target
checkouts in `repository/<target>/`, and product output in
`generated/<target>-curriculum/`. Respect configured curriculum_source_path.

The actual package layout uses `src/<curriculum_product_name>/`, with apps.py,
migrations and data/curriculum.json, plus root pyproject.toml, README.md, agent
documents, tests and provenance. Use the existing product templates and the
education_curriculum.products entry point. Do not generate a bespoke Django
runtime or assume a root-level curriculum_product directory is mandatory.

Before invoking the existing command `python -m education_generator --project
<configuration-file>`, prepare an isolated generator workspace and an explicit
configuration pointing at validated JSON and the authored exact target commit.
The CLI has only --project in the inspected revision; --author, --serialize,
--validate-only and --no-promote are not implemented. Its normal pipeline
promotes output and may make local Git commits according to configuration.
Use the isolated output for all package/database/rendering checks before an
intentional production promotion. Do not point trial runs at accepted products.

Assembly requires an explicit metadata profile resolving the 2.1/2.2 mismatch.
The existing scaffold compiles Python but does not perform all required release
checks or package the new Markdown packet automatically. Stage two must include
the accepted packet under provenance/authoring/, the serialization field map and
validation report under provenance/, and ensure their paths are listed in the
deliverable archive. Inspect wheel/package-data rules before claiming these
sidecars are also installed resources. An archive can retain provenance outside
the wheel, but its availability must be documented.

Copy the root specification together with its linked spec/ subtree whenever
product agent documents reference it, or emit a self-contained product-specific
contract with valid links. Copying only the new router would break the existing
copy_agent_documents behavior. No generated product may depend on missing paths
in the Generator repository after distribution.

Perform clean installation with a declared compatible runtime; apply migrations,
explicitly refresh packaged curricula through load_curricula, then collectstatic.
Use an isolated database for verification. Product documentation must explain
installation, runtime compatibility, source commit, regeneration, validation and
baseline conflicts. Honor automated_commit and use repository-local Git identity;
never push or publish merely because local assembly finished.
