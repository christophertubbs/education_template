# Work log

## 2026-09-11 — Source inspection

- Retrieved project-pivot SPEC.md through the GitHub connector; original retained in source/SPEC.original.md.
- Repository tree observed at 6aea0519d9297049f371952915b011f7a51ba7f4. SPEC blob: 41f3a10e5b0ddb54d901ca6e5455e52ca4988ece.
- Read repository agent instructions, style, prior status/tasks/decisions, artifact loader, validator, CLI, pipeline, configuration, scaffold, and content contract.
- Shared conversation URL could not be fetched. Personal-context retrieval recovered the user's proposal that Astra writes detailed Markdown and Sol serializes it. No unavailable assistant discussion is treated as evidence.
- Scope: specification refactor and downloadable handoff bundle; no upstream writes or application implementation.

## Decisions

- Preserve original requirements with a section-by-section migration map, plus explicit stage-specific amendments.
- Add a shared, versioned Markdown handoff contract. Free-form prose alone cannot carry deterministic scoring and complete field mappings reliably.
- Keep runtime requirements separately addressable, without making runtime development a third curriculum-generation stage.
- Authoring owns all substantive teaching, scientific judgments, examples, answer keys and review decisions. Serialization owns representation, validation and existing project assembly.
- Keep source evidence and concise decision rationales, not private internal deliberation.

## Observed integration risks

- Contract documents say 2.2; metadata constants have been reported as 2.1 in repository status. Verify directly before final report.
- Original spec lists twelve audit passes but calls them ten; preserve twelve and fix wording.
- Existing validator requires all coverage dimension values true, with no explicit not-applicable representation. Do not fabricate true values for unsupported applicability.
- Existing pipeline promotes after structural/source validation and Python compilation; broader release checks need an isolated staging workflow before production promotion.

## Draft checkpoint

Created the routed specification tree, preserved numbered requirements, added explicit ownership amendments, handoff grammar, serialization profile and paired illustrative fixtures. Saved draft-checkpoint.zip before final checks. Directly confirmed baseline branch commit and metadata mismatch. Inspected renderer/importer/grading code; recorded unconditional text normalization and non-atomic existing-product replacement as integration issues.

## Final review and validation

- Ran work/validate_delivery.py. First run found generated Python bytecode while checking source snapshots; fixed the checker to ignore bytecode and disabled further bytecode writes. Subsequent run passed.
- Preserved all 46 retained numbered sections (including 40.1); replaced original section 2 navigation explicitly. Checked 81 relative links, fixture metadata/prose/equation preservation and applicable original validator checks. Verified 26 source blob identities.
- Added exact validation limitations and remaining implementation issues to the delivered documentation. Full Django tests are not applicable to this specification-only change and were not run.
- Added concise stage invocation prompts. Updated existing agent navigation and appended durable status, tasks and decisions without deleting prior records.
- Final deliverable is a specification overlay and work archive; no upstream GitHub changes, production assembly or deployment.
