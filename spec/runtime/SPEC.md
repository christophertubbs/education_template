# Spec

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 25. Education Runtime Requirements

The shared Education Runtime must provide generic functionality for:

* curriculum registration and discovery;
* sections and lessons;
* rich curriculum content;
* glossary entries;
* assessments;
* questions, answers, and feedback;
* source references;
* progress reporting;
* administration;
* shared navigation and styling;
* stable curriculum identifiers;
* curriculum-version awareness;
* import and migration validation;
* accessibility behavior.

The Education Runtime must not contain Target Repository-specific educational content except for fixtures or examples used to test the runtime itself.

The Education Runtime should support one or more installed Curriculum Products without product-specific source changes.

Each installable Curriculum Product must advertise its Django application with
the standard `education_curriculum.products` Python package entry-point group.
The Standalone Runner must discover every advertised installed product
automatically before Django constructs `INSTALLED_APPS`. Migration and server
launch commands must not require a per-product environment variable or settings
edit. A legacy explicit package list may remain as an additive compatibility
path, but it must not disable automatic discovery.

When the Standalone Runner executes from the generator repository, it must also
discover local products by cross-referencing project directories under
`curricula/` with the `target_repository_name` provenance of repositories under
`generated/`. A local product is eligible only when both sides exist. Discovery
must use declared metadata and must not require the generated repository,
Curriculum Product, package, or curriculum identifier to contain the word
`curriculum` or follow another inferred naming convention.

---

# 26. Optional Standalone Runner

A thin Standalone Runner may be provided for convenient local or independent deployment.

The Standalone Runner may provide:

* Django settings;
* root URL configuration;
* ASGI and WSGI configuration;
* database defaults;
* static-file configuration;
* administration;
* discovery of installed Curriculum Products.

Installed-product discovery must be deterministic, reject malformed or
conflicting advertisements, and fail clearly before migration or server startup
rather than silently omitting an available curriculum.

Local project discovery must likewise be deterministic. It must reject multiple
generated repositories that claim the same reviewed curriculum project and
must not activate a generated repository that has no matching `curricula/`
project directory.

The Standalone Runner must not duplicate curriculum content or generic Education Runtime behavior.

A default standalone deployment may use SQLite.

The existence of a Standalone Runner must not prevent Curriculum Products from being installed into another compatible Django service.

---

# 27. Database Behavior

The Education Runtime must use Django's configured database facilities.

Curriculum Products must not require a specific database backend unless explicitly documented and justified.

Curriculum data should be represented through generic runtime models where practical.

Curriculum Product migrations must be deterministic and safe to apply according to documented compatibility requirements.

Installation and deployment preparation must not assume that curriculum content
changes always require a new schema migration. After applying migrations, the
Standalone Runner must explicitly import the current packaged
`data/curriculum.json` from every discovered Curriculum Product through the
conflict-preserving baseline importer. The installation workflow must also run
Django static-file collection so current runtime and product assets are ready
for service.

---

# 28. Learner Progress

User accounts must not be required.

Learner progress and preferences must be capable of being stored client-side.

Progress must survive:

* page reloads;
* navigation between curriculum pages;
* browser restarts;
* temporary loss of network connectivity.

Progress must not depend solely on:

* tab-local session state;
* volatile JavaScript memory;
* cookies.

A persistent browser storage mechanism such as IndexedDB may be used.

Persisted Learner data may include:

* completed lessons;
* concept mastery state;
* section progress;
* quiz attempts and scores;
* exam attempts and scores;
* glossary progress;
* accessibility preferences;
* review history;
* missed concepts.

Persisted data must use stable identifiers that do not depend solely on display order.

---

# 29. Progress Versioning and Portability

Client-side progress data must be versioned.

Curriculum sections, lessons, concepts, assessments, and questions that participate in persisted state must have stable identifiers.

Curriculum Product updates should preserve compatible progress whenever practical.

When stored progress becomes incompatible with a newer curriculum version, the Education Runtime must handle the situation explicitly rather than silently corrupting or discarding progress.

Learners must be able to export progress to a portable file and restore progress from a previously exported file without requiring a user account.

Deployment of new client-side assets must not erase compatible Learner progress.

---

# 30. Administrative Editing and Generated Baselines

Lessons, glossary entries, quizzes, examinations, questions, answers, and feedback should be editable through the Django administrative interface where practical.

The system must distinguish between:

* the generated baseline supplied by a Curriculum Product; and
* human modifications made after installation.

A later Curriculum Product update must not silently overwrite human-modified content.

Conflicts must be detectable and surfaced explicitly.

The implementation may use version metadata, stable identifiers, content fingerprints, override records, or another reliable mechanism.

---

# 40. User Interface

The Education Runtime must provide clear navigation through:

* curricula;
* curriculum sections;
* lessons;
* concepts;
* assessments;
* glossary entries;
* progress information;
* source references.

Learners must be able to revisit previously completed material.

Current progress should be visible.

Important source references should be accessible without requiring the Learner to manually locate referenced code.

The interface should support the presentation of equations, source excerpts or links, diagrams, worked examples, diagnostic scenarios, and comparisons between methods where required by Curriculum Products.

# 42. Accessibility

The Education Runtime should meet WCAG 2.2 AA expectations where practical.

Core functionality must be usable by keyboard.

Core learning and assessment functionality must not depend solely upon:

* color;
* sound;
* hover interactions;
* animation.

Timed activities must provide a mechanism for disabling or extending timing without requiring a user account.

Mathematical and scientific material should be represented in accessible forms where practical.

---

# 43. Networking

The Education Runtime may use asynchronous networking where it improves responsiveness or operational behavior.

WebSockets may be used when a concrete feature requires persistent bidirectional communication.

WebSockets are not required merely for lesson navigation, assessment interaction, or client-side progress storage.

Standard HTTP requests, Server-Sent Events, or other simpler mechanisms should be preferred where appropriate.

Curriculum Products should not introduce networking requirements unless their educational content genuinely requires them.

---
