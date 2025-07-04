import re

import django_filters
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camel_to_underscore, camelize_re, underscore_to_camel
from rest_framework.filters import BaseFilterBackend, OrderingFilter

from api.utils.simplified_status import SimplifiedStatusHelper


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
