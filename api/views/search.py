import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import OrderedDict
from django.core.exceptions import BadRequest
from api.serializers import SearchResultSerializer
from data.models import Plant, Microorganism, Ingredient, Substance
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

logger = logging.getLogger(__name__)


class SearchView(APIView):
    serializer_class = SearchResultSerializer
    default_limit = 12
    search_rank_threshold = 0.1

    def post(self, request, *args, **kwargs):
        search_term = request.data.get("search")
        if not search_term or len(search_term) < 3:
            raise BadRequest()

        results = self.get_sorted_objects(search_term)
        serialized_data = self.serialize_results(results)
        paginated_results = self.paginate_results(serialized_data)
        return self.get_paginated_response(paginated_results)

    def get_sorted_objects(self, search_term):
        query = SearchQuery(search_term)

        plants = self.get_plants(query)
        microorganisms = self.get_microorganisms(query)
        ingredients = self.get_ingredients(query)
        substances = self.get_substances(query)

        results = plants + microorganisms + ingredients + substances
        results.sort(key=lambda x: x.rank, reverse=True)
        return results

    def get_plants(self, query):
        vector = SearchVector("name", weight="A") + SearchVector("name_en", weight="B")
        plants = Plant.objects.annotate(rank=SearchRank(vector, query))
        return list(plants.filter(rank__gte=self.search_rank_threshold).all())

    def get_microorganisms(self, query):
        vector = SearchVector("name", weight="A") + SearchVector("name_en", weight="B")
        microorganisms = Microorganism.objects.annotate(rank=SearchRank(vector, query))
        return list(microorganisms.filter(rank__gte=self.search_rank_threshold).all())

    def get_ingredients(self, query):
        vector = (
            SearchVector("name", weight="A")
            + SearchVector("name_en", weight="B")
            + SearchVector("description", weight="C")
        )
        ingredients = Ingredient.objects.annotate(rank=SearchRank(vector, query))
        return list(ingredients.filter(rank__gte=self.search_rank_threshold).all())

    def get_substances(self, query):
        vector = (
            SearchVector("cas_number", weight="A")
            + SearchVector("name", weight="A")
            + SearchVector("name_en", weight="B")
        )
        substance = Substance.objects.annotate(rank=SearchRank(vector, query))
        return list(substance.filter(rank__gte=self.search_rank_threshold).all())

    def serialize_results(self, results):
        serialized_results = self.serializer_class(results, many=True).data
        camelized = CamelCaseJSONRenderer().render(serialized_results)
        return json.loads(camelized.decode("utf-8"))

    def paginate_results(self, results, view=None):
        self.limit = self.request.data.get("limit") or self.default_limit
        self.count = len(results)
        self.offset = self.request.data.get("offset") or 0

        if self.count == 0 or self.offset > self.count:
            return []

        # Disable Flake8 for next line because of this:
        # https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-760190686
        return results[self.offset : self.offset + self.limit]  # noqa: E203

    def get_paginated_response(self, data):
        return Response(OrderedDict([("count", self.count), ("results", data)]))
