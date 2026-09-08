"""Generic curriculum models owned by the Education Runtime."""

from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class BaselineContent(models.Model):
    """Shared state separating generated baselines from human changes."""

    baseline_fingerprint = models.CharField(max_length=64, editable=False)
    is_human_modified = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Curriculum(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=120)
    title = models.CharField(max_length=240)
    description = models.TextField()
    version = models.CharField(max_length=40)
    schema_version = models.CharField(max_length=40)
    source_repository_url = models.URLField(max_length=500)
    source_commit = models.CharField(max_length=64)
    runtime_compatibility = models.CharField(max_length=100)
    pop_quiz_probability = models.FloatField(
        default=0.15,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    pop_quiz_cooldown = models.PositiveIntegerField(default=3)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

    def get_pop_assessment_url(self) -> str:
        assessment = self.assessment_set.filter(kind="pop").first()
        if assessment is None:
            return ""
        return reverse(
            "education_runtime:assessment",
            args=(self.identifier, assessment.identifier),
        )


class Section(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=160)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    summary = models.TextField(blank=True)
    sequence = models.PositiveIntegerField()

    class Meta:
        ordering = ("curriculum", "sequence")
        constraints = [
            models.UniqueConstraint(
                fields=("curriculum", "sequence"), name="unique_section_sequence"
            )
        ]

    def __str__(self) -> str:
        return self.title


class Concept(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=160)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    description = models.TextField()
    importance = models.CharField(max_length=30)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    class Meta:
        ordering = ("curriculum", "title")

    def __str__(self) -> str:
        return self.title


class MasteryContract(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=180)
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE)
    competencies = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"Mastery: {self.concept}"


class SourceReference(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=180)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    evidence_kind = models.CharField(max_length=40)
    citation = models.TextField()
    file_path = models.CharField(max_length=500, blank=True)
    symbol = models.CharField(max_length=240, blank=True)
    start_line = models.PositiveIntegerField(null=True, blank=True)
    end_line = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(max_length=1000, blank=True)
    certainty = models.CharField(max_length=40, default="verified")

    def __str__(self) -> str:
        return self.citation


class Lesson(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=180)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    summary = models.TextField()
    sequence = models.PositiveIntegerField()
    content = models.JSONField(default=list)
    concepts = models.ManyToManyField(Concept, blank=True)
    sources = models.ManyToManyField(SourceReference, blank=True)

    class Meta:
        ordering = ("section", "sequence")
        constraints = [
            models.UniqueConstraint(
                fields=("section", "sequence"), name="unique_lesson_sequence"
            )
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            "education_runtime:lesson",
            args=(self.section.curriculum_id, self.identifier),
        )


class GlossaryEntry(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=180)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    term = models.CharField(max_length=240)
    definition = models.TextField()
    concepts = models.ManyToManyField(Concept, blank=True)
    lessons = models.ManyToManyField(Lesson, blank=True)

    class Meta:
        ordering = ("term",)

    def __str__(self) -> str:
        return self.term


class Assessment(BaselineContent):
    KIND_CHOICES = (
        ("pop", "Pop quiz"),
        ("section", "Section quiz"),
        ("midterm", "Mid-curriculum examination"),
        ("final", "Final examination"),
    )
    identifier = models.SlugField(primary_key=True, max_length=180)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, null=True, blank=True, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=240)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    selection_count = models.PositiveIntegerField()
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    configuration = models.JSONField(default=dict)

    class Meta:
        ordering = ("curriculum", "kind", "title")

    def __str__(self) -> str:
        return self.title


class Question(BaselineContent):
    identifier = models.SlugField(primary_key=True, max_length=200)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    review_lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    assessments = models.ManyToManyField(Assessment, related_name="questions")
    concepts = models.ManyToManyField(Concept)
    mastery_contracts = models.ManyToManyField(MasteryContract)
    terminal_outcomes = models.JSONField(default=list)
    question_type = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=20)
    prompt = models.TextField()
    scoring = models.JSONField(default=dict)
    feedback_correct = models.TextField()
    feedback_incorrect = models.TextField()

    def __str__(self) -> str:
        return self.prompt[:80]


class CoverageRecord(BaselineContent):
    concept = models.OneToOneField(Concept, primary_key=True, on_delete=models.CASCADE)
    dimensions = models.JSONField(default=dict)
    lesson_identifiers = models.JSONField(default=list)
    question_identifiers = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"Coverage: {self.concept}"


class ImportConflict(models.Model):
    """A generated update that differs from a human-modified record."""

    curriculum_identifier = models.CharField(max_length=120)
    model_name = models.CharField(max_length=120)
    object_identifier = models.CharField(max_length=200)
    installed_fingerprint = models.CharField(max_length=64)
    incoming_fingerprint = models.CharField(max_length=64)
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ("-detected_at",)
