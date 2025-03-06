from django import forms


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
                if "change_reason" in form.cleaned_data.keys()
                else "Modification via l'admin"
            )

        super().save_model(request, obj, form, change)
