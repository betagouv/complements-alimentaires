from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Preparation

from .abstract_admin import ChangeReasonAdminMixin


class PreparationForm(forms.ModelForm):
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


@admin.register(Preparation)
class PreparationAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = PreparationForm
    fields = [
        "name",
        "ca_name",
        "is_obsolete",
        "ca_is_obsolete",
        "contains_alcohol",
        "creation_date",
        "modification_date",
        "change_reason",
    ]
    readonly_fields = [
        "name",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = ["name", "modification_date", "contains_alcohol"]
    list_filter = ("is_obsolete",)
    show_facets = admin.ShowFacets.NEVER
