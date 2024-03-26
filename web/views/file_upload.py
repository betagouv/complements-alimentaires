import logging
from django.views.generic import FormView
from django.shortcuts import render
from ..forms import FileUploadForm

logger = logging.getLogger(__name__)


class FileUploadView(FormView):
    """
    View du formulaire d'upload de fichier à importer en BDD
    """

    def post(self, request, *args, **kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_type = form.cleaned_data["file_type"]
            self.handle_uploaded_file(uploaded_file, file_type)
            return render(request, "upload_success.html", {"file_name": uploaded_file.name})
        return render(request, "upload_file.html", {"form": form})

    def handle_uploaded_file(self, file, file_type):
        logger.info(f"J'ai bien reçu le fichier {file} de type {file_type}")

        # destination = open(f"some/file/{file.name}", "wb+")
        # for chunk in file.chunks():
        #     destination.write(chunk)
        # destination.close()
