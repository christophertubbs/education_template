"""Runtime queries and deterministic assessment selection."""

from __future__ import annotations

import random

from django.db.models import QuerySet

from .models import Assessment, Question


def select_assessment_questions(
    assessment: Assessment,
    eligible_lesson_ids: set[str] | None = None,
) -> list[Question]:
    """Choose a varied question set from a validated oversized bank."""

    query = assessment.questions.select_related("review_lesson").prefetch_related(
        "concepts", "mastery_contracts"
    )
    if eligible_lesson_ids is not None:
        query = query.filter(review_lesson_id__in=eligible_lesson_ids)
    questions = list(query)
    random.SystemRandom().shuffle(questions)
    selection_count = min(assessment.selection_count, len(questions))
    selected = questions[:selection_count]
    for question in selected:
        options = question.scoring.get("options")
        if options:
            shuffled_options = list(options)
            random.SystemRandom().shuffle(shuffled_options)
            question.display_scoring = {**question.scoring, "options": shuffled_options}
        else:
            question.display_scoring = question.scoring
    return selected


def curriculum_assessments(curriculum_id: str) -> QuerySet[Assessment]:
    """Return assessment navigation for one curriculum."""

    return Assessment.objects.filter(curriculum_id=curriculum_id).select_related(
        "section"
    )
