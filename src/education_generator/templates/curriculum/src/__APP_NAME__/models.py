"""Database models for editable generated curriculum content."""

from __future__ import annotations

from django.db import models


class GeneratedContentModel(models.Model):
    """Base model for generated content with modification tracking."""

    identifier = models.SlugField(max_length=120, unique=True)
    baseline_fingerprint = models.CharField(max_length=64, blank=True)
    is_human_modified = models.BooleanField(default=False)
    generated_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(GeneratedContentModel):
    """Represent the generated course as a whole."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    passing_score = models.FloatField(default=0.8)

    def __str__(self) -> str:
        """Return a readable course label."""

        return self.title


class Lesson(GeneratedContentModel):
    """Represent an editable curriculum lesson."""

    sequence = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.JSONField(default=list)

    class Meta:
        ordering = ["sequence", "identifier"]

    def __str__(self) -> str:
        """Return a readable lesson label."""

        return f"{self.sequence}. {self.title}"


class SourceReference(models.Model):
    """Record source evidence for a lesson claim."""

    lesson = models.ForeignKey(
        Lesson,
        related_name="sources",
        on_delete=models.CASCADE,
    )
    file_path = models.CharField(max_length=300)
    start_line = models.PositiveIntegerField()
    end_line = models.PositiveIntegerField()
    url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ["lesson__sequence", "file_path", "start_line"]

    def __str__(self) -> str:
        """Return a readable source label."""

        return f"{self.file_path}:{self.start_line}-{self.end_line}"


class GlossaryEntry(GeneratedContentModel):
    """Define an editable glossary term."""

    term = models.CharField(max_length=120)
    definition = models.TextField()

    class Meta:
        ordering = ["term"]

    def __str__(self) -> str:
        """Return the glossary term."""

        return self.term


class Assessment(GeneratedContentModel):
    """Represent a quiz or examination."""

    SECTION = "section"
    MIDTERM = "midterm"
    FINAL = "final"
    POP = "pop"
    ASSESSMENT_TYPES = [
        (SECTION, "Section quiz"),
        (MIDTERM, "Mid-curriculum examination"),
        (FINAL, "Final examination"),
        (POP, "Pop quiz"),
    ]

    title = models.CharField(max_length=200)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    lessons = models.ManyToManyField(Lesson, related_name="assessments", blank=True)
    time_limit_seconds = models.PositiveIntegerField(default=0)
    question_count = models.PositiveIntegerField(default=0)
    passing_score = models.FloatField(default=0.8)

    class Meta:
        ordering = ["assessment_type", "title"]

    def __str__(self) -> str:
        """Return a readable assessment label."""

        return self.title


class Question(GeneratedContentModel):
    """Represent an editable multiple-choice assessment question."""

    assessment = models.ForeignKey(
        Assessment,
        related_name="questions",
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name="questions",
        on_delete=models.PROTECT,
    )
    prompt = models.TextField()
    answers = models.JSONField(default=list)
    correct_index = models.PositiveIntegerField(default=0)
    feedback = models.TextField()

    def __str__(self) -> str:
        """Return a short question label."""

        return self.prompt[:80]


class CoverageRecord(models.Model):
    """Map significant target repository concepts to lessons and assessments."""

    concept = models.CharField(max_length=160, unique=True)
    lessons = models.ManyToManyField(Lesson, related_name="coverage_records")
    assessments = models.ManyToManyField(
        Assessment,
        related_name="coverage_records",
        blank=True,
    )

    class Meta:
        ordering = ["concept"]

    def __str__(self) -> str:
        """Return the covered concept."""

        return self.concept
