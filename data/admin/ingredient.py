from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Ingredient, IngredientMaxQuantityPerPopulationRelation, IngredientSynonym

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    HasMaxCommentListFilter,
    HasWarningCommentListFilter,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class IngredientSynonymInline(admin.TabularInline):
    model = IngredientSynonym
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class IngredientMaxQuantitiesInline(admin.TabularInline):
    model = IngredientMaxQuantityPerPopulationRelation
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class SubstanceInlineAdmin(admin.TabularInline):
    model = Ingredient.substances.through
    extra = 0


class IngredientForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Ingredient)
class IngredientAdmin(RecomputeDeclarationArticleAtIngredientSaveMixin, ChangeReasonAdminMixin, SimpleHistoryAdmin):
    declaredingredient_set = "declaredingredient_set"
    form = IngredientForm
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
                    "ingredient_type",
                    "is_obsolete",
                    "novel_food",
                    "status",
                    "regulatory_resource_links",
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
                    "unit",
                ],
            },
        ),
    ]
    inlines = (
        IngredientMaxQuantitiesInline,
        SubstanceInlineAdmin,
        IngredientSynonymInline,
    )
    list_display = (
        "name",
        "is_obsolete",
        "status",
        "is_risky",
        "requires_analysis_report",
        "novel_food",
        "has_linked_substances",
    )
    list_filter = (
        "is_obsolete",
        "status",
        "is_risky",
        "requires_analysis_report",
        "novel_food",
        "ingredient_type",
        HasMaxCommentListFilter,
        HasWarningCommentListFilter,
    )
    show_facets = admin.ShowFacets.NEVER
    search_fields = ["id", "name"]

    def has_linked_substances(self, obj):
        return "Oui" if obj.substances.exists() else "Non"
