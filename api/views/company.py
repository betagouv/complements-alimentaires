from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from data.choices import CountryChoices
from data.models import Company
from enum import StrEnum, auto
from ..serializers import CompanySerializer


class CountryListView(APIView):
    def get(self, request):
        countries = [{"value": country[0], "text": country[1]} for country in CountryChoices.choices]
        return Response(countries)


class CompanyStatusChoices(StrEnum):
    """4 cas sont possibles après vérification d'un SIRET valide"""

    # Entreprise non enregistrée
    UNREGISTERED_COMPANY = auto()
    # Entreprise enregistrée et supervisée par l'utilisateur lui-même
    REGISTERED_AND_SUPERVISED_BY_ME = auto()
    # Entreprise enregistrée et supervisée par un autre gestionnaire que l'utilisateur
    REGISTERED_AND_SUPERVISED_BY_OTHER = auto()
    # Entreprise enregistrée mais non supervisée, sans gestionnaire (ex: suite à un import)
    REGISTERED_AND_UNSUPERVISED = auto()


class CheckSiretView(APIView):
    """
    Vérifie le SIRET pour indiquer au front-end dans quel cas fonctionnel on se situe.
    NOTE: cette méthode ne vérifie volontairement pas la validité du SIRET, car cette étape sera déléguée à l'API externe
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, siret):
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


class CompanyCreateView(CreateAPIView):
    """Création d'une entreprise"""

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
