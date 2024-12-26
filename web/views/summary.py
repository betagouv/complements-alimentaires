import logging
import os

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework.generics import GenericAPIView
from xhtml2pdf import pisa

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration

logger = logging.getLogger(__name__)


class SummaryView(GenericAPIView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get(self, request, *args, **kwargs):
        declaration = self.get_object()
        template = get_template("summary.html")
        html = template.render(self.get_context(declaration))

        # return HttpResponse(html)

        response = HttpResponse(content_type="application/pdf")
        filename = self.get_pdf_file_name(declaration)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=SummaryView.link_callback)

        if pisa_status.err:
            logger.error(f"Error while generating PDF for teledeclaration {declaration.id}:\n{pisa_status.err}")
            return HttpResponse("An error ocurred", status=500)

        return response

    def get_context(self, declaration):
        product_table_rows = (
            ("Nom du produit", declaration.name),
            ("Marque", declaration.brand or "Non spécifiée"),
            ("Gamme", declaration.gamme or "Non spécifiée"),
            ("Description", declaration.description or "Non spécifiée"),
            ("Populations cibles", "TODO"),
            ("Populations à consommation déconseillée", "TODO"),
            ("Forme galénique", "TODO"),
            ("Mode d'emploi", declaration.instructions or "Non spécifié"),
            ("Unité de consommation", "TODO"),
            ("Dose journalière recommandée", declaration.daily_recommended_dose or "Non spécifiée"),
            ("Conditionnement", declaration.conditioning or "Non spécifié"),
            ("Durabilité minimale / DLUO (en mois)", declaration.minimum_duration or "Non spécifiée"),
            ("Objectifs / effets", "TODO"),
        )
        return {
            "product_table_rows": product_table_rows,
            "declaration": declaration,
            "declared_plants": declaration.declared_plants.all(),
            "declared_microorganisms": declaration.declared_microorganisms.all(),
            "declared_ingredients": declaration.declared_ingredients.all(),
            "declared_substances": declaration.declared_substances.all(),
            "computed_substances": declaration.computed_substances.all(),
            "attachments": declaration.attachments.all(),
        }

    def get_pdf_file_name(self, declaration):
        # Le load-balancer Sozu a du mal avec les noms de fichier pdf contenant des caractères non-ASCII
        # https://github.com/betagouv/complements-alimentaires/issues/1367
        name = declaration.name.encode("ascii", "ignore")
        return f"attestation-{name.decode()}.pdf"

    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources.
        """
        # Gestion des fichiers STATIC
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        # Gestion des fichiers MEDIA
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        else:
            return uri  # On le laisse tel qu'il est car pas static ni media

        # On vérifie que le path existe
        if not os.path.isfile(path):
            raise Exception(f"File does not exist: {path}")
        return path
