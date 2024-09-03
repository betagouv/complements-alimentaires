from django import forms
from django.contrib import admin

from data.models import Declaration, Snapshot


class SnapshotInline(admin.TabularInline):
    model = Snapshot
    can_delete = False
    fields = ("user", "creation_date", "status", "comment")
    readonly_fields = fields
    extra = 0

    def has_add_permission(self, request, object):
        return False


class DeclarationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "address": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "additional_details": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "postal_code": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "cedex": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "country": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "brand": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "gamme": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "flavor": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "description": forms.Textarea(attrs={"cols": 35, "rows": 3}),
            "conditioning": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "instructions": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "warning": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "post_validation_producer_message": forms.Textarea(attrs={"cols": 35, "rows": 3}),
            "private_notes": forms.Textarea(attrs={"cols": 35, "rows": 3}),
            "other_galenic_formulation": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "other_effects": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "other_conditions": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "daily_recommended_dose": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "minimum_duration": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    form = DeclarationForm
    list_display = ("name", "status", "company", "author")
    list_filter = ("status", "company", "author")
    inlines = (SnapshotInline,)

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "name",
                    "brand",
                    "gamme",
                    "flavor",
                    "calculated_article",
                    "overriden_article",
                )
            },
        ),
        (
            "Identité du déclarant·e",
            {
                "classes": ["collapse"],
                "fields": (
                    "author",
                    "company",
                ),
            },
        ),
        (
            "Instruction e Visa",
            {
                "classes": ["collapse"],
                "fields": (
                    "status",
                    "instructor",
                    "visor",
                    "private_notes",
                ),
            },
        ),
        (
            "Produit",
            {
                "classes": ["collapse"],
                "fields": (
                    "description",
                    "galenic_formulation",
                    "unit_quantity",
                    "unit_measurement",
                    "conditioning",
                    "daily_recommended_dose",
                    "minimum_duration",
                    "instructions",
                    "warning",
                    "populations",
                    "conditions_not_recommended",
                    "other_conditions",
                    "effects",
                    "other_effects",
                ),
            },
        ),
        (
            "Adresse d'étiquetage",
            {
                "classes": ["collapse"],
                "fields": (
                    "address",
                    "additional_details",
                    "postal_code",
                    "city",
                    "cedex",
                    "country",
                ),
            },
        ),
    )
