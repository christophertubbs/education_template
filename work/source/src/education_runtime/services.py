"""Runtime queries and deterministic assessment selection."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

from django.db.models import QuerySet

from .models import Assessment, Question

CoverageKey = TypeVar("CoverageKey", bound=Hashable)


def select_assessment_questions(
    assessment: Assessment,
    eligible_lesson_ids: set[str] | None = None,
) -> list[Question]:
    """Choose a varied question set from a validated oversized bank."""

    query = assessment.questions.select_related(
        "review_lesson__section"
    ).prefetch_related("concepts", "mastery_contracts__concept")
    if eligible_lesson_ids is not None:
        query = query.filter(review_lesson_id__in=eligible_lesson_ids)
    questions = list(query)
    random_source = random.SystemRandom()
    random_source.shuffle(questions)
    selection_count = min(assessment.selection_count, len(questions))
    selected = _coverage_preserving_selection(
        questions,
        selection_count,
        assessment,
        random_source,
    )
    for question in selected:
        options = question.scoring.get("options")
        if options:
            shuffled_options = list(options)
            random_source.shuffle(shuffled_options)
            question.display_scoring = {**question.scoring, "options": shuffled_options}
        else:
            question.display_scoring = question.scoring
    return selected


def _coverage_preserving_selection(
    questions: list[Question],
    selection_count: int,
    assessment: Assessment,
    random_source: random.Random,
) -> list[Question]:
    """Select a varied attempt while retaining required competency coverage."""

    if assessment.kind == "pop":
        return questions[:selection_count]

    selected: list[Question] = []
    selected_ids: set[str] = set()

    major_concept_ids = {
        concept.identifier
        for question in questions
        for concept in question.concepts.all()
        if concept.importance == "major"
    }
    configured_minimum = assessment.configuration.get(
        "required_minimum_per_major_concept", 1
    )
    if not isinstance(configured_minimum, int) or configured_minimum < 1:
        configured_minimum = 1
    _select_for_minimum_coverage(
        questions,
        selected,
        selected_ids,
        major_concept_ids,
        configured_minimum,
        lambda question: {
            concept.identifier
            for concept in question.concepts.all()
            if concept.importance == "major"
        },
        selection_count,
        random_source,
        "major concepts",
    )

    major_contract_ids = {
        contract.identifier
        for question in questions
        for contract in question.mastery_contracts.all()
        if contract.concept.importance == "major"
    }
    _select_for_minimum_coverage(
        questions,
        selected,
        selected_ids,
        major_contract_ids,
        1,
        lambda question: {
            contract.identifier
            for contract in question.mastery_contracts.all()
            if contract.concept.importance == "major"
        },
        selection_count,
        random_source,
        "major Mastery Contracts",
    )

    if assessment.kind in {"midterm", "final"}:
        section_ids = {question.review_lesson.section_id for question in questions}
        _select_for_minimum_coverage(
            questions,
            selected,
            selected_ids,
            section_ids,
            1,
            lambda question: {question.review_lesson.section_id},
            selection_count,
            random_source,
            "curriculum sections",
        )
        terminal_outcomes = {
            outcome for question in questions for outcome in question.terminal_outcomes
        }
        _select_for_minimum_coverage(
            questions,
            selected,
            selected_ids,
            terminal_outcomes,
            1,
            lambda question: set(question.terminal_outcomes),
            selection_count,
            random_source,
            "terminal outcomes",
        )

    remaining = [
        question for question in questions if question.identifier not in selected_ids
    ]
    random_source.shuffle(remaining)
    selected.extend(remaining[: selection_count - len(selected)])
    random_source.shuffle(selected)
    return selected


def _select_for_minimum_coverage(
    questions: list[Question],
    selected: list[Question],
    selected_ids: set[str],
    required_keys: Iterable[CoverageKey],
    minimum: int,
    question_keys: Callable[[Question], set[CoverageKey]],
    selection_count: int,
    random_source: random.Random,
    coverage_name: str,
) -> None:
    """Greedily add randomized questions until each required key meets a quota."""

    required = set(required_keys)
    covered: Counter[CoverageKey] = Counter()
    for question in selected:
        covered.update(question_keys(question) & required)

    while any(covered[key] < minimum for key in required):
        unmet = {key for key in required if covered[key] < minimum}
        candidates = [
            question
            for question in questions
            if question.identifier not in selected_ids
            and question_keys(question) & unmet
        ]
        if not candidates or len(selected) >= selection_count:
            missing = sorted(str(key) for key in unmet)
            raise ValueError(
                f"Assessment {coverage_name} cannot fit required coverage "
                f"within {selection_count} questions; missing {missing}"
            )
        random_source.shuffle(candidates)
        candidate = max(
            candidates,
            key=lambda question: len(question_keys(question) & unmet),
        )
        selected.append(candidate)
        selected_ids.add(candidate.identifier)
        covered.update(question_keys(candidate) & required)


def curriculum_assessments(curriculum_id: str) -> QuerySet[Assessment]:
    """Return assessment navigation for one curriculum."""

    return Assessment.objects.filter(curriculum_id=curriculum_id).select_related(
        "section"
    )

