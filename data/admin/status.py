from django import forms
from django.contrib import admin
from data.models import IngredientStatus


class IngredientStatusForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
        }


@admin.register(IngredientStatus)
class IngredientStatusAdmin(admin.ModelAdmin):
    form = IngredientStatusForm
    fields = [
        "name",
    ]
    readonly_fields = [
        "siccrf_id",
    ]
