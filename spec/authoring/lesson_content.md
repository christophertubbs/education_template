# Lesson Content

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

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
