from django.conf import settings

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration, Snapshot

from .pdfview import PdfDeclarationView

OTHER_OPTION = "Autre (à préciser)"


class SummaryView(PdfDeclarationView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get_template_path(self, declaration):
        return "summary.html"

    def get_context(self, declaration):
        product_table_rows = (
            ("Nom du produit", declaration.name),
            ("Marque", declaration.brand or "Non spécifiée"),
            ("Gamme", declaration.gamme or "Non spécifiée"),
            ("Description", declaration.description or "Non spécifiée"),
            ("Populations cibles", ", ".join(list(declaration.populations.all().values_list("name", flat=True)))),
            ("Populations à consommation déconseillée", self.get_conditions_string(declaration)),
            ("Mise en garde et avertissement", declaration.warning or "Non spécifiée"),
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

        environment = getattr(settings, "ENVIRONMENT")

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
            "environment": environment if environment in ["dev", "staging", "demo"] else None,
        }

    def get_conditions_string(self, declaration):
        has_other_conditions = declaration.conditions_not_recommended.filter(name=OTHER_OPTION).exists()
        conditions = ", ".join(
            list(declaration.conditions_not_recommended.exclude(name=OTHER_OPTION).values_list("name", flat=True))
        )
        if has_other_conditions and declaration.other_conditions:
            other = " : ".join([OTHER_OPTION, declaration.other_conditions])
            return ", ".join([conditions, other])
        return conditions

    def get_effects_string(self, declaration):
        has_other_effect = declaration.effects.filter(name=OTHER_OPTION).exists()
        effects = ", ".join(list(declaration.effects.exclude(name=OTHER_OPTION).values_list("name", flat=True)))
        if has_other_effect and declaration.other_effects:
            other = " : ".join([OTHER_OPTION, declaration.other_effects])
            return ", ".join([effects, other])
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
