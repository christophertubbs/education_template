"""Deterministically import generated baselines while preserving human edits."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from django.apps import apps as global_apps
from django.db import transaction


def import_product_payload(
    payload: dict[str, Any],
    *,
    apps=global_apps,
    using: str = "default",
) -> None:
    """Import a validated product payload into generic runtime models."""

    curriculum_data = payload["curriculum"]
    curriculum_id = curriculum_data["identifier"]
    with transaction.atomic(using=using):
        curriculum = _upsert(
            apps,
            using,
            "Curriculum",
            curriculum_id,
            {
                "title": curriculum_data["title"],
                "description": curriculum_data["description"],
                "version": payload["metadata"]["curriculum_product_version"],
                "schema_version": payload["metadata"]["curriculum_schema_version"],
                "source_repository_url": payload["metadata"]["target_repository_url"],
                "source_commit": payload["metadata"]["resolved_target_commit"],
                "runtime_compatibility": payload["metadata"][
                    "compatible_education_runtime"
                ],
                "pop_quiz_probability": curriculum_data.get(
                    "pop_quiz_probability", 0.15
                ),
                "pop_quiz_cooldown": curriculum_data.get("pop_quiz_cooldown", 3),
            },
            curriculum_id,
        )
        sections = {}
        for record in payload["sections"]:
            sections[record["identifier"]] = _upsert(
                apps,
                using,
                "Section",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "title": record["title"],
                    "summary": record.get("summary", ""),
                    "sequence": record["sequence"],
                },
                curriculum_id,
            )
        concepts = {}
        for record in payload["knowledge_map"]["concepts"]:
            concepts[record["identifier"]] = _upsert(
                apps,
                using,
                "Concept",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "title": record["title"],
                    "description": record["description"],
                    "importance": record["importance"],
                },
                curriculum_id,
            )
        for relationship in payload["knowledge_map"].get("relationships", []):
            if relationship.get("type") == "prerequisite":
                dependent = concepts[relationship["source"]]
                if _relations_are_generated(dependent):
                    dependent.prerequisites.add(concepts[relationship["target"]])
        contracts = {}
        for record in payload["mastery_contracts"]:
            contracts[record["identifier"]] = _upsert(
                apps,
                using,
                "MasteryContract",
                record["identifier"],
                {
                    "concept_id": concepts[record["concept_identifier"]].pk,
                    "competencies": record["competencies"],
                },
                curriculum_id,
            )
        sources = {}
        for record in payload["sources"]:
            sources[record["identifier"]] = _upsert(
                apps,
                using,
                "SourceReference",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "evidence_kind": record["evidence_kind"],
                    "citation": record["citation"],
                    "file_path": record.get("file_path", ""),
                    "symbol": record.get("symbol", ""),
                    "start_line": record.get("start_line"),
                    "end_line": record.get("end_line"),
                    "url": record.get("url", ""),
                    "certainty": record.get("certainty", "verified"),
                },
                curriculum_id,
            )
        lessons = {}
        for record in payload["lessons"]:
            lesson = _upsert(
                apps,
                using,
                "Lesson",
                record["identifier"],
                {
                    "section_id": sections[record["section_identifier"]].pk,
                    "title": record["title"],
                    "summary": record["summary"],
                    "sequence": record["sequence"],
                    "content": record["content"],
                },
                curriculum_id,
            )
            if _relations_are_generated(lesson):
                lesson.concepts.set(
                    [concepts[value] for value in record["concept_identifiers"]]
                )
                lesson.sources.set(
                    [sources[value] for value in record["source_identifiers"]]
                )
            lessons[record["identifier"]] = lesson
        for record in payload["glossary"]:
            entry = _upsert(
                apps,
                using,
                "GlossaryEntry",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "term": record["term"],
                    "definition": record["definition"],
                },
                curriculum_id,
            )
            if _relations_are_generated(entry):
                entry.concepts.set(
                    [concepts[value] for value in record.get("concept_identifiers", [])]
                )
                entry.lessons.set(
                    [lessons[value] for value in record.get("lesson_identifiers", [])]
                )
        assessments = {}
        for record in payload["assessments"]:
            section_id = record.get("section_identifier")
            assessments[record["identifier"]] = _upsert(
                apps,
                using,
                "Assessment",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "section_id": sections[section_id].pk if section_id else None,
                    "title": record["title"],
                    "kind": record["kind"],
                    "selection_count": record["selection_count"],
                    "time_limit_seconds": record.get("time_limit_seconds"),
                    "configuration": record.get("configuration", {}),
                },
                curriculum_id,
            )
        for record in payload["questions"]:
            scoring = {
                key: record[key]
                for key in (
                    "options",
                    "accepted_value",
                    "tolerance",
                    "accepted_answers",
                    "normalization",
                )
                if key in record
            }
            question = _upsert(
                apps,
                using,
                "Question",
                record["identifier"],
                {
                    "curriculum_id": curriculum.pk,
                    "review_lesson_id": lessons[record["review_lesson_identifier"]].pk,
                    "terminal_outcomes": record.get("terminal_outcomes", []),
                    "question_type": record["type"],
                    "difficulty": record["difficulty"],
                    "prompt": record["prompt"],
                    "scoring": scoring,
                    "feedback_correct": record["feedback_correct"],
                    "feedback_incorrect": record["feedback_incorrect"],
                },
                curriculum_id,
            )
            if _relations_are_generated(question):
                question.assessments.set(
                    [assessments[value] for value in record["assessment_identifiers"]]
                )
                question.concepts.set(
                    [concepts[value] for value in record["concept_identifiers"]]
                )
                question.mastery_contracts.set(
                    [
                        contracts[value]
                        for value in record["mastery_contract_identifiers"]
                    ]
                )
        for record in payload["coverage"]:
            _upsert(
                apps,
                using,
                "CoverageRecord",
                record["concept_identifier"],
                {
                    "concept_id": concepts[record["concept_identifier"]].pk,
                    "dimensions": record["dimensions"],
                    "lesson_identifiers": record["lesson_identifiers"],
                    "question_identifiers": record["question_identifiers"],
                },
                curriculum_id,
                primary_key_name="concept_id",
            )


def _upsert(
    apps,
    using: str,
    model_name: str,
    identifier: str,
    values: dict[str, Any],
    curriculum_identifier: str,
    *,
    primary_key_name: str = "identifier",
):
    """Update generated content or record a conflict for a human override."""

    model = apps.get_model("education_runtime", model_name)
    manager = model.objects.using(using)
    fingerprint = _fingerprint(values)
    lookup = {primary_key_name: identifier}
    instance = manager.filter(**lookup).first()
    if instance is not None and instance.is_human_modified:
        if instance.baseline_fingerprint != fingerprint:
            conflict_model = apps.get_model("education_runtime", "ImportConflict")
            conflict_model.objects.using(using).get_or_create(
                curriculum_identifier=curriculum_identifier,
                model_name=model_name,
                object_identifier=identifier,
                incoming_fingerprint=fingerprint,
                defaults={"installed_fingerprint": instance.baseline_fingerprint},
            )
        instance._preserved_human_override = True
        return instance
    values["baseline_fingerprint"] = fingerprint
    values["is_human_modified"] = False
    instance, _ = manager.update_or_create(defaults=values, **lookup)
    instance._preserved_human_override = False
    return instance


def _fingerprint(value: dict[str, Any]) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _relations_are_generated(instance) -> bool:
    """Return whether import may synchronize this record's relationships."""

    return not getattr(instance, "_preserved_human_override", False)
