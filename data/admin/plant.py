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
class PlantAdmin(SimpleHistoryAdmin):
    form = PlantForm
    fieldsets = [
        (
            None,  # Pas d'entête
            {
                "fields": [
                    "siccrf_name",
                    "ca_name",
                    "name",
                    "is_obsolete",
                    "status",
                    "ca_is_obsolete",
                ],
            },
        ),
        (
            "Commentaires",
            {
                "fields": [
                    "siccrf_public_comments",
                    "siccrf_private_comments",
                    "ca_public_comments",
                    "ca_private_comments",
                ],
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
    list_display = ("name", "siccrf_family", "status")
    list_filter = ("is_obsolete", "siccrf_family", "status")
    readonly_fields = (
        "siccrf_name",
        "name",
        "is_obsolete",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_family",
        "family",
    )
