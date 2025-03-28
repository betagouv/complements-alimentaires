from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Population

from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class PopulationForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Population)
class PopulationAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = PopulationForm
    fields = [
        "change_reason",
        "name",
        "ca_name",
        "category",
        "is_obsolete",
        "ca_is_obsolete",
        "is_defined_by_anses",
        "min_age",
        "max_age",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "name",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
        "is_defined_by_anses",
    ]
    list_filter = (
        "is_obsolete",
        "is_defined_by_anses",
    )
    show_facets = admin.ShowFacets.NEVER
