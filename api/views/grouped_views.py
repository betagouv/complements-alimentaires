import json

from django.http import JsonResponse

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import status
from rest_framework.views import APIView

from api.views import (
    ConditionListView,
    EffectListView,
    GalenicFormulationListView,
    PlantPartListView,
    PopulationListView,
    PreparationListView,
    UnitListView,
)


class DeclarationFieldsGroupedView(APIView):
    """
    Cette view permet de grouper les éléments nécessaires pour afficher toutes les
    dépendances d'une déclaration. Elle existe pour éviter de faire plusieurs appels API
    pour les récuperer individuellement.
    """

    def get(self, request, *args, **kwargs):
        json_content = {
            "populations": PopulationListView.as_view()(request._request).data,
            "conditions": ConditionListView.as_view()(request._request).data,
            "effects": EffectListView.as_view()(request._request).data,
            "galenicFormulations": GalenicFormulationListView.as_view()(request._request).data,
            "preparations": PreparationListView.as_view()(request._request).data,
            "plantParts": PlantPartListView.as_view()(request._request).data,
            "units": UnitListView.as_view()(request._request).data,
        }
        payload = json.loads(CamelCaseJSONRenderer().render(json_content))
        return JsonResponse(payload, status=status.HTTP_200_OK)
