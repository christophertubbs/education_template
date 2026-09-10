"""Behavior tests for generic runtime import and rendering."""

from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from education_generator.artifacts import load_artifacts
from education_runtime.importing import import_product_payload
from education_runtime.models import Assessment, Curriculum, ImportConflict, Lesson
from education_runtime.product_loading import load_installed_product_payloads
from education_runtime.services import select_assessment_questions


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class RuntimeTests(TestCase):
    """Exercise generic runtime behavior with any discovered products installed."""

    @classmethod
    def setUpTestData(cls) -> None:
        artifacts = load_artifacts(Path("curricula/cfe"))
        cls.payload = artifacts.as_product_payload()
        cls.payload["metadata"] = {
            "curriculum_product_version": "1.0.0",
            "curriculum_schema_version": "2.0",
            "target_repository_url": "https://example.test/cfe.git",
            "resolved_target_commit": "a" * 40,
            "compatible_education_runtime": ">=1.0,<2.0",
        }
        import_product_payload(cls.payload)

    def test_import_populates_generic_runtime_models(self) -> None:
        self.assertEqual(Curriculum.objects.filter(pk="cfe-curriculum").count(), 1)
        self.assertEqual(
            Lesson.objects.filter(section__curriculum_id="cfe-curriculum").count(), 7
        )

    def test_packaged_json_refreshes_content_without_a_new_migration(self) -> None:
        """The explicit loader applies the current JSON after migrations ran."""

        changed = json.loads(json.dumps(self.payload))
        changed["lessons"][0]["title"] = "Current packaged title"
        with tempfile.TemporaryDirectory() as directory_name:
            package_root = Path(directory_name)
            data_path = package_root / "data" / "curriculum.json"
            data_path.parent.mkdir()
            data_path.write_text(json.dumps(changed), encoding="utf-8")
            app_config = SimpleNamespace(name="example_curriculum_product")
            with patch(
                "education_runtime.product_loading.files", return_value=package_root
            ):
                loaded = load_installed_product_payloads([app_config])

        self.assertEqual(loaded, ["cfe-curriculum"])
        self.assertEqual(
            Lesson.objects.get(pk="cfe-purpose").title, "Current packaged title"
        )

    def test_human_modified_content_is_preserved_and_conflict_is_recorded(self) -> None:
        lesson = Lesson.objects.get(pk="cfe-purpose")
        original_concepts = list(lesson.concepts.values_list("pk", flat=True))
        lesson.title = "Human title"
        lesson.is_human_modified = True
        lesson.save()
        changed = json.loads(json.dumps(self.payload))
        changed["lessons"][0]["title"] = "Incoming generated title"
        changed["lessons"][0]["concept_identifiers"] = ["timestep-water-accounting"]
        import_product_payload(changed)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, "Human title")
        self.assertEqual(
            list(lesson.concepts.values_list("pk", flat=True)), original_concepts
        )
        self.assertTrue(
            ImportConflict.objects.filter(object_identifier=lesson.pk).exists()
        )

    def test_curriculum_and_lesson_pages_render(self) -> None:
        curriculum_url = reverse(
            "education_runtime:curriculum-detail", args=("cfe-curriculum",)
        )
        lesson_url = reverse(
            "education_runtime:lesson", args=("cfe-curriculum", "cfe-purpose")
        )
        self.assertEqual(self.client.get(curriculum_url).status_code, 200)
        response = self.client.get(lesson_url)
        self.assertContains(response, "Mark lesson complete")
        self.assertContains(response, "Evidence")
        self.assertContains(response, "Definitions in this lesson")
        self.assertContains(response, 'class="variable-table"')
        self.assertContains(response, "mathjax@4/tex-chtml.js")

    def test_partitioning_lesson_renders_semantic_content(self) -> None:
        url = reverse(
            "education_runtime:lesson",
            args=("cfe-curriculum", "partitioning-and-et"),
        )
        response = self.client.get(url)
        self.assertContains(response, "Schaake Partitioning")
        self.assertContains(response, 'class="glossary-term"')
        self.assertContains(response, 'class="equation"', count=2)
        self.assertContains(response, "Schaake variables")
        self.assertContains(response, 'class="worked-example"')

    def test_assessment_renders_exact_selection_count(self) -> None:
        url = reverse(
            "education_runtime:assessment", args=("cfe-curriculum", "cfe-final")
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 50)

    def test_non_pop_selection_preserves_required_coverage(self) -> None:
        """Every section or examination attempt retains required coverage."""

        assessments = Assessment.objects.filter(curriculum_id="cfe-curriculum").exclude(
            kind="pop"
        )
        for assessment in assessments:
            with self.subTest(assessment=assessment.identifier):
                selected = select_assessment_questions(assessment)
                bank = assessment.questions.prefetch_related(
                    "concepts", "mastery_contracts__concept", "review_lesson__section"
                )
                selected_concepts = {
                    concept.identifier
                    for question in selected
                    for concept in question.concepts.all()
                    if concept.importance == "major"
                }
                required_concepts = {
                    concept.identifier
                    for question in bank
                    for concept in question.concepts.all()
                    if concept.importance == "major"
                }
                selected_contracts = {
                    contract.identifier
                    for question in selected
                    for contract in question.mastery_contracts.all()
                    if contract.concept.importance == "major"
                }
                required_contracts = {
                    contract.identifier
                    for question in bank
                    for contract in question.mastery_contracts.all()
                    if contract.concept.importance == "major"
                }
                self.assertEqual(selected_concepts, required_concepts)
                self.assertEqual(selected_contracts, required_contracts)
                if assessment.kind in {"midterm", "final"}:
                    selected_sections = {
                        question.review_lesson.section_id for question in selected
                    }
                    required_sections = {
                        question.review_lesson.section_id for question in bank
                    }
                    selected_outcomes = {
                        outcome
                        for question in selected
                        for outcome in question.terminal_outcomes
                    }
                    required_outcomes = {
                        outcome
                        for question in bank
                        for outcome in question.terminal_outcomes
                    }
                    self.assertEqual(selected_sections, required_sections)
                    self.assertEqual(selected_outcomes, required_outcomes)

    def test_randomized_attempts_vary_while_preserving_coverage(self) -> None:
        """Different random seeds produce materially different valid attempts."""

        assessment = Assessment.objects.get(pk="cfe-final")
        attempts: set[frozenset[str]] = set()
        for seed in range(6):
            with patch(
                "education_runtime.services.random.SystemRandom",
                return_value=random.Random(seed),
            ):
                selected = select_assessment_questions(assessment)
            attempts.add(frozenset(question.identifier for question in selected))
        self.assertGreater(len(attempts), 1)

    def test_pop_selection_respects_eligible_prior_lessons(self) -> None:
        """A pop quiz cannot draw material outside the completed lesson set."""

        assessment = Assessment.objects.get(pk="cfe-pop-review")
        eligible_lessons = set(
            Lesson.objects.filter(section__curriculum_id="cfe-curriculum").values_list(
                "identifier", flat=True
            )[:3]
        )
        selected = select_assessment_questions(assessment, eligible_lessons)
        self.assertEqual(len(selected), assessment.selection_count)
        self.assertTrue(
            all(question.review_lesson_id in eligible_lessons for question in selected)
        )

    def test_configured_major_concept_minimum_is_enforced(self) -> None:
        """A product may require multiple independently scored items per concept."""

        assessment = Assessment.objects.get(pk="cfe-final")
        assessment.configuration = {"required_minimum_per_major_concept": 2}
        selected = select_assessment_questions(assessment)
        counts: dict[str, int] = {}
        for question in selected:
            for concept in question.concepts.all():
                if concept.importance == "major":
                    counts[concept.identifier] = counts.get(concept.identifier, 0) + 1
        self.assertTrue(counts)
        self.assertTrue(all(count >= 2 for count in counts.values()))

    def test_infeasible_coverage_requirement_fails_explicitly(self) -> None:
        """The runtime must not silently return an under-covered examination."""

        assessment = Assessment.objects.get(pk="cfe-final")
        assessment.configuration = {"required_minimum_per_major_concept": 100}
        with self.assertRaisesRegex(ValueError, "major concepts"):
            select_assessment_questions(assessment)
