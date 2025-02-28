from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Ingredient, IngredientSynonym

from .abstract_admin import ChangeReasonAdminMixin


class IngredientSynonymInline(admin.TabularInline):
    model = IngredientSynonym
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class SubstanceInlineAdmin(admin.TabularInline):
    model = Ingredient.substances.through
    extra = 0


class IngredientForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "change_reason": forms.Textarea(attrs={"size": "70"}),
        }

    # saved in ChangeReasonAdminMixin.save()
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
    )


@admin.register(Ingredient)
class IngredientAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = IngredientForm
    inlines = (
        SubstanceInlineAdmin,
        IngredientSynonymInline,
    )
    list_display = ("name", "is_obsolete", "status", "is_risky", "novel_food", "has_linked_substances")
    list_filter = ("is_obsolete", "status", "is_risky", "novel_food", "ingredient_type")
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
    search_fields = ["id", "name"]

    def has_linked_substances(self, obj):
        return "Oui" if obj.substances.exists() else "Non"
