from django.db import transaction

from rest_framework import serializers

from data.models import Population
from data.models.substance import MaxQuantityPerPopulationRelation, Substance, SubstanceSynonym

from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    COMMON_FETCH_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithName,
)
from .utils import PrivateFieldsSerializer


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("id", "name")
        read_only_fields = fields


class SubstanceMaxQuantitySerializer(serializers.ModelSerializer):
    population = PopulationSerializer()

    class Meta:
        model = MaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class SubstanceSerializer(CommonIngredientReadSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Substance
        fields = COMMON_FETCH_FIELDS + (
            "name_en",
            "cas_number",
            "einec_number",
            "source",
            "must_specify_quantity",
            "max_quantity",
            "max_quantities",
            "nutritional_reference",
            "unit",
            "unit_id",
        )
        read_only_fields = fields


class SubstanceShortSerializer(PrivateFieldsSerializer):
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "name_en",
            "cas_number",
            "einec_number",
            "unit",
            "unit_id",
            "max_quantities",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "must_specify_quantity",
        )
        read_only_fields = fields


class SubstanceSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = ("name",)


class SubstanceMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.PrimaryKeyRelatedField(queryset=Population.objects.all())
    max_quantity = serializers.FloatField(source="ca_max_quantity")

    class Meta:
        model = MaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")


class SubstanceModificationSerializer(CommonIngredientModificationSerializer, WithName):
    synonyms = SubstanceSynonymModificationSerializer(many=True, source="substancesynonym_set", required=False)
    cas_number = serializers.CharField(source="ca_cas_number", required=False, allow_blank=True)
    einec_number = serializers.CharField(source="ca_einec_number", required=False, allow_blank=True)
    max_quantities = SubstanceMaxQuantityModificationSerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )

    nutritional_reference = serializers.FloatField(source="ca_nutritional_reference", required=False, allow_null=True)

    synonym_model = SubstanceSynonym
    synonym_set_field_name = "substancesynonym_set"

    class Meta:
        model = Substance
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "cas_number",
                "einec_number",
                "max_quantity",  # une property du Model, set grâce à create() et update()
                "max_quantities",
                "nutritional_reference",
                "unit",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS

    # @transaction.atomic
    # def create(self, validated_data):
    #     # le champ `max_quantity` n'existe pas dans validated_data
    #     # car ce n'est pas un champ du Model mais une property
    #     max_quantity = self.initial_data.get("max_quantity")
    #     substance = super().create(validated_data)
    #     if max_quantity:
    #         general_population = Population.objects.get(name="Population générale")
    #         MaxQuantityPerPopulationRelation.objects.create(
    #             substance=substance, population=general_population, ca_max_quantity=max_quantity
    #         )

    #     return substance

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     substance = super().update(instance, validated_data)

    #     # le champ `max_quantity` n'existe pas dans validated_data
    #     # car ce n'est pas un champ du Model mais une property
    #     if "max_quantity" in self.initial_data.keys():
    #         max_quantity = self.initial_data.get("max_quantity")

    #         general_population = Population.objects.get(name="Population générale")
    #         max_qty_general_pop = MaxQuantityPerPopulationRelation.objects.filter(
    #             substance=substance, population=general_population
    #         )

    #         # delete
    #         if max_qty_general_pop.exists() and max_quantity is None:
    #             max_qty_general_pop.first().delete()
    #         # update
    #         elif max_qty_general_pop.exists() and max_quantity is not None:
    #             max_quantity_to_change = max_qty_general_pop.first()
    #             max_quantity_to_change.ca_max_quantity = max_quantity
    #             max_quantity_to_change.save()
    #         # create
    #         elif not max_qty_general_pop.exists() and max_quantity is not None:
    #             MaxQuantityPerPopulationRelation.objects.create(
    #                 substance=substance, population=general_population, ca_max_quantity=max_quantity
    #             )

    #     return substance
    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    @transaction.atomic
    def create(self, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().create(validated_data)
        if max_quantities is None:
            return substance

        for max_quantity in max_quantities:
            self.add_max_quantity(substance, max_quantity)

        return substance

    @transaction.atomic
    def update(self, instance, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().update(instance, validated_data)
        if max_quantities is None:
            return substance

        # TODO: make this more sophisticated
        substance.maxquantityperpopulationrelation_set.all().delete()

        for max_quantity in max_quantities:
            self.add_max_quantity(substance, max_quantity)

        # synonyms = validated_data.pop(self.synonym_set_field_name, [])
        # change_reason = validated_data.pop("change_reason", "Modification via Compl'Alim")
        # data_items = copy.deepcopy(validated_data).items()
        # for key, value in data_items:
        #     if key.startswith("ca_"):
        #         siccrf_key = key.replace("ca_", "siccrf_")
        #         siccrf_value = getattr(instance, siccrf_key, None)
        #         ca_value = getattr(instance, key, None)
        #         if not value and (siccrf_value or ca_value):
        #             validated_data[siccrf_key] = value  # mettre comme None ou "" selon la requête
        #             logger.info(
        #                 f"SICCRF champ supprimé : le champ '{siccrf_key}' a été supprimé sur l'ingrédient type '{instance.object_type}', id '{instance.id}'"
        #             )
        #         elif value == siccrf_value and not ca_value:
        #             # si la valeur siccrf n'a pas été surpassée par une valeur CA, et la valeur donnée est la même que l'existante, pas besoin de la sauvegarder
        #             validated_data.pop(key, None)

        # super().update(instance, validated_data)
        # update_change_reason(instance, change_reason)

        # try:
        #     new_synonym_list = [s["name"] for s in synonyms]
        # except KeyError:
        #     raise ParseError(detail="Must provide 'name' to create new synonym")
        # existing_synonyms = getattr(instance, self.synonym_set_field_name)

        # # TODO: is it important to update, rather delete and recreate, 'new' synonyms ?
        # synonyms_to_delete = existing_synonyms.exclude(name__in=new_synonym_list)
        # synonyms_to_delete.delete()

        # for synonym in synonyms:
        #     if not existing_synonyms.filter(name=synonym["name"]).exists():
        #         self.add_synonym(instance, synonym)

        # return instance
        return substance

    def add_max_quantity(self, substance, max_quantity):
        MaxQuantityPerPopulationRelation.objects.create(
            substance=substance, population=max_quantity["population"], ca_max_quantity=max_quantity["ca_max_quantity"]
        )
