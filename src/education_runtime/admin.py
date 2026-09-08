"""Administrative editing for generic curriculum records."""

from django.contrib import admin

from . import models


class BaselineAdmin(admin.ModelAdmin):
    """Expose generated ownership state to administrators."""

    list_filter = ("is_human_modified",)
    readonly_fields = ("baseline_fingerprint",)

    def save_model(self, request, obj, form, change):
        if change:
            obj.is_human_modified = True
        super().save_model(request, obj, form, change)


for model in (
    models.Curriculum,
    models.Section,
    models.Concept,
    models.MasteryContract,
    models.SourceReference,
    models.Lesson,
    models.GlossaryEntry,
    models.Assessment,
    models.Question,
    models.CoverageRecord,
):
    admin.site.register(model, BaselineAdmin)


@admin.register(models.ImportConflict)
class ImportConflictAdmin(admin.ModelAdmin):
    list_display = (
        "curriculum_identifier",
        "model_name",
        "object_identifier",
        "resolved",
    )
    list_filter = ("resolved", "model_name")
    readonly_fields = ("detected_at",)
