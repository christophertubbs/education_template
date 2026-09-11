# Serialization and product assembly activity

## Mission

Convert an accepted Markdown Authoring Packet into the system's five JSON
artifacts and an independently usable Curriculum Product, preserving all meaning.
GPT-5.6 is the intended executor; deterministic parsing, encoding, cross-reference
resolution, comparison and existing scaffolding take precedence over model work.

## Required reading and inputs

Read the root SPEC, [handoff](../common/handoff.md),
[schema](schema.md), [identifiers](identifiers.md),
[normalization](normalization.md), [validation](validation.md),
[project structure](project_structure.md), and [JSON examples](json_examples.md).
Consult common citations/terminology for preservation rules and lifecycle/runtime
requirements for provenance, installation, baseline conflicts and compatibility.

Required inputs are the accepted manifest and all inventoried files, project
configuration, pinned generator/schema/runtime capability profile, reviewed
prior identifiers/baselines if updating, and the authorized output location.

## Procedure

1. Verify manifest status, hashes, versions, required fields and absence of
   unresolved required issues. Record the exact input manifest hash.
2. Confirm the chosen schema profile against the checked-out generator, importer
   and renderer. If incompatible, emit a bounded issue; do not relabel metadata
   or alter a validator to make the packet appear supported.
3. Build a complete entity/reference index. Work in small deterministic batches
   by lesson or question file; preserve global references via that index.
4. Lower typed metadata and semantic Markdown into the five artifact objects.
   Preserve words, units, equations, citations, answer flags and sequence.
   Use a JSON encoder, not manually escaped string assembly.
5. Emit the entity/block/field-to-JSON-Pointer map and retained authoring records.
   Compare every protected field after decoding JSON. Reject omissions, duplicate
   records, unexplained additions and unsupported semantic content.
6. Validate all five objects together, verify source references at the authored
   target commit, and perform the release checks in validation.md.
7. Use existing product templates/scaffolding in an isolated staging workflow.
   Verify the package and runtime behavior before promoting production output.
8. Save output hashes, exact commands/results, failed checks, schema decisions
   and release status. Preserve the authoring packet and mappings with provenance.

## Allowed and forbidden repairs

Allowed: JSON escaping, deterministic syntax conversion, resolving explicit IDs,
derived sequence numbers, build metadata, and repairs to the serializer's own
incorrect mapping that do not change the accepted packet.

Forbidden: changing answers, tolerances, factual claims, terminology definitions,
difficulty, coverage applicability, assessment quotas, or instructional order;
inventing citations; summarizing explanations; padding banks; treating omitted
content as optional; marking an authoring review performed by the serializer.

Schema defects belong to integration work. Content defects belong to authoring.
Both return exact file/anchor/field issues. A structurally valid but incomplete
curriculum is blocked, not a successful serialization.
