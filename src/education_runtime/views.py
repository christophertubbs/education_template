"""Thin HTTP views delegating curriculum behavior to runtime services."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Assessment, Curriculum, Lesson
from .services import curriculum_assessments, select_assessment_questions


def curriculum_list(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "education_runtime/curriculum_list.html",
        {"curricula": Curriculum.objects.all()},
    )


def curriculum_detail(request: HttpRequest, curriculum_id: str) -> HttpResponse:
    curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
    sections = curriculum.section_set.prefetch_related("lesson_set")
    return render(
        request,
        "education_runtime/curriculum_detail.html",
        {
            "curriculum": curriculum,
            "sections": sections,
            "assessments": curriculum_assessments(curriculum_id),
        },
    )


def lesson_detail(
    request: HttpRequest,
    curriculum_id: str,
    lesson_id: str,
) -> HttpResponse:
    lesson = get_object_or_404(
        Lesson.objects.select_related("section__curriculum").prefetch_related(
            "sources", "concepts"
        ),
        pk=lesson_id,
        section__curriculum_id=curriculum_id,
    )
    curriculum = lesson.section.curriculum
    ordered_lessons = list(
        Lesson.objects.filter(section__curriculum=curriculum).select_related("section")
    )
    lesson_index = next(
        index
        for index, candidate in enumerate(ordered_lessons)
        if candidate.pk == lesson.pk
    )
    next_lesson = (
        ordered_lessons[lesson_index + 1]
        if lesson_index + 1 < len(ordered_lessons)
        else None
    )
    if next_lesson is None or next_lesson.section_id != lesson.section_id:
        assessment = Assessment.objects.filter(
            curriculum=curriculum, section=lesson.section, kind="section"
        ).first()
        advance_url = (
            reverse(
                "education_runtime:assessment",
                args=(curriculum.pk, assessment.pk),
            )
            if assessment
            else next_lesson.get_absolute_url()
            if next_lesson
            else ""
        )
    else:
        advance_url = next_lesson.get_absolute_url()
    return render(
        request,
        "education_runtime/lesson.html",
        {
            "curriculum": curriculum,
            "lesson": lesson,
            "advance_url": advance_url,
            "glossary_entries": curriculum.glossaryentry_set.filter(
                lessons=lesson
            ).distinct(),
        },
    )


def assessment_detail(
    request: HttpRequest,
    curriculum_id: str,
    assessment_id: str,
) -> HttpResponse:
    assessment = get_object_or_404(
        Assessment.objects.select_related("curriculum", "section"),
        pk=assessment_id,
        curriculum_id=curriculum_id,
    )
    eligible_lessons = None
    if assessment.kind == "pop":
        eligible_lessons = {
            value for value in request.GET.get("lessons", "").split(",") if value
        }
    questions = select_assessment_questions(assessment, eligible_lessons)
    question_payload = [
        {
            "identifier": question.identifier,
            "type": question.question_type,
            "scoring": question.display_scoring,
            "feedback_correct": question.feedback_correct,
            "feedback_incorrect": question.feedback_incorrect,
            "review_url": question.review_lesson.get_absolute_url()
            if hasattr(question.review_lesson, "get_absolute_url")
            else "",
        }
        for question in questions
    ]
    return render(
        request,
        "education_runtime/assessment.html",
        {
            "curriculum": assessment.curriculum,
            "assessment": assessment,
            "questions": questions,
            "question_payload": question_payload,
            "next_url": _next_assessment_url(assessment),
        },
    )


def glossary(request: HttpRequest, curriculum_id: str) -> HttpResponse:
    curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
    return render(
        request,
        "education_runtime/glossary.html",
        {
            "curriculum": curriculum,
            "entries": curriculum.glossaryentry_set.prefetch_related(
                "concepts", "lessons"
            ),
        },
    )


def sources(request: HttpRequest, curriculum_id: str) -> HttpResponse:
    curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
    return render(
        request,
        "education_runtime/sources.html",
        {"curriculum": curriculum, "sources": curriculum.sourcereference_set.all()},
    )


def progress(request: HttpRequest, curriculum_id: str) -> HttpResponse:
    curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
    return render(
        request, "education_runtime/progress.html", {"curriculum": curriculum}
    )


def _next_assessment_url(assessment: Assessment) -> str:
    """Return the required learning destination after an assessment."""

    curriculum = assessment.curriculum
    if assessment.kind == "pop":
        return reverse("education_runtime:curriculum-detail", args=(curriculum.pk,))
    sections = list(curriculum.section_set.all())
    if assessment.kind == "section" and assessment.section in sections:
        section_index = sections.index(assessment.section)
        midpoint_index = max(0, (len(sections) // 2) - 1)
        if section_index == midpoint_index:
            midterm = curriculum.assessment_set.filter(kind="midterm").first()
            if midterm:
                return reverse(
                    "education_runtime:assessment", args=(curriculum.pk, midterm.pk)
                )
        if section_index + 1 < len(sections):
            next_lesson = sections[section_index + 1].lesson_set.first()
            if next_lesson:
                return next_lesson.get_absolute_url()
    if assessment.kind == "midterm":
        next_section = sections[len(sections) // 2] if sections else None
        next_lesson = next_section.lesson_set.first() if next_section else None
        if next_lesson:
            return next_lesson.get_absolute_url()
    if assessment.kind == "section":
        final = curriculum.assessment_set.filter(kind="final").first()
        if final:
            return reverse(
                "education_runtime:assessment", args=(curriculum.pk, final.pk)
            )
    return reverse("education_runtime:curriculum-detail", args=(curriculum.pk,))
