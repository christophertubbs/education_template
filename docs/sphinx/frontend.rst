Templates and browser behavior
==============================

Template composition
--------------------

``base.html`` defines the accessible page shell, skip link, curriculum-aware
navigation, MathJax configuration/loading, CSS, and progress script.  Page
templates extend it:

* ``curriculum_list.html`` lists every loaded curriculum;
* ``curriculum_detail.html`` groups lessons by section and links assessments;
* ``lesson.html`` renders ordered semantic blocks, lesson definitions, sources,
  completion, and onward navigation;
* ``assessment.html`` renders form controls, embeds scoring JSON safely with
  Django ``json_script``, and loads assessment behavior;
* ``glossary.html`` and ``sources.html`` expose target knowledge and provenance;
* ``progress.html`` supplies local export, import, summary, and reset controls.

``content_block.html`` is the semantic block dispatcher.  It owns HTML for
paragraphs, headings, equations, code, callouts, examples, diagnostics, lists,
tables, definitions/principles, procedures, quotes, and source references.
``inline_content.html`` maps typed spans to prose, code, math, glossary links,
emphasis, file/command markup, and citations.  Adding a schema type requires
coordinated validator, template, styling, import/render, and accessibility work.

Assessment JavaScript
---------------------

``assessment.js`` reads the embedded question payload, scores option, numeric,
and normalized text answers in the browser, displays per-question feedback and
the aggregate score, exposes the next-navigation control, and appends attempts
to local progress when that API exists.  Answer options are shuffled server-side
before serialization.  Because scoring criteria are delivered to the browser,
this is deterministic self-assessment, not a secure proctored examination.

Progress JavaScript
-------------------

``progress.js`` stores one record per curriculum in the
``education-runtime-progress`` IndexedDB database.  A record contains schema and
curriculum versions, completed lessons, attempts, missed concepts, navigation
since the last pop quiz, and preferences.  Import rejects a mismatched schema,
curriculum identifier, or curriculum version.  Export downloads JSON; reset
requires browser confirmation.

Learning-navigation links increment a local counter.  Once at least one lesson
is complete and the configured cooldown is exceeded, the configured probability
can redirect navigation to the pop assessment with completed lesson IDs in the
query string.  The server uses those IDs to constrain the question bank.

CSS and accessibility
---------------------

``runtime.css`` supplies the shared visual language for navigation, focus,
semantic callouts, equations, code, tables, examples, definitions, forms, and
feedback.  It includes a skip link, visible focus, horizontal overflow for
technical content, a narrow-screen variable-table rule, and reduced-motion
handling.  Correct/incorrect status currently uses both text and styling.

``favicon.ico`` is the only binary authored asset under ``src`` and supplies the
site icon.  Browser-level WCAG verification remains a recorded follow-up; do not
infer conformance solely from template semantics and CSS rules.
