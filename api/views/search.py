import logging
import json
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import SearchResultSerializer
from data.models import Plant, Microorganism, Ingredient, Substance
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import JsonResponse
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

logger = logging.getLogger(__name__)


class SearchView(APIView):
    serializer_class = SearchResultSerializer

    def post(self, request, *args, **kwargs):
        search_term = request.data.get("search")
        # If no search term return Bad Request
        results = self.get_sorted_objects(search_term)
        serialized_data = self.serialize_results(results)
        return JsonResponse(serialized_data, safe=False, status=status.HTTP_200_OK)

    def get_sorted_objects(self, search_term):
        query = SearchQuery(search_term)
        min_rank = 0.2
        plant_vector = SearchVector("name", weight="A") + SearchVector("name_en", weight="B")
        microorganism_vector = SearchVector("name", weight="A") + SearchVector("name_en", weight="B")
        ingredient_vector = (
            SearchVector("name", weight="A")
            + SearchVector("name_en", weight="B")
            + SearchVector("description", weight="C")
        )
        substance_vector = (
            SearchVector("cas_number", weight="A")
            + SearchVector("name", weight="A")
            + SearchVector("name_en", weight="B")
        )

        plants = Plant.objects.annotate(rank=SearchRank(plant_vector, query)).filter(rank__gte=min_rank).all()
        microorganisms = (
            Microorganism.objects.annotate(rank=SearchRank(microorganism_vector, query))
            .filter(rank__gte=min_rank)
            .all()
        )
        ingredients = (
            Ingredient.objects.annotate(rank=SearchRank(ingredient_vector, query)).filter(rank__gte=min_rank).all()
        )
        substance = (
            Substance.objects.annotate(rank=SearchRank(substance_vector, query)).filter(rank__gte=min_rank).all()
        )

        results = list(plants) + list(microorganisms) + list(ingredients) + list(substance)

        def sortKey(val):
            return val.rank

        results.sort(key=sortKey)
        return results

    def serialize_results(self, results):
        serialized_results = self.serializer_class(results, many=True).data
        camelized = CamelCaseJSONRenderer().render(serialized_results)
        return json.loads(camelized.decode("utf-8"))
