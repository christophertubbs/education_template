"""Services for loading packaged curriculum data into the database."""

from __future__ import annotations

import hashlib
import json
from importlib import resources
from typing import Any

from django.utils import timezone

from . import models


def load_packaged_curriculum() -> dict[str, int]:
    """Load deterministic packaged curriculum records into the database.

    Existing records marked as human modified are preserved. Generated
    records are updated when their baseline fingerprint still matches
    generated ownership.

    :return: Counts of loaded record types.
    """

    data = read_curriculum_data()
    generated_at = timezone.now()
    course_count = upsert_course(data["course"], generated_at)
    lesson_count = upsert_lessons(data["lessons"], generated_at)
    glossary_count = upsert_glossary(data["glossary"], generated_at)
    assessment_count = upsert_assessments(data["assessments"], generated_at)
    question_count = upsert_questions(data["questions"], generated_at)
    coverage_count = upsert_coverage(data["coverage"])
    return {
        "courses": course_count,
        "lessons": lesson_count,
        "glossary_entries": glossary_count,
        "assessments": assessment_count,
        "questions": question_count,
        "coverage_records": coverage_count,
    }


def read_curriculum_data() -> dict[str, Any]:
    """Read packaged curriculum JSON data.

    :return: Parsed curriculum data.
    """

    curriculum_file = resources.files("__APP_NAME__") / "data" / "curriculum.json"
    return json.loads(curriculum_file.read_text())


def fingerprint(record: dict[str, Any]) -> str:
    """Create a stable content fingerprint for a generated record.

    :param record: Structured record content.
    :return: SHA-256 hexadecimal fingerprint.
    """

    payload = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def should_update(instance: models.GeneratedContentModel) -> bool:
    """Return whether generated loading may update a model instance."""

    return not instance.is_human_modified


def upsert_generated_model(
    model_class: type[models.GeneratedContentModel],
    identifier: str,
    defaults: dict[str, Any],
    generated_at,
) -> tuple[models.GeneratedContentModel, bool]:
    """Create or update a generated content model while preserving edits."""

    record_fingerprint = fingerprint({"identifier": identifier, **defaults})
    instance, was_created = model_class.objects.get_or_create(
        identifier=identifier,
        defaults={
            **defaults,
            "baseline_fingerprint": record_fingerprint,
            "generated_at": generated_at,
        },
    )
    if not was_created and should_update(instance):
        for field_name, field_value in defaults.items():
            setattr(instance, field_name, field_value)
        instance.baseline_fingerprint = record_fingerprint
        instance.generated_at = generated_at
        instance.save()
    return instance, was_created


def upsert_course(course: dict[str, Any], generated_at) -> int:
    """Load the generated course record."""

    upsert_generated_model(
        models.Course,
        course["identifier"],
        {
            "title": course["title"],
            "description": course["description"],
            "passing_score": course["passing_score"],
        },
        generated_at,
    )
    return 1


def upsert_lessons(lessons: list[dict[str, Any]], generated_at) -> int:
    """Load generated lesson and source-reference records."""

    for lesson in lessons:
        lesson_instance, _ = upsert_generated_model(
            models.Lesson,
            lesson["identifier"],
            {
                "sequence": int(lesson["sequence"]),
                "title": lesson["title"],
                "summary": lesson["summary"],
                "body": lesson["body"],
            },
            generated_at,
        )
        if should_update(lesson_instance):
            lesson_instance.sources.all().delete()
            for source in lesson["sources"]:
                models.SourceReference.objects.create(
                    lesson=lesson_instance,
                    file_path=source["file_path"],
                    start_line=source["start_line"],
                    end_line=source["end_line"],
                    url=source["url"],
                )
    return len(lessons)


def upsert_glossary(entries: list[dict[str, Any]], generated_at) -> int:
    """Load generated glossary entries."""

    for entry in entries:
        upsert_generated_model(
            models.GlossaryEntry,
            entry["identifier"],
            {"term": entry["term"], "definition": entry["definition"]},
            generated_at,
        )
    return len(entries)


def upsert_assessments(assessments: list[dict[str, Any]], generated_at) -> int:
    """Load generated assessment records."""

    for assessment in assessments:
        assessment_instance, _ = upsert_generated_model(
            models.Assessment,
            assessment["identifier"],
            {
                "title": assessment["title"],
                "assessment_type": assessment["assessment_type"],
                "time_limit_seconds": assessment["time_limit_seconds"],
                "question_count": assessment["question_count"],
                "passing_score": assessment["passing_score"],
            },
            generated_at,
        )
        lesson_instances = models.Lesson.objects.filter(
            identifier__in=assessment["lesson_identifiers"]
        )
        assessment_instance.lessons.set(lesson_instances)
    return len(assessments)


def upsert_questions(questions: list[dict[str, Any]], generated_at) -> int:
    """Load generated assessment question records."""

    for question in questions:
        upsert_generated_model(
            models.Question,
            question["identifier"],
            {
                "assessment": models.Assessment.objects.get(
                    identifier=question["assessment_identifier"]
                ),
                "lesson": models.Lesson.objects.get(
                    identifier=question["lesson_identifier"]
                ),
                "prompt": question["prompt"],
                "answers": question["answers"],
                "correct_index": question["correct_index"],
                "feedback": question["feedback"],
            },
            generated_at,
        )
    return len(questions)


def upsert_coverage(records: list[dict[str, Any]]) -> int:
    """Load concept-to-curriculum coverage records."""

    for record in records:
        coverage, _ = models.CoverageRecord.objects.get_or_create(
            concept=record["concept"]
        )
        coverage.lessons.set(
            models.Lesson.objects.filter(identifier__in=record["lessons"])
        )
        coverage.assessments.set(
            models.Assessment.objects.filter(identifier__in=record["assessments"])
        )
    return len(records)
