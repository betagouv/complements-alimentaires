from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from data.models import Substance
from data.admin.abstract_admin import IngredientAdminWithHistoryChangedFields


class SubstanceForm(forms.ModelForm):
    class Meta:
        widgets = {
            "CA_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "CA_source": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "CA_public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "CA_private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Substance)
class SubstanceAdmin(IngredientAdminWithHistoryChangedFields):
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
            None,  # Pas d'entête
            {
                "fields": ["siccrf_name", "CA_name", "siccrf_name_en", "siccrf_is_obsolete", "CA_is_obsolete", "siccrf_source", "CA_source"],
            },
        ),
        (
            "Commentaires",
            {
                "fields": ["siccrf_public_comments", "siccrf_private_comments", "CA_public_comments", "CA_private_comments"],
            },
        ),
        (
            "Identifiants dans les répertoires de substances chimiques",
            {
                "fields": ["siccrf_cas_number", "siccrf_einec_number", "CA_cas_number", "CA_einec_number"],
            },
        ),
        (
            "Quantités",
            {
                "fields": ["siccrf_must_specify_quantity", "siccrf_max_quantity", "siccrf_nutritional_reference", "CA_must_specify_quantity", "CA_max_quantity", "CA_nutritional_reference"],
            },
        ),
        (
            "Présence dans les ingrédients",
            {
                "fields": ["get_plants", "get_microorganisms", "get_ingredients"],
            },
        ),
    ]
    readonly_fields = ["siccrf_name", "siccrf_name_en", "siccrf_is_obsolete", "siccrf_source", "siccrf_public_comments", "siccrf_private_comments", "siccrf_cas_number", "siccrf_einec_number", "siccrf_must_specify_quantity", "siccrf_max_quantity", "siccrf_nutritional_reference", "get_plants", "get_microorganisms", "get_ingredients"]

    list_display = (
        "name",
        "get_plants",
        "get_microorganisms",
        "get_ingredients",
    )
    list_filter = (
        "siccrf_is_obsolete",
        "CA_is_obsolete",
    )
