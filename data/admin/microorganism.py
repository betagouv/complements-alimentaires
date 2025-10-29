from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Microorganism, MicroorganismMaxQuantityPerPopulationRelation, MicroorganismSynonym

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    HasMaxCommentListFilter,
    HasWarningCommentListFilter,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class MicroorganismForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


class MicroorganismSynonymInline(admin.TabularInline):
    model = MicroorganismSynonym
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class MicroorganismMaxQuantitiesInline(admin.TabularInline):
    model = MicroorganismMaxQuantityPerPopulationRelation
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


@admin.register(Microorganism)
class MicroorganismAdmin(RecomputeDeclarationArticleAtIngredientSaveMixin, ChangeReasonAdminMixin, SimpleHistoryAdmin):
    declaredingredient_set = "declaredmicroorganism_set"
    form = MicroorganismForm
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
                    "description",
                    "is_obsolete",
                    "novel_food",
                    "status",
                    "regulatory_resource_links",
                ],
            },
        ),
        (
            "Genre et espèce",
            {
                "fields": [
                    "genus",
                    "species",
                ],
            },
        ),
        (
            "Avertissements",
            {
                "fields": [
                    "warnings_on_label",
                    "is_risky",
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
            "Quantités",
            {
                "fields": [
                    "must_specify_quantity",
                    "unit",
                ],
            },
        ),
    ]
    inlines = (
        MicroorganismMaxQuantitiesInline,
        MicroorganismSynonymInline,
    )

    list_display = (
        "name",
        "is_obsolete",
        "status",
        "is_risky",
        "requires_analysis_report",
        "novel_food",
    )
    list_filter = (
        "is_obsolete",
        "status",
        "is_risky",
        "requires_analysis_report",
        "novel_food",
        HasMaxCommentListFilter,
        HasWarningCommentListFilter,
    )
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = ("name",)
    search_fields = ["id", "name"]
