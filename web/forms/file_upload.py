from django import forms
from data.models import ELEMENT_MODELS

# TODO ajout des relations


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="Sélectionnez un fichier :", help_text="Taille maximale : 500 Mo. Format supporté : csv."
    )

    file_type = forms.ChoiceField(
        choices=[(model.__name__, model.__name__) for model in ELEMENT_MODELS],
        label="Dans quelle table ces données doivent-elles être importées ?",
    )
