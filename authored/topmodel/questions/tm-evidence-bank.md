---
handoff_version: "1.0"
status: "in_review"
---
# Evidence review question bank

Canonical records for one initial pop review. Single-choice scoring awards one
point for the sole correct option and zero otherwise, including a blank response.
Question options are randomly ordered at presentation. All scenarios are author-created;
current-test premises are supported by the adjacent source references.

## Record: tm-evidence-q1

```yaml
{
  "identifier": "tm-evidence-q1",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q1-a",
      "text": "The source is written to compare corresponding outputs across uninterrupted and restarted runs.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q1-b",
      "text": "The test passed on the reviewer's machine.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q1-c",
      "text": "Restart works for every configuration.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q1-d",
      "text": "The model's predictions are scientifically accurate.",
      "correct": false
    }
  ]
}
```

### prompt

A reviewer has inspected the restart test source but has no build log or run output. Which statement is supported? [Restart test](citation:src-restart-test)

### feedback_correct

The first statement describes the observed source. None of the other statements follows without execution evidence or additional evaluation.

### feedback_incorrect

Reading an assertion does not execute it. Review tm-evidence-current-test and distinguish what code checks from what a run observed.

### option_explanations

A: The first statement describes the observed source. None of the other statements follows without execution evidence or additional evaluation.

B–D: Reading an assertion does not execute it. Review tm-evidence-current-test and distinguish what code checks from what a run observed. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## Record: tm-evidence-q2

```yaml
{
  "identifier": "tm-evidence-q2",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q2-a",
      "text": "Exercise positive delay and several queue weights against independently calculated expected entries.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q2-b",
      "text": "Repeat the identical run and declare all queue sizes covered.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q2-c",
      "text": "Change only the printed test title.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q2-d",
      "text": "Remove the queue limitation from the test comment.",
      "correct": false
    }
  ]
}
```

### prompt

A supplied successful test run used zero initial delay and one arrival weight. Its source warns that some queue defects go undetected. Which next check addresses that limitation? [Restart test](citation:src-restart-test)

### feedback_correct

Changing the delay and number of weights exercises the missing behavior. Independently expected queue entries give the check an answer to compare against.

### feedback_incorrect

Repetition or cosmetic edits do not expand the tested conditions. Review tm-evidence-fixture-limit and choose an input that reaches the omitted behavior.

### option_explanations

A: Changing the delay and number of weights exercises the missing behavior. Independently expected queue entries give the check an answer to compare against.

B–D: Repetition or cosmetic edits do not expand the tested conditions. Review tm-evidence-fixture-limit and choose an input that reaches the omitted behavior. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## Record: tm-evidence-q3

```yaml
{
  "identifier": "tm-evidence-q3",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q3-a",
      "text": "The instructions and current build layout disagree; inspect the current targets and record the revision.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q3-b",
      "text": "The hydrological equations must be wrong.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q3-c",
      "text": "The current tests must already have passed.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q3-d",
      "text": "Compiler warnings can safely be disabled.",
      "correct": false
    }
  ]
}
```

### prompt

The test README names an old executable, while the pinned CMake file defines different current test targets. What is the best immediate conclusion? [Current build](citation:src-build) [Historical test instructions](citation:src-test-doc)

### feedback_correct

The mismatch is evidence of a documentation/build-layout discrepancy. It does not establish a scientific or numerical defect.

### feedback_incorrect

Separate an unsuitable command from the behavior of a calculation that has actually run. Review tm-evidence-old-doc.

### option_explanations

A: The mismatch is evidence of a documentation/build-layout discrepancy. It does not establish a scientific or numerical defect.

B–D: Separate an unsuitable command from the behavior of a calculation that has actually run. Review tm-evidence-old-doc. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## Record: tm-evidence-q4

```yaml
{
  "identifier": "tm-evidence-q4",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q4-a",
      "text": "The compared calculations agree under the tested conditions; agreement alone does not establish real-world adequacy.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q4-b",
      "text": "Every calculated value is a correct measurement of the real system.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q4-c",
      "text": "No further implementation test can be useful.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q4-d",
      "text": "All input-data errors have been ruled out.",
      "correct": false
    }
  ]
}
```

### prompt

Two runs agree exactly, including after a restart. No comparison with real observations has been supplied. Which conclusion is justified?

### feedback_correct

Two calculations can share the same mistake. Agreement supports reproducibility of the tested behavior, not agreement with reality.

### feedback_incorrect

Ask which comparison was performed. A run-to-run comparison cannot substitute for a comparison with appropriate observations. Review tm-evidence-start and tm-evidence-kinds.

### option_explanations

A: Two calculations can share the same mistake. Agreement supports reproducibility of the tested behavior, not agreement with reality.

B–D: Ask which comparison was performed. A run-to-run comparison cannot substitute for a comparison with appropriate observations. Review tm-evidence-start and tm-evidence-kinds. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## Record: tm-evidence-q5

```yaml
{
  "identifier": "tm-evidence-q5",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q5-a",
      "text": "The exact inspected commit and relevant file location, with the behavior stated precisely.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q5-b",
      "text": "A stronger confidence adjective.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q5-c",
      "text": "The repository's popularity.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q5-d",
      "text": "An unrelated benchmark score.",
      "correct": false
    }
  ]
}
```

### prompt

A report cites a file path and says 'the current source does this,' but records neither a commit nor the inspected source bytes. What evidence most directly makes the claim reproducible?

### feedback_correct

A commit and relevant location identify the source version used for the claim. Wording and popularity do not recover missing provenance.

### feedback_incorrect

Someone else must be able to inspect the same code. Review tm-evidence-procedure, particularly the revision and source-location step.

### option_explanations

A: A commit and relevant location identify the source version used for the claim. Wording and popularity do not recover missing provenance.

B–D: Someone else must be able to inspect the same code. Review tm-evidence-procedure, particularly the revision and source-location step. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## Record: tm-evidence-q6

```yaml
{
  "identifier": "tm-evidence-q6",
  "type": "single_choice",
  "difficulty": "foundational",
  "concept_identifiers": [
    "tm-evidence"
  ],
  "mastery_contract_identifiers": [
    "tm-evidence-contract"
  ],
  "assessment_identifiers": [
    "tm-evidence-review"
  ],
  "terminal_outcomes": [
    "tm-verify-claims"
  ],
  "review_lesson_identifier": "tm-evidence-lesson",
  "terminology_identifiers": [],
  "options": [
    {
      "identifier": "tm-evidence-q6-a",
      "text": "The test did not complete because input opening failed; this run does not establish the numerical result.",
      "correct": true
    },
    {
      "identifier": "tm-evidence-q6-b",
      "text": "The scientific model is disproven.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q6-c",
      "text": "The test passed because no mismatching outputs were printed.",
      "correct": false
    },
    {
      "identifier": "tm-evidence-q6-d",
      "text": "Restart equivalence is proven for this input.",
      "correct": false
    }
  ]
}
```

### prompt

A test executable never started because its working-directory-dependent input path could not be opened. Which report keeps the evidence categories separate?

### feedback_correct

Failure to reach the comparison is not a successful comparison or a test of the model's scientific adequacy. Record the input-opening failure and conditions.

### feedback_incorrect

No mismatch is meaningful only if the intended comparison actually ran. Review tm-evidence-old-doc and the execution-evidence row of tm-evidence-kinds.

### option_explanations

A: Failure to reach the comparison is not a successful comparison or a test of the model's scientific adequacy. Record the input-opening failure and conditions.

B–D: No mismatch is meaningful only if the intended comparison actually ran. Review tm-evidence-old-doc and the execution-evidence row of tm-evidence-kinds. Each distractor either claims evidence the scenario has not
provided or proposes an action that cannot supply that missing evidence.

## References

NOAA-OWP TOPMODEL BMI, commit 89e4dc529dfdf7f23b7365530973e9f238fb740d,
consulted 2026-09-11. src-restart-test: test/main_integration_test_serialization.c,
lines 1–237. src-build: CMakeLists.txt, lines 1–121. src-test-doc: test/README.md,
lines 1–59. Full pinned source records are in sources.md.

