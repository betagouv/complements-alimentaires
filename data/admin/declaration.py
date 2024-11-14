from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import (
    ComputedSubstance,
    Declaration,
    DeclaredIngredient,
    DeclaredMicroorganism,
    DeclaredPlant,
    DeclaredSubstance,
    Snapshot,
)


class SnapshotInline(admin.TabularInline):
    model = Snapshot
    can_delete = False
    fields = ("user", "creation_date", "status", "comment")
    readonly_fields = fields
    extra = 0

    def has_add_permission(self, request, object):
        return False


# Declared Plants inline


class DeclaredPlantInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            "new_name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "new_description": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


class DeclaredPlantInline(admin.StackedInline):
    model = DeclaredPlant
    form = DeclaredPlantInlineForm
    can_delete = True
    fields = (
        "plant",
        "active",
        "used_part",
        "quantity",
        "unit",
        "preparation",
        "first_ocurrence",
        "new",
        "new_name",
        "new_description",
    )
    autocomplete_fields = ("plant",)
    extra = 0

    def has_add_permission(self, request, object):
        return True


# Declared Microorganisms inline


class DeclaredMicroorganismInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            "new_species": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "new_genre": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "new_description": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "strain": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "quantity": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


class DeclaredMicroorganismInline(admin.StackedInline):
    model = DeclaredMicroorganism
    form = DeclaredMicroorganismInlineForm
    can_delete = True
    fields = (
        "microorganism",
        "activated",
        "strain",
        "quantity",
        "first_ocurrence",
        "new",
        "new_species",
        "new_genre",
        "new_description",
    )
    autocomplete_fields = ("microorganism",)

    extra = 0

    def has_add_permission(self, request, object):
        return True


# Declared Ingredients inline


class DeclaredIngredientInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            "new_name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "new_description": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "quantity": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


class DeclaredIngredientInline(admin.StackedInline):
    model = DeclaredIngredient
    form = DeclaredIngredientInlineForm
    can_delete = True
    fields = (
        "ingredient",
        "active",
        "quantity",
        "unit",
        "first_ocurrence",
        "new",
        "new_name",
        "new_type",
        "new_description",
    )
    autocomplete_fields = ("ingredient",)
    extra = 0

    def has_add_permission(self, request, object):
        return True


# Declared Substances inline


class DeclaredSubstanceInline(admin.StackedInline):
    model = DeclaredSubstance
    can_delete = True
    fields = ("substance", "quantity", "unit")
    autocomplete_fields = ("substance",)
    extra = 0

    def has_add_permission(self, request, object):
        return True


# Computed Substance inline


class ComputedSubstanceInline(admin.TabularInline):
    model = ComputedSubstance
    can_delete = False
    fields = ("substance", "quantity", "unit")
    autocomplete_fields = ("substance",)
    extra = 0

    def has_add_permission(self, request, object):
        return True


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
            "private_notes_instruction": forms.Textarea(attrs={"cols": 35, "rows": 3}),
            "private_notes_visa": forms.Textarea(attrs={"cols": 35, "rows": 3}),
            "other_galenic_formulation": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "other_effects": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "other_conditions": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "daily_recommended_dose": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "minimum_duration": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(Declaration)
class DeclarationAdmin(SimpleHistoryAdmin):
    form = DeclarationForm
    list_display = ("id", "name", "status", "company", "author")
    list_filter = ("status", "company", "author")
    list_select_related = ["author", "company"]

    show_facets = admin.ShowFacets.NEVER
    inlines = (
        DeclaredPlantInline,
        DeclaredMicroorganismInline,
        DeclaredIngredientInline,
        DeclaredSubstanceInline,
        ComputedSubstanceInline,
        SnapshotInline,
    )
    search_fields = (
        "name",
        "author__first_name",
        "author__last_name",
        "company__social_name",
        "company__commercial_name",
    )

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
                    "private_notes_instruction",
                    "private_notes_visa",
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
