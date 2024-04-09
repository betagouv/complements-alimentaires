from django import forms
from django.contrib import admin
from data.models import Population


class PopulationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(Population)
class PopulationAdmin(admin.ModelAdmin):
    form = PopulationForm
    fields = [
        "name",
        "ca_name",
        "is_obsolete",
        "ca_is_obsolete",
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
    ]
    list_filter = ("is_obsolete",)
