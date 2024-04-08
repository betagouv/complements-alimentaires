from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from data.choices import CountryChoices
from data.models import Company
from django.db import models


class CountryListView(APIView):
    def get(self, request):
        countries = [{"value": country[0], "text": country[1]} for country in CountryChoices.choices]
        return Response(countries)


class CompanyStatusChoices(models.TextChoices):
    # 4 cas sont possibles après vérification d'un SIRET valide :
    UNREGISTERED_COMPANY = "Entreprise non enregistrée"
    REGISTERED_AND_SUPERVISED_BY_ME = "Entreprise enregistrée et supervisée par moi-même"
    REGISTERED_AND_SUPERVISED_BY_OTHER = "Entreprise enregistrée et supervisée par quelqu'un d'autre"
    REGISTERED_AND_UNSUPERVISED = "Entreprise enregistrée mais non supervisée"  # ex : suite à un import


class CheckSiretView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, siret):
        """NOTE: cette méthode ne vérifie volontairement pas la validité du SIRET, car cette étape sera déléguée à l'API externe"""
        try:
            company = Company.objects.get(siret=siret)
        except Company.DoesNotExist:
            company_status = CompanyStatusChoices.UNREGISTERED_COMPANY
        else:
            if company.supervisors.exists():
                supervisor = request.user.role("companysupervisor")
                if supervisor and company in supervisor.companies.all():
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME
                else:
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER
            else:
                company_status = CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED

        return Response({"company_status": company_status})
