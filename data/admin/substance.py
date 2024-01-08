from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

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
                "fields": ["name", "name_en", "is_obsolete", "source"],
            },
        ),
        (
            "Commentaires",
            {
                "fields": ["public_comments", "private_comments"],
            },
        ),
        (
            "Identifiants dans les répertoires de substances chimiques",
            {
                "fields": ["cas_number", "einec_number"],
            },
        ),
        (
            "Quantités",
            {
                "fields": ["must_specify_quantity", "min_quantity", "max_quantity", "nutritional_reference"],
            },
        ),
        (
            "Présence dans les ingrédients",
            {
                "fields": ["get_plants", "get_microorganisms", "get_ingredients"],
            },
        ),
    ]
    readonly_fields = ["get_plants", "get_microorganisms", "get_ingredients"]

    list_display = (
        "name",
        "get_plants",
        "get_microorganisms",
        "get_ingredients",
    )
    list_filter = ("is_obsolete",)
