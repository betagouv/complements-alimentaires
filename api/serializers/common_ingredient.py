import copy
import logging
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ParseError
from simple_history.utils import update_change_reason

from api.utils.choice_field import GoodReprChoiceField
from data.models import Substance, IngredientStatus, Declaration

from .historical_record import HistoricalRecordField
from .utils import HistoricalModelSerializer, PrivateFieldsSerializer

from config import tasks

logger = logging.getLogger(__name__)

COMMON_NAME_FIELDS = ("name",)

COMMON_FIELDS = (
    "id",
    "synonyms",
    "public_comments",
    "private_comments",
    "status",
    "novel_food",
    "is_risky",
    "change_reason",
    "public_change_reason",
    "to_be_entered_in_next_decree",
)

COMMON_READ_ONLY_FIELDS = ("id",)

COMMON_FETCH_FIELDS = (
    "id",
    "name",
    "synonyms",
    "public_comments",
    "activity",
    "status",
    "novel_food",
    "is_risky",
    "history",
    "object_type",
    # Les suivants sont cachés si l'utilisateur.ice ne fait pas partie de l'administration
    "private_comments",
    "origin_declaration",
    "to_be_entered_in_next_decree",
)


class WithSubstances(serializers.ModelSerializer):
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all(), required=False)


class WithName(serializers.ModelSerializer):
    name = serializers.CharField(source="ca_name")


class CommonIngredientModificationSerializer(serializers.ModelSerializer):
    public_comments = serializers.CharField(source="ca_public_comments", required=False, allow_blank=True)
    private_comments = serializers.CharField(source="ca_private_comments", required=False, allow_blank=True)
    status = serializers.IntegerField(source="ca_status", required=False)
    change_reason = serializers.CharField(required=False, allow_blank=True)
    public_change_reason = serializers.CharField(required=False, allow_blank=True)
    to_be_entered_in_next_decree = serializers.BooleanField(source="ca_to_be_entered_in_next_decree", required=False)

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    @transaction.atomic
    def create(self, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        change_reason = validated_data.pop("change_reason", "Création via Compl'Alim")
        ingredient = super().create(validated_data)
        self.update_change_reason(ingredient, change_reason, "")

        for synonym in synonyms:
            self.add_synonym(ingredient, synonym)

        return ingredient

    @transaction.atomic
    def update(self, instance, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        change_reason = validated_data.pop("change_reason", "Modification via Compl'Alim")
        public_change_reason = validated_data.pop("public_change_reason", "")
        data_items = copy.deepcopy(validated_data).items()
        for key, value in data_items:
            if key.startswith("ca_"):
                siccrf_key = key.replace("ca_", "siccrf_")
                siccrf_value = getattr(instance, siccrf_key, None)
                ca_value = getattr(instance, key, None)
                if not value and value is not False and (siccrf_value or ca_value):
                    validated_data[siccrf_key] = value  # mettre comme None ou "" selon la requête
                    logger.info(
                        f"SICCRF champ supprimé : le champ '{siccrf_key}' a été supprimé sur l'ingrédient type '{instance.object_type}', id '{instance.id}'"
                    )
                elif value == siccrf_value and (ca_value is None or value == ca_value):
                    # si la valeur siccrf n'a pas été surpassée par une valeur CA, et la valeur donnée est la même que l'existante, pas besoin de la sauvegarder
                    validated_data.pop(key, None)

        super().update(instance, validated_data)
        self.update_change_reason(instance, change_reason, public_change_reason)

        try:
            new_synonym_list = [s["name"] for s in synonyms]
        except KeyError:
            raise ParseError(detail="Must provide 'name' to create new synonym")
        existing_synonyms = getattr(instance, self.synonym_set_field_name)

        # TODO: is it important to update, rather delete and recreate, 'new' synonyms ?
        synonyms_to_delete = existing_synonyms.exclude(name__in=new_synonym_list)
        synonyms_to_delete.delete()

        for synonym in synonyms:
            if not existing_synonyms.filter(name=synonym["name"]).exists():
                self.add_synonym(instance, synonym)

        self.update_declaration_articles(instance, validated_data)
        return instance

    def add_synonym(self, instance, synonym):
        try:
            name = synonym["name"]
            if name and name != instance.name and not self.synonym_model.objects.filter(name=name).exists():
                self.synonym_model.objects.create(standard_name=instance, name=name)
        except KeyError:
            raise ParseError(detail="Must provide 'name' to create new synonym")

    # inspiré par https://github.com/jazzband/django-simple-history/blob/626ece4082c4a7f87d14566e7a3c568043233ac5/simple_history/utils.py#L8
    def update_change_reason(self, instance, private_change_reason, public_change_reason):
        update_change_reason(instance, private_change_reason)
        record = instance.history.order_by("-history_date").first()
        record.history_public_change_reason = public_change_reason
        record.save()

    def update_declaration_articles(self, instance, validated_data):
        irrelevant_changes = [
            # synonyms, change_reason and public_change_reason ont été popped avant
            "ca_public_comments",
            "ca_private_comments",
            "novel_food",
            "ca_to_be_entered_in_next_decree",
            "ca_family",  # plante
            # substance
            "ca_cas_number",
            "ca_einec_number",
            "ca_must_specify_quantity",
            # microorganism
            "ca_genus",
            "ca_species",
        ]
        if len(set(validated_data.keys()) - set(irrelevant_changes)) > 0:
            ids_using_ingredient = []
            for field_name in self.declaredingredient_set_field_names:
                ids_using_ingredient += getattr(instance, field_name).values_list("declaration_id", flat=True)
            tasks.recalculate_article_for_ongoing_declarations(
                Declaration.objects.filter(id__in=ids_using_ingredient),
                f"Article recalculé après modification via l'interface de {instance.name} ({instance.object_type} id {instance.id})",
            )


class CommonIngredientReadSerializer(HistoricalModelSerializer, PrivateFieldsSerializer):
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

    private_fields = ("private_comments", "origin_declaration", "to_be_entered_in_next_decree")
