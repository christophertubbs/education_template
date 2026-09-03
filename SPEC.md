# Product Specification

## 1. Purpose

This application generates independent educational Django applications from a configured target Git repository.

Each generated educational application must teach the target repository deeply enough that a professional software developer can independently inspect, explain, build, diagnose, modify, and contribute to the target repository.

Generated curricula must cover both:

* the target repository itself; and
* prerequisite knowledge required to understand it.

Prerequisite knowledge may include:

* programming languages;
* frameworks;
* libraries;
* protocols;
* build systems;
* algorithms;
* mathematics;
* scientific concepts;
* data formats;
* deployment technologies;
* operational behavior.

The generated educational application must provide structured lessons, assessments, source references, progress tracking, and administrative editing.

---

# 2. Terminology

## 2.1 Generator

The **Generator** is this repository and the tooling contained within it.

It is responsible for:

* reading generation configuration;
* acquiring the Target Repository;
* analyzing source code and documentation;
* researching prerequisite concepts when necessary;
* creating a curriculum;
* generating Django applications;
* validating generated output;
* creating and maintaining generated Git repositories.

---

## 2.2 Target Repository

The **Target Repository** is the external Git repository identified by `project.json`.

The generated curriculum teaches the Target Repository.

Examples include:

* `t-route`;
* scientific modeling applications;
* web applications;
* libraries;
* command-line tools.

---

## 2.3 Generated Host Project

The **Generated Host Project** is the standalone Django project created under:

`./generated/education`

It contains the Django project-level configuration required to run generated Curriculum Apps together as a standalone educational website.

It is responsible for concerns such as:

* Django settings;
* root URL configuration;
* ASGI configuration;
* WSGI configuration;
* shared navigation;
* shared styles and static resources;
* database configuration;
* Django administration;
* integration of Curriculum Apps.

The Generated Host Project must not contain domain functionality required by individual Curriculum Apps.

---

## 2.4 Curriculum App

A **Curriculum App** is a reusable Django application generated for one Target Repository.

A Curriculum App contains the educational functionality for that repository, including:

* lessons;
* glossary entries;
* assessments;
* models;
* migrations;
* views;
* URLs;
* templates;
* static resources;
* administrative interfaces;
* packaged curriculum data;
* source references.

Each Curriculum App must be independently installable into another Django project.

---

## 2.5 Generated Project

A **Generated Project** is the complete generated educational system consisting of:

* the Generated Host Project; and
* one or more Curriculum Apps.

---

## 2.6 Learner

A **Learner** is a person using a generated educational application.

The expected Learner is a professional software developer who may not already understand:

* the Target Repository's implementation language;
* the Target Repository's framework;
* the Target Repository's scientific or mathematical domain;
* the Target Repository's runtime architecture.

The curriculum must not assume domain expertise unless the relevant knowledge has already been introduced.

---

# 3. Learning Outcomes

After completing the curriculum and passing the final examination, a Learner should be able to:

* clearly explain the Target Repository's purpose and design philosophy;
* explain the major architectural components;
* explain the full application lifecycle;
* identify the source code responsible for major behaviors;
* determine which code should be modified for common changes;
* build and install the Target Repository;
* diagnose common build failures;
* diagnose common runtime failures;
* trace failures through relevant code paths;
* understand important operational behavior;
* understand major performance characteristics;
* understand known implementation gotchas;
* understand critical known defects or technical limitations;
* understand enough of each major technology used by the Target Repository to contribute meaningfully;
* verify technical claims made by the curriculum against source code and authoritative references.

The curriculum must also teach the domain knowledge required to understand the Target Repository.

For scientific or mathematical repositories, the Learner must understand the scientific and mathematical logic necessary to explain the implementation.

For example, if understanding an algorithm requires knowledge of mathematical integration and the Learner cannot reasonably be expected to know integration, the curriculum must teach enough integration for the Learner to understand the algorithm and its implementation.

---

# 4. Generator Input

## 4.1 project.json

Generation is controlled by a file named:

`project.json`

The file must identify at least:

* the Target Repository name;
* the Target Repository Git URL;
* the configured revision;
* the generated Curriculum App package name;
* a human-readable display name.

A minimal conceptual structure is:

```json
{
    "name": "t-route",
    "repository_url": "https://github.com/NOAA-OWP/t-route.git",
    "revision": "main",
    "curriculum_app_name": "t_route",
    "display_name": "t-route"
}
```

The exact schema may be expanded as necessary.

Potential optional configuration may include:

* description;
* excluded paths;
* required curriculum topics;
* source documentation URLs;
* additional authoritative references;
* build instructions;
* source repository submodule behavior;
* expected learner prerequisites;
* generated project settings.

The generator must validate `project.json` before generation begins.

---

## 4.2 Repository Names

Target Repository names must not be assumed to be valid Python package names.

For example:

`t-route`

is a valid Git repository name but not a valid Python module identifier.

The generator must derive or accept a valid Python package identifier while preserving the original repository name for display.

---

# 5. Target Repository Acquisition

The Target Repository must be stored under:

`./repository/<repository-name>`

If the repository is not already present, the Generator must clone it.

If the repository already exists, the Generator must fetch available remote changes before analysis.

The Generator must not silently discard local modifications in the Target Repository checkout.

The configured revision may represent:

* a branch;
* a tag;
* an exact commit.

Before analysis begins, the Generator must resolve the configured revision to an exact Git commit identifier.

The resolved commit must be recorded in generated metadata.

Generated curriculum must always be traceable to an exact Target Repository revision.

---

# 6. Generation Lifecycle

Generation must proceed through defined stages.

The expected lifecycle is:

1. load and validate `project.json`;
2. acquire or update the Target Repository;
3. resolve the exact Target Repository revision;
4. analyze source code and repository documentation;
5. identify prerequisite knowledge;
6. research required external concepts where necessary;
7. construct a curriculum plan;
8. generate curriculum content;
9. generate assessment material;
10. generate or update the Curriculum App;
11. generate or update the Generated Host Project;
12. validate generated Django code;
13. validate curriculum coverage;
14. initialize or update generated Git repositories;
15. record generation metadata;
16. promote successful output into its final location.

Generation should occur in a temporary or staging workspace where practical.

Incomplete or failed generation must not be treated as a valid completed Generated Project.

---

# 7. Intermediary Work

Reusable Python and shell tooling used by the Generator must be stored under:

`./src`

Significant development and generation actions should be reproducible through code stored within the repository.

One-off scratch code does not need to be retained.

The Generator should avoid relying on undocumented manual procedures for important generation behavior.

---

# 8. Generated Repository Structure

If no Generated Host Project exists under:

`./generated/education`

the Generator must create one.

The Generated Host Project must itself be an independent Git repository.

A conceptual structure is:

```text
generated/
└── education/
    ├── .git/
    ├── standalone/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── t-route/
    ├── another-repository/
    ├── manage.py
    └── README.md
```

The exact package layout may differ where required by Django packaging conventions.

---

# 9. Curriculum App Repositories

Each Curriculum App must be created as its own independent Git repository.

For example:

`./generated/education/t-route`

must be a distinct Git repository from:

`./generated/education`

Curriculum Apps may be tracked by the Generated Host Project as Git submodules.

The Generated Host Project must not directly absorb the internal Git history of Curriculum Apps.

When Curriculum Apps are tracked as submodules, the Generated Host Project must contain valid `.gitmodules` configuration.

Generated documentation must explain how to initialize and update submodules.

---

# 10. Generated Host Project Requirements

The Generated Host Project must:

* operate as a valid standalone Django project;
* discover or configure installed Curriculum Apps;
* provide shared navigation;
* provide shared styling where appropriate;
* provide Django settings;
* provide root URL configuration;
* provide ASGI and WSGI entry points;
* provide static-file configuration;
* provide database configuration;
* expose the Django administrative interface.

The standalone project should remain a thin host.

Reusable curriculum and domain behavior must reside in Curriculum Apps.

---

# 11. Curriculum App Reusability

Each Curriculum App must be independently installable into another Django project.

A consuming Django project must be able to:

1. install the Curriculum App as a Python dependency;
2. add the app to `INSTALLED_APPS`;
3. include the app's URL configuration;
4. run its migrations;
5. load its packaged curriculum data;
6. access its administrative interfaces where Django admin is enabled.

The Curriculum App must not import or otherwise depend upon the Generated Host Project.

Dependency direction must be:

`Generated Host Project -> Curriculum App`

and never:

`Curriculum App -> Generated Host Project`

Reusable resources must be namespaced, including:

* URLs;
* templates;
* static assets;
* settings;
* template tags where applicable.

---

# 12. Database Behavior

Curriculum Apps must use Django's configured database facilities.

They must not require a specific database backend unless explicitly documented.

The Generated Host Project may use SQLite by default for standalone deployment.

When installed into another Django service, Curriculum Apps must use the host project's configured database.

---

# 13. Packaged Curriculum Data

Lessons, assessments, glossary entries, and related educational content must ultimately be available in the database.

A fresh installation must be able to populate the curriculum deterministically from content contained within the Curriculum App repository.

The Curriculum App repository must therefore contain the canonical generated curriculum content or another deterministic representation sufficient to rebuild database state.

The implementation may use mechanisms such as:

* packaged structured data;
* management commands;
* fixtures;
* data migrations;
* other documented import mechanisms.

The generated repository must remain self-contained.

---

# 14. Curriculum Content

The curriculum must teach the Target Repository from foundational concepts through implementation detail.

Curriculum structure should include, where applicable:

* introduction;
* repository purpose;
* development philosophy;
* prerequisite programming knowledge;
* prerequisite framework knowledge;
* prerequisite scientific or mathematical knowledge;
* architecture;
* source layout;
* runtime lifecycle;
* major components;
* algorithms;
* data flow;
* external interfaces;
* configuration;
* persistence;
* build system;
* installation;
* testing;
* debugging;
* logging;
* performance;
* common failure modes;
* known limitations;
* known critical defects;
* contribution workflow.

---

# 15. Prerequisite Discovery

The Generator must identify prerequisite knowledge necessary to understand the Target Repository.

Prerequisites may include:

* languages;
* libraries;
* frameworks;
* algorithms;
* scientific concepts;
* mathematics;
* protocols;
* storage technologies;
* data formats;
* build tools;
* deployment technologies.

When prerequisite knowledge cannot reasonably be assumed of a general professional software developer, the curriculum must teach enough of that prerequisite to support understanding of the Target Repository.

Prerequisites should be introduced before curriculum content that depends upon them.

---

# 16. Source Traceability

Technical claims about the Target Repository should be traceable to supporting evidence whenever practical.

Generated curriculum should retain provenance including:

* Target Repository revision;
* relevant source files;
* relevant symbols;
* relevant line ranges where useful;
* repository documentation;
* authoritative external references.

Learners should be able to inspect supporting source references for important technical claims.

The Target Repository at the recorded revision should be treated as authoritative when curriculum descriptions conflict with actual source behavior.

---

# 17. External Research

The Generator may use authoritative external sources when the Target Repository itself does not contain enough information to teach prerequisite or domain knowledge.

Preferred source order is:

1. official project documentation;
2. standards and formal specifications;
3. primary scientific literature;
4. official framework and library documentation;
5. reputable secondary sources.

External claims should retain citations or provenance where practical.

---

# 18. Hallucination Awareness

The curriculum must explicitly teach Learners how to verify claims.

Learners should be taught to:

* inspect relevant source code;
* inspect repository history where useful;
* consult official documentation;
* consult authoritative external references;
* identify conflicts between curriculum statements and source behavior;
* prefer verified source behavior over unsupported generated explanations.

The generated curriculum must not present unverifiable generated assumptions as unquestionable fact.

---

# 19. Curriculum Coverage

The Generator must maintain traceability between important Target Repository concepts and curriculum material.

Significant components, algorithms, technologies, and domain concepts must map to one or more lessons.

Important concepts should also map to one or more assessment questions.

Critical or difficult components must not be omitted merely because they are difficult to explain.

---

# 20. Glossary

Each Curriculum App must provide a glossary.

Glossary entries should include important:

* repository-specific terms;
* acronyms;
* algorithms;
* framework terminology;
* scientific terminology;
* mathematical terminology;
* operational terminology.

Glossary entries should link back to relevant curriculum material where practical.

---

# 21. Assessments

The curriculum must contain:

* randomized review pop quizzes;
* section quizzes;
* one mid-curriculum examination;
* one final examination.

Assessment questions must only test concepts already taught unless a question explicitly provides enough information to test reasoning rather than recall.

---

## 21.1 Pop Quizzes

Pop quizzes must:

* draw only from previously taught material;
* be somewhat randomized;
* be timed by default;
* vary question order where practical;
* vary answer order where appropriate;
* avoid excessive immediate repetition.

Pop quiz timing must be configurable or disableable for accessibility purposes.

Pop quizzes may use concepts the Learner previously answered incorrectly more frequently.

---

## 21.2 Section Quizzes

Each major curriculum section must contain a quiz covering material taught in that section.

Section quizzes should verify meaningful understanding rather than simple memorization.

---

## 21.3 Mid-Curriculum Examination

The curriculum must contain a mid-curriculum examination covering material taught in the first major portion of the curriculum.

---

## 21.4 Final Examination

The curriculum must contain a final examination covering the complete curriculum.

Passing the final examination represents successful curriculum completion.

Passing criteria must be configurable.

---

# 22. Assessment Feedback

Incorrect answers must provide useful explanatory feedback.

Feedback should explain:

* why the submitted answer was incorrect;
* why the correct answer is correct;
* what concept the question is testing;
* what curriculum material should be reviewed.

Where useful, assessment feedback should link to relevant lessons or glossary entries.

---

# 23. Assessment Randomization

Assessment systems should draw from sufficiently large question pools to reduce memorization based solely on question order.

Randomization may include:

* question selection;
* question order;
* answer order.

Randomization must not make questions ambiguous or misleading.

---

# 24. Learner Progress

User accounts must not be required.

Learner progress and preferences must be stored client-side.

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

---

# 25. Progress Data

Persisted Learner data may include:

* completed lessons;
* section progress;
* quiz attempts;
* quiz scores;
* exam attempts;
* exam scores;
* glossary progress;
* accessibility preferences;
* review history;
* missed concepts.

Persisted data must use stable identifiers.

Identifiers must not depend solely on display order.

---

# 26. Progress Versioning

Client-side progress data must be versioned.

Curriculum sections, lessons, assessments, and questions that participate in persisted state must have stable identifiers.

Generated application updates should preserve compatible progress whenever practical.

When stored progress becomes incompatible with a newer curriculum version, the application must handle the situation explicitly rather than silently corrupting or discarding progress.

---

# 27. Progress Export and Import

Learners must be able to export their progress to a portable file.

Learners must be able to restore progress from a previously exported file.

This functionality must not require a user account.

---

# 28. Client-Side Asset Updates

Deployment of new client-side assets must not erase persisted Learner progress.

Normal page reloads and application updates must preserve compatible progress.

Client-side assets may be updated independently of stored Learner progress.

---

# 29. Administrative Editing

Lessons, glossary entries, quizzes, examinations, questions, answers, and feedback should be editable through the Django administrative interface.

Curriculum content must be stored in models suitable for administrative editing.

---

# 30. Human-Modified Curriculum

Curriculum content modified by an administrator after generation must not be silently overwritten during later regeneration.

The system must distinguish between:

* generated baseline content; and
* human-modified content.

Regeneration conflicts must be detectable.

The implementation may use version metadata, content fingerprints, explicit override flags, or another reliable mechanism.

---

# 31. Regeneration

Generated Curriculum Apps must record the exact Target Repository revision used during the most recent successful generation.

When generation occurs against a newer Target Repository revision, the Generator should determine the differences between:

* the previously analyzed revision; and
* the new revision.

The Generator should update curriculum material affected by relevant source changes.

Existing unaffected curriculum should be preserved where practical.

Human modifications must not be silently overwritten.

Regeneration should preserve stable curriculum identifiers where concepts remain equivalent.

---

# 32. Generated Metadata

Each generated repository should contain machine-readable generation metadata.

Metadata should include, where applicable:

* Generator name;
* Generator version;
* generation timestamp;
* Target Repository name;
* Target Repository URL;
* configured revision;
* resolved Target Repository commit;
* generated package name;
* curriculum schema version;
* template version.

Structured metadata should use a machine-readable format such as JSON.

---

# 33. Generated Documentation

Every generated repository must contain sufficient documentation to build, install, run, test, and continue development without requiring access to the Generator repository.

Generated documentation should include, where applicable:

* `README.md`;
* `AGENTS.md`;
* `SPEC.md`;
* `STYLE.md`;
* build instructions;
* installation instructions;
* migration instructions;
* testing instructions;
* Git submodule instructions;
* generation provenance.

---

# 34. Generated Repository Git Initialization

After successful generation and validation, generated repositories must:

1. be initialized as independent Git repositories;
2. use `main` as the initial branch unless configured otherwise;
3. stage generated files;
4. create an initial generation commit;
5. record generation metadata;
6. remain independently cloneable and usable.

The Generator must not modify global Git configuration merely to make automated commits possible.

Repository-local Git identity may be configured when necessary.

---

# 35. Generated Project Validation

A Generated Project must not be considered successfully generated solely because files were produced.

Generated Django applications must pass appropriate validation.

Validation should include, where applicable:

* Python syntax validation;
* Django system checks;
* migration consistency checks;
* automated tests;
* static analysis;
* formatting checks;
* package installation checks;
* validation that Curriculum Apps can be imported independently of the Generated Host Project.

Validation failures must prevent incomplete output from being treated as a successful generated release.

---

# 36. User Interface

Generated educational applications must provide clear navigation through:

* curriculum sections;
* lessons;
* assessments;
* glossary entries;
* progress information.

Learners should be able to revisit previously completed material.

Current progress should be visible.

Important source references should be accessible without requiring the Learner to manually locate the referenced code.

---

# 37. Tone

Curriculum tone should be:

* friendly;
* colloquial;
* technically rigorous;
* approachable without being patronizing.

Occasional unexpected examples, humor, challenge questions, or changes in presentation may be used to restore attention.

Such material must not:

* reduce technical accuracy;
* demean the Learner;
* introduce irrelevant offensive material;
* make assessments intentionally misleading;
* interfere with accessibility.

---

# 38. Accessibility

Generated educational applications should meet WCAG 2.2 AA expectations where practical.

Core functionality must be usable by keyboard.

Core learning and assessment functionality must not depend solely upon:

* color;
* sound;
* hover interactions;
* animation.

Timed activities must provide a mechanism for disabling or extending timing for accessibility purposes without requiring a user account.

---

# 39. Networking

The application may use asynchronous networking functionality where it improves responsiveness or operational behavior.

WebSockets may be used where a concrete feature requires persistent bidirectional communication.

WebSockets are not required merely for ordinary lesson navigation, assessment interaction, or client-side progress storage.

Other mechanisms such as standard HTTP requests or Server-Sent Events may be used where more appropriate.

---

# 40. Security

Generated applications and Generator tooling must treat external input as untrusted.

The Generator must prevent:

* path traversal outside configured generation roots;
* unsafe shell command construction;
* accidental credential storage;
* accidental inclusion of secrets in generated repositories;
* silent execution of arbitrary Target Repository code where not explicitly required.

User-supplied project names and paths must be validated.

Generated repositories must not contain secrets, private keys, access tokens, or environment-specific credentials.

---

# 41. Non-Goals

The generated curriculum is not intended to:

* replace the Target Repository's authoritative source code;
* replace official upstream documentation;
* require a user account;
* require a centralized progress-tracking service;
* hide source evidence from Learners;
* silently overwrite human-authored curriculum changes;
* assume that current generated explanations are infallible.

---

# 42. Completion Criteria

Generation is complete only when:

* the configured Target Repository revision has been resolved;
* required repository analysis has completed;
* prerequisite knowledge has been identified;
* curriculum content has been generated;
* curriculum coverage has been validated;
* required assessments exist;
* source provenance has been recorded;
* the Curriculum App is independently installable;
* the Generated Host Project can load the Curriculum App;
* generated Django validation passes;
* generated Git repositories are valid;
* generated documentation is sufficient for independent use;
* generation metadata has been recorded.

A generated application must be independently usable without access to the Generator repository.
