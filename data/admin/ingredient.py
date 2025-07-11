from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Ingredient, IngredientSynonym

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    HasCommentListFilter,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class IngredientSynonymInline(admin.TabularInline):
    model = IngredientSynonym
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class SubstanceInlineAdmin(admin.TabularInline):
    model = Ingredient.substances.through
    extra = 0

    readonly_fields = ("siccrf_is_related",)


class IngredientForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
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
                    "siccrf_name_en",
                    "description",
                    "ingredient_type",
                    "is_obsolete",
                    "is_risky",
                    "is_novel_food",
                    "status",
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
    inlines = (
        SubstanceInlineAdmin,
        IngredientSynonymInline,
    )
    list_display = ("name", "is_obsolete", "status", "is_risky", "is_novel_food", "has_linked_substances")
    list_filter = ("is_obsolete", "status", "is_risky", "is_novel_food", "ingredient_type", HasCommentListFilter)
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = ("siccrf_name_en",)
    search_fields = ["id", "name"]

    def has_linked_substances(self, obj):
        return "Oui" if obj.substances.exists() else "Non"
