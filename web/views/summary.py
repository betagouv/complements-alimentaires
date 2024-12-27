import logging
import os

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework.generics import GenericAPIView
from xhtml2pdf import pisa

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration, Snapshot

logger = logging.getLogger(__name__)

OTHER_OPTION = "Autre (à préciser)"


class SummaryView(GenericAPIView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get(self, request, *args, **kwargs):
        declaration = self.get_object()
        template = get_template("summary.html")
        html = template.render(self.get_context(declaration))

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
            ("Populations cibles", ", ".join(list(declaration.populations.all().values_list("name", flat=True)))),
            ("Populations à consommation déconseillée", self.get_conditions_string(declaration)),
            (
                "Forme galénique",
                declaration.galenic_formulation or declaration.other_galenic_formulation or "Non spécifiée",
            ),
            ("Mode d'emploi", declaration.instructions or "Non spécifié"),
            ("Unité de consommation", self.get_measurement_unit_string(declaration)),
            ("Dose journalière recommandée", declaration.daily_recommended_dose or "Non spécifiée"),
            ("Conditionnement", declaration.conditioning or "Non spécifié"),
            ("Durabilité minimale / DLUO (en mois)", declaration.minimum_duration or "Non spécifiée"),
            ("Objectifs / effets", self.get_effects_string(declaration)),
        )
        try:
            last_submission_snapshot = declaration.snapshots.filter(action=Snapshot.SnapshotActions.SUBMIT).latest(
                "creation_date"
            )
            submission_date = last_submission_snapshot.creation_date
        except Exception as _:
            submission_date = None

        return {
            "product_table_rows": product_table_rows,
            "declaration": declaration,
            "declared_plants": declaration.declared_plants.all(),
            "declared_microorganisms": declaration.declared_microorganisms.all(),
            "declared_ingredients": declaration.declared_ingredients.all(),
            "declared_substances": declaration.declared_substances.all(),
            "computed_substances": declaration.computed_substances.all(),
            "attachments": declaration.attachments.all(),
            "submission_date": submission_date,
        }

    def get_conditions_string(self, declaration):
        has_other_conditions = declaration.conditions_not_recommended.filter(name=OTHER_OPTION).exists()
        conditions = ", ".join(
            list(declaration.conditions_not_recommended.exclude(name=OTHER_OPTION).values_list("name", flat=True))
        )
        if has_other_conditions and declaration.other_conditions:
            return ", ".join([conditions, declaration.other_conditions])
        return conditions

    def get_effects_string(self, declaration):
        has_other_effect = declaration.effects.filter(name=OTHER_OPTION).exists()
        effects = ", ".join(list(declaration.effects.exclude(name=OTHER_OPTION).values_list("name", flat=True)))
        if has_other_effect and declaration.other_effects:
            return ", ".join([effects, declaration.other_effects])
        return effects

    def get_measurement_unit_string(self, declaration):
        if not declaration.unit_quantity or not declaration.unit_measurement:
            return "Non spécifiée"
        return f"{declaration.unit_quantity} {declaration.unit_measurement.name}"

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

        return path
