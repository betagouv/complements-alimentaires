from django import forms
from django.contrib import admin
from django.db import models

from simple_history.admin import SimpleHistoryAdmin

from data.models import Declaration, Ingredient, IngredientSynonym

from .abstract_admin import (
    ChangeReasonAdminMixin,
    ChangeReasonFormMixin,
    RecomputeDeclarationArticleAtIngredientSaveMixin,
)


class IngredientSynonymInline(admin.TabularInline):
    model = IngredientSynonym
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


class SubstanceInlineAdmin(admin.TabularInline):
    model = Ingredient.substances.through
    extra = 0


class IngredientForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Ingredient)
class IngredientAdmin(RecomputeDeclarationArticleAtIngredientSaveMixin, ChangeReasonAdminMixin, SimpleHistoryAdmin):
    declaredingredient_set = "declaredingredient_set"
    form = IngredientForm
    inlines = (
        SubstanceInlineAdmin,
        IngredientSynonymInline,
    )
    list_display = ("name", "is_obsolete", "status", "is_risky", "novel_food", "has_linked_substances")
    list_filter = ("is_obsolete", "status", "is_risky", "novel_food", "ingredient_type")
    show_facets = admin.ShowFacets.NEVER
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
    search_fields = ["id", "name"]

    def has_linked_substances(self, obj):
        return "Oui" if obj.substances.exists() else "Non"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # recalcul de l'article pour les déclarations concernées
        if change and form["is_risky"].has_changed():
            for declaration in Declaration.objects.filter(
                id__in=obj.declaredingredient_set.values_list("declaration_id", flat=True),
                status__in=(
                    Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
                    Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
                    Declaration.DeclarationStatus.AWAITING_VISA,
                    Declaration.DeclarationStatus.OBSERVATION,
                    Declaration.DeclarationStatus.OBJECTION,
                ),
            ):
                declaration.assign_calculated_article()
                declaration.save()
