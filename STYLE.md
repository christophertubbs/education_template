# Programming Style

Write direct, readable, typed Python following Django and Python conventions.
Prefer explicit control flow and small focused functions over clever compression
or speculative abstraction.

Use four spaces, descriptive names, public-function type annotations, and useful
docstrings. Avoid unexplained abbreviations and one-character names. Keep lines
near the configured 88-character limit without contorting readable code.

Separate concerns: views coordinate HTTP; services implement behavior; models
express generic persisted data and integrity; generator phases consume and
produce explicit artifacts; templates present data; client modules own
client-only persistence and interaction.

Use `pathlib`, context managers, immutable dataclasses where useful, and
argument-list subprocess calls. Never interpolate untrusted strings into shell
commands. Validate paths before access. Use Django ORM, migrations, URL
reversing, configured databases, static discovery, and accessible controls.

Use `logging` for diagnostics with parameterized messages. Never use `print()`
for application diagnostics or log secrets, credentials, private learner data,
or complete untrusted payloads.

Tests assert behavior and failure modes. Use temporary locations and clean
databases. Add regression tests where practical. Keep comments and documentation
accurate when behavior changes.
