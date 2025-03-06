from django import forms
from django.contrib import admin
from django.db import models

from data.models import Declaration, Plant, PlantSynonym

from .abstract_admin import ElementAdminWithChangeReason


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
class PlantAdmin(ElementAdminWithChangeReason):
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
                    "is_risky",
                    "novel_food",
                    "siccrf_status",
                    "ca_status",
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
                "fields": ["siccrf_family", "ca_family"],
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
    readonly_fields = (
        "siccrf_name",
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_family",
    )
    search_fields = ["id", "name"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # recalcul de l'article pour les déclarations concernées
        if change and form["is_risky"].has_changed():
            for declaration in Declaration.objects.filter(
                id__in=obj.declaredplant_set.values_list("declaration_id", flat=True),
                status__in=(
                    Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
                    Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
                    Declaration.DeclarationStatus.AWAITING_VISA,
                    Declaration.DeclarationStatus.OBSERVATION,
                    Declaration.DeclarationStatus.OBJECTION,
                ),
            ):
                declaration.assign_calculated_article()
                declaration.save()
