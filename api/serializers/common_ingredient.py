import logging

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from simple_history.utils import update_change_reason

from api.utils.choice_field import GoodReprChoiceField
from config import tasks
from data.models import Declaration, IngredientStatus, Substance

from .historical_record import HistoricalRecordField
from .utils import HistoricalModelSerializer, PrivateFieldsSerializer

logger = logging.getLogger(__name__)

COMMON_NAME_FIELDS = ("name",)

COMMON_FIELDS = (
    "id",
    "synonyms",
    "description",
    "warnings_on_label",
    "public_comments",
    "max_quantities",
    "unit",
    "private_comments",
    "status",
    "novel_food",
    "is_risky",
    "change_reason",
    "public_change_reason",
    "to_be_entered_in_next_decree",
    "requires_analysis_report",
    "regulatory_resource_links",
    "revoked_detail",
    "is_obsolete",
    "origin_declaration",
)

COMMON_READ_ONLY_FIELDS = ("id",)

COMMON_FETCH_FIELDS = (
    "id",
    "name",
    "synonyms",
    "description",
    "warnings_on_label",
    "public_comments",
    "max_quantities",
    "unit",
    "unit_id",
    "activity",
    "status",
    "novel_food",
    "is_risky",
    "history",
    "object_type",
    "requires_analysis_report",
    "regulatory_resource_links",
    "is_obsolete",
    "revoked_detail",
    # Les suivants sont cachés si l'utilisateur.ice ne fait pas partie de l'administration
    "private_comments",
    "origin_declaration",
    "to_be_entered_in_next_decree",
)


class WithSubstances(serializers.ModelSerializer):
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all(), required=False)


class CommonIngredientModificationSerializer(serializers.ModelSerializer):
    change_reason = serializers.CharField(required=False, allow_blank=True)
    public_change_reason = serializers.CharField(required=False, allow_blank=True)

    def validate_max_quantities(self, value):
        population_ids = [v["population"].id for v in value]
        unique_pop_ids = list(set(population_ids))
        if len(population_ids) != len(unique_pop_ids):
            raise serializers.ValidationError("Veuillez ne donner qu'une quantité maximale par population")
        return value

    def validate(self, data):
        status = data.get("status")
        if status == IngredientStatus.AUTHORIZATION_REVOKED:
            if self.instance.status != IngredientStatus.AUTHORIZED:
                raise serializers.ValidationError(
                    {"status": "Pas possible de retirer l'autorisation d'un ingrédient non-autorisé"}
                )
            if not data.get("revoked_detail"):
                raise serializers.ValidationError(
                    {"revoked_detail": "Il faut donner du détail sur la décision de retirer l'ingrédient"}
                )
        return data

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    @transaction.atomic
    def create(self, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        max_quantities = validated_data.pop(self.max_quantities_set_field_name, [])
        change_reason = validated_data.pop("change_reason", "Création via Compl'Alim")

        ingredient = super().create(validated_data)
        for synonym in synonyms:
            self.add_synonym(ingredient, synonym)
        for max_quantity in max_quantities:
            self.add_max_quantity(ingredient, max_quantity)

        self.update_change_reason(ingredient, change_reason, "")

        return ingredient

    @transaction.atomic
    def update(self, instance, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        max_quantities = validated_data.pop(self.max_quantities_set_field_name, None)
        change_reason = validated_data.pop("change_reason", "Modification via Compl'Alim")
        public_change_reason = validated_data.pop("public_change_reason", "")
        ingredient = super().update(instance, validated_data)
        self.update_change_reason(instance, change_reason, public_change_reason)

        try:
            new_synonym_list = [s["name"] for s in synonyms]
        except KeyError:
            raise ParseError(detail="Must provide 'name' to create new synonym")
        existing_synonyms = getattr(instance, self.synonym_set_field_name)

        # si le nom du synonym à changé il est recréé
        synonyms_to_delete = existing_synonyms.exclude(name__in=new_synonym_list)
        synonyms_to_delete.delete()

        for synonym in synonyms:
            if not existing_synonyms.filter(name=synonym["name"]).exists():
                self.add_synonym(instance, synonym)
            # si le type de synonyme à changé, il est mis à jour
            else:
                to_update = existing_synonyms.get(name=synonym["name"])
                to_update.synonym_type = synonym["synonym_type"]
                to_update.save()

        if max_quantities is not None:
            # cette condition est importante pour
            # * si max_quantities = None, rien n'est modifié sur les max_quantities
            # * si max_quantities = [], alors suppression
            # * sinon modification
            try:
                populations_to_keep = [q["population"] for q in max_quantities]
            except KeyError:
                raise ParseError(detail="Must provide 'population' to create new max_quantity")
            getattr(ingredient, self.max_quantities_set_field_name).exclude(
                population__in=populations_to_keep
            ).delete()

            for max_quantity in max_quantities:
                existing_q = getattr(ingredient, self.max_quantities_set_field_name).filter(
                    population=max_quantity["population"].id
                )
                if existing_q.exists():
                    existing_q = existing_q.first()
                    existing_q.max_quantity = max_quantity["max_quantity"]
                    existing_q.save()
                else:
                    self.add_max_quantity(ingredient, max_quantity)

        self.update_declaration_articles(instance, validated_data)
        return instance

    def add_max_quantity(self, ingredient, max_quantity):
        kwargs = {
            self.ingredient_name_field: ingredient,
        }
        try:
            self.max_quantities_model.objects.create(
                population=max_quantity["population"],
                max_quantity=max_quantity["max_quantity"],
                **kwargs,
            )
        except KeyError:
            raise ParseError(detail="Must provide 'population' and 'max_quantity' to create new max_quantities")

    def add_synonym(self, instance, synonym):
        try:
            name = synonym["name"]
            synonym_type = synonym["synonym_type"]
            if name and name != instance.name and not self.synonym_model.objects.filter(name=name).exists():
                self.synonym_model.objects.create(standard_name=instance, name=name, synonym_type=synonym_type)
        except KeyError:
            raise ParseError(detail="Must provide 'name' and 'synonym_type' to create new synonym")

    # inspiré par https://github.com/jazzband/django-simple-history/blob/626ece4082c4a7f87d14566e7a3c568043233ac5/simple_history/utils.py#L8
    def update_change_reason(self, instance, private_change_reason, public_change_reason):
        if len(private_change_reason) > 100:
            logger.warn(f"private_change_reason '{private_change_reason}' too long. Truncating to 100 characters.")
            private_change_reason = private_change_reason[:100]
        if len(public_change_reason) > 100:
            logger.warn(f"public_change_reason '{public_change_reason}' too long. Truncating to 100 characters.")
            public_change_reason = public_change_reason[:100]
        update_change_reason(instance, private_change_reason)
        record = instance.history.order_by("-history_date").first()
        record.history_public_change_reason = public_change_reason
        record.save()

    def update_declaration_articles(self, instance, validated_data):
        irrelevant_changes = [
            # synonyms, change_reason and public_change_reason ont été popped avant
            "public_comments",
            "private_comments",
            "novel_food",
            "to_be_entered_in_next_decree",
            "family",  # plante
            # substance
            "cas_number",
            "einec_number",
            "must_specify_quantity",
            # microorganism
            "genus",
            "species",
        ]
        if len(set(validated_data.keys()) - set(irrelevant_changes)) > 0:
            ids_using_ingredient = []
            for field_name in self.declaredingredient_set_field_names:
                ids_using_ingredient += getattr(instance, field_name).values_list("declaration_id", flat=True)
            tasks.recalculate_article_for_ongoing_declarations(
                Declaration.objects.filter(id__in=ids_using_ingredient),
                f"Article recalculé après modification via l'interface de {instance.object_type} id {instance.id} : {instance.name}",
            )


class CommonIngredientReadSerializer(HistoricalModelSerializer, PrivateFieldsSerializer):
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")

    history = HistoricalRecordField(read_only=True)

    private_fields = ("private_comments", "origin_declaration", "to_be_entered_in_next_decree")
