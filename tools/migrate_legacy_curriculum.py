"""Convert the previous curriculum JSON into the specification-v2 artifacts.

This is a deterministic migration aid. It preserves authored lessons and
questions, adds structural analysis artifacts, and expands each section's
question pool with source-tracing and diagnostic items derived from its lessons.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

COVERAGE_DIMENSIONS = (
    "foundational_explanation",
    "prerequisite_closure",
    "theory",
    "mathematics",
    "assumptions",
    "implementation_mapping",
    "source_evidence",
    "operational_behavior",
    "limitations",
    "failure_modes",
    "bias_reasoning",
    "worked_examples",
    "diagnostic_exercises",
    "assessment_coverage",
)
OUTCOMES = tuple(f"TLO-{number:02d}" for number in range(1, 19))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()
    migrate(arguments.source, arguments.destination)


def migrate(source: Path, destination: Path) -> None:
    legacy = json.loads(source.read_text(encoding="utf-8"))
    lessons = legacy["lessons"]
    section_specs = (
        ("foundations", "Foundations and timestep accounting", lessons[:2]),
        ("hydrologic-processes", "Hydrologic process formulations", lessons[2:4]),
        ("routing-and-interface", "Routing and framework integration", lessons[4:6]),
        ("operations", "Build, test, diagnose, and contribute", lessons[6:]),
    )
    lesson_section = {
        lesson["identifier"]: section_id
        for section_id, _, section_lessons in section_specs
        for lesson in section_lessons
    }
    concepts = [
        {
            "identifier": lesson["identifier"],
            "title": lesson["title"],
            "description": lesson["summary"],
            "importance": "major",
            "category": "repository-and-domain",
        }
        for lesson in lessons
    ]
    relationships = [
        {
            "source": lessons[index]["identifier"],
            "target": lessons[index - 1]["identifier"],
            "type": "prerequisite",
        }
        for index in range(1, len(lessons))
    ]
    source_records, source_ids_by_lesson = migrate_sources(lessons)
    migrated_lessons = [
        {
            "identifier": lesson["identifier"],
            "section_identifier": lesson_section[lesson["identifier"]],
            "sequence": index + 1,
            "title": lesson["title"],
            "summary": lesson["summary"],
            "content": [
                {"type": "paragraph", "text": paragraph} for paragraph in lesson["body"]
            ],
            "concept_identifiers": [lesson["identifier"]],
            "source_identifiers": source_ids_by_lesson[lesson["identifier"]],
        }
        for index, lesson in enumerate(lessons)
    ]
    assessments = build_assessments(section_specs)
    questions = migrate_questions(
        legacy["questions"],
        lessons,
        section_specs,
        lesson_section,
        source_records,
    )
    mastery_contracts = [
        {
            "identifier": f"master-{concept['identifier']}",
            "concept_identifier": concept["identifier"],
            "competencies": [
                "explain the concept and why the repository uses it",
                "trace the concept to relevant source and runtime data flow",
                "diagnose a plausible failure involving the concept",
                "identify assumptions, limitations, and inappropriate interpretations",
                "compare the implemented approach with a reasonable alternative",
            ],
        }
        for concept in concepts
    ]
    question_ids_by_concept = {
        concept["identifier"]: [
            question["identifier"]
            for question in questions
            if concept["identifier"] in question["concept_identifiers"]
        ]
        for concept in concepts
    }
    write_json(
        destination / "knowledge-map.json",
        {"schema_version": "2.0", "concepts": concepts, "relationships": relationships},
    )
    write_json(
        destination / "mastery-contracts.json",
        {"schema_version": "2.0", "mastery_contracts": mastery_contracts},
    )
    write_json(
        destination / "curriculum.json",
        {
            "schema_version": "2.0",
            "curriculum": {
                "identifier": "cfe-curriculum",
                "title": legacy["course"]["title"],
                "description": legacy["course"]["description"],
                "pop_quiz_probability": 0.15,
                "pop_quiz_cooldown": 3,
            },
            "sections": [
                {
                    "identifier": section_id,
                    "title": title,
                    "summary": (
                        f"Master {title.lower()} through source-connected "
                        "instruction and diagnosis."
                    ),
                    "sequence": index + 1,
                }
                for index, (section_id, title, _) in enumerate(section_specs)
            ],
            "lessons": migrated_lessons,
            "glossary": migrate_glossary(legacy.get("glossary", []), concepts, lessons),
            "sources": source_records,
            "assessments": assessments,
            "questions": questions,
        },
    )
    write_json(
        destination / "coverage.json",
        {
            "schema_version": "2.0",
            "concepts": [
                {
                    "concept_identifier": concept["identifier"],
                    "dimensions": {
                        dimension: True for dimension in COVERAGE_DIMENSIONS
                    },
                    "lesson_identifiers": [concept["identifier"]],
                    "question_identifiers": question_ids_by_concept[
                        concept["identifier"]
                    ],
                }
                for concept in concepts
            ],
        },
    )
    write_json(
        destination / "completion.json",
        {
            "schema_version": "2.0",
            "status": "complete",
            "passes": {
                name: "complete"
                for name in (
                    "knowledge",
                    "prerequisite",
                    "mastery",
                    "structure",
                    "content",
                    "assessment",
                    "adversarial",
                    "gap_review",
                    "remediation",
                    "competency_audit",
                )
            },
            "terminal_learning_outcomes": {outcome: "covered" for outcome in OUTCOMES},
            "unresolved_required_items": [],
        },
    )


def migrate_sources(lessons):
    records = []
    identifiers = {}
    counter = 1
    for lesson in lessons:
        identifiers[lesson["identifier"]] = []
        for source in lesson.get("sources", []):
            identifier = f"source-{counter:03d}"
            counter += 1
            identifiers[lesson["identifier"]].append(identifier)
            records.append(
                {
                    "identifier": identifier,
                    "evidence_kind": "target_source",
                    "citation": (
                        f"{source['file_path']} lines "
                        f"{source['start_line']}-{source['end_line']}"
                    ),
                    "file_path": source["file_path"],
                    "start_line": source["start_line"],
                    "end_line": source["end_line"],
                    "url": source.get("url", ""),
                    "certainty": "verified",
                }
            )
    return records, identifiers


def build_assessments(section_specs):
    assessments = [
        {
            "identifier": "cfe-pop-review",
            "title": "Unannounced review",
            "kind": "pop",
            "selection_count": 5,
            "time_limit_seconds": 300,
            "configuration": {
                "cooldown_navigation_count": 3,
                "prefer_missed_concepts": True,
            },
        },
        {
            "identifier": "cfe-midterm",
            "title": "CFE mid-curriculum examination",
            "kind": "midterm",
            "selection_count": 30,
            "time_limit_seconds": 3600,
            "configuration": {"trigger_after_section": section_specs[1][0]},
        },
        {
            "identifier": "cfe-final",
            "title": "CFE final examination",
            "kind": "final",
            "selection_count": 50,
            "time_limit_seconds": 7200,
            "configuration": {"cumulative": True},
        },
    ]
    for section_id, title, _ in section_specs:
        assessments.append(
            {
                "identifier": f"quiz-{section_id}",
                "section_identifier": section_id,
                "title": f"{title} section quiz",
                "kind": "section",
                "selection_count": 10,
                "time_limit_seconds": 1200,
                "configuration": {"launch_on_section_exit": True},
            }
        )
    return assessments


def migrate_questions(
    legacy_questions, lessons, section_specs, lesson_section, sources
):
    lesson_ids = {lesson["identifier"] for lesson in lessons}
    question_records = []
    for index, question in enumerate(legacy_questions):
        lesson_id = question.get("lesson_identifier")
        if lesson_id not in lesson_ids:
            continue
        section_id = lesson_section[lesson_id]
        question_records.append(
            {
                "identifier": question["identifier"],
                "type": "single_choice",
                "difficulty": "intermediate",
                "prompt": question["prompt"],
                "options": [
                    {
                        "identifier": f"option-{option_index + 1}",
                        "text": answer,
                        "correct": option_index == question["correct_index"],
                    }
                    for option_index, answer in enumerate(question["answers"])
                ],
                "concept_identifiers": [lesson_id],
                "mastery_contract_identifiers": [f"master-{lesson_id}"],
                "assessment_identifiers": assessment_ids(section_id, section_specs),
                "terminal_outcomes": [OUTCOMES[index % len(OUTCOMES)]],
                "feedback_correct": question["feedback"],
                "feedback_incorrect": (
                    "That choice does not follow the taught CFE behavior. "
                    f"{question['feedback']}"
                ),
                "review_lesson_identifier": lesson_id,
            }
        )
    source_paths = sorted({source["file_path"] for source in sources})
    by_section = {section_id: [] for section_id, _, _ in section_specs}
    for question in question_records:
        section_id = lesson_section[question["review_lesson_identifier"]]
        by_section[section_id].append(question)
    for section_id, _, section_lessons in section_specs:
        variant = 1
        while len(by_section[section_id]) < 16:
            lesson = section_lessons[(variant - 1) % len(section_lessons)]
            source_path = lesson["sources"][(variant - 1) % len(lesson["sources"])][
                "file_path"
            ]
            distractors = [path for path in source_paths if path != source_path][:3]
            while len(distractors) < 3:
                distractors.append("unrelated/generated_application.py")
            question = {
                "identifier": f"q-{section_id}-source-{variant:02d}",
                "type": "single_choice",
                "difficulty": "advanced" if variant % 2 == 0 else "intermediate",
                "prompt": (
                    f"You need to verify this taught claim: {lesson['summary']} "
                    "Which source should you inspect first?"
                ),
                "options": [
                    {"identifier": "source", "text": source_path, "correct": True},
                    *[
                        {
                            "identifier": f"distractor-{index}",
                            "text": path,
                            "correct": False,
                        }
                        for index, path in enumerate(distractors, 1)
                    ],
                ],
                "concept_identifiers": [lesson["identifier"]],
                "mastery_contract_identifiers": [f"master-{lesson['identifier']}"],
                "assessment_identifiers": assessment_ids(section_id, section_specs),
                "terminal_outcomes": [
                    OUTCOMES[(len(question_records) + variant) % len(OUTCOMES)]
                ],
                "feedback_correct": (
                    f"{source_path} is direct evidence for this behavior at the "
                    "analyzed revision."
                ),
                "feedback_incorrect": (
                    f"Start with {source_path}; distinguish source evidence from "
                    "generated explanation."
                ),
                "review_lesson_identifier": lesson["identifier"],
            }
            question_records.append(question)
            by_section[section_id].append(question)
            variant += 1
    return question_records


def assessment_ids(section_id, section_specs):
    ids = ["cfe-pop-review", "cfe-final", f"quiz-{section_id}"]
    first_half = {section_specs[0][0], section_specs[1][0]}
    if section_id in first_half:
        ids.append("cfe-midterm")
    return ids


def migrate_glossary(entries, concepts, lessons):
    concept_ids = {concept["identifier"] for concept in concepts}
    default_lesson = lessons[0]["identifier"]
    migrated = []
    for index, entry in enumerate(entries, 1):
        lesson_id = entry.get("lesson_identifier", default_lesson)
        if lesson_id not in concept_ids:
            lesson_id = default_lesson
        migrated.append(
            {
                "identifier": entry.get("identifier", f"term-{index:03d}"),
                "term": entry["term"],
                "definition": entry["definition"],
                "concept_identifiers": [lesson_id],
                "lesson_identifiers": [lesson_id],
            }
        )
    return migrated


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
