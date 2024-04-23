from django import forms
from django.contrib import admin

from data.models import Microorganism
from data.admin.abstract_admin import IngredientAdminHistorisableChangedFields


class MicroorganismForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Microorganism)
class MicroorganismAdmin(IngredientAdminHistorisableChangedFields):
    form = MicroorganismForm
    fieldsets = [
        (
            None,  # Pas d'entête
            {
                "fields": [
                    "name",
                    "is_obsolete",
                    "status",
                    "ca_is_obsolete",
                ],
            },
        ),
        (
            "Genre et espèce",
            {
                "fields": [
                    "siccrf_genus",
                    "ca_genus",
                    "siccrf_species",
                    "ca_species",
                ],
            },
        ),
        (
            "Commentaires",
            {
                "fields": [
                    "siccrf_public_comments",
                    "ca_public_comments",
                    "siccrf_private_comments",
                    "ca_private_comments",
                ],
            },
        ),
    ]

    list_display = ("name", "status")
    list_filter = ("is_obsolete", "status")
    history_list_display = ["changed_fields"]
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_genus",
        "siccrf_species",
    )
