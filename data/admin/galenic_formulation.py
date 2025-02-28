from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import GalenicFormulation

from .abstract_admin import ChangeReasonAdminMixin


class GalenicFormulationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "change_reason": forms.TextInput(attrs={"size": "70"}),
        }

    # saved in ChangeReasonAdminMixin.save()
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
    )


@admin.register(GalenicFormulation)
class GalenicFormulationAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = GalenicFormulationForm
    fields = [
        "name",
        "ca_name",
        "siccrf_name_en",
        "is_liquid",
        "is_risky",
        "is_obsolete",
        "ca_is_obsolete",
        "creation_date",
        "modification_date",
        "change_reason",
    ]
    readonly_fields = [
        "name",
        "siccrf_name_en",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
        "is_risky",
    ]
    list_filter = (
        "is_obsolete",
        "is_liquid",
        "is_risky",
    )
    show_facets = admin.ShowFacets.NEVER
