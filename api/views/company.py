from rest_framework.response import Response
from rest_framework.views import APIView
from data.choices import CountryChoices


class CountryListView(APIView):
    def get(self, request):
        countries = [{"value": country[0], "text": country[1]} for country in CountryChoices.choices]
        return Response(countries)
