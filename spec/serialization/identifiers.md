# Identifiers and relationship integrity

Copy authored stable identifiers verbatim. Do not derive identity from sequence,
display titles, array position or a fresh slugification pass. Use separate IDs
for concepts, contracts, sections, lessons, glossary, terminology, sources,
assessments, questions and options. Existing persisted IDs take priority over a
new preferred naming convention. IDs must be nonempty and unique within their
entity namespace; cross-kind references must resolve in the intended namespace.

The baseline runtime uses identifier primary keys; check cross-product collision
behavior before installation of multiple products. Author new IDs with a stable
product prefix when needed to avoid collisions. The serializer never silently
renames existing IDs or assumes the display name is globally unique.

Prerequisite `source` is the dependent concept; `target` is its prerequisite.
Verify every relationship endpoint, prerequisite acyclicity and teaching order.
Verify section/lesson ownership, concept/contract mappings, source and glossary
links, terminology first introduction, question review lessons and eligibility,
and terminal-outcome coverage. A nonempty reference is not sufficient evidence
that it points to the right record.

Block and claim IDs remain in provenance maps if runtime objects lack their
fields. Option IDs must be unique within each item and stable under shuffling.
Question correctness must reference option identity, never presentation index.

For updates, supply an explicit ID change map and compatibility decision whenever
a semantic change requires a new ID. Retain semantically unchanged IDs and record
retired records. Check baseline conflict handling and progress compatibility;
never overwrite human edits or discard learner state to simplify serialization.
