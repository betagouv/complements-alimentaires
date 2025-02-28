from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Microorganism

from .abstract_admin import ChangeReasonAdminMixin


class MicroorganismForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "change_reason": forms.TextInput(attrs={"size": "70"}),
        }

    # saved in ChangeReasonAdminMixin.save()
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
    )


@admin.register(Microorganism)
class MicroorganismAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = MicroorganismForm
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

    list_display = ("name", "is_obsolete", "status", "is_risky", "novel_food")
    list_filter = ("is_obsolete", "status", "is_risky", "novel_food")
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_genus",
        "siccrf_species",
    )
    search_fields = ["id", "name"]
