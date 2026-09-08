"""HTTP views for the generated curriculum application."""

from __future__ import annotations

import random

from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import models


def index(request):
    """Render the curriculum lesson index."""

    lessons = models.Lesson.objects.prefetch_related("assessments").all()
    assessments = models.Assessment.objects.all()
    return render(
        request,
        "__APP_NAME__/index.html",
        {"lessons": lessons, "assessments": assessments},
    )


def lesson_detail(request, identifier: str):
    """Render a lesson with source references."""

    lesson = get_object_or_404(
        models.Lesson.objects.prefetch_related("sources"),
        identifier=identifier,
    )
    next_lesson = models.Lesson.objects.filter(
        sequence__gt=lesson.sequence
    ).order_by("sequence").first()
    related_assessments = list(lesson.assessments.all())
    assessment_priority = {"section": 0, "midterm": 1, "final": 2, "pop": 3}
    related_assessments.sort(
        key=lambda assessment: assessment_priority.get(
            assessment.assessment_type,
            99,
        )
    )
    next_assessment = related_assessments[0] if related_assessments else None
    next_assessment_url = (
        reverse(
            "__APP_NAME__:assessment",
            kwargs={"identifier": next_assessment.identifier},
        )
        if next_assessment
        else ""
    )
    return render(
        request,
        "__APP_NAME__/lesson.html",
        {
            "lesson": lesson,
            "next_lesson": next_lesson,
            "next_assessment": next_assessment,
            "next_assessment_url": next_assessment_url,
        },
    )


def assessment_detail(request, identifier: str):
    """Render an assessment with client-side answer checking."""

    assessment = get_object_or_404(
        models.Assessment.objects.prefetch_related("questions", "lessons"),
        identifier=identifier,
    )
    lesson_sequences = [lesson.sequence for lesson in assessment.lessons.all()]
    next_lesson = None
    if lesson_sequences:
        next_lesson = models.Lesson.objects.filter(
            sequence__gt=max(lesson_sequences)
        ).order_by("sequence").first()
    next_url = (
        reverse("__APP_NAME__:lesson", kwargs={"identifier": next_lesson.identifier})
        if next_lesson
        else reverse("__APP_NAME__:index")
    )
    questions = list(assessment.questions.select_related("lesson"))
    random.shuffle(questions)
    if assessment.question_count:
        questions = questions[: assessment.question_count]
    for question in questions:
        question.answer_pairs = list(enumerate(question.answers))
        random.shuffle(question.answer_pairs)
    return render(
        request,
        "__APP_NAME__/assessment.html",
        {"assessment": assessment, "questions": questions, "next_url": next_url},
    )


def glossary(request):
    """Render glossary entries."""

    entries = models.GlossaryEntry.objects.all()
    return render(request, "__APP_NAME__/glossary.html", {"entries": entries})


def progress(request):
    """Render client-side progress controls."""

    return render(request, "__APP_NAME__/progress.html")
