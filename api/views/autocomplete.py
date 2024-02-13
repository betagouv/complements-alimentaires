import logging
import json
from difflib import SequenceMatcher
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from django.db.models import Q, F
from api.serializers import AutocompleteItemSerializer
from data.models import Plant, Microorganism, Ingredient, Substance
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

logger = logging.getLogger(__name__)


class AutocompleteView(APIView):
    serializer_class = AutocompleteItemSerializer
    min_query_length = 3

    def post(self, request, *args, **kwargs):
        query = request.data.get("term")
        if not query or len(query) < self.min_query_length:
            raise BadRequest(f"Le terme de recherche doit être supérieur ou égal à {self.min_query_length} caractères")

        results = self.get_sorted_objects(query)
        return JsonResponse(self.serialize_results(results), safe=False)

    def get_sorted_objects(self, query):
        plants = self.get_plants(query)
        microorganisms = self.get_microorganisms(query)
        ingredients = self.get_ingredients(query)
        substances = self.get_substances(query)

        results = plants + microorganisms + ingredients + substances

        # Triage par proximité au term original
        # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
        results.sort(key=lambda x: SequenceMatcher(None, x.autocomplete_match, query).ratio(), reverse=True)

        return results

    def get_plants(self, query):
        # TODO : add unaccent add-on : https://stackoverflow.com/questions/54071944/fielderror-unsupported-lookup-unaccent-for-charfield-or-join-on-the-field-not
        plant_qs = Plant.objects.filter(Q(name__icontains=query)).annotate(autocomplete_match=F("name"))
        plant_synonym_qs = Plant.objects.filter(plantsynonym__name__icontains=query).annotate(
            autocomplete_match=F("plantsynonym__name")
        )

        return list(plant_qs.union(plant_synonym_qs))

    def get_microorganisms(self, query):
        microorganism_qs = Microorganism.objects.filter(Q(name__icontains=query)).annotate(
            autocomplete_match=F("name")
        )
        microorganism_synonym_qs = Microorganism.objects.filter(microorganismsynonym__name__icontains=query).annotate(
            autocomplete_match=F("microorganismsynonym__name")
        )

        return list(microorganism_qs.union(microorganism_synonym_qs))

    def get_ingredients(self, query):
        ingredient_qs = Ingredient.objects.filter(Q(name__icontains=query)).annotate(autocomplete_match=F("name"))
        ingredient_synonym_qs = Ingredient.objects.filter(ingredientsynonym__name__icontains=query).annotate(
            autocomplete_match=F("ingredientsynonym__name")
        )

        return list(ingredient_qs.union(ingredient_synonym_qs))

    def get_substances(self, query):
        substance_qs = Substance.objects.filter(Q(name__icontains=query)).annotate(autocomplete_match=F("name"))
        substance_synonym_qs = Substance.objects.filter(substancesynonym__name__icontains=query).annotate(
            autocomplete_match=F("substancesynonym__name")
        )

        return list(substance_qs.union(substance_synonym_qs))

    def serialize_results(self, results):
        serialized_results = self.serializer_class(results, many=True).data
        camelized = CamelCaseJSONRenderer().render(serialized_results)
        return json.loads(camelized.decode("utf-8"))
