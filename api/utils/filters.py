import re

from django.db.models import Q

import django_filters
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camel_to_underscore, camelize_re, underscore_to_camel
from rest_framework.filters import BaseFilterBackend, OrderingFilter

from api.utils.simplified_status import SimplifiedStatusHelper
from data.choices import CountryChoices
from data.models import Declaration


class BaseNumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    Ce filtre permet d'effectuer des recherches par plusieurs chiffres avec la virgule comme
    séparateur. Pratique pour le filtrage d'IDs des modèles.

    Par exemple, dans un URL on pourrait avoir `company=12,13,14` pour filtrer des objets ayant
    comme entreprise une de ces trois (IDs 12, 13 ou 14).
    """

    pass


class CamelCaseOrderingFilter(OrderingFilter):
    """
    Allows filtering with camel case parameters. More info :
    https://github.com/vbabiy/djangorestframework-camel-case/issues/87
    """

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)

        if ordering is None:
            return None

        return [camel_to_underscore(field, **api_settings.JSON_UNDERSCOREIZE) for field in ordering]

    def get_valid_fields(self, queryset, view, context=None):
        if context is None:
            context = {}
        fields = super().get_valid_fields(queryset, view, context=context)

        return [(re.sub(camelize_re, underscore_to_camel, f[0]), f[1]) for f in fields]


class SimplifiedStatusFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        simplified_status = request.query_params.get("simplifiedStatus")
        if not simplified_status:
            return queryset

        status_values = simplified_status.split(",")
        conditions = SimplifiedStatusHelper.get_filter_conditions(status_values)
        return queryset.filter(conditions)


class DepartmentFilterBackend(BaseFilterBackend):
    """
    Ce filtre permet d'obtenir le département (ou l'étranger avec "99") à partir du
    code postale
    """

    def filter_queryset(self, request, queryset, view):
        departments = request.query_params.get("departments", None)
        if not departments:
            return queryset

        departments_list = [d.strip() for d in departments.split(",")]

        queries = Q()
        include_foreign_objects = "99" in departments_list

        # Héxagone
        mainland_deps = [d for d in departments_list if d != "99" and len(d) == 2 and d not in ["2A", "2B"]]
        if mainland_deps:
            queries |= Q(
                country=CountryChoices.FRANCE,
                postal_code__regex=r"^(?!97|98|20)(" + "|".join(mainland_deps) + r")\d{3}",
            )

        # La Corse (2A, 2B)
        corse_deps = [d for d in departments_list if d in ["2A", "2B"]]
        if corse_deps:
            corsica_queries = Q()
            if "2A" in corse_deps:
                corsica_queries |= Q(country=CountryChoices.FRANCE, postal_code__startswith="200") | Q(
                    country=CountryChoices.FRANCE, postal_code__startswith="201"
                )
            if "2B" in corse_deps:
                corsica_queries |= Q(country=CountryChoices.FRANCE, postal_code__startswith="202") | Q(
                    country=CountryChoices.FRANCE, postal_code__startswith="206"
                )
            queries |= corsica_queries

        # DOM-TOMs (97, 98)
        overseas_deps = [d for d in departments_list if len(d) == 3 and d.startswith(("97", "98"))]
        if overseas_deps:
            overseas_query = Q()
            for dep in overseas_deps:
                overseas_query |= Q(country=CountryChoices.FRANCE, postal_code__startswith=dep)
            queries |= overseas_query

        # Étranger (99)
        if include_foreign_objects:
            queries |= ~Q(country=CountryChoices.FRANCE)

        return queryset.filter(queries).distinct()


class SurveillanceOnlyFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        surveillance_only = request.query_params.get("surveillanceOnly", "")

        if surveillance_only == "true":
            surveillance_articles = [
                Declaration.Article.ARTICLE_15_WARNING,
                Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION,
                Declaration.Article.ARTICLE_16,
            ]
            return queryset.filter(article__in=surveillance_articles)

        return queryset
