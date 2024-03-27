import csv
import logging
from django.apps import apps
from django.views.generic import FormView
from django.shortcuts import render

from web.forms import FileUploadForm
from data.csv_importer import _import_csv_to_model
from data.exceptions import CSVFileError

logger = logging.getLogger(__name__)


class FileUploadView(FormView):
    """
    View du formulaire d'upload de fichier à importer en BDD
    """

    def get(self, request, *args, **kwargs):
        return render(request, "upload_file.html", {"form": FileUploadForm()})

    def post(self, request, *args, **kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_type = form.cleaned_data["file_type"]
            self.handle_uploaded_file(uploaded_file, file_type)
            return render(request, "upload_success.html", {"file_name": uploaded_file.name})
        return render(request, "upload_file.html", {"form": form})

    def handle_uploaded_file(self, csv_file, file_type):
        logger.info(f"J'ai bien reçu le fichier {csv_file.name} de type {file_type}")
        # TODO enregistrer le fichier sur disque ?
        # destination = open(f"some/file/{csv_file.name}", "wb+")
        # for chunk in csv_file.chunks():
        #     destination.write(chunk)
        # destination.close()

        # Importer le fichier en base
        model = list(filter(lambda model: model.__name__ == "Ingredient", apps.get_models()))[0]
        try:
            csv_string = csv_file.read().decode("utf-8-sig")
        except UnicodeDecodeError as e:
            raise CSVFileError(f"'{csv_file.name}' n'est pas un fichier unicode.", e)
        try:
            csv_lines = csv_string.splitlines()
            dialect = csv.Sniffer().sniff(csv_lines[0])
        except csv.Error as e:
            raise CSVFileError(f"'{csv_file.name}' n'est pas un fichier csv.", e)

        csvreader = csv.DictReader(csv_lines, dialect=dialect)

        nb_row, nb_created, updated_models = _import_csv_to_model(csvreader, csv_file.name, model, is_relation=False)
        logger.info(
            f"Import de {csv_file.name} dans le modèle {model.__name__} terminé : {nb_row} objets importés, {nb_created} objets créés."
        )
