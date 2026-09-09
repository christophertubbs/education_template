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
    "terminology_closure",
    "readability_review",
}
REQUIRED_TERMINOLOGY_FIELDS = {
    "identifier",
    "term",
    "full_name",
    "decomposition",
    "definition",
    "purpose",
    "role",
    "units",
    "dimensionality",
    "valid_range",
    "behavior",
    "related_terms",
    "equation_relationships",
    "source_mappings",
    "example",
    "misconception",
    "lesson_identifiers",
}
TERMINOLOGY_ROLES = {
    "input",
    "parameter",
    "state",
    "flux",
    "intermediate",
    "configuration",
    "output",
}
REQUIRED_BEHAVIOR_FIELDS = {"zero", "smaller", "larger", "limits"}
ASSESSMENT_MINIMUMS = {"section": 10, "midterm": 30, "final": 50}
REQUIRED_ASSESSMENT_KINDS = {"pop", "section", "midterm", "final"}
SUPPORTED_BLOCK_TYPES = {
    "paragraph",
    "heading",
    "equation",
    "code",
    "callout",
    "worked_example",
    "diagnostic_example",
    "warning",
    "note",
    "definition",
    "theorem",
    "rule",
    "principle",
    "ordered_list",
    "unordered_list",
    "table",
    "comparison_table",
    "quote",
    "procedure",
    "source_reference",
    "variable_table",
}
SUPPORTED_INLINE_TYPES = {
    "text",
    "code",
    "math",
    "glossary",
    "emphasis",
    "strong",
    "file",
    "command",
    "citation",
}
CALLOUT_TYPES = {
    "note",
    "important",
    "warning",
    "implementation-detail",
    "scientific-assumption",
    "common-mistake",
    "performance-concern",
    "debugging-tip",
    "source-discrepancy",
    "model-limitation",
}


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
        "terminology",
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
    glossary_entries = {
        item["identifier"]: item
        for item in curriculum["glossary"]
        if isinstance(item.get("identifier"), str)
    }
    question_ids = _identifiers(curriculum["questions"])
    terminology = curriculum["terminology"]
    terminology_ids = _identifiers(terminology)
    source_ids = _identifiers(curriculum["sources"])
    major_concepts = {
        item["identifier"] for item in concepts if item.get("importance") == "major"
    }
    _require_unique_identifiers(report, "terminology", terminology)
    _validate_terminology(
        report,
        terminology,
        lesson_ids=lesson_ids,
        source_ids=source_ids,
    )

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

    taught_terminology: set[str] = set()
    section_sequence = {
        section.get("identifier"): section.get("sequence", 0)
        for section in curriculum["sections"]
    }
    ordered_lessons = sorted(
        curriculum["lessons"],
        key=lambda item: (
            section_sequence.get(item.get("section_identifier"), 0),
            item.get("sequence", 0),
        ),
    )
    for lesson in ordered_lessons:
        report.require(
            set(lesson.get("concept_identifiers", [])) <= concept_ids,
            f"lesson {lesson.get('identifier')} references unknown concepts",
        )
        report.require(
            bool(lesson.get("content")),
            f"lesson {lesson.get('identifier')} has no content",
        )
        introduced = set(lesson.get("introduced_terminology_identifiers", []))
        report.require(
            introduced <= terminology_ids,
            f"lesson {lesson.get('identifier')} introduces unknown terminology",
        )
        _validate_lesson_content(
            report,
            lesson,
            glossary_entries,
            terminology_ids,
            taught_terminology,
            introduced,
        )
        taught_terminology.update(introduced)

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
        question_terms = set(question.get("terminology_identifiers", []))
        report.require(
            bool(question_terms),
            f"question {question.get('identifier')} lacks terminology mapping",
        )
        report.require(
            question_terms <= terminology_ids,
            f"question {question.get('identifier')} references unknown terminology",
        )
        review_lesson = question.get("review_lesson_identifier")
        taught_for_review = {
            item["identifier"]
            for item in terminology
            if review_lesson in item.get("lesson_identifiers", [])
        }
        report.require(
            question_terms <= taught_for_review,
            f"question {question.get('identifier')} uses terminology not taught "
            "in its review lesson",
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
        "terminology_closure",
        "readability_review",
    }
    passes = completion.get("passes", {})
    report.require(
        all(passes.get(pass_name) == "complete" for pass_name in required_passes),
        "all generation and audit passes must be complete",
    )
    audits = completion.get("audit_evidence", {})
    for audit_name in ("terminology_closure", "readability_review"):
        audit = audits.get(audit_name, {})
        report.require(
            audit.get("status") == "complete"
            and bool(audit.get("method"))
            and bool(audit.get("reviewed_lesson_identifiers"))
            and not audit.get("unresolved_items"),
            f"{audit_name} audit evidence is incomplete",
        )
    readability = audits.get("readability_review", {})
    report.require(
        readability.get("manual_contextual_review") is True,
        "readability review cannot rely only on an automated score",
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


def _validate_lesson_content(
    report: ValidationReport,
    lesson: dict[str, Any],
    glossary_entries: dict[str, dict[str, Any]],
    terminology_ids: set[str],
    taught_terminology: set[str],
    introduced_terminology: set[str],
) -> None:
    """Validate structured lesson blocks and their semantic inline content."""

    lesson_id = lesson.get("identifier")
    blocks = lesson.get("content", [])
    declared_terms = set(lesson.get("terminology_identifiers", []))
    report.require(
        bool(declared_terms), f"lesson {lesson_id} lacks a terminology inventory"
    )
    report.require(
        declared_terms <= terminology_ids,
        f"lesson {lesson_id} references unknown terminology",
    )
    report.require(
        introduced_terminology <= declared_terms,
        f"lesson {lesson_id} introduces terminology it does not declare",
    )
    report.require(
        declared_terms <= taught_terminology | introduced_terminology,
        f"lesson {lesson_id} uses terminology before it is taught",
    )
    serialized_content = str(blocks).casefold()
    for glossary_id, entry in glossary_entries.items():
        recognized_terms = [entry.get("term", ""), *entry.get("aliases", [])]
        if any(
            isinstance(value, str) and value and value.casefold() in serialized_content
            for value in recognized_terms
        ):
            report.require(
                lesson_id in entry.get("lesson_identifiers", []),
                f"lesson {lesson_id} mentions glossary entry {glossary_id} "
                "without a visible lesson definition",
            )
    block_types = {block.get("type") for block in blocks if isinstance(block, dict)}
    report.require(
        all(isinstance(block, dict) for block in blocks),
        f"lesson {lesson_id} contains a non-object content block",
    )
    report.require(
        block_types <= SUPPORTED_BLOCK_TYPES,
        f"lesson {lesson_id} contains unsupported block types: "
        f"{sorted(str(value) for value in block_types - SUPPORTED_BLOCK_TYPES)}",
    )
    report.require(
        block_types != {"paragraph"},
        f"lesson {lesson_id} flattens all content into paragraphs",
    )
    defined_variables: set[str] = set()
    for index, block in enumerate(blocks):
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")
        location = f"lesson {lesson_id} block {index + 1}"
        if block_type in {
            "paragraph",
            "callout",
            "warning",
            "note",
            "definition",
            "theorem",
            "rule",
            "principle",
        }:
            _validate_inline(report, block.get("inline"), location, glossary_entries)
        if block_type == "equation":
            report.require(bool(block.get("latex")), f"{location} lacks LaTeX")
            report.require(
                bool(block.get("accessible_text")),
                f"{location} lacks accessible equation text",
            )
            equation_variables = set(block.get("variable_identifiers", []))
            report.require(
                bool(equation_variables),
                f"{location} lacks explicit variable mappings",
            )
            report.require(
                equation_variables <= terminology_ids,
                f"{location} references unknown equation variables",
            )
            report.require(
                equation_variables <= defined_variables,
                f"{location} uses variables before their variable-table definitions",
            )
            report.require(
                _balanced_braces(block.get("latex", "")),
                f"{location} has malformed mathematical markup",
            )
        elif block_type == "code":
            report.require(bool(block.get("code")), f"{location} has no code")
            report.require(
                bool(block.get("language")), f"{location} lacks code language metadata"
            )
            report.require(bool(block.get("kind")), f"{location} lacks code kind")
        elif block_type in {"callout", "warning", "note"}:
            semantic_type = block.get("semantic_type", block_type)
            report.require(
                semantic_type in CALLOUT_TYPES,
                f"{location} has unsupported callout type {semantic_type}",
            )
            report.require(bool(block.get("title")), f"{location} lacks a title")
        elif block_type == "variable_table":
            rows = block.get("rows", [])
            report.require(bool(block.get("caption")), f"{location} lacks a caption")
            report.require(bool(rows), f"{location} has no variable rows")
            for row in rows:
                required = {
                    "symbol",
                    "accessible_symbol",
                    "identifier",
                    "meaning",
                    "units",
                    "role",
                }
                report.require(
                    isinstance(row, dict) and required <= row.keys(),
                    f"{location} has an incomplete variable definition",
                )
                terminology_identifier = row.get("terminology_identifier")
                report.require(
                    terminology_identifier in terminology_ids,
                    f"{location} has a variable missing from the terminology inventory",
                )
                if terminology_identifier in terminology_ids:
                    defined_variables.add(terminology_identifier)
        elif block_type in {"table", "comparison_table"}:
            headers = block.get("headers", [])
            rows = block.get("rows", [])
            report.require(bool(block.get("caption")), f"{location} lacks a caption")
            report.require(
                bool(headers) and bool(rows), f"{location} has an empty table"
            )
            for row in rows:
                report.require(
                    len(row) == len(headers),
                    f"{location} has a row with the wrong number of cells",
                )
                for cell in row:
                    _validate_inline(report, cell, location, glossary_entries)
        elif block_type in {"ordered_list", "unordered_list"}:
            report.require(bool(block.get("items")), f"{location} has no list items")
            for item in block.get("items", []):
                _validate_inline(report, item, location, glossary_entries)
        elif block_type in {"worked_example", "diagnostic_example", "procedure"}:
            report.require(bool(block.get("title")), f"{location} lacks a title")
            if block_type in {"worked_example", "procedure"}:
                report.require(bool(block.get("steps")), f"{location} has no steps")
                for step in block.get("steps", []):
                    _validate_inline(report, step, location, glossary_entries)


def _validate_terminology(
    report: ValidationReport,
    records: list[dict[str, Any]],
    *,
    lesson_ids: set[str],
    source_ids: set[str],
) -> None:
    """Validate the machine-readable terminology contract."""

    for record in records:
        identifier = record.get("identifier", "<missing>")
        report.require(
            REQUIRED_TERMINOLOGY_FIELDS <= record.keys(),
            f"terminology {identifier} has incomplete contract fields",
        )
        for field_name in REQUIRED_TERMINOLOGY_FIELDS - {
            "identifier",
            "behavior",
            "related_terms",
            "equation_relationships",
            "source_mappings",
            "lesson_identifiers",
        }:
            report.require(
                isinstance(record.get(field_name), str)
                and bool(record.get(field_name, "").strip()),
                f"terminology {identifier} has empty {field_name}",
            )
        report.require(
            record.get("role") in TERMINOLOGY_ROLES,
            f"terminology {identifier} has unsupported semantic role",
        )
        behavior = record.get("behavior", {})
        report.require(
            isinstance(behavior, dict)
            and REQUIRED_BEHAVIOR_FIELDS <= behavior.keys()
            and all(
                isinstance(behavior.get(name), str) and behavior[name].strip()
                for name in REQUIRED_BEHAVIOR_FIELDS
            ),
            f"terminology {identifier} has incomplete behavior semantics",
        )
        definition = record.get("definition", "").strip().casefold()
        term = record.get("term", "").strip().casefold()
        full_name = record.get("full_name", "").strip().casefold()
        report.require(
            definition not in {term, full_name},
            f"terminology {identifier} has a circular or restated definition",
        )
        related = record.get("related_terms")
        report.require(
            isinstance(related, list),
            f"terminology {identifier} has invalid related-term distinctions",
        )
        if isinstance(related, list):
            for comparison in related:
                report.require(
                    isinstance(comparison, dict)
                    and bool(comparison.get("identifier"))
                    and bool(comparison.get("distinction")),
                    f"terminology {identifier} has an incomplete "
                    "related-term distinction",
                )
        source_mappings = record.get("source_mappings")
        report.require(
            isinstance(source_mappings, list) and bool(source_mappings),
            f"terminology {identifier} lacks source mappings",
        )
        if isinstance(source_mappings, list):
            for mapping in source_mappings:
                report.require(
                    isinstance(mapping, dict)
                    and bool(mapping.get("code_identifier"))
                    and mapping.get("source_identifier") in source_ids,
                    f"terminology {identifier} has an invalid source mapping",
                )
        taught_lessons = record.get("lesson_identifiers", [])
        report.require(
            isinstance(taught_lessons, list)
            and bool(taught_lessons)
            and set(taught_lessons) <= lesson_ids,
            f"terminology {identifier} has invalid teaching lessons",
        )


def _validate_inline(
    report: ValidationReport,
    inline: Any,
    location: str,
    glossary_entries: dict[str, dict[str, Any]],
) -> None:
    report.require(
        isinstance(inline, list) and bool(inline),
        f"{location} lacks structured inline content",
    )
    if not isinstance(inline, list):
        return
    for item in inline:
        item_type = item.get("type") if isinstance(item, dict) else None
        report.require(
            item_type in SUPPORTED_INLINE_TYPES,
            f"{location} has unsupported inline type {item_type}",
        )
        if not isinstance(item, dict) or item_type not in SUPPORTED_INLINE_TYPES:
            continue
        report.require(bool(item.get("text")), f"{location} has empty inline content")
        if item_type == "math":
            report.require(
                bool(item.get("latex")), f"{location} inline math lacks LaTeX"
            )
            report.require(
                bool(item.get("accessible_text")),
                f"{location} inline math lacks accessible text",
            )
        elif item_type == "glossary":
            glossary_id = item.get("glossary_identifier")
            report.require(
                glossary_id in glossary_entries,
                f"{location} references unknown glossary entry {glossary_id}",
            )
            report.require(
                bool(item.get("definition")),
                f"{location} glossary reference lacks a definition",
            )


def _balanced_braces(value: str) -> bool:
    """Perform a conservative structural check for generated LaTeX."""

    depth = 0
    for character in value:
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


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
