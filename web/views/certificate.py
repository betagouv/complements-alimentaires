import logging

from rest_framework.exceptions import NotFound

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration, Snapshot

from .pdfview import PdfDeclarationView

logger = logging.getLogger(__name__)


class CertificateView(PdfDeclarationView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get_template_path(self, declaration):
        status = Declaration.DeclarationStatus
        article_map = {
            Declaration.Article.ARTICLE_15: 15,
            Declaration.Article.ARTICLE_15_WARNING: 15,
            Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION: 15,
            Declaration.Article.ARTICLE_16: 16,
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
        }

    def get_pdf_file_name(self, declaration):
        # Le load-balancer Sozu a du mal avec les noms de fichier pdf contenant des caractères non-ASCII
        # https://github.com/betagouv/complements-alimentaires/issues/1367
        name = declaration.name.encode("ascii", "ignore")
        return f"attestation-{name.decode()}.pdf"
