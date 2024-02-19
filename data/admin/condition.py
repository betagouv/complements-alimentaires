from django import forms
from django.contrib import admin
from data.models import Condition


class ConditionForm(forms.ModelForm):
    class Meta:
        widgets = {
            "CA_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    form = ConditionForm
    fields = [
        "CA_name",
        "siccrf_name",
        "siccrf_name_en",
        "siccrf_is_obsolete",
        "CA_is_obsolete",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "siccrf_name",
        "siccrf_name_en",
        "siccrf_is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
    ]
    list_filter = (
        "siccrf_is_obsolete",
        "CA_is_obsolete",
    )
