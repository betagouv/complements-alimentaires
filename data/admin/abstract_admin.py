from django import forms

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
        if change and form["is_risky"]._has_changed():
            ids_using_ingredient = getattr(obj, self.declaredingredient_set).values_list("declaration_id", flat=True)
            tasks.recalculate_article_for_ongoing_declarations(
                Declaration.objects.filter(id__in=ids_using_ingredient),
                f"Article recalculé après modification via l'admin de {obj.name} ({obj.object_type} id {obj.id})",
            )
