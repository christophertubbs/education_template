# Curriculum Structure

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 9. Knowledge Map

Before complete lesson generation begins, the Generator must construct a machine-readable knowledge map.

The knowledge map must identify, where applicable:

* repository components;
* major symbols and code paths;
* algorithms;
* data formats;
* protocols;
* frameworks and libraries;
* build and deployment concepts;
* mathematical concepts;
* scientific concepts;
* numerical methods;
* physical models;
* configuration concepts;
* operational concepts;
* performance concepts;
* known defects and limitations;
* prerequisite relationships.

Major concepts must have stable identifiers.

Relationships between concepts must be explicit enough to support ordering, prerequisite analysis, coverage auditing, and regeneration.

---

# 10. Recursive Prerequisite Discovery

Every concept required to understand another concept must itself be taught unless it is part of the configured entry knowledge.

Prerequisite discovery must recurse until the dependency graph is closed against the assumed Learner baseline.

For example, if a routing method depends upon understanding a conservation equation, and understanding that equation depends upon derivatives, flux, and control-volume reasoning, the Generator must ensure those concepts are either configured prerequisites or taught before the routing method.

The Generator must not use statements such as "by the standard derivation" or "using familiar numerical methods" to hide required knowledge that the Learner has not been taught.

Prerequisite material may be scoped to the depth necessary for the Target Repository, but it must be sufficient for later reasoning rather than superficial vocabulary recognition.

---

# 11. Mastery Contract

Every major curriculum concept must have an explicit **Mastery Contract** defining what successful understanding means.

A Mastery Contract should identify applicable competencies such as the ability to:

* define the concept;
* explain why it exists;
* explain how it relates to neighboring concepts;
* use it correctly;
* derive or justify relevant mathematics;
* map it to source code;
* recognize valid and invalid use;
* diagnose failures involving it;
* compare alternatives;
* predict qualitative behavior.

Lesson generation and assessment generation must be driven by these competencies.

A concept must not be marked complete merely because explanatory text exists.

---

# 14. Repository and Implementation Understanding

The curriculum must connect abstract concepts to the actual Target Repository.

Where applicable, curriculum coverage must include:

* repository purpose;
* design philosophy;
* architecture;
* source layout;
* major modules and components;
* runtime lifecycle;
* important call paths;
* data flow;
* memory and ownership behavior where relevant;
* concurrency and parallelism where relevant;
* algorithms;
* external interfaces;
* configuration;
* persistence and storage;
* build system;
* installation;
* testing;
* debugging;
* logging;
* performance behavior;
* resource-use characteristics;
* common failure modes;
* known limitations;
* known critical defects;
* contribution workflow.

The curriculum must explicitly map major theoretical concepts to implementation files, symbols, and code paths where possible.

---

# 17. Curriculum Coverage Matrix

The Generator must maintain a machine-readable coverage matrix.

For each major concept, the matrix must indicate coverage of applicable dimensions, including at minimum:

* foundational explanation;
* prerequisite closure;
* theory or conceptual basis;
* mathematics;
* assumptions;
* implementation mapping;
* source evidence;
* operational behavior;
* limitations;
* failure modes;
* bias or error reasoning;
* worked examples;
* diagnostic exercises;
* assessment coverage;
* terminology closure;
* readability review.

A concept may only be marked complete when every required applicable dimension is complete.

The coverage matrix must be used as a generation control mechanism. Missing required coverage must trigger additional generation or explicit unresolved-status reporting rather than being silently accepted.

---
