from django import forms
from django.contrib import admin
from data.models import Condition


class ConditionForm(forms.ModelForm):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    form = ConditionForm
    fields = [
        "name",
        "ca_name",
        "siccrf_name_en",
        "is_obsolete",
        "ca_is_obsolete",
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
