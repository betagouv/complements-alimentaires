from django import forms
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from simple_history.admin import SimpleHistoryAdmin

from data.models import Substance, SubstanceSynonym
from data.models.declaration import Declaration

from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class SubstanceForm(ChangeReasonFormMixin):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "source": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


class SubstanceSynonymInline(admin.TabularInline):
    model = SubstanceSynonym
    extra = 1

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"cols": 60, "rows": 1})},
    }


@admin.register(Substance)
class SubstanceAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    @classmethod
    def links_to_objects(cls, object_name, objects):
        rel_list = "<ul>"
        for obj in objects:
            link = reverse(f"admin:data_{object_name}_change", args=[obj.id])
            rel_list += "<li><a href='{}'>{}</a></li>".format(link, obj.name)
        rel_list += "</ul>"
        return format_html(rel_list)

    @admin.display(description="plantes")
    def get_plants(self, obj):
        return self.links_to_objects("plant", obj.plant_set.all())

    @admin.display(description="microorganismes")
    def get_microorganisms(self, obj):
        return self.links_to_objects("microorganism", obj.microorganism_set.all())

    @admin.display(description="ingrédients")
    def get_ingredients(self, obj):
        return self.links_to_objects("ingredient", obj.ingredient_set.all())

    form = SubstanceForm
    fieldsets = [
        (
            None,
            {"fields": ["change_reason"]},
        ),
        (
            None,  # Pas d'entête
            {
                "fields": [
                    "siccrf_name",
                    "ca_name",
                    "siccrf_name_en",
                    "is_obsolete",
                    "ca_is_obsolete",
                    "siccrf_status",
                    "ca_status",
                    "siccrf_source",
                    "ca_source",
                    "is_risky",
                    "novel_food",
                ],
            },
        ),
        (
            "Commentaires",
            {
                "fields": [
                    "siccrf_public_comments",
                    "siccrf_private_comments",
                    "ca_public_comments",
                    "ca_private_comments",
                ],
            },
        ),
        (
            "Identifiants dans les répertoires de substances chimiques",
            {
                "fields": [
                    "siccrf_cas_number",
                    "siccrf_einec_number",
                    "ca_cas_number",
                    "ca_einec_number",
                ],
            },
        ),
        (
            "Quantités",
            {
                "fields": [
                    "siccrf_must_specify_quantity",
                    "siccrf_max_quantity",
                    "siccrf_nutritional_reference",
                    "ca_must_specify_quantity",
                    "ca_max_quantity",
                    "ca_nutritional_reference",
                    "unit",
                ],
            },
        ),
        (
            "Présence dans les ingrédients",
            {
                "fields": ["get_plants", "get_microorganisms", "get_ingredients"],
            },
        ),
    ]
    inlines = (SubstanceSynonymInline,)
    readonly_fields = [
        "siccrf_name",
        "siccrf_name_en",
        "is_obsolete",
        "siccrf_status",
        "siccrf_source",
        "siccrf_public_comments",
        "siccrf_private_comments",
        "siccrf_cas_number",
        "siccrf_einec_number",
        "siccrf_must_specify_quantity",
        "siccrf_max_quantity",
        "siccrf_nutritional_reference",
        "get_plants",
        "get_microorganisms",
        "get_ingredients",
    ]
    list_display = (
        "name",
        "is_obsolete",
        "get_plants",
        "get_microorganisms",
        "get_ingredients",
        "status",
        "is_risky",
        "novel_food",
    )
    list_filter = ("is_obsolete", "status", "is_risky", "novel_food")
    show_facets = admin.ShowFacets.NEVER
    search_fields = ["id", "name"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # recalcul de l'article pour les déclarations concernées
        if change and form["is_risky"]._has_changed():
            declared_substances_ids = obj.declaredsubstance_set.values_list("declaration_id", flat=True)
            computed_substances_ids = obj.computedsubstance_set.values_list("declaration_id", flat=True)
            for declaration in Declaration.objects.filter(
                id__in=declared_substances_ids.union(computed_substances_ids),
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
