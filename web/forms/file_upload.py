from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(
        label="Sélectionnez un fichier :", help_text="Taille maximale : 500 Mo. Format supporté : csv."
    )

    file_type = forms.ChoiceField(
        choices=[("ingredient", "Ingredient"), ("plante", "Plante")],
        label="Fichier contenant les données de ",
    )
