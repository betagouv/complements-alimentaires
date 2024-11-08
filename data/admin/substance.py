from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from data.models import Substance

from .abstract_admin import ElementAdminWithChangeReason


class SubstanceForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "siccrf_name_en": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "source": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "public_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
            "private_comments": forms.Textarea(attrs={"cols": 60, "rows": 4}),
        }


@admin.register(Substance)
class SubstanceAdmin(ElementAdminWithChangeReason):
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
    list_display = ("name", "get_plants", "get_microorganisms", "get_ingredients", "status", "is_risky")
    list_filter = ("is_obsolete", "status", "is_risky")
    search_fields = ["id", "name"]
