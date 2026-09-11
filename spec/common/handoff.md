# Markdown handoff contract 1.0

## Ownership and versions

The Authoring Packet is the source of truth for instructional meaning. Runtime
JSON is a derived product. Existing accepted JSON curricula remain supported;
migrating them to this packet is a separate, explicitly reviewed operation.

Record `handoff_version: "1.0"` independently of curriculum schema version,
product version, generator revision and target revision. Record exact commits for
the generator/schema profile and Target Repository. A changed file invalidates
the acceptance of that file and any affected dependent records.

## Required packet

Paths are relative to `authored/<target>/`. Markdown files are substantive,
reviewable products, not outlines promising that another model will write them.

| Path | Required contents |
| --- | --- |
| `MANIFEST.md` | Packet identity/version; target URL, configured revision and resolved commit; generator commit; schema profile; product identity; learner baseline; required topics; ordered file inventory with SHA-256 hashes; stage status; review record pointers |
| `curriculum.md` | Curriculum title/description; exact section/lesson order; outcomes; entry assumptions; navigation and assessment policy values; publication scope |
| `knowledge-map.md` | Stable concepts, importance, category, description; typed relationships with explicit direction; entry-knowledge closure records |
| `mastery-contracts.md` | Stable contract and concept IDs; complete competencies; links to teaching and assessment evidence |
| `terminology.md` | Full terminology contracts, not glossary-only summaries |
| `glossary.md` | Stable entries, definitions, aliases, concept IDs and all lessons mentioning them |
| `sources.md` | Stable source records, complete citations, exact source locators, provenance and verification status |
| `claims.md` | Claim IDs; exact supporting source and locator; claim category; lesson/block or question/feedback location; verification and uncertainty |
| `lessons/<lesson-id>.md` | Complete ordered lesson prose and semantic content records with metadata and references |
| `assessments/<assessment-id>.md` | Kind, scope, selection count, time policy, eligible item IDs, concept/contract/outcome quotas and rationale |
| `questions/<question-id>.md` | Full prompt, options or accepted response, scoring policy, feedback and all relationships |
| `coverage.md` | Each required concept/dimension, applicability, status, lesson/block and item evidence, reviewer and unresolved issues |
| `completion.md` | Twelve pass records, terminal outcomes, audit evidence and unresolved required items |
| `decisions.md` | Concise accepted decisions, evidence, alternatives rejected when useful, assumptions and impact |
| `issues.md` | Stable issue ID, severity, affected records, owner stage, evidence, required resolution and status |
| `CHANGELOG.md` | Packet changes, invalidated reviews, identifier compatibility and regenerated dependencies |

Small packets may group question records in one Markdown file per assessment if
the manifest records each question ID and anchor exactly once. Questions eligible
for several assessments MUST NOT be copied into competing canonical records.

## Record grammar

Use UTF-8, LF and standard Markdown. Each file has exactly one YAML front matter
mapping bounded by `---` lines at its start. Use a safe data-only YAML parser:
no custom tags, duplicate mapping keys, aliases, executable values or implicit
timestamp objects. Quote versions, IDs, ambiguous scalars and date strings.
Use actual booleans and numbers only for typed fields. Metadata holds IDs,
relations, enums, scalar configuration and review state; detailed teaching stays
in the Markdown body. YAML is a metadata convention, not a new runtime input.

For multi-record reference files, each record begins with
`## Record: <stable-id>`. Its first fenced `yaml` block holds that record's
metadata. Prose fields use `### <field_name>` headings. Lists use Markdown lists;
ordered content MUST retain its order. A field must be defined exactly once.
Nested headings inside a prose field begin at level four. A literal line that
resembles a record delimiter must be fenced as content. Unknown fields or
ambiguous delimiters fail handoff validation rather than being ignored.

Lesson metadata uses the runtime lesson fields other than `content`; its body is
an ordered series of `## Block: <block-id> | <semantic-type>` records. Each block
has an optional first `yaml` fence for scalar metadata. Its body fields use
`### <field_name>` headings. A paragraph's `inline` field is ordinary Markdown
prose; code uses a language-tagged fence in its `code` field; equations use a
`latex` fence and a separate `accessible_text` field. Tables, variable tables,
examples and procedures retain their structured fields. See
[authoring examples](../authoring/examples.md).

Each ordered step or list item remains separate. A table uses a header row and
equal-width rows. Multiline or pipe-containing table cells use individually
numbered row/cell subsections instead of ambiguous Markdown pipe syntax. The
serializer rejects duplicate or missing cell numbers. Variable-table rows are
metadata records with explicit `terminology_identifier` and the fields required
by the schema profile; their `identifier` is the literal code/configuration
identifier, not a newly minted term ID.

Block IDs exist for fidelity tracking even when the target runtime has no block
ID field. Keep those IDs in the serialization map; do not add unsupported fields
to runtime objects. References and other packet-only material are preserved in
the packaged authoring/provenance files when not represented in runtime fields.

## Inline and content semantics

Ordinary prose, backtick code, emphasis and strong emphasis use normal Markdown.
For semantic distinctions not supplied by Markdown use `[label](kind:identifier)`:
`citation:source-id`, `glossary:glossary-id`, `file:exact-path`,
`command:exact-command`, or `math:math-id`. URI-encode reserved characters in
file/command targets and decode once. Never execute link targets. Glossary labels
and definitions come from authored glossary records. Math links refer to block
metadata `inline_math` records keyed by ID, with exact `latex`, `accessible_text`
and display `text`. They are lowered into inline math objects, not links.

Ordinary external links require an explicit mapping supported by the pinned
runtime; absent that, preserve their information as a source record plus citation
or raise an issue. Do not silently drop link destinations. Citations appear
adjacent to the claims they support. Each lesson has a `## References` section
listing the full used source records; it is metadata for bibliography/source
lowering, not an untyped lesson paragraph. Claims in prompts, feedback, captions
and worked steps are covered by the same rule.

Prose, numeric literals, signs, units, equation notation, source excerpts, option
wording, correct flags, tolerances, normalized answer sets, and instructional
order are protected content. Serialization may escape or encode them; it may not
rewrite, summarize, round, reorder, or remove them to fit the schema.

## Required metadata by entity

Use the field names and types in the pinned profile in
[serialization/schema.md](../serialization/schema.md). The author MUST supply
every substantive field; serialization can only fill values that are declared
mechanical derivations. Those derivations are: JSON escaping; ordered sequence
integers from explicit manifest order; manifest hashes; build timestamps and
tool-reported versions; wrapper keys; and explicit cross-reference expansion.
Defaults affecting teaching or assessment behavior require authored values.

For every terminology record supply: identifier, term, full_name, decomposition,
definition, purpose, role, units, dimensionality, valid_range, behavior with zero/
smaller/larger/limits, related_terms with distinctions, equation_relationships,
source_mappings, example, misconception, and lesson_identifiers. A pure theory
term without a code symbol must say so truthfully; if the current runtime forces
a nonempty code identifier or unsuitable role, log a schema incompatibility.

For every question supply type, difficulty, prompt, scoring data, correct and
incorrect feedback, review lesson, terminology/concept/mastery/assessment IDs,
and terminal outcomes. Option-level explanations may remain in instructor
records if the runtime cannot display them; required explanatory feedback still
must reach the learner. Unsupported essential semantics block publication.

## Acceptance and deterministic inspection

Each file has `status: draft | in_review | authoring_ready | blocked` and a
review record identifying reviewed content hash, review method, result and
remaining issues. Review means an actual performed content review; an automated
hash check is not a science, pedagogy or readability review. Record model-assisted
versus human review honestly.

Before handoff, verify all inventoried paths/hashes, unique IDs, known relation
targets, prerequisite acyclicity, ordered first use of terminology, required
fields, complete answer keys, claim/source closure and coverage evidence. All
publication-required files must be authoring_ready and all required issues
resolved. Source bytes and authoring review evidence remain available to the
serializer without repeating open-ended research.

The manifest hash inventory excludes the manifest itself to avoid self-reference;
the serializer records a separate hash of the complete accepted manifest. Hashes
are of exact UTF-8 file bytes, not normalized prose. Partial packets are useful
checkpoints but are not eligible for release. A serialization dry run may inspect
a partial packet and emit an issue report without marking it accepted.

## Stage-two return contract

Emit a serialization report with input manifest hash, exact schema profile,
output hashes, and one mapping per authored entity/block/field to a JSON Pointer
or a retained sidecar location. Every learner-required content field must have a
runtime destination; sidecar-only retention is insufficient for essential teaching.
For one-to-many lowering, record all pointers and the explicit rule. Compare
decoded output fields to the authored values, including math/code whitespace
where significant. Count matching records, missing records, duplicates and
unexpected additions. Counts supplement field comparisons; they do not replace them.

Issue records identify the exact file/anchor, expected field, observed defect,
whether it is authoring or schema/integration work, and the smallest requested
repair. Preserve accepted inputs. After a repair, rehash and revalidate affected
dependencies before resuming. Do not ask the frontier model to repeat completed
repository analysis merely because a JSON field is missing.
