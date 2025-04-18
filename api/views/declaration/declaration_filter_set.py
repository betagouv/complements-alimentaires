import logging

from django.db.models import F, Func, Q
from django.db.models.functions import Lower

from django_filters import rest_framework as django_filters
from unidecode import unidecode

from api.exceptions import ProjectAPIException
from api.utils.filters import BaseNumberInFilter
from data.models import Condition, Declaration, Population

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
