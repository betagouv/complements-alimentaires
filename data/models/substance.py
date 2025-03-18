from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Coalesce, NullIf

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_models import IngredientCommonModel
from .ingredient_type import IngredientType
from .mixins import WithMissingImportBoolean
from .population import Population
from .unit import SubstanceUnit


class SubstanceType(models.IntegerChoices):
    """
    enzymes, vitamines, minéraux, acide aminés, acide gras, métabolite
    """

    VITAMIN = 1, "Vitamine"
    MINERAL = 2, "Minéral"
    SECONDARY_METABOLITE = 3, "Métabolite secondaire de plante"
    CARBOHYDRATE = 4, "Glucide"
    ENZYME = (
        5,
        "Enzyme",
    )
    # pas encore de règle connue par nous pour les déterminer de manière fiable
    # LIPID = 3, "Lipides"
    # AMINO_ACID = 4, "Acide aminé"


class Substance(IngredientCommonModel):
    """
    siccrf_min_quantity présente dans les tables SICCRF n'est strictement jamais remplie, donc pas transformée en champ du modèle
    siccrf_source_en présente dans les tables SICCRF est très peu remplie, donc pas transformée en champ du modèle
    TODO: à terme cette table de substance ne devrait contenir que les substances à but nutritionnel ou physiologique (pas les enzymes, etc)
    """

    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    # cas_number
    siccrf_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS (selon la base SICCRF)")
    ca_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    cas_number = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_cas_number"), Value("")), F("siccrf_cas_number")),
        output_field=models.CharField(max_length=10, blank=True, verbose_name="numéro CAS"),
        db_persist=True,
    )

    # einec_number
    siccrf_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS (selon la base SICCRF)",
    )
    ca_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    einec_number = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_einec_number"), Value("")), F("siccrf_einec_number")),
        output_field=models.CharField(max_length=7, blank=True, verbose_name="numéro EINECS"),
        db_persist=True,
    )

    # source
    siccrf_source = models.TextField(blank=True)
    ca_source = models.TextField(blank=True)
    source = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_source"), Value("")), F("siccrf_source")),
        output_field=models.TextField(),
        db_persist=True,
    )

    # must_specify_quantity
    siccrf_must_specify_quantity = models.BooleanField(
        default=False, verbose_name="spécification de quantité obligatoire (selon la base SICCRF)"
    )
    ca_must_specify_quantity = models.BooleanField(
        null=True, default=None, verbose_name="spécification de quantité obligatoire"
    )
    must_specify_quantity = models.GeneratedField(
        expression=Coalesce(F("ca_must_specify_quantity"), F("siccrf_must_specify_quantity")),
        output_field=models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire"),
        db_persist=True,
    )

    # max_quantity
    max_quantities = models.ManyToManyField(Population, through="MaxQuantityPerPopulationRelation")

    # nutritional_reference
    siccrf_nutritional_reference = models.FloatField(
        null=True, blank=True, verbose_name="apport nutritionnel conseillé"
    )
    ca_nutritional_reference = models.FloatField(null=True, blank=True, verbose_name="apport nutritionnel conseillé")
    nutritional_reference = models.GeneratedField(
        expression=Coalesce("ca_nutritional_reference", "siccrf_nutritional_reference"),
        output_field=models.FloatField(null=True, blank=True, verbose_name="apport nutritionnel conseillé"),
        db_persist=True,
    )
    unit = models.ForeignKey(
        SubstanceUnit,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="unité des quantités spécifiées (quantité max, apport de référence)",
    )
    substance_types = ArrayField(
        models.IntegerField(null=True, choices=SubstanceType.choices),
        null=True,
        verbose_name="type(s) de la substance",
    )

    history = HistoricalRecords(
        inherit=True,
        excluded_fields=[
            "name",
            "is_obsolete",
            "private_comments",
            "public_comments",
            "cas_number",
            "einec_number",
            "source",
            "must_specify_quantity",
            "nutritional_reference",
            "status",
            "siccrf_status",
            "substance_types",
        ],
    )

    @property
    def name_en(self):
        return self.siccrf_name_en

    @property
    def max_quantity(self):
        """
        Cette property renvoie la max_quantity pour la Population Générale
        """
        try:
            return self.max_quantities.through.objects.get(
                population__name="Population générale", substance=self
            ).max_quantity
        except MaxQuantityPerPopulationRelation.DoesNotExist:
            return

    def compute_substance_types(self):
        """
        Cette fontion permet de mettre à jour le type de substance.
        Elle est appelée dès que l'un des champs de substance est modifié.
        Sauf pour les metabolites secondaires, les vitamines et les minéraux, la liste n'est pas exhaustive.
        """

        list_of_type = []

        if len(self.ingredient_set.all()) != 0 and any(
            [ingredient.ingredient_type == IngredientType.FORM_OF_SUPPLY for ingredient in self.ingredient_set.all()]
        ):
            if self.siccrf_name.startswith("vitamine") or self.ca_name.startswith("vitamine"):
                list_of_type.append(SubstanceType.VITAMIN)
            else:
                list_of_type.append(SubstanceType.MINERAL)
        if len(self.plant_set.all()) != 0:
            list_of_type.append(SubstanceType.SECONDARY_METABOLITE)

        # ces conditions sont indicatives de ce qu'une substance est un ose, ase, etc mais pas extensives
        if self.siccrf_name.endswith("ose") or self.ca_name.endswith("ose"):
            list_of_type.append(SubstanceType.CARBOHYDRATE)
        elif self.siccrf_name.endswith("ase") or self.ca_name.endswith("ase"):
            list_of_type.append(SubstanceType.ENZYME)

        return list_of_type

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Calcul après la sauvegarde initiale
        if not self.substance_types:
            self.substance_types = self.compute_substance_types()

            # Mise à jour sans appeler save() à nouveau
            # super().save(update_fields={"substance_types": self.substance_types})
            Substance.objects.filter(pk=self.pk).update(substance_types=self.substance_types)


class SubstanceSynonym(TimeStampable, Historisable, WithMissingImportBoolean):
    class Meta:
        verbose_name = "synonyme substance active"

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    name = models.TextField(verbose_name="nom")
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète selon SICCRF", default=False)
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys

    @property
    def is_obsolete(self):
        return self.siccrf_is_obsolete

    def __str__(self):
        return self.name


class MaxQuantityPerPopulationRelation(Historisable):
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    population = models.ForeignKey(Population, on_delete=models.CASCADE)
    siccrf_max_quantity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="quantité maximale autorisée pour la population cible (selon la base SICCRF)",
    )
    ca_max_quantity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="quantité maximale autorisée pour la population cible",
    )
    max_quantity = models.GeneratedField(
        expression=Coalesce(F("ca_max_quantity"), F("siccrf_max_quantity")),
        output_field=models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée"),
        db_persist=True,
    )
