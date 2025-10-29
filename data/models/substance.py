from django.contrib.postgres.fields import ArrayField
from django.db import models

from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason

from data.validators import validate_cas

from .abstract_ingredient_models import IngredientCommonModel
from .abstract_ingredient_relation_models import (
    MaxQuantityPerPopulationRelationCommonModel,
    SynonymCommonModel,
)
from .mixins import PublicReasonHistoricalModel
from .population import Population


class SubstanceType(models.IntegerChoices):
    """
    enzymes, vitamines, minéraux, acide aminés, acide gras, métabolite
    """

    VITAMIN = 1, "Vitamine"
    MINERAL = 2, "Minéral"
    SECONDARY_METABOLITE = (
        3,
        "Métabolite secondaire de plante",
    )
    BIOACTIVE_SUBSTANCE = (
        4,
        "Substance active à but nutritionnel ou physiologique",
    )  # elles respectent l'arrêté substances du 26 sept 2016 (substances acceptées par la DGCCRF)

    # ce sont des types qui pourraient être intéressant pour information
    # aux consommateurices mais n'ont pas d'intérêt pour la règlementation des CA
    # CARBOHYDRATE = 5, "Glucide" - finissent par ose
    # ENZYME = 5, "Enzyme" - finissent par ase
    # ESSENTIAL_FATTY_ACID = 6, "Lipides"
    # AMINO_ACID = 7, "Acide aminé"


class Substance(IngredientCommonModel):
    """
    TODO: à terme cette table de substance ne devrait contenir que les substances à but nutritionnel ou physiologique (pas les enzymes, etc)
    """

    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    # cas_number
    cas_number = models.CharField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="n° CAS",
        validators=[validate_cas],
    )
    # einec_number
    einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    # must_specify_quantity
    must_specify_quantity = models.BooleanField(
        default=False, verbose_name="spécification de quantité obligatoire lors de la déclaration ?"
    )

    # max_quantity
    max_quantities = models.ManyToManyField(Population, through="SubstanceMaxQuantityPerPopulationRelation")

    # nutritional_reference (concerne seulement les types vitamines et minéraux)
    nutritional_reference = models.FloatField(null=True, blank=True, verbose_name="apport nutritionnel conseillé")

    substance_types = ArrayField(
        models.IntegerField(choices=SubstanceType.choices),
        verbose_name="type(s) de la substance",
        default=list,
    )

    history = HistoricalRecords(
        bases=[
            PublicReasonHistoricalModel,
        ],
        inherit=True,
    )

    @property
    def max_quantity(self):
        """
        Cette property renvoie la max_quantity pour la Population Générale
        """
        try:
            return self.max_quantities.through.objects.get(
                population__name="Population générale", substance=self
            ).max_quantity
        except SubstanceMaxQuantityPerPopulationRelation.DoesNotExist:
            return

    def update_metabolite_type(self):
        # ajoute le type métabolite secondaire s'il n'a pas été indiqué dans les types
        if self.plant_set.count() and SubstanceType.SECONDARY_METABOLITE not in self.substance_types:
            self.substance_types.append(SubstanceType.SECONDARY_METABOLITE)
            self.save(update_substance_types=False)
            update_change_reason(self, "Cette substance est liée à une plante")
        # supprime le type métabolite secondaire s'il est dans les types mais n'est pas valide
        elif SubstanceType.SECONDARY_METABOLITE in self.substance_types and self.plant_set.count() == 0:
            self.substance_types.remove(SubstanceType.SECONDARY_METABOLITE)
            self.save(update_substance_types=False)
            update_change_reason(self, "Cette substance n'est pas liée à une plante")

    def save(self, update_substance_types=True, *args, **kwargs):
        # Les string vides rompent la contrainte d'unicité
        if not self.cas_number:
            self.cas_number = None
        super().save(*args, **kwargs)
        if update_substance_types:
            self.update_metabolite_type()


class SubstanceSynonym(SynonymCommonModel):
    class Meta:
        verbose_name = "synonyme substance active"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_substance_synonym",
            )
        ]

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")


class SubstanceMaxQuantityPerPopulationRelation(MaxQuantityPerPopulationRelationCommonModel):
    class Meta:
        verbose_name = "quantité maximum de substance autorisée pour une population cible"
        constraints = [
            models.UniqueConstraint(
                fields=["substance", "population"],
                name="unique_substance_max_quantity_per_population",
            )
        ]

    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
