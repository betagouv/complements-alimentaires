from django import forms
from django.contrib import admin
from data.models import Substance


class SubstanceForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "source": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Substance)
class SubstanceAdmin(admin.ModelAdmin):
    form = SubstanceForm
    fields = (
        "is_obsolete",
        ("name", "name_en"),
        "source",
        ("public_comments", "private_comments"),
        ("cas_number", "einec_number"),
        "must_specify_quantity",
        ("min_quantity", "max_quantity"),
        "nutritional_reference",
    )

    list_display = (
        "name",
        "source",
    )
    list_filter = ("is_obsolete",)
