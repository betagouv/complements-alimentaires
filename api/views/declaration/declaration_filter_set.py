import logging
import re
from datetime import datetime, time

from django.db.models import F, Func, Q
from django.db.models.functions import Lower
from django.utils import timezone

from django_filters import rest_framework as django_filters
from unidecode import unidecode

from api.exceptions import ProjectAPIException
from api.utils.filters import BaseNumberInFilter
from data.models import Condition, Declaration, Ingredient, Population, Snapshot, SubstanceUnit

logger = logging.getLogger(__name__)


class Unaccent(Func):
    function = "unaccent"


class DeclarationFilterSet(django_filters.FilterSet):
    author = BaseNumberInFilter(field_name="author__id")
    instructor = django_filters.CharFilter(method="nullable_instructor")
    visor = django_filters.CharFilter(method="nullable_visor")
    galenic_formulation = BaseNumberInFilter(field_name="galenic_formulation__id")
    population = django_filters.ModelMultipleChoiceFilter(
        field_name="populations__id", to_field_name="id", queryset=Population.objects.all()
    )
    condition = django_filters.ModelMultipleChoiceFilter(
        field_name="conditions_not_recommended__id", to_field_name="id", queryset=Condition.objects.all()
    )
    country = django_filters.CharFilter(field_name="company__country")
    company = BaseNumberInFilter(field_name="company__id")
    company_name_start = django_filters.CharFilter(method="company_name_start__gte")
    company_name_end = django_filters.CharFilter(method="company_name_end__lte")
    status = django_filters.CharFilter(method="status__in")
    plants = django_filters.CharFilter(method="plants__and")
    microorganisms = django_filters.CharFilter(method="microorganisms__and")
    substances = django_filters.CharFilter(method="substances__and")
    ingredients = django_filters.CharFilter(method="ingredients__and")
    dose = django_filters.CharFilter(method="filter_by_dose")
    submission_date_after = django_filters.CharFilter(method="filter_submission_date_after")
    submission_date_before = django_filters.CharFilter(method="filter_submission_date_before")
    decision_date_after = django_filters.CharFilter(method="filter_decision_date_after")
    decision_date_before = django_filters.CharFilter(method="filter_decision_date_before")

    # Une fois https://github.com/carltongibson/django-filter/issues/1673 on peut
    # enlever cette ligne
    article = django_filters.CharFilter()

    class Meta:
        model = Declaration
        fields = [
            "company",
            "status",
            "author",
            "instructor",
            "visor",
            "galenic_formulation",
            "population",
            "condition",
            "company_name_start",
            "company_name_end",
            "article",
            "dose",
            "submission_date_after",
            "submission_date_before",
            "decision_date_after",
            "decision_date_before",
        ]

    def nullable_instructor(self, queryset, value, *args, **kwargs):
        empty_term = "None"
        filter_values = args[0].split(",")

        if not filter_values:
            return queryset

        try:
            declaration_ids = [int(x.strip()) for x in filter_values if x != empty_term]
        except Exception as _:
            raise ProjectAPIException(global_error="Vérifier votre filtre instructeur")

        include_unassigned = empty_term in filter_values
        if include_unassigned:
            return queryset.filter(Q(instructor__isnull=True) | Q(instructor__id__in=declaration_ids))
        else:
            return queryset.filter(instructor__id__in=declaration_ids)

    def nullable_visor(self, queryset, value, *args, **kwargs):
        empty_term = "None"
        filter_values = args[0].split(",")

        if not filter_values:
            return queryset

        unassigned_declarations = (
            queryset.filter(visor__isnull=True) if empty_term in filter_values else Declaration.objects.none()
        )

        try:
            declaration_ids = [int(x.strip()) for x in filter_values if x != empty_term]
        except Exception as _:
            raise ProjectAPIException(global_error="Vérifier votre filtre viseur")
        filtered_declarations = (
            queryset.filter(visor__id__in=declaration_ids) if declaration_ids else Declaration.objects.none()
        )

        return unassigned_declarations.union(filtered_declarations)

    def company_name_start__gte(self, queryset, value, *args, **kwargs):
        return self._annotate_queryset(queryset).filter(name_unaccented_lower__gte=args[0].lower())

    def company_name_end__lte(self, queryset, value, *args, **kwargs):
        # Afin d'inclure les compagnies avec la lettre chosie on doit prendre la lettre de l'alphabet
        # s'après. Par exemple, un filtre avec company_name_end "U" doit contenir "Umbrella corporation".
        # "Cz" doit inclure "Czech industries"

        normalized_input = unidecode(args[0].lower())
        # Si le premier char est "z" on peut considérer qu'on n'a pas de end-filter
        if normalized_input[0] == "z":
            return self._annotate_queryset(queryset)

        # Si le dernier char est "z" on peut l'ignorer et faire monter l'avant-dernier
        if normalized_input[-1] == "z":
            normalized_input = normalized_input[slice(-1)]
        last_char = normalized_input[-1]
        letter_order = "abcdefghijklmnopqrstuvwxyz"
        if last_char in letter_order:
            normalized_input = normalized_input[slice(-1)] + letter_order[letter_order.index(last_char) + 1]
        return self._annotate_queryset(queryset).filter(name_unaccented_lower__lt=normalized_input)

    def _annotate_queryset(self, queryset):
        return queryset.annotate(name_unaccented_lower=Lower(Unaccent(F("company__social_name"))))

    def status__in(self, queryset, value, *args, **kwargs):
        return queryset.filter(status__in=args[0].split(","))

    def plants__and(self, queryset, name, value, *args, **kwargs):
        for id in value.split(","):
            queryset = queryset.filter(declared_plants__plant__id=id)
        return queryset

    def microorganisms__and(self, queryset, name, value, *args, **kwargs):
        for id in value.split(","):
            queryset = queryset.filter(declared_microorganisms__microorganism__id=id)
        return queryset

    def substances__and(self, queryset, name, value, *args, **kwargs):
        for id in value.split(","):
            queryset = queryset.filter(computed_substances__substance__id=id)
        return queryset

    def ingredients__and(self, queryset, name, value, *args, **kwargs):
        for id in value.split(","):
            queryset = queryset.filter(declared_ingredients__ingredient__id=id)
        return queryset

    # Filtre par dose

    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = "≥"
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "≤"
    EQUAL = "="
    BETWEEN = "≬"

    def filter_by_dose(self, queryset, name, value):
        dose_filters = self.data.getlist("dose")

        if not dose_filters:
            return queryset.none()

        for dose_string in dose_filters:
            queryset = self._apply_single_dose_filter(queryset, dose_string)

        return queryset

    def _apply_single_dose_filter(self, queryset, value):
        if not value:
            return queryset.none()
        try:
            parts = re.split(r"\|\|", value)
            if len(parts) < 5:
                logger.error(f"Declaration filter by dose error : {value} not splittable by > 5 parts")
                return queryset.none()

            element_type = parts[0]  # plant, substance, microorganism, ingredient
            if element_type != "microorganism" and len(parts) < 6:
                logger.error(
                    f"Declaration filter by dose error : {value} for type {element_type} not splittable by 6 parts"
                )
                return queryset.none()

            element_id = parts[2].split("|")[0] if "|" in parts[2] else parts[2]
            operation = parts[3]
            quantity_parts = parts[4].split("|")
            unit_id = parts[5] if len(parts) > 5 else None
            quantity = float(quantity_parts[0])

            if operation == self.BETWEEN:
                if len(quantity_parts) < 2:
                    logger.error(
                        f"Declaration filter by dose error : {value} for BETWEEN operation doesn't have two quantities : {parts[4]}"
                    )
                    return queryset.none()

            quantity_max = float(quantity_parts[1]) if operation == self.BETWEEN else None

            # Prendre l'unité si elle est spécifiée (pour les microorganismes ce n'est pas le cas)
            unit = SubstanceUnit.objects.get(pk=unit_id) if unit_id else None

            # Faire le filtre basé sur le type d'ingrédient
            if element_type == "plant":
                plant_part_id = parts[2].split("|")[1] if "|" in parts[2] and len(parts[2].split("|")) > 1 else None
                return self.filter_plant_dose(
                    queryset, element_id, plant_part_id, operation, quantity, quantity_max, unit
                )
            elif element_type == "substance":
                return self.filter_substance_dose(queryset, element_id, operation, quantity, quantity_max, unit)
            elif element_type in ["form_of_supply", "active_ingredient"]:
                ingredient = Ingredient.objects.get(pk=element_id)
                if ingredient.substances.count():
                    return self.filter_active_ingredient_dose(
                        queryset, ingredient, operation, quantity, quantity_max, unit
                    )
                else:
                    return self.filter_ingredient_dose(queryset, element_id, operation, quantity, quantity_max, unit)
            elif element_type == "microorganism":
                return self.filter_microorganism_dose(queryset, element_id, operation, quantity, quantity_max)
            elif element_type in ["ingredient", "aroma", "additive", "non_active_ingredient"]:
                return self.filter_ingredient_dose(queryset, element_id, operation, quantity, quantity_max, unit)
            logger.error(
                f"Declaration filter by dose error : {element_type} not supported (needs plant, substance, microorganism or ingredient)"
            )
            return queryset.none()
        except (ValueError, IndexError, SubstanceUnit.DoesNotExist, Ingredient.DoesNotExist) as e:
            logger.exception(e)
            return queryset.none()

    def filter_plant_dose(self, queryset, plant_id, plant_part_id, operation, quantity, quantity_max=None, unit=None):
        filters = Q(declared_plants__plant_id=plant_id)
        if plant_part_id and plant_part_id != "-":
            filters &= Q(declared_plants__used_part_id=plant_part_id)
        return self._apply_quantity_filter(
            queryset, filters, operation, quantity, quantity_max, "declared_plants__", unit
        )

    def filter_substance_dose(self, queryset, substance_id, operation, quantity, quantity_max=None, unit=None):
        filters = Q(computed_substances__substance_id=substance_id)
        return self._apply_quantity_filter(
            queryset, filters, operation, quantity, quantity_max, "computed_substances__", unit
        )

    def filter_active_ingredient_dose(self, queryset, ingredient, operation, quantity, quantity_max=None, unit=None):
        filters = Q(computed_substances__substance__in=ingredient.substances.all())
        filters &= Q(declared_ingredients__ingredient_id=ingredient.id)
        return self._apply_quantity_filter(
            queryset, filters, operation, quantity, quantity_max, "computed_substances__", unit
        )

    def filter_microorganism_dose(self, queryset, microorganism_id, operation, quantity, quantity_max=None):
        filters = Q(declared_microorganisms__microorganism_id=microorganism_id)
        return self._apply_quantity_filter(
            queryset, filters, operation, quantity, quantity_max, "declared_microorganisms__"
        )

    def filter_ingredient_dose(self, queryset, ingredient_id, operation, quantity, quantity_max=None, unit=None):
        filters = Q(declared_ingredients__ingredient_id=ingredient_id)
        return self._apply_quantity_filter(
            queryset, filters, operation, quantity, quantity_max, "declared_ingredients__", unit
        )

    def _apply_quantity_filter(
        self, queryset, other_filters, operation, quantity, quantity_max=None, relation_field="", unit=None
    ):
        quantity_filter = self._get_quantity_filter(
            operation=operation, quantity=quantity, quantity_max=quantity_max, relation_field=relation_field, unit=unit
        )
        return queryset.filter(other_filters & quantity_filter).distinct()

    def _get_quantity_filter(self, operation, quantity, quantity_max=None, relation_field="", unit=None):
        """
        Aide pour obtenir la requête necessaire pour la quantité. Traite les conversions automatiquement.
        """

        # Une même combinaison unité + quantité (par exemple, 200 g) peut avoir des équivalences dans
        # d'autres unités (par exemple 0.2 kg, 200000 mg, etc).
        equivalent_measures = self._get_equivalent_measures(unit, quantity, quantity_max)

        sql_modifiers = {
            self.GREATER_THAN: "__gt",
            self.GREATER_THAN_OR_EQUAL: "__gte",
            self.LESS_THAN: "__lt",
            self.LESS_THAN_OR_EQUAL: "__lte",
            self.EQUAL: "",
        }

        filters = []

        if operation == self.BETWEEN:
            filters = [
                Q(**{f"{relation_field}quantity__gte": eq_quantity})
                & Q(**{f"{relation_field}quantity__lte": eq_max_quantity})
                & Q(**{f"{relation_field}unit": eq_unit} if eq_unit else {})
                for (eq_unit, eq_quantity, eq_max_quantity) in equivalent_measures
            ]
        else:
            filters = [
                Q(**{f"{relation_field}quantity{sql_modifiers[operation]}": eq_quantity})
                & Q(**{f"{relation_field}unit": eq_unit} if eq_unit else {})
                for (eq_unit, eq_quantity, _) in equivalent_measures
            ]

        query = Q()
        for filter in filters:
            query |= filter
        return query

    # Les conversions d'unité se passent ici :

    BASE_WEIGHT_UNIT = "g"
    WEIGHT_UNITS = {
        "µg": 0.000001,  # 1 microgram = 0.000001 g
        "mg": 0.001,  # 1 milligram = 0.001 g
        "g": 1.0,  # Unité de base (gram)
    }

    # NOTE: Pour l'instant on a seulement ml comme unité de volume en prod. Si on en ajoute d'autres,
    # il faudra les décommenter dans le dictionnaire ci-dessous.
    BASE_VOLUME_UNIT = "l"
    VOLUME_UNITS = {
        # "ml": 0.001,  # 1 milliliter = 0.001 l
        # "cl": 0.01,  # 1 centiliter = 0.01 l
        # "l": 1.0,  # Unité de base (liter)
    }

    def _get_equivalent_measures(self, unit, quantity, quantity_max=None):
        """
        Cette fonction permet d'obtenir des mesures avec le même valeur, par exemple, pour 200 g sont
        la même chose que 200g, 200000mg et 0.2kg.
        Cette opération nous permet après de créer des querysets pour la même dose même si les objets
        utilisent des unités différentes.
        """
        if not unit or (unit.name not in self.WEIGHT_UNITS and unit not in self.VOLUME_UNITS):
            return [(unit, quantity, quantity_max)]

        unit_dict = self.WEIGHT_UNITS if unit.name in self.WEIGHT_UNITS else self.VOLUME_UNITS

        base_quantity = unit_dict[unit.name] * quantity
        base_quantity_max = unit_dict[unit.name] * quantity_max if quantity_max else None
        equivalences = []

        for unit_name, multiplier in unit_dict.items():
            try:
                equivalences.append(
                    (
                        SubstanceUnit.objects.get(name=unit_name),
                        base_quantity / multiplier,
                        (base_quantity_max / multiplier if base_quantity_max else None),
                    )
                )
            except SubstanceUnit.DoesNotExist:
                continue

        return equivalences

    # Les filtres pour les dates se passent ici.
    # À noter que si le filtre est trop lent (ou beaucoup utilisé) l'ajout de ces indexes pourrait
    # accélerer les choses :
    # class Meta:
    # indexes = [
    #     models.Index(fields=['action', 'creation_date']),
    #     models.Index(fields=['status', 'creation_date']),
    # ]

    def _parse_date(self, date_str, end_of_day):
        """Helper to parse dd-mm-yyyy dates into timezone-aware datetimes"""
        try:
            naive_date = datetime.strptime(date_str, "%Y-%m-%d")
            time_to_use = time.max if end_of_day else time.min
            naive_datetime = datetime.combine(naive_date, time_to_use)
            return timezone.make_aware(naive_datetime)
        except (ValueError, TypeError):
            logger.exception(f"Unable to convert to date object: {date_str}")
            return None

    def filter_submission_date_after(self, queryset, name, value):
        filters = Q(snapshots__action=Snapshot.SnapshotActions.SUBMIT)
        return self.filter_date(queryset, value, filters, False, "snapshots__creation_date__gte")

    def filter_submission_date_before(self, queryset, name, value):
        filters = Q(snapshots__action=Snapshot.SnapshotActions.SUBMIT)
        return self.filter_date(queryset, value, filters, True, "snapshots__creation_date__lte")

    def filter_decision_date_after(self, queryset, name, value):
        filters = Q(
            snapshots__status__in=[Declaration.DeclarationStatus.AUTHORIZED, Declaration.DeclarationStatus.REJECTED],
        )
        return self.filter_date(queryset, value, filters, False, "snapshots__creation_date__gte")

    def filter_decision_date_before(self, queryset, name, value):
        filters = Q(
            snapshots__status__in=[Declaration.DeclarationStatus.AUTHORIZED, Declaration.DeclarationStatus.REJECTED],
        )
        return self.filter_date(queryset, value, filters, True, "snapshots__creation_date__lte")

    def filter_date(self, queryset, value, other_filters, end_of_day, date_lookup_parameter):
        date = self._parse_date(value, end_of_day)
        if not date:
            return queryset.none()

        final_filters = other_filters or Q()
        final_filters &= Q(**{f"{date_lookup_parameter}": date})
        return queryset.filter(final_filters)
