from django import forms
from django.contrib import admin
from data.models import Condition


class ConditionForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    form = ConditionForm
    fields = [
        "name",
        "name_en",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
    ]
    list_filter = ("is_obsolete",)
