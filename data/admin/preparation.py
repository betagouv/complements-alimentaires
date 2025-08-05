from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Preparation

from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class PreparationForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Preparation)
class PreparationAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = PreparationForm
    fields = [
        "change_reason",
        "name",
        "is_obsolete",
        "contains_alcohol",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "creation_date",
        "modification_date",
    ]
    list_display = ["name", "modification_date", "contains_alcohol"]
    list_filter = ("is_obsolete",)
    show_facets = admin.ShowFacets.NEVER
