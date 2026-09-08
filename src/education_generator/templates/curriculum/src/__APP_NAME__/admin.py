"""Administrative editing configuration for curriculum models."""

from __future__ import annotations

from django.contrib import admin

from . import models


class SourceReferenceInline(admin.TabularInline):
    """Edit lesson source references inline."""

    model = models.SourceReference
    extra = 0


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for courses."""

    list_display = ("identifier", "title", "is_human_modified", "updated_at")
    list_filter = ("is_human_modified",)


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for lessons."""

    list_display = ("sequence", "identifier", "title", "is_human_modified")
    list_filter = ("is_human_modified",)
    inlines = [SourceReferenceInline]


@admin.register(models.GlossaryEntry)
class GlossaryEntryAdmin(admin.ModelAdmin):
    """Admin configuration for glossary entries."""

    list_display = ("term", "identifier", "is_human_modified")
    search_fields = ("term", "definition")


@admin.register(models.Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    """Admin configuration for assessments."""

    list_display = ("title", "assessment_type", "question_count", "time_limit_seconds")
    filter_horizontal = ("lessons",)


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for questions."""

    list_display = ("identifier", "assessment", "lesson", "is_human_modified")
    list_filter = ("assessment", "lesson", "is_human_modified")


@admin.register(models.CoverageRecord)
class CoverageRecordAdmin(admin.ModelAdmin):
    """Admin configuration for coverage records."""

    list_display = ("concept",)
    filter_horizontal = ("lessons", "assessments")
