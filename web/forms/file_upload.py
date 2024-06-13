from django import forms

from data.models import DECLARATION_MODELS, ELEMENT_MODELS

# TODO ajout des relations


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="Sélectionnez un fichier :", help_text="Taille maximale : 500 Mo. Format supporté : csv."
    )

    file_type = forms.ChoiceField(
        choices=[(model.__name__, model.__name__) for model in ELEMENT_MODELS + DECLARATION_MODELS],
        label="Dans quelle table ces données doivent-elles être importées ?",
    )

    export_date = forms.DateField(
        label="Quelle est la date d'export du dump ?",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
