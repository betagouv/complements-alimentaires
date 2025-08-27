from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Microorganism

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class MicroorganismForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
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
                    "is_obsolete",
                    "is_risky",
                    "novel_food",
                    "status",
                    "requires_analysis_report",
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
            "Commentaires",
            {
                "fields": [
                    "public_comments",
                    "private_comments",
                    "to_be_entered_in_next_decree",
                ],
            },
        ),
    ]

    list_display = ("name", "is_obsolete", "status", "is_risky", "novel_food")
    list_filter = ("is_obsolete", "status", "is_risky", "novel_food")
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = ("name",)
    search_fields = ["id", "name"]
