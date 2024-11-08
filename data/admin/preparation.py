from django import forms
from django.contrib import admin

from data.models import Preparation


class PreparationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Preparation)
class PreparationAdmin(admin.ModelAdmin):
    form = PreparationForm
    fields = [
        "name",
        "ca_name",
        "is_obsolete",
        "ca_is_obsolete",
        "contains_alcohol",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "name",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = ["name", "modification_date", "contains_alcohol"]
    list_filter = ("is_obsolete",)
