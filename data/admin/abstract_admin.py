from django import forms
from django.contrib import admin

from config import tasks
from data.models import Declaration


class ChangeReasonFormMixin(forms.ModelForm):
    # thanks to https://github.com/jazzband/django-simple-history/issues/853#issuecomment-1105754544
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
        widget=forms.TextInput(attrs={"size": "100"}),
    )


class ChangeReasonAdminMixin:
    def save_model(self, request, obj, form, change):
        if change:
            obj._change_reason = (
                form.cleaned_data["change_reason"]
                if "change_reason" in form.changed_data
                else "Modification via l'admin"
            )

        super().save_model(request, obj, form, change)


class RecomputeDeclarationArticleAtIngredientSaveMixin:
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # recalcul de l'article pour les déclarations concernées
        if change:
            ids_using_ingredient = getattr(obj, self.declaredingredient_set).values_list("declaration_id", flat=True)
            tasks.recalculate_article_for_ongoing_declarations(
                Declaration.objects.filter(id__in=ids_using_ingredient),
                f"Article recalculé après modification via l'admin de {obj.object_type} id {obj.id} : {obj.name}",
            )


class HasCommentListFilter(admin.SimpleListFilter):
    # Titre lisible par l'homme qui sera affiché dans le
    # Barre latérale d'administration droite juste au-dessus des options de filtre.
    title = "Avec commentaire"

    # Paramètre du filtre qui sera utilisé dans la requête URL.
    parameter_name = "has_comment"

    def lookups(self, request, model_admin):
        return [
            ("public", "Public"),
            ("private", "Privé"),
            ("none", "Aucun"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Comparez la valeur demandée (soit '80s' ou '90s')
        # pour décider comment filtrer l'ensemble de requêtes.
        if self.value() == "public":
            return queryset.exclude(public_comments=None)
        if self.value() == "private":
            return queryset.exclude(private_comments=None)
        if self.value() == "none":
            return queryset.filter(public_comments=None, private_comments=None)
