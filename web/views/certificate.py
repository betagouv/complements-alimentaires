import logging

from rest_framework.exceptions import NotFound

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration, Snapshot

from .pdfview import PdfView

logger = logging.getLogger(__name__)


class CertificateView(PdfView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get_template_path(self, declaration):
        status = Declaration.DeclarationStatus
        article_map = {
            Declaration.Article.ARTICLE_15: 15,
            Declaration.Article.ARTICLE_15_WARNING: 15,
            Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION: 15,
            Declaration.Article.ARTICLE_16: 16,
            Declaration.Article.ARTICLE_18: 18,
            Declaration.Article.ANSES_REFERAL: "anses",
        }
        article = article_map.get(declaration.article, 15)
        if declaration.status in [
            status.AWAITING_INSTRUCTION,
            status.AWAITING_VISA,
            status.ONGOING_INSTRUCTION,
            status.ONGOING_VISA,
        ]:
            return f"certificates/certificate-submitted-art-{article}.html"

        template_status = declaration.status

        # La mise en abandon ne produit pas de Snapshot (car pas effectué en tant qu'action usager).
        # On vérifie donc le status du dernier snapshot pour calculer le template
        if template_status == status.ABANDONED:
            template_status = declaration.snapshots.latest("creation_date").status

        if template_status in [status.AUTHORIZED, status.WITHDRAWN]:
            return f"certificates/certificate-art-{article}.html"
        if template_status == status.OBJECTION:
            return "certificates/certificate-objected.html"
        if template_status == status.REJECTED:
            return "certificates/certificate-rejected.html"

        raise NotFound()

    def get_context(self, declaration):
        status = Declaration.DeclarationStatus
        date_statuses = [status.AWAITING_INSTRUCTION, status.AUTHORIZED, status.REJECTED]
        direction = (
            "de la concurrence, de la consommation et de la répression des fraudes (DGCCRF)"
            if declaration.siccrf_id
            else "de l'alimentation (DGAL)"
        )
        address_street = "59 BD VINCENT AURIOL - TÉLÉDOC 223" if declaration.siccrf_id else "251 RUE DE VAUGIRARD"
        address_cedex = "75703 PARIS CEDEX 13" if declaration.siccrf_id else "75732 PARIS CEDEX 15"
        bureau = (
            "Bureau 4A - Nutrition et information sur les denrées alimentaires"
            if declaration.siccrf_id
            else "BEPIAS (Bureau des Etablissements et Produits des Industries Alimentaires Spécialisées)"
        )
        mail = (
            "bureau-4A@dgccrf.finances.gouv.fr" if declaration.siccrf_id else "bepias.sdssa.dgal@agriculture.gouv.fr"
        )
        signature_title = (
            "La Sous-Direction"
            if declaration.siccrf_id
            else "La Sous-Directrice de la sécurité sanitaire des aliments"
        )
        signature_name = "" if declaration.siccrf_id else "Vanessa HUMMEL-FOURRAT"
        try:
            date = (
                declaration.snapshots.filter(status__in=date_statuses)
                .exclude(action=Snapshot.SnapshotActions.REFUSE_VISA)
                .latest("creation_date")
                .creation_date
            )
        except Exception as e:
            logger.error(f"Error obtaining certificate date for declaration {declaration.id}")
            logger.exception(e)
            date = declaration.creation_date

        try:
            submission_actions = [
                Snapshot.SnapshotActions.SUBMIT,
                Snapshot.SnapshotActions.RESPOND_TO_OBJECTION,
                Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION,
            ]
            last_submission_date = (
                declaration.snapshots.filter(action__in=submission_actions).latest("creation_date").creation_date
            )
        except Exception as e:
            logger.error(f"Error obtaining last submission date for declaration {declaration.id}")
            logger.exception(e)
            last_submission_date = declaration.creation_date

        return {
            "date": date,
            "last_submission_date": last_submission_date,
            "include_recipient_address": declaration.status == Declaration.DeclarationStatus.REJECTED,
            "recipient_lines": [
                declaration.company.social_name,
                declaration.company.address,
                f"{declaration.company.city} {declaration.company.country}",
            ],
            "declaration": declaration,
            "direction": direction,
            "address_street": address_street,
            "address_cedex": address_cedex,
            "bureau": bureau,
            "mail": mail,
            "signature_title": signature_title,
            "signature_name": signature_name,
        }

    def get_pdf_file_name(self, declaration):
        # Le load-balancer Sozu a du mal avec les noms de fichier pdf contenant des caractères non-ASCII
        # https://github.com/betagouv/complements-alimentaires/issues/1367
        name = declaration.name.encode("ascii", "ignore")
        return f"attestation-{name.decode()}.pdf"
