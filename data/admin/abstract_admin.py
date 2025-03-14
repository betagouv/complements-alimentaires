from django import forms

from data.models import Declaration


class ChangeReasonFormMixin(forms.ModelForm):
    # thanks to https://github.com/jazzband/django-simple-history/issues/853#issuecomment-1105754544
    change_reason = forms.CharField(
        label="Raison de modification (rendue publique dans le cas des Ingrédients, Plantes, Substances, Microorganismes)",
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
            for declaration in Declaration.objects.filter(
                id__in=getattr(obj, self.declaredingredient_set).values_list("declaration_id", flat=True),
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
