from django import forms
from django.contrib import admin
from django.db import models
from simple_history.admin import SimpleHistoryAdmin

from data.models import Plant, PlantSynonym


class PlantSynonymInline(admin.TabularInline):
    model = PlantSynonym
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class PartInlineAdmin(admin.TabularInline):
    model = Plant.plant_parts.through
    extra = 1


class PlantForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Plant)
class PlantAdmin(SimpleHistoryAdmin):
    form = PlantForm
    fieldsets = [
        (
            None,  # Pas d'entête
            {
                "fields": ["name", "is_obsolete"],
            },
        ),
        (
            "Commentaires",
            {
                "fields": ["public_comments", "private_comments"],
            },
        ),
        (
            "Commentaires",
            {
                "fields": ["family", "substances"],
            },
        ),
    ]

    inlines = (
        PartInlineAdmin,
        PlantSynonymInline,
    )
    list_display = (
        "name",
        "family",
    )
    list_filter = ("is_obsolete", "family")
