  Regenerate both the CFE and SAC-SMA Curriculum Products in this repository.

  Configuration files:

  - `cfe.project.json` configures CFE.
  - `project.json` configures SAC-SMA.

  Before working, follow `AGENTS.md`. Read the relevant parts of `SPEC.md`,
  `STYLE.md`, `docs/agent/STATUS.md`, `docs/agent/TASKS.md`,
  `docs/agent/DECISIONS.md`, the current Git status and diff, and recent relevant
  history. Preserve all existing user changes. Target repositories under
  `repository/` are read-only evidence.

  First, strengthen the durable generation requirements so this problem cannot
  recur. Update `SPEC.md`, `src/education_generator/CONTENT_SCHEMA.md`, generator
  validation, and tests as necessary to enforce the following requirements:

  Audience:

  - Assume a professional C++ or Python developer.
  - Assume no prior hydrology, hydrologic-modeling, Fortran, numerical-modeling,
    or Earth-science knowledge beyond secondary-school algebra.
  - Write ordinary explanatory prose at approximately a US grade 8–10 reading
    level.
  - Use short sentences and introduce one unfamiliar idea at a time.
  - Preserve the required scientific and mathematical depth. Lower reading level
    must mean clearer teaching, not omitted mathematics.

  Required instructional order:

  1. Explain the physical or software idea in ordinary language.
  2. Give a concrete example or carefully bounded analogy.
  3. Introduce the precise technical term.
  4. Define every variable, parameter, unit, and constraint.
  5. Present and derive the equation step by step.
  6. Map the equation to exact source identifiers and code paths.
  7. Translate relevant implementation logic into familiar C++ and Python
     concepts.
  8. Explain assumptions, limitations, failure signatures, and common mistakes.

  Terminology closure:

  Do not use a domain term, acronym, abbreviation, mathematical symbol, parameter,
  state variable, flux, source identifier, or implementation-specific phrase
  before teaching it.

  Create or extend machine-readable terminology data so every specialized item has
  a stable record. Each record must provide, where applicable:

  - full or expanded name;
  - decomposition of the abbreviated source name;
  - plain-language definition;
  - why the item exists;
  - semantic role: input, parameter, state, flux, intermediate, configuration, or
    output;
  - units and dimensionality;
  - expected or valid range;
  - meaning of zero, larger values, smaller values, and important limiting values;
  - comparison with similarly named or related quantities;
  - governing-equation relationships;
  - exact source-code identifier and commit-pinned source location;
  - a small numerical or concrete example;
  - a likely misconception.

  An acronym expansion alone is not an adequate definition. A definition that
  depends on other unexplained domain words is incomplete. A glossary entry
  elsewhere does not satisfy first-use teaching.

  Add explicit `terminology_closure` and `readability_review` coverage dimensions
  and completion gates, or equivalent enforceable state. Validation must fail if:

  - a specialized item is missing from the terminology inventory;
  - an acronym is not expanded on first use;
  - a variable appears in an equation or example before it is defined;
  - a definition is circular or merely restates the source name;
  - related identifiers are not distinguished;
  - a parameter lacks role, units, range, behavior, or source mapping;
  - assessments use terminology not taught beforehand;
  - the readability and jargon audits have not completed;
  - unresolved terminology remains.

  Automated readability scores may support review, but do not use them as the only
  evidence. Source names and equations can distort those scores.

  SAC-SMA requirements:

  Teach all important model parameters, states, and fluxes individually. In
  particular, give a complete explanation of:

  - `PCTIM`: permanently impervious area fraction;
  - `ADIMP`: additional area fraction that becomes increasingly
    runoff-producing as wetness increases;
  - how the name `ADIMP` is formed from “additional” and “impervious”;
  - what “impervious” means in plain language;
  - `ADIMC`: the water-depth state controlling wetness over the additional
    impervious area;
  - `PAREA = 1 - ADIMP - PCTIM`;
  - the differences among `PCTIM`, `ADIMP`, `ADIMC`, and `PAREA`;
  - their units, ranges, invariants, equations, source locations, and behavior
    under dry, intermediate, and wet conditions;
  - a numerical example showing how they affect runoff.

  Apply the same standard to all other SAC-SMA identifiers, including the upper
  and lower tension/free-water stores, ET terms, runoff components, percolation,
  primary and supplemental baseflow, recession coefficients, HRU aggregation,
  timesteps, and mass-balance variables.

  Explain why the BMI driver is required. Teach its lifecycle, forcing exchange,
  time control, resource ownership, and framework role. Translate Fortran syntax,
  mutation, allocation, indexing, derived types, type-bound methods,
  `INTENT`, `ASSOCIATE`, `ISO_C_BINDING`, `BIND(C)`, and opaque pointers into C,
  C++, and Python concepts.

  CFE requirements:

  Apply the same first-use and terminology-contract rules to all CFE scientific
  and implementation vocabulary. Fully teach and distinguish rainfall
  partitioning, Schaake and Xinanjiang parameters, soil and groundwater storage,
  conceptual reservoirs, evapotranspiration, infiltration excess, GIUH routing,
  Nash cascades, lateral flow, mass balance, BMI lifecycle, configuration, units,
  and source identifiers. Do not assume that a software developer already
  understands any hydrologic term.

  For both curricula:

  - Reinspect the exact configured target revisions and use commit-pinned source
    evidence.
  - Do not execute arbitrary target-repository code merely for analysis.
  - Preserve explicit generation phases and fail closed.
  - Include rich structured content: definitions, variable tables, equations,
    code, comparisons, worked examples, diagnostic cases, and callouts.
  - Explain every equation symbol before using the equation.
  - Preserve units through every derivation and worked example.
  - Include cases where the model should work well, where assumptions are
    stressed, and where the formulation is inappropriate.
  - Ensure assessment questions and feedback use only previously taught language.
  - Questions must test reasoning, diagnosis, source tracing, translation,
    parameter behavior, and model criticism—not primarily vocabulary recall.
  - Perform a fresh jargon/first-use audit and a readability review after content
    generation.
  - Do not mark any coverage field or completion pass complete without supporting
    content.

  Generate both products using their configuration files. The intended commands
  are equivalent to:

      PYTHONPATH=src python -m education_generator --project cfe.project.json
      PYTHONPATH=src python -m education_generator --project project.json

  Do not overwrite human-modified generated content or promote over a dirty
  generated repository. Report any baseline conflict or unresolved requirement
  instead of hiding it.

  Before completion, validate both products comprehensively:

  - artifact and terminology validation;
  - commit-pinned source-reference validation;
  - focused and full tests;
  - Ruff formatting and lint;
  - Django system checks;
  - migration-drift checks;
  - clean-database migration tests for each product;
  - package installation and wheel builds;
  - generated-product tests;
  - representative curriculum, lesson, glossary, source, assessment, and progress
    routes;
  - clean Target Repository and generated-product Git status.

  Inspect representative rendered lessons from both products to confirm that a new
  participant can understand terminology at first use. Do not rely solely on the
  structural validator.

  Update `docs/agent/STATUS.md` and `docs/agent/TASKS.md` with exact revisions,
  generated-product commits, validation commands and results, failures, blockers,
  and the next action. Record durable architecture or schema decisions in
  `docs/agent/DECISIONS.md`.

  Continue until both regenerated curricula satisfy the revised requirements and
  are promoted successfully, or until a genuine unresolved blocker must be
  reported.
