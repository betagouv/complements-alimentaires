from django import forms
from django.contrib import admin
from django.db import models

from data.models import Plant, PlantSynonym
from data.admin.abstract_admin import IngredientAdminWithHistoryChangedFields


class PlantSynonymInline(admin.TabularInline):
    model = PlantSynonym
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class PartInlineAdmin(admin.TabularInline):
    model = Plant.plant_parts.through
    extra = 1


class SubstanceInlineAdmin(admin.TabularInline):
    model = Plant.substances.through
    extra = 1


class PlantForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Plant)
class PlantAdmin(IngredientAdminWithHistoryChangedFields):
    form = PlantForm
    fieldsets = [
        (
            None,  # Pas d'entête
            {
                "fields": ["name", "siccrf_is_obsolete"],
            },
        ),
        (
            "Commentaires",
            {
                "fields": ["public_comments", "private_comments"],
            },
        ),
        (
            "Famille",
            {
                "fields": ["siccrf_family"],
            },
        ),
    ]

    inlines = (
        PartInlineAdmin,
        SubstanceInlineAdmin,
        PlantSynonymInline,
    )
    list_display = (
        "name",
        "siccrf_family",
    )
    list_filter = ("siccrf_is_obsolete", "siccrf_family")
    history_list_display = ["changed_fields"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None
