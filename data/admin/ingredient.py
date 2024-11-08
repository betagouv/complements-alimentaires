from django import forms
from django.contrib import admin
from django.db import models

from data.models import Ingredient, IngredientSynonym

from .abstract_admin import ElementAdminWithChangeReason


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
        }


@admin.register(Ingredient)
class IngredientAdmin(ElementAdminWithChangeReason):
    form = IngredientForm
    inlines = (
        SubstanceInlineAdmin,
        IngredientSynonymInline,
    )
    list_display = ("name", "status", "is_risky")
    list_filter = ("is_obsolete", "status", "is_risky")
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
    search_fields = ["id", "name"]
