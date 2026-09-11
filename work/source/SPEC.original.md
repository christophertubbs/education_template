# Product Specification

## 1. Purpose

This repository defines a system for producing deeply technical educational curricula from configured target Git repositories.

The system is intentionally split into two major concerns:

1. a reusable **Education Runtime** that provides the Django application, user interface, persistence, assessment behavior, progress tracking, administration, and curriculum rendering; and
2. independently versioned **Curriculum Products** that contain the knowledge, lessons, assessments, provenance, and database population logic for a specific Target Repository.

The Generator must not recreate a complete Django application for every Target Repository when equivalent behavior can be provided by the shared Education Runtime.

The primary generated artifact is therefore a Curriculum Product, not a bespoke educational website.

A Curriculum Product must teach its Target Repository deeply enough that a successful Learner can independently inspect, explain, build, diagnose, modify, evaluate, and contribute to the Target Repository. For scientific, mathematical, engineering, or modeling software, the Learner must also understand the governing domain concepts deeply enough to evaluate when the implementation is appropriate, when its assumptions are violated, how those violations affect results, and what forms of bias or failure should be expected.

The system must prioritize durable knowledge extraction and validated curriculum design over repeated generation of application boilerplate.

---

# 2. Specification Navigation

This specification is the authoritative product contract.

Agents and developers should read the sections relevant to the current task rather than repeatedly loading the entire specification. Requirements identified by referenced sections remain binding even when those sections are not loaded into the active working context.

Reading only task-relevant sections is a context and computational optimization. It does not exempt generated work from compliance with the complete specification.

## 2.1 Navigation by Task

| Task or Concern                                                                        | Primary Sections                                                                  | Supporting Sections                                                                                   |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Understand the system architecture and responsibilities                                | Purpose; Design Principles; Terminology                                           | Non-Goals                                                                                             |
| Determine required Learner competency                                                  | Terminal Learning Outcomes                                                        | Mastery Contract; Required Depth; Model Criticism and Failure Reasoning                               |
| Configure a generation                                                                 | Generator Input                                                                   | Terminology; Target Repository Acquisition and Revision Control                                       |
| Acquire and resolve the Target Repository                                              | Target Repository Acquisition and Revision Control                                | Generator Input; Generation Metadata; Source Traceability and Evidence                                |
| Plan or orchestrate the complete generation process                                    | Generation Architecture                                                           | Multi-Pass Generation and Auditing; Machine-Readable Completion State; Completion Criteria            |
| Analyze repository architecture and implementation                                     | Knowledge Map; Repository and Implementation Understanding                        | Source Traceability and Evidence; Intermediate Artifacts                                              |
| Discover required prerequisite knowledge                                               | Recursive Prerequisite Discovery                                                  | Generator Input: Entry Knowledge; Knowledge Map; Mastery Contract                                     |
| Define what constitutes mastery                                                        | Mastery Contract                                                                  | Terminal Learning Outcomes; Curriculum Coverage Matrix; Assessment Requirements                       |
| Analyze scientific, mathematical, or numerical concepts                                | Required Depth for Major Scientific, Mathematical, and Numerical Concepts         | Model Criticism and Failure Reasoning; External Research; Source Traceability and Evidence            |
| Analyze model validity, failure, bias, and inappropriate use                           | Model Criticism and Failure Reasoning                                             | Required Depth; Terminal Learning Outcomes; Assessment Requirements                                   |
| Perform external technical or scientific research                                      | External Research                                                                 | Source Traceability and Evidence; Hallucination Resistance and Uncertainty                            |
| Establish source provenance and verify claims                                          | Source Traceability and Evidence                                                  | External Research; Hallucination Resistance and Uncertainty; Generation Metadata                      |
| Determine whether curriculum coverage is complete                                      | Curriculum Coverage Matrix                                                        | Mastery Contract; Machine-Readable Completion State; Completion Criteria                              |
| Generate or review lessons and curriculum structure                                    | Knowledge Map; Recursive Prerequisite Discovery; Mastery Contract; Required Depth | Multi-Pass Generation and Auditing; Curriculum Coverage Matrix                                        |
| Generate assessments                                                                   | Assessment Requirements; Assessment Feedback                                      | Assessment Item terminology; Mastery Contract; Curriculum Coverage Matrix                             |
| Implement deterministic assessment behavior                                            | Assessment Item terminology; Assessment Requirements                              | Education Runtime Requirements; Assessment Feedback                                                   |
| Audit curriculum quality and identify gaps                                             | Multi-Pass Generation and Auditing                                                | Curriculum Coverage Matrix; Machine-Readable Completion State; Completion Criteria                    |
| Track generation progress and unresolved work                                          | Machine-Readable Completion State                                                 | Intermediate Artifacts; Hallucination Resistance and Uncertainty; Completion Criteria                 |
| Build a Curriculum Product                                                             | Curriculum Product Representation; Curriculum Product Repository Structure        | Database Behavior; Generation Metadata; Git and Product Independence                                  |
| Develop or modify the shared Django application                                        | Education Runtime Requirements                                                    | Database Behavior; Learner Progress; Progress Versioning and Portability; User Interface              |
| Build a standalone deployment                                                          | Optional Standalone Runner                                                        | Education Runtime Requirements; Database Behavior; Networking; Security                               |
| Implement database and migration behavior                                              | Database Behavior; Curriculum Product Representation                              | Validation; Regeneration and Incremental Updates                                                      |
| Implement Learner progress persistence                                                 | Learner Progress; Progress Versioning and Portability                             | Education Runtime Requirements; User Interface; Accessibility                                         |
| Implement administrative curriculum editing                                            | Administrative Editing and Generated Baselines                                    | Regeneration and Incremental Updates; Progress Versioning and Portability                             |
| Regenerate curriculum after Target Repository changes                                  | Regeneration and Incremental Updates                                              | Source Traceability and Evidence; Generation Metadata; Intermediate Artifacts; Validation             |
| Record generation provenance                                                           | Generation Metadata                                                               | Source Traceability and Evidence; Regeneration and Incremental Updates                                |
| Create or improve reusable agent procedures                                            | Reusable Skills and Agent Procedure Capture                                       | Frontier, Local, and Deterministic Work Allocation; Intermediate Artifacts                            |
| Decide whether work belongs to frontier models, local models, or deterministic tooling | Frontier, Local, and Deterministic Work Allocation                                | Reusable Skills and Agent Procedure Capture; Intermediate Artifacts                                   |
| Persist expensive or reusable analysis                                                 | Intermediate Artifacts                                                            | Reusable Skills and Agent Procedure Capture; Regeneration and Incremental Updates                     |
| Handle uncertainty, contradictory evidence, or possible hallucination                  | Hallucination Resistance and Uncertainty                                          | Source Traceability and Evidence; External Research; Machine-Readable Completion State                |
| Generate supporting documentation                                                      | Generated Documentation                                                           | Generation Metadata; Curriculum Product Repository Structure                                          |
| Create and maintain independent Git repositories                                       | Git and Product Independence                                                      | Curriculum Product Repository Structure; Regeneration and Incremental Updates                         |
| Validate a Curriculum Product                                                          | Validation                                                                        | Curriculum Coverage Matrix; Machine-Readable Completion State; Completion Criteria                    |
| Implement Learner-facing presentation                                                  | User Interface                                                                    | Education Runtime Requirements; Learner Progress; Accessibility; Tone                                 |
| Generate or review instructional writing style                                         | Tone                                                                              | Accessibility; Required Depth                                                                         |
| Implement accessibility requirements                                                   | Accessibility                                                                     | User Interface; Assessment Requirements; Learner Progress                                             |
| Implement networking behavior                                                          | Networking                                                                        | Education Runtime Requirements; Security                                                              |
| Review security requirements                                                           | Security                                                                          | Target Repository Acquisition and Revision Control; External Research; Networking                     |
| Determine what the system explicitly should not do                                     | Non-Goals                                                                         | Purpose; Design Principles                                                                            |
| Decide whether generation is finished                                                  | Completion Criteria                                                               | Validation; Machine-Readable Completion State; Curriculum Coverage Matrix; Terminal Learning Outcomes |

## 2.2 Cross-Cutting Requirements

Some requirements apply across multiple generation stages and should be consulted whenever they materially affect the current task.

In particular:

* **Terminal Learning Outcomes** define the ultimate competency the curriculum must produce.
* **Source Traceability and Evidence** applies whenever technical or scientific claims are generated.
* **Hallucination Resistance and Uncertainty** applies whenever evidence is incomplete, contradictory, or interpretive.
* **Accessibility** applies to Learner-facing functionality and assessments.
* **Security** applies to Generator tooling, Target Repository interaction, external content, generated products, and runtime behavior.
* **Generation Metadata** applies whenever generation results are persisted or released.
* **Validation** defines executable checks that must succeed before release.
* **Completion Criteria** defines the final authority for whether a Curriculum Product may be considered complete.

## 2.3 Full-Specification Review

Task-local reading must not replace final whole-product review.

Before a Curriculum Product is declared complete:

* all applicable requirements in this specification must be considered;
* the complete **Completion Criteria** must be evaluated;
* the complete **Validation** requirements must be evaluated;
* every **Terminal Learning Outcome** must have sufficient instructional and assessment support;
* unresolved required fields must remain explicitly unresolved rather than being silently accepted;
* cross-cutting requirements such as provenance, security, accessibility, progress compatibility, and hallucination resistance must be reviewed;
* conflicts between task-specific instructions, generated Skills, intermediate artifacts, and this specification must be resolved in favor of this specification unless the specification itself has been explicitly changed.

The navigation guidance in this section exists to reduce unnecessary context loading. It must never be interpreted as permission to ignore requirements outside the currently loaded subset.

---

# 3. Design Principles

## 3.1 Shared behavior belongs in the Education Runtime

Functionality that does not materially vary between Target Repositories should be implemented once in the Education Runtime.

Examples include:

* Django models representing generic curriculum concepts;
* lesson rendering;
* glossary presentation;
* assessment execution;
* question randomization;
* scoring;
* progress tracking;
* client-side progress persistence;
* administrative editing;
* shared navigation;
* accessibility behavior;
* common templates and static assets;
* curriculum import and validation;
* source-reference presentation.

Curriculum Products must not duplicate these facilities without a documented requirement.

## 3.2 Generated products should primarily contain knowledge, not application infrastructure

The Generator should produce structured curriculum content, source mappings, assessments, metadata, and deterministic database population logic.

Where Django data migrations are a suitable representation, a Curriculum Product may consist primarily of migrations and packaged supporting data that populate Education Runtime models.

The Generator must not repeatedly generate equivalent views, models, templates, URLs, or JavaScript merely because a new Target Repository is being taught.

## 3.3 Expensive reasoning should create reusable leverage

High-capability model compute should be concentrated on work that genuinely requires substantial reasoning, such as:

* repository understanding;
* scientific and mathematical analysis;
* prerequisite discovery;
* architectural reconstruction;
* identifying assumptions and validity regimes;
* identifying model-form limitations and expected biases;
* designing mastery requirements;
* resolving contradictory evidence;
* reviewing and auditing curriculum completeness;
* discovering reusable analysis procedures.

Routine transformation, formatting, structured expansion, deterministic validation, and repetitive implementation should be delegated to ordinary code or lower-cost/local models where practical.

## 3.4 Completion must be defined structurally

The Generator must not consider a curriculum complete merely because it has produced a plausible quantity of prose.

Completion must be determined from explicit mastery requirements, prerequisite closure, concept coverage, source traceability, assessment coverage, and machine-readable completion criteria.

---

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

# 5. Terminal Learning Outcomes

After completing a Curriculum Product and passing its final examination, a Learner must be able to perform the outcomes applicable to the Target Repository.

The Learner should be able to:

* clearly explain the Target Repository's purpose and design philosophy;
* explain its major architectural components;
* explain its full application or model lifecycle;
* trace important runtime and data-flow paths through the source;
* identify the source code responsible for major behaviors;
* determine which code should be modified for common changes;
* build and install the Target Repository;
* diagnose common build and runtime failures;
* distinguish symptoms from root causes;
* understand major performance characteristics and resource-use behavior;
* identify important implementation gotchas, defects, and technical limitations;
* understand enough of each major technology to contribute meaningfully;
* verify curriculum claims against source code and authoritative references;
* evaluate alternative implementation or modeling approaches where relevant.

For scientific, numerical, mathematical, or engineering repositories, successful completion must additionally allow the Learner to:

* explain the physical or mathematical phenomena represented by each major model;
* explain or derive the governing equations at the level required to understand the implementation;
* identify assumptions and approximations made by each major method;
* explain why those assumptions are made;
* identify the intended regime of validity;
* identify conditions where the method becomes inaccurate, unstable, biased, or physically inappropriate;
* predict the likely direction and qualitative character of errors caused by violated assumptions;
* distinguish input-data error, parameter error, calibration error, discretization error, numerical error, implementation error, and structural model error;
* compare the implemented approach with reasonable alternatives;
* explain why one model or numerical method may outperform another under particular physical conditions;
* connect theoretical quantities and equations directly to concrete implementation symbols and code paths;
* inspect suspicious output and form technically defensible hypotheses about why the model behaved that way.

The intended standard is not familiarity. The intended standard is sufficient understanding to reason critically about the Target Repository and its outputs without depending upon generated explanations as an oracle.

---

# 6. Generator Input

## 6.1 `project.json`

Generation is controlled by `project.json`.

The file must identify at least:

* Target Repository name;
* Target Repository Git URL;
* configured revision;
* Curriculum Product package or identifier;
* human-readable display name.

A minimal conceptual structure is:

```json
{
    "name": "t-route",
    "repository_url": "https://github.com/NOAA-OWP/t-route.git",
    "revision": "main",
    "curriculum_product_name": "t_route_curriculum",
    "display_name": "t-route"
}
```

Optional configuration may include:

* description;
* excluded paths;
* explicitly required topics;
* source documentation URLs;
* authoritative external references;
* known build instructions;
* source repository submodule behavior;
* assumed learner prerequisites;
* desired curriculum emphasis;
* runtime compatibility requirements;
* standalone packaging behavior;
* generation model or execution policy.

The Generator must validate `project.json` before generation begins.

## 6.2 Entry knowledge

Assumed Learner knowledge must be explicit where it materially affects prerequisite generation.

The Generator must not silently assume undergraduate or graduate-level domain education merely because the Target Repository implements scientific software.

If no domain prerequisites are configured, the default assumption is a competent professional software developer with general programming knowledge but no specialized scientific or mathematical training beyond ordinary secondary-school mathematics.


## 6.3 Learner Language and Terminology Contract

Unless configured otherwise, the Learner is proficient in general-purpose
software development but has no specialized knowledge of the Target
Repository's scientific domain, mathematical notation, numerical methods, or
implementation language.

Ordinary explanatory prose should target approximately a United States grade
8–10 reading level. This requirement does not apply mechanically to source
code, equations, citations, or unavoidable proper names.

The curriculum must use progressive disclosure:

1. explain the idea in ordinary language;
2. provide a concrete example or analogy;
3. introduce the precise technical term;
4. define its variables, units, and constraints;
5. present the mathematics;
6. map the mathematics to source code;
7. translate relevant implementation logic into familiar C++ and Python
   concepts; and
8. explain assumptions, limitations, failure signatures, and common mistakes.

A glossary entry elsewhere does not satisfy the first-use requirement.

---

# 7. Target Repository Acquisition and Revision Control

The Target Repository must be available under a controlled workspace such as:

`./repository/<repository-name>`

If absent, the Generator may clone it.

If already present, the Generator must fetch available remote changes before analysis where network access permits.

The Generator must not silently discard local modifications.

The configured revision may be a branch, tag, or exact commit.

Before analysis begins, the Generator must resolve the configured revision to an exact Git commit identifier.

The exact commit must be recorded in Curriculum Product metadata and source provenance.

Curriculum claims about repository behavior must always be traceable to an exact analyzed revision.

---

# 8. Generation Architecture

Generation must be treated as a multi-stage knowledge-production pipeline rather than a single prompt that asks a model to produce a course.

At minimum, the lifecycle must distinguish:

1. configuration validation;
2. repository acquisition;
3. exact revision resolution;
4. repository inventory and architecture analysis;
5. domain and algorithm identification;
6. knowledge-map construction;
7. prerequisite discovery and recursive expansion;
8. external research where necessary;
9. mastery-contract construction;
10. curriculum ordering and lesson planning;
11. lesson generation;
12. assessment generation;
13. model-criticism and adversarial-case generation where applicable;
14. source and evidence verification;
15. curriculum coverage auditing;
16. gap detection and additional generation;
17. final competency auditing;
18. Curriculum Product assembly;
19. migration or structured-data generation;
20. runtime compatibility validation;
21. metadata and provenance recording;
22. release promotion.

These stages may be implemented by one agent, multiple agents, deterministic tooling, local models, frontier models, or combinations thereof.

The implementation should choose the least expensive reliable mechanism for each stage.

Failed or incomplete generation must not be promoted as a completed Curriculum Product.

---

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

# 12. Required Depth for Major Scientific, Mathematical, and Numerical Concepts

Every major scientific model, numerical method, mathematical algorithm, or physically meaningful computational method must cover all applicable areas below.

1. Physical or conceptual interpretation.
2. Governing equations.
3. Mathematical derivation or a sufficiently complete derivation sketch.
4. Definitions, dimensions, and units of important quantities.
5. Assumptions and approximations.
6. Why those assumptions are made.
7. Numerical formulation and discretization.
8. Stability, consistency, convergence, and resolution considerations where applicable.
9. Parameter interpretation.
10. Sensitivity to parameters, forcing, initial conditions, boundary conditions, geometry, and resolution where applicable.
11. Intended validity regime.
12. Conditions that violate the formulation's assumptions.
13. Failure modes.
14. Expected error signatures and likely directions of bias.
15. Structural limitations that calibration cannot remove.
16. Comparison with important alternative methods.
17. Mapping from theory to concrete source code.
18. Worked examples.
19. Marginal or stressed examples.
20. Clearly inappropriate-use examples.
21. Diagnostic exercises.
22. Assessments requiring reasoning rather than recall.
23. Supporting source or authoritative external references.

A major concept is incomplete while any applicable required area lacks adequate coverage.

---

# 13. Model Criticism and Failure Reasoning

For scientific and numerical Target Repositories, model criticism must be a first-class curriculum objective rather than an appendix.

The curriculum must teach the Learner to reason from model structure to expected behavior.

Where applicable, the Learner must encounter scenarios involving:

* violated physical assumptions;
* inappropriate model selection;
* poor parameterization;
* invalid calibration transfer;
* insufficient spatial resolution;
* insufficient temporal resolution;
* numerical instability;
* numerical diffusion or dispersion;
* inaccurate forcing data;
* inaccurate boundary conditions;
* implementation defects;
* structural model bias.

The curriculum must distinguish problems that can plausibly be corrected by parameter calibration from problems that require a different formulation, different forcing, different discretization, or code changes.

For important methods, the curriculum must include at least:

* one case in which the method should perform well;
* one marginal case in which important assumptions are stressed; and
* one case in which the method is clearly inappropriate.

Each case must explain why the expected behavior follows from the method's mathematics and assumptions.

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

# 15. Source Traceability and Evidence

Important technical claims must be traceable to evidence whenever practical.

Curriculum provenance should include:

* Target Repository revision;
* source files;
* relevant symbols;
* relevant line ranges where useful;
* repository documentation;
* standards and specifications;
* primary scientific literature;
* official framework or library documentation;
* other authoritative references.

The Target Repository at the recorded revision is authoritative for claims about actual implementation behavior.

External scientific or mathematical claims should be supported by appropriate authoritative sources.

The curriculum must distinguish:

* facts directly observed in source;
* claims supported by upstream documentation;
* claims supported by external references;
* reasonable interpretations;
* unresolved uncertainties.

Unverified generated assumptions must not be presented as unquestionable fact.

---

# 16. External Research

The Generator may and should use external research when repository material is insufficient to teach domain or prerequisite knowledge correctly.

Preferred source order is:

1. official project documentation;
2. standards and formal specifications;
3. primary scientific literature;
4. official framework and library documentation;
5. reputable academic or professional secondary sources;
6. other reputable secondary sources when necessary.

The Generator should prefer primary sources for governing equations, numerical methods, model validity, and scientific claims.

External research must retain enough provenance for later verification.

## 16.1 Source and Citation Requirements

All externally derived factual claims MUST be explicitly cited.

This includes, but is not limited to:

- equations, formulas, and mathematical notation;
- definitions of variables, symbols, objective functions, and metrics;
- numerical constants, thresholds, coefficients, parameter ranges, and defaults;
- descriptions of algorithms, models, physical processes, calibration methods, and optimization methods;
- statements about model behavior, limitations, assumptions, accuracy, or computational characteristics;
- historical claims or claims about how a method is commonly implemented;
- terminology or notation attributed to a particular field, publication, software package, or modeling framework.

### 16.1.1 Citation placement

Citations MUST appear adjacent to the claim they support. Do not rely solely on a bibliography or "Sources" section at the end of a document.

For example:

> The calibration objective can be represented as a mean-squared-error loss,
> \(J(\theta) = \frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i(\theta))^2\) [Smith et al., 2024].

If the source defines the objective function but does NOT use the symbol `J`, do not imply that it does. Instead state explicitly that the notation is being introduced for the curriculum:

> Using `J` here as curriculum notation, define the mean-squared-error objective as ...

### 16.1.2 Source fidelity

Never invent, infer, or fabricate a citation.

A citation MUST correspond to a source that was actually consulted and that materially supports the associated claim.

If no authoritative source can be found for a factual claim:

1. omit the claim;
2. qualify it as an interpretation or illustrative example; or
3. explicitly state that no supporting source was identified.

Do not present uncited external knowledge as established fact.

### 16.1.3 Original synthesis

Reasoning, explanations, examples, analogies, exercises, and pedagogical simplifications created by the curriculum generator do not require citations merely because they are original synthesis.

However, any factual premises used by that synthesis MUST still be cited.

### 16.1.4 References

Every generated curriculum document containing cited material MUST include a `References` section containing enough information to identify and retrieve each cited source.

Where available, include:

- author or organization;
- title;
- publication or documentation name;
- publication year or version;
- DOI or stable URL;
- date accessed for mutable web documentation.

Prefer primary sources, official documentation, peer-reviewed literature, standards, and authoritative technical reports over secondary summaries.

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

# 18. Multi-Pass Generation and Auditing

Curriculum generation must use iterative review rather than trusting the first generated pass.

The expected logical passes are:

1. **Knowledge pass**: determine what must be understood.
2. **Prerequisite pass**: recursively identify what must be taught first.
3. **Mastery pass**: define what competent understanding of each major concept means.
4. **Structure pass**: order concepts and construct curriculum sections.
5. **Content pass**: produce lessons, examples, and references.
6. **Assessment pass**: create questions and exercises mapped to Mastery Contracts.
7. **Adversarial pass**: identify cases, counterexamples, assumption violations, and likely failure signatures.
8. **Gap-review pass**: determine what a successful Learner could still misunderstand.
9. **Remediation pass**: generate missing or inadequate material.
10. **Competency-audit pass**: verify every terminal learning outcome has sufficient instructional and assessment support.
11. **Terminology-closure pass**: verify every specialized item is inventoried,
    taught before use, distinguished from related items, and closed across
    lessons and assessments.
12. **Readability-review pass**: review ordinary prose for grade 8–10 clarity,
    short sentences, jargon load, progressive disclosure, and retained
    scientific and mathematical depth.

These passes do not require ten separate model invocations if an implementation can achieve equivalent independence and verification more efficiently.

Where practical, final review should be performed with fresh context or an independent reviewing agent so that the author is not the sole judge of its own completeness.

---

# 19. Machine-Readable Completion State

The Generator must maintain machine-readable generation state sufficient to determine whether a Curriculum Product is actually complete.

For each major concept, state should record applicable fields such as:

* prerequisite status;
* mastery-contract status;
* theory coverage;
* mathematical coverage;
* assumptions coverage;
* implementation mapping;
* source verification;
* validity-regime coverage;
* failure-mode coverage;
* bias-analysis coverage;
* example coverage;
* diagnostic-exercise coverage;
* assessment coverage;
* unresolved uncertainty.

Generation must continue while required fields remain incomplete unless generation cannot proceed because evidence is unavailable or another explicit failure condition has been reached.

Inability to complete a required field must be surfaced as an unresolved issue. It must not be converted to "complete" merely to terminate generation.

---

# 20. Assessment Requirements

Every Curriculum Product must contain:

* randomized review pop quizzes;
* section quizzes;
* one mid-curriculum examination;
* one final examination.

Assessments must map to taught concepts and Mastery Contracts.

Questions should test explanation, diagnosis, prediction, comparison, derivation, source tracing, and application where appropriate rather than relying predominantly on vocabulary recall.

For scientific and numerical curricula, assessments must include model-selection, failure-analysis, and bias-reasoning questions where applicable.

Assessment questions must not test material that has not been taught unless the question itself supplies the information required for a reasoning exercise.

## 20.1 Pop quizzes

Pop quizzes must:

* draw only from previously taught material;
* contain between 3 and 8 questions;
* be designed to require relatively little time compared with section quizzes or examinations;
* be timed by default;
* vary question selection, question order, and answer order where practical;
* avoid excessive immediate repetition;
* permit timing to be disabled or extended for accessibility;
* preferentially draw from concepts previously answered incorrectly where appropriate;
* appear unpredictably during normal navigation after sufficient material has been taught;
* never appear before the Learner has completed enough material to support at least 3 meaningful review questions;
* use configurable probability and cooldown rules so that consecutive or excessively frequent pop quizzes are avoided;
* not announce their occurrence before the navigation action that triggers them.

## 20.2 Section quizzes

Each major curriculum section must conclude with a section quiz.

The section quiz should launch when the Learner attempts to advance from the completed section into the next section.

Each section quiz must:

* contain at least 10 questions;
* contain enough questions to assess every major Mastery Contract associated with the section;
* include multiple questions for concepts identified as major, difficult, high-risk, or foundational;
* sample across the full section rather than disproportionately testing the final lessons;
* contain enough variation that repeated attempts do not simply reproduce the same quiz.

## 20.3 Mid-curriculum examination

The mid-curriculum examination must comprehensively assess material from the first major portion of the curriculum.

It should launch when the Learner first attempts to proceed beyond the curriculum midpoint.

The examination must:

* contain at least 30 questions;
* include assessment of every major section completed before the midpoint;
* include questions spanning multiple earlier sections;
* test integration of concepts rather than treating each section as isolated material;
* include higher-order questions involving diagnosis, comparison, prediction, source tracing, derivation, or application where applicable.

## 20.4 Final examination

The final examination must comprehensively assess the complete curriculum.

The final examination must contain at least 50 questions.

The final examination must:

* include meaningful coverage of every major curriculum section;
* assess every terminal learning outcome;
* assess every major Mastery Contract, either directly or through a question that integrates multiple Mastery Contracts;
* include multiple questions for concepts classified as foundational, difficult, high-risk, or central to the Target Repository;
* include cumulative questions requiring the Learner to combine concepts taught in different sections;
* include diagnosis, prediction, comparison, source-tracing, application, and model-criticism questions where applicable;
* not satisfy coverage requirements solely through simple recall questions;
* contain sufficient question-bank depth that repeated attempts substantially vary while preserving equivalent coverage and difficulty.


## 20.5 Assessment Coverage and Question Pools

Minimum question counts define only the minimum size of an individual assessment and must not be treated as sufficient evidence of curriculum coverage.

Assessment generation must maintain mappings between:

* questions;
* curriculum concepts;
* Mastery Contracts;
* sections;
* difficulty;
* question type;
* terminal learning outcomes where applicable.

Question banks must contain substantially more questions than are presented in a single randomized assessment.

The Generator must ensure that:

* every major Mastery Contract is assessable;
* foundational and high-risk concepts receive proportionally greater assessment coverage;
* repeated assessment attempts can vary materially without omitting required competencies;
* assessments do not become dominated by whichever concepts are easiest to generate questions for;
* cumulative examinations contain questions that integrate knowledge from multiple sections;
* question-count minimums are not satisfied through excessive low-value recall questions.


---

# 21. Assessment Feedback

Incorrect answers must provide useful explanatory feedback.

Feedback should explain:

* why the submitted answer was incorrect;
* why the correct answer is correct;
* what concept and Mastery Contract competency the question tests;
* what material should be reviewed;
* which mistaken assumption or reasoning step is likely involved where appropriate.

Where useful, feedback should link to relevant lessons, glossary entries, source references, or worked examples.

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

# 23. Curriculum Product Representation

Curriculum Products must be independently versioned and reproducibly installable into the Education Runtime.

The canonical content representation may use:

* Django data migrations;
* packaged structured data;
* generated Python modules;
* fixtures;
* management-command inputs;
* or another deterministic representation.

Django data migrations are explicitly supported as a first-class mechanism for producing independently versioned curriculum products.

A Curriculum Product should avoid defining its own generic education models. It should populate models owned by the Education Runtime unless a concrete target-specific requirement makes additional models necessary.

A fresh installation must be able to reconstruct the intended generated curriculum deterministically from the Curriculum Product repository alone plus its declared Education Runtime dependency.

---

# 24. Curriculum Product Repository Structure

Each Curriculum Product must be capable of existing as an independent Git repository.

A conceptual product may resemble:

```text
<target>-curriculum/
├── pyproject.toml
├── README.md
├── SPEC.md
├── AGENTS.md
├── curriculum_product/
│   ├── __init__.py
│   ├── apps.py
│   ├── migrations/
│   └── data/
├── provenance/
│   ├── generation.json
│   ├── coverage.json
│   └── source-map.json
└── tests/
```

The exact layout may differ according to packaging needs.

A Curriculum Product must not require access to the Generator repository after generation.

---

# 25. Education Runtime Requirements

The shared Education Runtime must provide generic functionality for:

* curriculum registration and discovery;
* sections and lessons;
* rich curriculum content;
* glossary entries;
* assessments;
* questions, answers, and feedback;
* source references;
* progress reporting;
* administration;
* shared navigation and styling;
* stable curriculum identifiers;
* curriculum-version awareness;
* import and migration validation;
* accessibility behavior.

The Education Runtime must not contain Target Repository-specific educational content except for fixtures or examples used to test the runtime itself.

The Education Runtime should support one or more installed Curriculum Products without product-specific source changes.

Each installable Curriculum Product must advertise its Django application with
the standard `education_curriculum.products` Python package entry-point group.
The Standalone Runner must discover every advertised installed product
automatically before Django constructs `INSTALLED_APPS`. Migration and server
launch commands must not require a per-product environment variable or settings
edit. A legacy explicit package list may remain as an additive compatibility
path, but it must not disable automatic discovery.

When the Standalone Runner executes from the generator repository, it must also
discover local products by cross-referencing project directories under
`curricula/` with the `target_repository_name` provenance of repositories under
`generated/`. A local product is eligible only when both sides exist. Discovery
must use declared metadata and must not require the generated repository,
Curriculum Product, package, or curriculum identifier to contain the word
`curriculum` or follow another inferred naming convention.

---

# 26. Optional Standalone Runner

A thin Standalone Runner may be provided for convenient local or independent deployment.

The Standalone Runner may provide:

* Django settings;
* root URL configuration;
* ASGI and WSGI configuration;
* database defaults;
* static-file configuration;
* administration;
* discovery of installed Curriculum Products.

Installed-product discovery must be deterministic, reject malformed or
conflicting advertisements, and fail clearly before migration or server startup
rather than silently omitting an available curriculum.

Local project discovery must likewise be deterministic. It must reject multiple
generated repositories that claim the same reviewed curriculum project and
must not activate a generated repository that has no matching `curricula/`
project directory.

The Standalone Runner must not duplicate curriculum content or generic Education Runtime behavior.

A default standalone deployment may use SQLite.

The existence of a Standalone Runner must not prevent Curriculum Products from being installed into another compatible Django service.

---

# 27. Database Behavior

The Education Runtime must use Django's configured database facilities.

Curriculum Products must not require a specific database backend unless explicitly documented and justified.

Curriculum data should be represented through generic runtime models where practical.

Curriculum Product migrations must be deterministic and safe to apply according to documented compatibility requirements.

Installation and deployment preparation must not assume that curriculum content
changes always require a new schema migration. After applying migrations, the
Standalone Runner must explicitly import the current packaged
`data/curriculum.json` from every discovered Curriculum Product through the
conflict-preserving baseline importer. The installation workflow must also run
Django static-file collection so current runtime and product assets are ready
for service.

---

# 28. Learner Progress

User accounts must not be required.

Learner progress and preferences must be capable of being stored client-side.

Progress must survive:

* page reloads;
* navigation between curriculum pages;
* browser restarts;
* temporary loss of network connectivity.

Progress must not depend solely on:

* tab-local session state;
* volatile JavaScript memory;
* cookies.

A persistent browser storage mechanism such as IndexedDB may be used.

Persisted Learner data may include:

* completed lessons;
* concept mastery state;
* section progress;
* quiz attempts and scores;
* exam attempts and scores;
* glossary progress;
* accessibility preferences;
* review history;
* missed concepts.

Persisted data must use stable identifiers that do not depend solely on display order.

---

# 29. Progress Versioning and Portability

Client-side progress data must be versioned.

Curriculum sections, lessons, concepts, assessments, and questions that participate in persisted state must have stable identifiers.

Curriculum Product updates should preserve compatible progress whenever practical.

When stored progress becomes incompatible with a newer curriculum version, the Education Runtime must handle the situation explicitly rather than silently corrupting or discarding progress.

Learners must be able to export progress to a portable file and restore progress from a previously exported file without requiring a user account.

Deployment of new client-side assets must not erase compatible Learner progress.

---

# 30. Administrative Editing and Generated Baselines

Lessons, glossary entries, quizzes, examinations, questions, answers, and feedback should be editable through the Django administrative interface where practical.

The system must distinguish between:

* the generated baseline supplied by a Curriculum Product; and
* human modifications made after installation.

A later Curriculum Product update must not silently overwrite human-modified content.

Conflicts must be detectable and surfaced explicitly.

The implementation may use version metadata, stable identifiers, content fingerprints, override records, or another reliable mechanism.

---

# 31. Regeneration and Incremental Updates

Each Curriculum Product must record the exact Target Repository revision used during its most recent successful generation.

When generation occurs against a newer revision, the Generator should compare the previously analyzed revision with the new revision and determine which concepts, source mappings, lessons, assessments, or assumptions may be affected.

Unchanged validated content should be preserved where practical.

Affected content must be re-audited rather than mechanically copied forward.

Stable concept and curriculum identifiers should be preserved where concepts remain semantically equivalent.

The Generator must distinguish changes caused by:

* Target Repository changes;
* Generator changes;
* Skill or methodology changes;
* Education Runtime schema changes;
* human curriculum modifications.

---

# 32. Generation Metadata

Each Curriculum Product must contain machine-readable generation metadata.

Metadata should include, where applicable:

* Generator name and version;
* generation timestamp;
* Target Repository name and URL;
* configured revision;
* resolved Target Repository commit;
* Curriculum Product name and version;
* curriculum schema version;
* compatible Education Runtime version or range;
* analysis methodology or Skill versions where useful;
* generation model information where reproducibility policy permits;
* prior source revision for incremental generations.

---

# 33. Reusable Skills and Agent Procedure Capture

The Generator may create or update reusable Skills when generation reveals a procedure that is likely to recur across Target Repositories.

Examples include procedures for:

* CMake analysis;
* Fortran module tracing;
* Python package analysis;
* BMI interface analysis;
* scientific model derivation review;
* source-provenance extraction;
* curriculum coverage auditing;
* assessment validation.

A reusable procedure should be captured as a Skill when doing so is expected to reduce repeated reasoning, improve consistency, or enable a lower-cost/local model to perform future work reliably.

Skills must be version controlled.

A Skill must not silently encode Target Repository-specific conclusions as universal rules.

Skills should contain, where applicable:

* a concise description usable for discovery without loading the full Skill;
* applicability conditions;
* required inputs;
* procedure;
* deterministic scripts or tools;
* expected outputs;
* validation rules;
* known limitations;
* failure conditions;
* escalation conditions.

When deterministic code can reliably replace repeated model reasoning, the Skill should prefer invoking that code.

Agents may propose or generate Skill changes as part of work, but a current task must not be declared successful merely by rewriting its own success criteria or weakening a Skill's validation requirements.

Changes that alter project policy belong in `SPEC.md` or `AGENTS.md`, not in a task-specific Skill.

---

# 34. Frontier, Local, and Deterministic Work Allocation

The architecture should allow generation tasks to be executed by different compute tiers.

Frontier-model work should focus on tasks whose failure would materially reduce correctness or educational depth and that require substantial synthesis or judgment.

Local or lower-cost models may be used for tasks such as:

* expanding content from already validated knowledge artifacts;
* applying established Skills;
* generating schema-conforming routine material;
* mechanical source mapping;
* repetitive assessment variants;
* formatting or migration generation;
* routine code changes.

Deterministic tooling should be preferred for tasks such as:

* repository inventories;
* symbol extraction where reliable parsers exist;
* schema validation;
* migration checks;
* link and provenance verification;
* coverage accounting;
* package installation tests;
* Django system checks.

Local or lower-capability execution must have explicit escalation criteria for cases that violate Skill assumptions, contain contradictory evidence, require unfamiliar scientific reasoning, or otherwise exceed established procedures.

The purpose of reusable Skills and intermediate artifacts is to reduce repeated frontier reasoning without lowering correctness standards.

---

# 35. Intermediate Artifacts

Significant analysis should produce persistent structured artifacts where they improve reproducibility or prevent repeated work.

Useful artifacts may include:

* repository inventories;
* architecture maps;
* concept graphs;
* prerequisite graphs;
* source maps;
* Mastery Contracts;
* coverage matrices;
* unresolved-question registers;
* scientific-model analyses;
* regeneration impact analyses.

Expensive, validated, or human-reviewed analysis may be version controlled.

Cheap deterministic caches should normally be regenerated rather than committed.

Transient agent scratch state, raw logs, and disposable plans should not be treated as canonical project knowledge.

Reusable Python and shell tooling must be stored in an appropriate source or tooling directory and version controlled.

---

# 36. Hallucination Resistance and Uncertainty

The Generator and generated curriculum must teach and enforce verification rather than treating generated prose as authority.

Learners should be taught to:

* inspect relevant source code;
* inspect repository history where useful;
* consult official documentation;
* consult authoritative external references;
* identify conflicts between curriculum statements and source behavior;
* distinguish implementation facts from interpretive explanations.

The Generator must not fabricate certainty where evidence is incomplete.

Important unresolved questions should be represented explicitly in generation state and, when appropriate, surfaced in generated material.

---

# 37. Generated Documentation

Every Curriculum Product must contain enough documentation to install, load, validate, update, and continue development without access to the Generator repository.

Documentation should include, where applicable:

* `README.md`;
* `SPEC.md` describing product-specific scope where useful;
* `AGENTS.md` for continued agent-assisted maintenance;
* installation instructions;
* migration instructions;
* testing instructions;
* Education Runtime compatibility;
* Target Repository provenance;
* regeneration provenance;
* known unresolved curriculum issues.

The Education Runtime and Standalone Runner must maintain their own independent documentation.

---

# 38. Git and Product Independence

Each Curriculum Product must be independently versionable and distributable.

Curriculum Products may be maintained as independent Git repositories.

A Standalone Runner or deployment repository may reference Curriculum Products using Python dependencies, Git submodules, package releases, or another documented mechanism.

A Curriculum Product's internal Git history must not be silently absorbed into an unrelated host repository.

After successful initial generation, a newly created Curriculum Product repository should:

1. use a configured initial branch, defaulting to `main`;
2. stage generated files;
3. record generation metadata;
4. create an initial generation commit where automated commit behavior is enabled;
5. remain independently cloneable and usable with a compatible Education Runtime.

The Generator must not modify global Git configuration merely to make automated commits possible.

---

# 39. Validation

A Curriculum Product must not be considered successfully generated solely because files or migrations were produced.

Validation must include applicable checks for:

* Curriculum Product package installation;
* Python syntax;
* Django system checks;
* migration consistency;
* migration application into a clean database;
* Education Runtime compatibility;
* stable identifier integrity;
* source-reference integrity;
* coverage-matrix completeness;
* Mastery Contract coverage;
* prerequisite closure;
* required assessment presence;
* final competency coverage;
* unresolved required fields;
* automated tests;
* static analysis and formatting where configured.

For scientific or numerical curricula, validation must also ensure that major methods have adequate assumptions, validity, failure-mode, and bias-analysis coverage.

Validation failure must prevent incomplete output from being promoted as a successful release.

Validation must include a terminology-closure and readability audit.

The audit must verify that:

* every specialized term and identifier is present in a terminology inventory;
* every acronym is expanded on first use;
* every variable is defined before it appears in an equation or worked example;
* definitions do not rely on terms that are introduced later;
* related variables with similar names are explicitly contrasted;
* every parameter definition includes role, units, range, behavior, and source;
* every lesson has been reviewed against the configured reading-level target;
* unexplained terminology remains an unresolved required item.

Automated readability scores may support this audit but must not be its sole
evidence, because equations, identifiers, and scientific names can distort such
scores.

## 39.1 Citation Verification During Generation

Before finalizing each lesson, maintain an internal claim-source mapping for externally derived factual content.

For each factual claim, record:

- the claim or concept;
- the supporting source;
- the exact section, page, heading, equation, or other locator when available;
- whether the curriculum is quoting, paraphrasing, synthesizing, or introducing its own notation.

Before emitting the final lesson, verify that every externally derived factual claim has at least one supporting citation.

The final curriculum need not expose this internal ledger unless requested.

---

# 40. User Interface

The Education Runtime must provide clear navigation through:

* curricula;
* curriculum sections;
* lessons;
* concepts;
* assessments;
* glossary entries;
* progress information;
* source references.

Learners must be able to revisit previously completed material.

Current progress should be visible.

Important source references should be accessible without requiring the Learner to manually locate referenced code.

The interface should support the presentation of equations, source excerpts or links, diagrams, worked examples, diagnostic scenarios, and comparisons between methods where required by Curriculum Products.

# 40.1 Curriculum Content Rendering

Curriculum lessons must be represented as structured rich content and rendered by the Education Runtime as semantic HTML.

Plain-text paragraphs alone are not sufficient for technical curriculum content.

The Generator must select content structures appropriate to the information being taught rather than expressing all material as prose paragraphs.

## Structured Content Blocks

Lesson content must support, at minimum, the following block types where applicable:

* paragraph;
* heading;
* equation;
* code block;
* callout;
* worked example;
* diagnostic example;
* warning;
* note;
* definition;
* theorem, rule, or principle;
* ordered list;
* unordered list;
* table;
* comparison table;
* figure or diagram;
* quote or source excerpt where licensing permits;
* step-by-step procedure;
* source-code reference;
* parameter or variable definition table.

The Generator must use these structures when they improve comprehension.

A lesson containing equations, source code, algorithms, warnings, examples, or structured comparisons must not flatten those elements into ordinary paragraphs merely because paragraph content is easier to generate.

## Inline Semantic Markup

Text-bearing content blocks must support inline semantic markup.

At minimum, the content representation must be capable of distinguishing:

* ordinary prose;
* variable names and mathematical symbols;
* source-code identifiers;
* file names and paths;
* commands;
* configuration keys and values;
* user input;
* emphasized text;
* strong emphasis;
* citations and source references;
* inline mathematical expressions.

For example, a sentence conceptually equivalent to:

> The variable `soil_reservoir.storage_m` represents stored soil water depth \(S\), measured in meters.

must render `soil_reservoir.storage_m` as a code identifier and \(S\) as mathematical notation rather than rendering the entire sentence as undifferentiated text.

The Generator must preserve these semantic distinctions in generated curriculum data.

## Mathematical Rendering

Scientific, mathematical, and numerical curricula must render mathematical notation using a mathematical typesetting mechanism rather than plain preformatted text.

The content representation must support:

* inline mathematics;
* display mathematics;
* equation numbering where useful;
* mathematical symbols;
* fractions;
* superscripts and subscripts;
* summations and integrals;
* matrices where applicable;
* aligned multi-line equations;
* variables containing Greek symbols;
* units and dimensional notation.

Mathematical expressions may be stored using LaTeX or another documented mathematical representation and rendered by the Education Runtime using a suitable renderer such as MathJax, KaTeX, MathML, or an equivalent mechanism.

Generated mathematical content must include accessible text or another accessible mathematical representation.

Important equations must not be represented solely as images.

The Generator must not replace an equation with a prose description when displaying the equation materially improves understanding.

## Code Rendering

Source code and pseudocode must be represented as code blocks rather than paragraph text.

Code blocks should include applicable metadata such as:

* programming language;
* source file;
* source revision;
* line range;
* caption;
* whether the content is exact source code, simplified source code, or pseudocode.

The Education Runtime should render code with syntax highlighting.

Inline source identifiers, function names, variable names, types, commands, and file paths must use appropriate inline code markup.

Generated lessons must use code examples when understanding the implementation requires seeing actual or simplified source behavior.

## Callouts

Lessons must support visually distinct semantic callouts.

Supported callout purposes should include at least:

* note;
* important;
* warning;
* implementation detail;
* scientific assumption;
* common mistake;
* performance concern;
* debugging tip;
* source discrepancy;
* model limitation.

A callout must include a semantic type in addition to its displayed title so that the Education Runtime can render it consistently and accessibly.

The Generator should use callouts to draw attention to information that would otherwise be easy to overlook, especially:

* assumptions;
* unit conversions;
* failure conditions;
* implementation traps;
* important distinctions;
* surprising behavior;
* limitations.

Callouts must not be overused to the point that ordinary instructional flow becomes fragmented.

## Worked Examples

Major concepts should include worked examples where an example materially improves understanding.

A worked example should support structured elements such as:

* problem or scenario;
* known values or inputs;
* assumptions;
* equations or method;
* intermediate steps;
* result;
* interpretation;
* connection to the Target Repository.

For scientific and numerical material, worked examples should preserve units throughout the calculation where applicable.

Worked examples must not be collapsed into a single explanatory paragraph when multiple reasoning steps are important to understanding the method.

## Diagnostic Examples

Where failure reasoning or model criticism is required, lessons should include structured diagnostic examples.

A diagnostic example should be capable of representing:

* observed behavior;
* relevant configuration or model conditions;
* candidate causes;
* reasoning;
* likely cause;
* rejected alternatives;
* recommended investigation or corrective action.

Diagnostic examples should explicitly connect symptoms to assumptions, mathematics, implementation behavior, or source code where applicable.

## Variable and Parameter Presentation

Major mathematical variables, model parameters, configuration values, and state variables should be introduced using structured definitions rather than only appearing within prose.

Definitions should include applicable fields such as:

* symbol;
* source-code identifier;
* human-readable name;
* meaning;
* units;
* valid or expected range;
* whether the value is input, parameter, state, flux, intermediate value, or output;
* source location;
* important constraints or assumptions.

Where multiple variables or parameters are introduced together, the Generator should prefer a table or other structured presentation.

Every domain-specific variable, parameter, state, flux, and acronym must have a
Terminology Contract before its first substantive use.

A Terminology Contract must contain:

* full or expanded name;
* abbreviation or identifier decomposition where meaningful;
* plain-language definition that does not depend on undefined domain terms;
* purpose in the model;
* semantic role: input, parameter, state, flux, intermediate, or output;
* units and dimensionality;
* expected or valid range;
* interpretation of zero, larger values, smaller values, and important limits;
* relationships and contrasts with similarly named quantities;
* equation mappings;
* source-code mappings;
* at least one concrete example;
* at least one likely misconception.

A definition that merely expands an acronym or replaces it with equally
specialized vocabulary is incomplete.

## Tables and Comparisons

Structured tables should be used for information that is inherently comparative or tabular.

Examples include:

* alternative numerical methods;
* parameters and units;
* build modes;
* configuration options;
* model assumptions;
* failure modes;
* data structures;
* source modules and responsibilities.

The Generator must not convert naturally tabular information into repetitive prose merely to avoid generating a table.

## Content Variety

Lessons should contain an appropriate mixture of prose and structured instructional elements.

For technically substantial lessons, the Generator should actively consider whether the lesson would benefit from:

* mathematical notation;
* code;
* tables;
* callouts;
* worked examples;
* diagnostic cases;
* lists;
* diagrams;
* source references.

A technically substantial lesson consisting almost entirely of consecutive prose paragraphs should be treated as a potential curriculum-quality defect and reviewed during curriculum auditing.

This requirement does not establish arbitrary quotas for visual elements. Content structure must be driven by pedagogical usefulness.

## HTML Rendering Responsibility

Curriculum Products should describe semantic content rather than contain arbitrary presentation-oriented HTML.

The Education Runtime is responsible for converting structured curriculum content into semantic HTML.

Generated curriculum content must not depend upon inline CSS, arbitrary JavaScript, or product-specific presentation markup.

If limited HTML content is supported for exceptional cases, the permitted element and attribute set must be explicitly defined, sanitized, and validated before rendering.

Presentation styling must remain the responsibility of the Education Runtime.

## Validation

Curriculum validation must detect applicable presentation defects, including:

* equations represented only as plain text when mathematical rendering is appropriate;
* code represented as ordinary prose;
* missing language metadata for code blocks where known;
* mathematical variables presented without semantic distinction;
* lessons containing only paragraph blocks despite having content that naturally requires richer presentation;
* malformed mathematical markup;
* unsupported content block types;
* unsafe HTML;
* inaccessible figures or mathematical content;
* missing captions or accessible descriptions where required.

Curriculum auditing should treat inappropriate flattening of structured technical content into prose as a content-quality defect.

---

# 41. Tone

Curriculum tone should be:

* friendly;
* colloquial where useful;
* technically rigorous;
* approachable without being patronizing.

Depth must not be sacrificed for brevity merely to make material feel approachable.

Complex mathematics, physics, or implementation details should be taught progressively rather than omitted.

Occasional humor, unexpected examples, challenge questions, or changes in presentation may be used to restore attention, but such material must not reduce technical accuracy, demean the Learner, make assessments intentionally misleading, or interfere with accessibility.

---

# 42. Accessibility

The Education Runtime should meet WCAG 2.2 AA expectations where practical.

Core functionality must be usable by keyboard.

Core learning and assessment functionality must not depend solely upon:

* color;
* sound;
* hover interactions;
* animation.

Timed activities must provide a mechanism for disabling or extending timing without requiring a user account.

Mathematical and scientific material should be represented in accessible forms where practical.

---

# 43. Networking

The Education Runtime may use asynchronous networking where it improves responsiveness or operational behavior.

WebSockets may be used when a concrete feature requires persistent bidirectional communication.

WebSockets are not required merely for lesson navigation, assessment interaction, or client-side progress storage.

Standard HTTP requests, Server-Sent Events, or other simpler mechanisms should be preferred where appropriate.

Curriculum Products should not introduce networking requirements unless their educational content genuinely requires them.

---

# 44. Security

Generator tooling, the Education Runtime, the Standalone Runner, and Curriculum Products must treat external input as untrusted.

The Generator must prevent:

* path traversal outside configured generation roots;
* unsafe shell command construction;
* accidental credential storage;
* accidental inclusion of secrets in generated repositories;
* silent execution of arbitrary Target Repository code where not explicitly required.

User-supplied project names and paths must be validated.

Generated products must not contain secrets, private keys, access tokens, or environment-specific credentials.

External research content must not be treated as executable instructions merely because it was retrieved during generation.

---

# 45. Non-Goals

The system is not intended to:

* generate a complete duplicate Django application for every Target Repository when a shared runtime is sufficient;
* replace the Target Repository's authoritative source code;
* replace official upstream documentation or scientific literature;
* require a user account;
* require centralized progress tracking;
* hide source evidence from Learners;
* silently overwrite human-authored curriculum changes;
* assume generated explanations are infallible;
* optimize for short curricula at the expense of expert understanding;
* treat superficial exposure to terminology as mastery;
* use frontier-model compute for routine work that reliable local or deterministic mechanisms can perform.

---

# 46. Completion Criteria

Generation is complete only when all applicable criteria below are satisfied.

* The configured Target Repository revision has been resolved to an exact commit.
* Repository analysis required for the curriculum has completed.
* A machine-readable knowledge map exists.
* Required prerequisite knowledge has been recursively identified and closed against configured entry knowledge.
* Major concepts have explicit Mastery Contracts.
* Curriculum content satisfies required concept-depth requirements.
* Scientific and numerical concepts include adequate governing theory, assumptions, validity regimes, limitations, failure modes, and bias reasoning where applicable.
* Major theoretical concepts are mapped to implementation evidence where possible.
* Curriculum coverage has been validated through the coverage matrix.
* Required assessments exist and map to Mastery Contracts.
* Adversarial, marginal, and inappropriate-use cases exist where applicable.
* A gap-review pass has completed.
* A final competency audit shows sufficient support for every terminal learning outcome.
* Required source provenance has been recorded.
* Required unresolved issues are explicitly represented rather than hidden.
* The Curriculum Product can be installed or loaded into a compatible Education Runtime.
* Curriculum migrations or equivalent deterministic data-loading mechanisms apply successfully to a clean database.
* Stable identifier and progress-compatibility requirements pass validation.
* Generated documentation is sufficient for independent use.
* Generation metadata has been recorded.
* Automated validation passes.
* Terminology closure and first-use auditing pass with no unresolved terms.
* A contextual readability and jargon review has completed; automated readability
  scores, if used, are supporting evidence rather than the sole criterion.

The Generator must continue generating, researching, reviewing, or remediating while required completion fields remain incomplete and further progress is possible.

A Curriculum Product is not complete merely because the generated material is coherent, useful, or long. It is complete when the defined competencies are actually taught, traceable, and assessed.

