# TASKS

## Complete

* Generate a standalone Django host project for the configured target
  repository. Requirements: `SPEC.md` sections 4-10, 32-35, 42. Verified with
  `manage.py check`, migrations, and route smoke tests.
* Generate an independent reusable curriculum app repository for `lstm`.
  Requirements: `SPEC.md` sections 9, 11-13, 29-34. Verified by editable
  installation, Django migrations, and packaged curriculum loading.
* Resolve and record exact target repository provenance. Requirements:
  `SPEC.md` sections 5, 16, 31-32. Resolved `master` to
  `9d21f2c2a5c93dae8a33796ed9bf63b790762e3c`.
* Generate improved curriculum, glossary, assessment, feedback, and coverage
  data. Requirements: `SPEC.md` sections 14-23. Verified by loader counts:
  7 longer lessons, 10 glossary entries, 10 assessments, 63 repository-only
  question records, 7 coverage records.
* Implement client-side progress persistence with export/import. Requirements:
  `SPEC.md` sections 24-28, 38. Implemented in generated static JavaScript.
* Fix lesson completion interaction. Requirements: `SPEC.md` sections 21,
  24-25, 36. Lesson completion now provides visible feedback and triggers the
  next related repository assessment.
* Fix section quiz navigation. Requirements: `SPEC.md` sections 21, 36. Each
  lesson has a unique section quiz; completing that quiz navigates to the next
  lesson.
* Generalize generated Django scaffold for other repositories. Requirements:
  `SPEC.md` sections 4, 7-13, 32-35. Generator now parameterizes app labels,
  URL namespaces, static paths, migrations, loader imports, progress storage,
  host import paths, generated README paths, and optional external curriculum
  content.

## Ready

* Add broader automated tests for generated output structure and a complete
  non-`lstm` fixture generation path.
* Expand curriculum depth further for hydrology prerequisites, CAMELS data
  interpretation, PyTorch recurrent-state mechanics, and NextGen operational
  failure modes.
* Add regeneration conflict tests that verify records marked
  `is_human_modified=True` are not overwritten by packaged curriculum loading.
* Add browser-level accessibility checks for keyboard navigation, assessment
  controls, and progress export/import.
