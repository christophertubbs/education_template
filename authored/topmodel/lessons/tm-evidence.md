---
handoff_version: "1.0"
identifier: "tm-evidence-lesson"
section_identifier: "tm-foundations"
sequence: 1
title: "What does the evidence actually establish?"
summary: "Use a source location, a test assertion and a run result to make different, appropriately bounded claims."
status: "in_review"
concept_identifiers: ["tm-evidence"]
source_identifiers: ["src-build", "src-test-doc", "src-restart-test", "src-protocol-test"]
terminology_identifiers: []
introduced_terminology_identifiers: []
---
## Block: tm-evidence-objectives | paragraph

### inline

By the end of this lesson, you should be able to classify a statement as a fact
about source code, a test's intended check, an observed result, or a claim about
the real world. You should also be able to identify evidence that is missing
and narrow a conclusion to what its evidence supports. You need ordinary
programming and test-reading skills. You do not need hydrology or calculus.

## Block: tm-evidence-start | paragraph

### inline

Imagine a pull request that says, “The model is correct because the restart test
passes.” Before accepting that sentence, ask what “correct” means here. A test
could show that saving and restoring a calculation reproduces the same answer.
Both calculations could still contain the same mistake. Agreement is useful,
but it answers a narrower question than whether the calculation describes a real
place well. The distinction in this example is a reasoning exercise:
identical answers do not by themselves
prove that either answer is true.

## Block: tm-evidence-kinds | comparison_table

### caption

Four claims that require different evidence

### headers

| Statement | Evidence needed | Limit of the conclusion |
| --- | --- | --- |

### rows

| This source contains a comparison loop. | Inspect the exact file at an exact commit. | Establishes what is written, not whether it ran. |
| This test checks every advertised output. | Inspect how output names are collected and how comparisons iterate. | Establishes the test's intended scope for its supplied inputs. |
| This run passed that test. | Retain the command, build, configuration, input revision, exit status and output. | Establishes an observation for those conditions. |
| These predictions adequately describe this place. | Compare appropriate observations and predictions, with uncertainty and conditions stated. | Requires a scientific evaluation beyond program agreement. |

## Block: tm-evidence-current-test | paragraph

### inline

The current restart integration test runs the forcing sequence without a restart,
then with one restart, then with three. It records each advertised output after
each step. Its comparison uses exact inequality between corresponding numbers,
and reports the first mismatch for each compared run. The test also destroys
the old model instance and creates a new one at a restart, so it does not simply
continue using the old instance's state. Those are source facts you can check
in `run`, `compare`, and `main`. They do not say that anyone ran the test during
this curriculum's authoring. [Restart test, lines 148–235](citation:src-restart-test)

## Block: tm-evidence-fixture-limit | paragraph

### inline

A test's input can leave an important path unused. The restart test itself
documents an example: its configuration has zero initial delay and only one
arrival-weight value. Those numbers describe how the model schedules water
to arrive at later steps. With this fixture, the queue has two stored entries.
The test's comment says that mistakes in queue sizing or omission of the
arrival weights can therefore go undetected. You do not need the routing
equations yet to understand the testing lesson: an input that uses only a small
special case cannot establish behavior for larger, more varied cases.
[Restart-test limitation, lines 9–15](citation:src-restart-test)

## Block: tm-evidence-example | worked_example

### title

Rewrite an overbroad restart claim

### scenario

A colleague supplies the current test source and writes, “Restart is proven
correct for all configurations.” No command output or build information is
provided. You have inspected the test's stated queue limitation.
[Restart test](citation:src-restart-test)

### steps

1. Separate source inspection from execution. You can say what the test is
   written to compare. You cannot report a passing run without a run result.
2. Identify the input limitation. The test documents a zero-delay, one-weight
   configuration. It does not supply a meaningful multi-step queue case.
3. Rewrite the statement: “This test is written to compare every advertised
   output at every forcing step across uninterrupted and restarted runs for
   its fixture.”
4. Add what remains untested: a configuration with delayed arrivals and several
   queue weights, plus evidence of an actual run with the recorded build.

### result

The revised statement is useful and checkable. It makes no claim of universal
restart correctness or of successful execution during this review.

### interpretation

Narrowing a claim does not make the test worthless. It identifies the confidence
the test can provide and the next experiment needed to extend that confidence.

## Block: tm-evidence-old-doc | diagnostic_example

### title

An old test command does not match the current build

### observed_behavior

The test README directs the reader to use make in test/ and run
run_bmi_unit_test, while the inspected root CMake file defines
simple_unit_tests and two serialization test executables.
[Historical instructions](citation:src-test-doc) [Current build](citation:src-build)

### conditions

The checkout is commit 89e4dc529dfdf7f23b7365530973e9f238fb740d. No test run
has been supplied with the report.

### candidate_causes

The instructions may describe an older build layout; the reader may be using
another revision; or the current build may have failed for a separate reason.

### reasoning

The file and target-name mismatch supports the first explanation for why the
documented command is unsuitable at this revision. It does not establish that
the science calculation is broken. Nor does an older README's assertion of
identical output prove the current executables produce identical output.
Check the revision before comparing instructions, and distinguish a build-path
problem from a numerical result problem.

### recommended_action

Read the current CMake target definitions and CI commands. Record the compiler,
dependencies, build options, working directory and selected executable with any
subsequent run. Report an actual build or run failure separately from the stale
documentation finding. Do not turn an unexecuted command into a passing result.

## Block: tm-evidence-procedure | procedure

### title

Make a claim reviewable

### steps

1. Write one concrete statement. Replace “works” with the behavior and conditions
   that matter: for example, which values are compared after a restart.
2. Identify the evidence kind: source, documentation, test definition, executed
   observation, or scientific measurement and analysis.
3. Record the exact revision, file and relevant range. For a run, also record
   its command, build, input, configuration, output and exit status.
4. Read the assertions and the input restrictions. Check what is never exercised.
5. State a plausible counterexample and the check that would distinguish it.
6. Write the conclusion at the supported scope. Keep unresolved questions visible.

## Block: tm-evidence-check | paragraph

### inline

Check your understanding: you have read a test that compares all fourteen output
names but have not run it. Can you say it passed? No. You can describe the
comparison the source implements. If someone later supplies a successful run,
can you claim all configurations are covered? Still no: the supplied inputs
bound the observation. The useful next step is a case that changes a material
condition, such as the number and delay of queue entries, while retaining an
independently justified expected result. [Test scope](citation:src-restart-test)

## References

NOAA-OWP, TOPMODEL BMI, commit `89e4dc529dfdf7f23b7365530973e9f238fb740d`,
consulted 2026-09-11. `src-restart-test`: test/main_integration_test_serialization.c,
lines 1–237. `src-test-doc`: test/README.md, lines 1–59.
`src-build`: CMakeLists.txt, lines 1–121. `src-protocol-test`:
test/main_unit_test_serialization.c, lines 209–393. Full pinned URLs in sources.md.
