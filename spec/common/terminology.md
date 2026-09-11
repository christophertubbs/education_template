# Terminology

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 4. Terminology

## 4.1 Generator

The **Generator** is the analysis and generation tooling contained within this repository.

It is responsible for:

* reading generation configuration;
* acquiring the Target Repository;
* resolving an exact source revision;
* analyzing code and documentation;
* discovering prerequisite knowledge;
* performing necessary external research;
* constructing a knowledge map;
* defining mastery requirements;
* generating and auditing curriculum content;
* generating assessments;
* generating or updating a Curriculum Product;
* validating curriculum completeness;
* recording provenance and generation metadata;
* creating or improving reusable generation skills when appropriate.

The Generator is not responsible for recreating the Education Runtime for each curriculum.

## 4.2 Education Runtime

The **Education Runtime** is the shared Django application that renders and executes Curriculum Products.

It owns generic educational behavior and generic data models.

The Education Runtime must support loading one or more Curriculum Products.

The Education Runtime may exist in this repository or in a separately versioned repository, but Curriculum Products must identify compatible runtime versions.

## 4.3 Target Repository

The **Target Repository** is the external Git repository identified by `project.json` and taught by a Curriculum Product.

Examples include:

* `t-route`;
* scientific modeling applications;
* web applications;
* libraries;
* command-line tools.

## 4.4 Curriculum Product

A **Curriculum Product** is an independently versioned and distributable package containing the complete educational content for one Target Repository.

A Curriculum Product may contain:

* structured lessons;
* glossary entries;
* assessments;
* worked examples;
* diagnostic exercises;
* source references;
* authoritative external references;
* concept and prerequisite graphs;
* mastery and coverage metadata;
* curriculum schema metadata;
* Django data migrations;
* packaged structured data;
* generation provenance;
* compatibility metadata for the Education Runtime.

A Curriculum Product should contain application code only when the Target Repository requires educational behavior that cannot reasonably be represented by the shared runtime.

## 4.5 Standalone Runner

A **Standalone Runner** is an optional thin Django host capable of loading the Education Runtime and one or more Curriculum Products.

The Standalone Runner exists for convenient independent deployment. It must not become the canonical home of curriculum-specific logic.

## 4.6 Learner

A **Learner** is a person using a Curriculum Product through the Education Runtime.

The expected Learner is a professional software developer who may not already understand:

* the Target Repository's implementation language;
* the Target Repository's framework;
* its scientific or mathematical domain;
* its runtime architecture;
* the numerical methods or physical models it implements.

The curriculum must not assume specialized domain expertise unless that expertise is explicitly configured as an entry prerequisite.

## 4.7 Skill

A **Skill** is a reusable, version-controlled procedure that teaches an agent how to perform a recurring class of work.

A Skill may include:

* concise discovery metadata;
* procedural instructions;
* references;
* scripts;
* schemas;
* examples;
* validation rules;
* failure and escalation conditions.

Skills are generation infrastructure. Target-specific facts belong in analysis artifacts or Curriculum Products rather than reusable Skills.

## 4.8 Assessment Item

An **Assessment Item** is the smallest independently and deterministically evaluated unit of an assessment.

Every scored Assessment Item must:

* test one or more explicitly identified curriculum concepts or Mastery Contract competencies;
* require a Learner response that can be evaluated programmatically by the Education Runtime without requiring an LLM, agent, external grading service, or human reviewer;
* define its scoring criteria completely within the Curriculum Product;
* provide or reference deterministic feedback appropriate to correct and incorrect responses.

Supported Assessment Item formats may include:

* multiple choice;
* multiple select;
* true/false where pedagogically appropriate;
* matching;
* ordering or sequencing;
* categorization;
* numeric response with explicitly defined tolerance;
* constrained text response with explicitly defined normalization and accepted answers;
* code-output prediction;
* source-code or component identification;
* structured diagnostic or reasoning responses;
* other formats for which correctness can be determined reliably and deterministically by the Education Runtime.

Free-form essays, unrestricted short answers, arbitrary code generation, unrestricted mathematical derivations, and other responses requiring subjective interpretation must not be required for scored assessments.

Complex reasoning should instead be assessed through carefully designed scenarios followed by one or more deterministically gradable Assessment Items.

A multipart scenario may contain multiple Assessment Items when each item requires a distinct Learner response and is independently scored.

Assessment Items must not be artificially divided into trivial subparts merely to increase an assessment's item count.

Conversely, multiple independently evaluated competencies must not be grouped into one nominal item merely to reduce the reported assessment size.

Unless otherwise specified, references to a **question** in this specification mean an Assessment Item.

---

# 22. Glossary

Each Curriculum Product must provide glossary content for important:

* repository-specific terms;
* acronyms;
* algorithms;
* framework terminology;
* scientific terminology;
* mathematical terminology;
* operational terminology.

Glossary entries should link to relevant lessons and concepts where practical.

A glossary is supplemental reference material and must not substitute for teaching a concept that is required for mastery.

---

## Two-stage terminology ownership

Authoring supplies every definition, example, unit, constraint, behavior,
misconception and contrast. Serialization preserves terminology contracts and
their first-use relationships exactly; it cannot infer missing meanings from
identifier spelling. A glossary summary alone does not satisfy a contract.

New workflow terms: Authoring Packet is the versioned Markdown source of teaching;
Serializer is the stage-two representation/assembly executor; Schema Profile is
the pinned combination of artifact, importer, renderer and grading capabilities;
Authoring Ready means substantively reviewed, not installable or released.
