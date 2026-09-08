"""Deterministic structural validation for curriculum analysis and products."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from .artifacts import CurriculumArtifacts

REQUIRED_COVERAGE_DIMENSIONS = {
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
}
ASSESSMENT_MINIMUMS = {"section": 10, "midterm": 30, "final": 50}
REQUIRED_ASSESSMENT_KINDS = {"pop", "section", "midterm", "final"}


@dataclass
class ValidationReport:
    """Machine-usable validation result with all detected failures."""

    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return whether no validation errors were detected."""

        return not self.errors

    def require(self, condition: bool, message: str) -> None:
        """Record a validation error when a condition is false."""

        if not condition:
            self.errors.append(message)

    def raise_for_errors(self) -> None:
        """Raise one actionable exception containing every detected error."""

        if self.errors:
            details = "\n".join(f"- {error}" for error in self.errors)
            raise ValueError(f"Curriculum validation failed:\n{details}")


def validate_artifacts(artifacts: CurriculumArtifacts) -> ValidationReport:
    """Validate closure, coverage, assessment depth, and completion state."""

    report = ValidationReport()
    curriculum = artifacts.curriculum
    required_lists = (
        "sections",
        "lessons",
        "glossary",
        "sources",
        "assessments",
        "questions",
    )
    report.require(isinstance(curriculum.get("curriculum"), dict), "missing curriculum")
    for field_name in required_lists:
        report.require(
            isinstance(curriculum.get(field_name), list), f"missing {field_name}"
        )
    if report.errors:
        return report

    concepts = artifacts.knowledge_map.get("concepts", [])
    relationships = artifacts.knowledge_map.get("relationships", [])
    contracts = artifacts.mastery_contracts.get("mastery_contracts", [])
    coverage = artifacts.coverage.get("concepts", [])
    completion = artifacts.completion
    _require_unique_identifiers(report, "concept", concepts)
    for name in required_lists:
        _require_unique_identifiers(report, name.rstrip("s"), curriculum[name])
    _require_unique_identifiers(report, "mastery contract", contracts)

    concept_ids = _identifiers(concepts)
    contract_ids = _identifiers(contracts)
    lesson_ids = _identifiers(curriculum["lessons"])
    question_ids = _identifiers(curriculum["questions"])
    major_concepts = {
        item["identifier"] for item in concepts if item.get("importance") == "major"
    }

    prerequisites = {
        relationship.get("target")
        for relationship in relationships
        if relationship.get("type") == "prerequisite"
    }
    referenced_concepts = {
        relationship.get("source") for relationship in relationships
    } | prerequisites
    report.require(
        referenced_concepts <= concept_ids,
        "knowledge-map relationships reference unknown concepts",
    )
    report.require(
        not _contains_cycle(concept_ids, relationships),
        "prerequisite graph has a cycle",
    )

    contract_concepts = {item.get("concept_identifier") for item in contracts}
    report.require(
        major_concepts <= contract_concepts,
        "every major concept must have a Mastery Contract",
    )
    for contract in contracts:
        report.require(
            bool(contract.get("competencies")),
            f"empty contract: {contract.get('identifier')}",
        )

    coverage_by_concept = {item.get("concept_identifier"): item for item in coverage}
    for concept_id in major_concepts:
        item = coverage_by_concept.get(concept_id)
        report.require(
            item is not None, f"missing coverage for major concept {concept_id}"
        )
        if item is None:
            continue
        dimensions = item.get("dimensions", {})
        missing_dimensions = REQUIRED_COVERAGE_DIMENSIONS - dimensions.keys()
        report.require(
            not missing_dimensions,
            f"{concept_id} missing coverage dimensions: {sorted(missing_dimensions)}",
        )
        incomplete = [
            name for name, complete in dimensions.items() if complete is not True
        ]
        report.require(
            not incomplete,
            f"{concept_id} has incomplete coverage: {sorted(incomplete)}",
        )

    for lesson in curriculum["lessons"]:
        report.require(
            set(lesson.get("concept_identifiers", [])) <= concept_ids,
            f"lesson {lesson.get('identifier')} references unknown concepts",
        )
        report.require(
            bool(lesson.get("content")),
            f"lesson {lesson.get('identifier')} has no content",
        )

    assessment_kinds = {item.get("kind") for item in curriculum["assessments"]}
    report.require(
        REQUIRED_ASSESSMENT_KINDS <= assessment_kinds,
        "required assessment kinds are missing",
    )
    questions_by_assessment: dict[str, int] = {}
    for question in curriculum["questions"]:
        for assessment_id in question.get("assessment_identifiers", []):
            questions_by_assessment[assessment_id] = (
                questions_by_assessment.get(assessment_id, 0) + 1
            )
        report.require(
            set(question.get("concept_identifiers", [])) <= concept_ids,
            f"question {question.get('identifier')} references unknown concepts",
        )
        report.require(
            set(question.get("mastery_contract_identifiers", [])) <= contract_ids,
            f"question {question.get('identifier')} references unknown contracts",
        )
        _validate_question(report, question)
    for assessment in curriculum["assessments"]:
        identifier = assessment.get("identifier")
        kind = assessment.get("kind")
        selection_count = assessment.get("selection_count", 0)
        minimum = ASSESSMENT_MINIMUMS.get(kind, 3 if kind == "pop" else 0)
        report.require(
            selection_count >= minimum,
            f"{identifier} selects fewer than {minimum} items",
        )
        report.require(
            questions_by_assessment.get(identifier, 0) > selection_count,
            f"{identifier} question bank must exceed its selection count",
        )
    section_ids = _identifiers(curriculum["sections"])
    sections_with_quizzes = {
        item.get("section_identifier")
        for item in curriculum["assessments"]
        if item.get("kind") == "section"
    }
    report.require(
        section_ids <= sections_with_quizzes, "every section must have a section quiz"
    )
    report.require(lesson_ids, "at least one lesson is required")
    report.require(question_ids, "at least one question is required")

    report.require(
        completion.get("status") == "complete", "completion status is not complete"
    )
    report.require(
        not completion.get("unresolved_required_items"),
        "required items remain unresolved",
    )
    required_passes = {
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
    }
    passes = completion.get("passes", {})
    report.require(
        all(passes.get(pass_name) == "complete" for pass_name in required_passes),
        "all generation and audit passes must be complete",
    )
    outcomes = completion.get("terminal_learning_outcomes", {})
    report.require(bool(outcomes), "terminal learning outcome audit is missing")
    report.require(
        all(value == "covered" for value in outcomes.values()),
        "terminal outcomes are not fully covered",
    )
    final_assessment_ids = {
        item["identifier"]
        for item in curriculum["assessments"]
        if item.get("kind") == "final"
    }
    final_questions = [
        question
        for question in curriculum["questions"]
        if final_assessment_ids & set(question.get("assessment_identifiers", []))
    ]
    final_outcomes = {
        outcome
        for question in final_questions
        for outcome in question.get("terminal_outcomes", [])
    }
    report.require(
        set(outcomes) <= final_outcomes,
        "the final examination does not assess every terminal outcome",
    )
    final_contracts = {
        contract
        for question in final_questions
        for contract in question.get("mastery_contract_identifiers", [])
    }
    major_contracts = {
        item["identifier"]
        for item in contracts
        if item.get("concept_identifier") in major_concepts
    }
    report.require(
        major_contracts <= final_contracts,
        "the final examination does not assess every major Mastery Contract",
    )
    return report


def _validate_question(report: ValidationReport, question: dict[str, Any]) -> None:
    """Validate a deterministically gradable question."""

    identifier = question.get("identifier")
    question_type = question.get("type")
    report.require(
        question_type
        in {"single_choice", "multiple_select", "true_false", "numeric", "text"},
        f"unsupported question type for {identifier}",
    )
    report.require(
        bool(question.get("feedback_correct")), f"{identifier} lacks correct feedback"
    )
    report.require(
        bool(question.get("feedback_incorrect")),
        f"{identifier} lacks incorrect feedback",
    )
    report.require(
        bool(question.get("review_lesson_identifier")),
        f"{identifier} lacks review material",
    )
    if question_type in {"single_choice", "multiple_select", "true_false"}:
        options = question.get("options", [])
        report.require(len(options) >= 2, f"{identifier} needs at least two options")
        report.require(
            any(option.get("correct") is True for option in options),
            f"{identifier} has no correct option",
        )
    elif question_type == "numeric":
        report.require(
            "accepted_value" in question, f"{identifier} lacks accepted_value"
        )
        report.require("tolerance" in question, f"{identifier} lacks tolerance")
    elif question_type == "text":
        report.require(
            bool(question.get("accepted_answers")),
            f"{identifier} lacks accepted_answers",
        )


def _require_unique_identifiers(
    report: ValidationReport,
    record_type: str,
    records: Iterable[dict[str, Any]],
) -> None:
    identifiers = [record.get("identifier") for record in records]
    report.require(
        all(isinstance(value, str) and value for value in identifiers),
        f"{record_type} identifiers must be non-empty strings",
    )
    report.require(
        len(identifiers) == len(set(identifiers)),
        f"duplicate {record_type} identifiers",
    )


def _identifiers(records: Iterable[dict[str, Any]]) -> set[str]:
    return {
        record["identifier"]
        for record in records
        if isinstance(record.get("identifier"), str)
    }


def _contains_cycle(concept_ids: set[str], relationships: list[dict[str, Any]]) -> bool:
    graph: dict[str, list[str]] = {identifier: [] for identifier in concept_ids}
    for relationship in relationships:
        if relationship.get("type") == "prerequisite":
            source = relationship.get("source")
            target = relationship.get("target")
            if source in graph and target in graph:
                graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> bool:
        if identifier in visiting:
            return True
        if identifier in visited:
            return False
        visiting.add(identifier)
        if any(visit(neighbor) for neighbor in graph.get(identifier, [])):
            return True
        visiting.remove(identifier)
        visited.add(identifier)
        return False

    return any(visit(identifier) for identifier in concept_ids)
