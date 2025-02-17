import json
import logging

from django.http import JsonResponse

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.views import APIView

from api.exception_handling import ProjectAPIException
from api.serializers import AutocompleteItemSerializer
from api.utils.search import search_elements

logger = logging.getLogger(__name__)


class AutocompleteView(APIView):
    serializer_class = AutocompleteItemSerializer
    min_query_length = 3
    max_autocomplete_items = 20

    def post(self, request, *args, **kwargs):
        term = request.data.get("term")
        if not term or len(term) < self.min_query_length:
            raise ProjectAPIException(
                global_error=f"Le terme de recherche doit être supérieur ou égal à {self.min_query_length} caractères"
            )

        query = {"term": term, "type": request.data.get("type")}
        results = search_elements(
            query, deduplicate=False, exclude_not_authorized=True, exclude_vitamines_minerals=True
        )[: self.max_autocomplete_items]
        return JsonResponse(self.serialize_results(results), safe=False)

    def serialize_results(self, results):
        serialized_results = self.serializer_class(results, many=True).data
        camelized = CamelCaseJSONRenderer().render(serialized_results)
        return json.loads(camelized.decode("utf-8"))
