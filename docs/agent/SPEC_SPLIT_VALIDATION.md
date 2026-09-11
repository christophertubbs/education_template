# Specification refactor validation

Validated 2026-09-11 against inspected project-pivot commit
6aea0519d9297049f371952915b011f7a51ba7f4.

- All 46 retained numbered sections, including the separately headed 40.1, are
  present in exactly one designated owner file. Original section 2 navigation is
  explicitly replaced. The sole retained-text correction changes ten to twelve
  in the review-pass explanation; stage behavior changes are explicit amendments.
- All 81 relative Markdown links checked at validation time resolved.
- Paired fixture metadata, question prose and equation bytes match the expected
  JSON. Applicable original lesson and question validator checks pass.
- All 26 retrieved source snapshots match recorded GitHub blob IDs, allowing a
  single terminal newline added by text transport.
- No application code was changed. Full Django/runtime tests, package builds,
  whole-curriculum validation and production assembly were not run for this
  documentation-only task. Fixtures remain explicitly draft fragments.

The first documentation-check run encountered Python bytecode generated while
importing the reference validator. The snapshot checker was corrected to ignore
bytecode and imports now disable bytecode writing; the subsequent run passed.

The delivered archive contains the validation script and machine-readable result
under work/. The script requires PyYAML for fixture metadata. It is a bundle
check, not a production Markdown parser or full curriculum acceptance validator.
