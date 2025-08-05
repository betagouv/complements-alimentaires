from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Plant, PlantSynonym

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class PlantSynonymInline(admin.TabularInline):
    model = PlantSynonym
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class PartInlineAdmin(admin.TabularInline):
    model = Plant.plant_parts.through
    extra = 1

    fields = ("plantpart", "is_useful")


class SubstanceInlineAdmin(admin.TabularInline):
    model = Plant.substances.through
    extra = 1


class PlantForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Plant)
class PlantAdmin(RecomputeDeclarationArticleAtIngredientSaveMixin, ChangeReasonAdminMixin, SimpleHistoryAdmin):
    declaredingredient_set = "declaredplant_set"
    form = PlantForm
    fieldsets = [
        (
            None,
            {"fields": ["change_reason"]},
        ),
        (
            None,  # Pas d'entête
            {
                "fields": [
                    "name",
                    "is_obsolete",
                    "is_risky",
                    "novel_food",
                    "status",
                    "requires_analysis_report",
                ],
            },
        ),
        (
            "Commentaires",
            {
                "fields": [
                    "public_comments",
                    "private_comments",
                    "to_be_entered_in_next_decree",
                ],
            },
        ),
        (
            "Famille",
            {
                "fields": ["family"],
            },
        ),
    ]

    inlines = (
        PartInlineAdmin,
        SubstanceInlineAdmin,
        PlantSynonymInline,
    )
    list_display = ("name", "is_obsolete", "family", "status", "is_risky", "novel_food")
    list_filter = ("is_obsolete", "family", "status", "is_risky", "novel_food")
    show_facets = admin.ShowFacets.NEVER
    search_fields = ["id", "name"]
