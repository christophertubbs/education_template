# DECISIONS

## Shared runtime boundary

This repository is independently versioned and contains target-specific
knowledge only. Generic models, presentation, deterministic scoring, progress,
and administration belong to the Education Runtime. The product depends on the
runtime; the runtime does not depend on this product.

## Semantic lesson content

Lesson data contains typed blocks and inline spans rather than arbitrary HTML.
The runtime owns mathematical, code, table, example, callout, and glossary
presentation. Lesson-linked glossary entries provide visible definitions, and
human-modified runtime rows remain protected during baseline refreshes.
