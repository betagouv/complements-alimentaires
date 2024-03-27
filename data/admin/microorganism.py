from django import forms
from django.contrib import admin

from data.models import Microorganism
from data.admin.abstract_admin import IngredientAdminWithHistoryChangedFields


class MicroorganismForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Microorganism)
class MicroorganismAdmin(IngredientAdminWithHistoryChangedFields):
    form = MicroorganismForm
    fieldsets = [
        (
            None,  # Pas d'entête
            {
                "fields": [
                    "name",
                    "is_obsolete",
                    "ca_is_obsolete",
                ],
            },
        ),
        (
            "Genre et espèce",
            {
                "fields": [
                    "siccrf_genre",
                    "ca_genre",
                    "siccrf_espece",
                    "ca_espece",
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

    list_display = ("name",)
    list_filter = ("is_obsolete",)
    history_list_display = ["changed_fields"]
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_genre",
        "siccrf_espece",
    )
