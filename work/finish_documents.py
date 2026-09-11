"""Add task-specific amendments and expected handoff examples.

TODO: AI-written by Codex; review and replace before adopting as project tooling.
"""

from pathlib import Path
import json
import yaml

ROOT: Path = Path('deliverable')
additions: dict[str, str] = {
 'spec/common/source_handling.md': '''
## Stage-specific inspection policy

Authoring inventories paths and sizes before reading bulk content. Exclude
generated artifacts, vendored dependencies, binaries, caches and repetitive data
from full-text inspection unless a stated teaching question requires them.
For CSV/JSON/NetCDF or other data/config collections, inspect representative
schema, dimensions, headers and bounded samples first. Record selection rationale,
limits and omissions. Do not read thousands of similar files to discover the same
shape repeatedly; expand only when concrete differences affect a claim.

Save reusable source inventories, exact file/symbol/line locators and consulted
reference summaries with claims. Serialization verifies the supplied source map
at the accepted commit; it does not restart repository exploration or open-ended
research. Failed links and conflicting evidence return to authoring with exact
locations. Target checkouts remain read-only evidence.

Record the requested ref and resolved commit separately. A later branch head is
not the accepted source. Do not let an assembly command silently re-resolve a
moving branch and label old authored material with a new commit. Use a resolved
commit in the assembly configuration and preserve the originally requested ref
in packet provenance.
''',
 'spec/common/terminology.md': '''
## Two-stage terminology ownership

Authoring supplies every definition, example, unit, constraint, behavior,
misconception and contrast. Serialization preserves terminology contracts and
their first-use relationships exactly; it cannot infer missing meanings from
identifier spelling. A glossary summary alone does not satisfy a contract.

New workflow terms: Authoring Packet is the versioned Markdown source of teaching;
Serializer is the stage-two representation/assembly executor; Schema Profile is
the pinned combination of artifact, importer, renderer and grading capabilities;
Authoring Ready means substantively reviewed, not installable or released.
''',
 'spec/authoring/review.md': '''
## Authoring acceptance gate

Review all twelve passes with evidence, not a checklist copied into complete
state. Every required outcome and major contract needs sufficient teaching and
assessment links. Check prerequisite closure, full depth, model criticism,
terminology first use, source fidelity, valid examples and answer keys, bank
variation, accessibility and contextual readability. Record reviews against
content hashes and identify the review method honestly.

Resolve defects while progress is possible. If an applicable requirement cannot
be fulfilled, preserve the partial product with exact unresolved items. If a
dimension genuinely does not apply, record the scientific/pedagogical reason and
review it; unknown is not inapplicable. Do not claim JSON, migrations, package or
runtime tests ran during authoring. Those are serialization/release checks.
''',
 'spec/serialization/project_structure.md': '''
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
''',
 'spec/serialization/validation.md': '''
## Stage-two release gates and current gaps

Run gates in order and record exact commands, versions, results and limitations.
All required gates must pass before production promotion; a blocked candidate is
still a useful handoff artifact.

1. Packet acceptance: verify file hashes, reviewed statuses, required fields,
   evidence and unresolved issues. Rejected inputs remain unchanged.
2. Serialization fidelity: compare protected decoded fields, references, order,
   equations/code, option flags, units and tolerances against authoring; verify
   every entity/block/field has a declared runtime or provenance destination.
3. Structural validation: use load_artifacts and validate_artifacts on all five
   JSON files. Add contract checks absent from the baseline validator: every
   cross-reference kind, exactly-one-answer constraints, finite numeric values,
   pop upper limit, full question scope and declaration/evidence consistency.
4. Source validation: verify exact target commit, paths and line ranges with
   validate_source_references. Citation existence is not claim support; retained
   authoring review must establish that support. Ensure learner-visible citations
   remain adjacent and complete source information remains accessible.
5. Assessment behavior: verify actual browser grading for every used item type,
   normalization, empty input, tolerances and option identity under shuffling.
   Check that selected attempts can satisfy every required quota/outcome/section
   and have meaningful variation. The current greedy selector can fail on a
   particular ordering even when a feasible selection exists; exercise the actual
   selection path and report the limitation rather than equating bank size with
   feasibility. Do not weaken authored quotas to evade selection failure.
6. Product/runtime integration: verify Python syntax, wheel build and package
   installation, entry-point discovery, compatible runtime, Django system checks,
   migration drift, clean database migration, explicit curriculum refresh,
   repeated import and human-baseline conflict preservation as applicable.
7. Rendering/accessibility: render every used block/inline type and representative
   full lessons and assessments; inspect equations, code, tables, definitions,
   citations, feedback and keyboard/timing controls. Hidden but retained JSON
   fields do not count as learner-visible content.
8. Final review: evaluate retained §46, archive completeness, independent product
   use, documentation links, provenance, identifier/progress compatibility and
   all unresolved items. Mark release complete only now.

Use the repository's documented commands for applicable implementation tests:
`python manage.py test`, `python manage.py check`,
`python manage.py makemigrations --check --dry-run`, and a clean isolated
installation workflow. Package build needs its declared build dependencies;
report missing dependencies without claiming success. Documentation-only changes
do not require application tests; validate their links, retained requirements,
examples and archive instead.

Known baseline limitations requiring explicit handling include schema labels,
not-applicable coverage, pure-concept terminology roles/source mappings,
unsupported figures/nesting, fixed heading levels, plaintext citation links,
unconditional text normalization, weak structural checks, non-transactional
replacement of existing product files, and insufficient built-in pre-promotion
checks. These are implementation observations, not authoring exemptions.
''',
 'spec/serialization/normalization.md': '''
## Inspected text-grading limitation

At the baseline commit, the browser always uses trim, toLocaleLowerCase and
whitespace collapse. It ignores configurable normalization data retained by the
importer. Record this exact behavior in the profile. Other authored policies
require integration changes; merely serializing a normalization field cannot
make the browser obey it.
''',
}
for relative, addition in additions.items():
    path: Path = ROOT / relative
    path.write_text(path.read_text(encoding='utf-8') + addition, encoding='utf-8')

# Expected fixtures are explicit constructions, not a claimed general serializer.
lesson_path: Path = ROOT / 'examples/handoff/lesson.md'
lesson_parts: list[str] = lesson_path.read_text().split('---', 2)
lesson: dict[str, object] = yaml.safe_load(lesson_parts[1])
lesson.pop('handoff_version')
lesson.pop('status')
body: str = lesson_parts[2]
variables_yaml: str = body.split('## Block: demo-variables | variable_table')[1].split('```yaml')[1].split('```')[0]
equation: str = body.split('```latex\n')[1].split('\n```')[0]
lesson['content'] = [
 {'type':'paragraph','inline':[{'type':'text','text':'This is an invented arithmetic example. An amount and a rate answer '},{'type':'strong','text':'different questions'},{'type':'text','text':'.'}]},
 {'type':'variable_table', **yaml.safe_load(variables_yaml)},
 {'type':'equation','variable_identifiers':['demo-amount','demo-duration','demo-rate-term'],'caption':'Average rate for the invented interval','latex':equation,'accessible_text':'The average rate r equals amount A divided by duration t: twelve meters divided by four seconds is three meters per second.'},
 {'type':'paragraph','inline':[{'type':'text','text':'The calculation describes the average during this interval. It does not tell us whether the amount arrived steadily or in a short burst.'}]},
]
(ROOT / 'examples/handoff/lesson.expected.json').write_text(json.dumps(lesson, indent=2) + '\n')
question_parts: list[str] = (ROOT / 'examples/handoff/question.md').read_text().split('---', 2)
question: dict[str, object] = yaml.safe_load(question_parts[1])
question.pop('handoff_version')
question.pop('status')
for part in question_parts[2].split('### ')[1:]:
    name, value = part.split('\n', 1)
    question[name.strip()] = value.strip()
(ROOT / 'examples/handoff/question.expected.json').write_text(json.dumps(question, indent=2) + '\n')
