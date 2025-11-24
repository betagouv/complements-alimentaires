import json
import logging
from collections import OrderedDict

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError

from api.exception_handling import ProjectAPIException
from api.serializers import SearchResultSerializer
from api.utils.search import search_elements

logger = logging.getLogger(__name__)


class PaginationExceded:
    global_error = "La limite de pagination excède {max_pagination_limit}"


class SearchView(APIView):
    serializer_class = SearchResultSerializer
    default_pagination_limit = 12
    max_pagination_limit = 48
    min_query_length = 3

    def post(self, request, *args, **kwargs):
        try:
            query = request.data.get("search")
        except AttributeError:
            raise ParseError("JSON objet attendu")
        if not query or len(query) < self.min_query_length:
            raise ProjectAPIException(
                global_error=f"Le terme de recherche doit être supérieur ou égal à {self.min_query_length} caractères"
            )

        try:
            limit = int(self.request.data.get("limit", 0))
        except (TypeError, ValueError):
            raise ParseError("Limit devrait être un chiffre entier")

        if limit > self.max_pagination_limit:
            raise ProjectAPIException(global_error=f"La limite de pagination excède {self.max_pagination_limit}")

        results = search_elements({"term": query}, deduplicate=True)
        paginated_results = self.paginate_results(results)
        serialized_data = self.serialize_results(paginated_results)
        return self.get_paginated_response(serialized_data)

    def serialize_results(self, results):
        serialized_results = self.serializer_class(results, many=True).data
        camelized = CamelCaseJSONRenderer().render(serialized_results)
        return json.loads(camelized.decode("utf-8"))

    def paginate_results(self, results, view=None):
        try:
            self.limit = int(self.request.data.get("limit", self.default_pagination_limit))
            self.offset = int(self.request.data.get("offset", 0))
        except (TypeError, ValueError):
            raise ParseError("Limit et offset devront être des chiffres entiers")

        self.count = len(results)
        if self.count == 0 or self.offset > self.count:
            return []

        # Disable Flake8 for next line because of this:
        # https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-760190686
        return results[self.offset : self.offset + self.limit]  # noqa: E203

    def get_paginated_response(self, data):
        return Response(OrderedDict([("count", self.count), ("results", data)]))
