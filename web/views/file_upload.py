import datetime
import logging

from django.apps import apps
from django.shortcuts import render
from django.views.generic import FormView

from data.etl.csv_importer import CSVImporter
from web.forms import FileUploadForm

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
            export_date: datetime.date = form.cleaned_data["export_date"]
            self._handle_uploaded_file(uploaded_file, file_type, export_date)
            return render(request, "upload_success.html", {"file_name": uploaded_file.name})
        return render(request, "upload_file.html", {"form": form})

    def _handle_uploaded_file(self, csv_file, file_type, export_date):
        model = list(filter(lambda model: model.__name__ == file_type, apps.get_models()))[0]
        csv_importer = CSVImporter(csv_file, model, is_relation=False)
        _ = csv_importer.import_csv(export_date)
        logger.info(
            f"Import de {csv_file.name} dans le modèle {model.__name__} terminé : {csv_importer.nb_line_in_success} objets importés, {csv_importer.nb_objects_created} objets créés."
        )
