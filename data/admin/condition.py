from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Condition

from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class ConditionForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Condition)
class ConditionAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = ConditionForm
    fields = [
        "change_reason",
        "name",
        "ca_name",
        "category",
        "siccrf_name_en",
        "is_obsolete",
        "ca_is_obsolete",
        "min_age",
        "max_age",
        "creation_date",
        "modification_date",
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
    ]
    list_filter = ("is_obsolete",)
    show_facets = admin.ShowFacets.NEVER
