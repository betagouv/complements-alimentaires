from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from data.choices import CountryChoices
from data.models import Company
from enum import StrEnum, auto
from django.shortcuts import get_object_or_404
from ..serializers import CompanySerializer
from api.exception_handling import ProjectAPIException
from django.core.mail import send_mail
from django.conf import settings


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
            social_name = None
        else:
            if company.supervisors.exists():
                supervisor = request.user.role("companysupervisor")
                if supervisor and company in supervisor.companies.all():
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME
                else:
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER
            else:
                company_status = CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED
            social_name = company.social_name

        return Response({"company_status": company_status, "social_name": social_name})


class ClaimCompanySupervisionView(APIView):
    """Envoi un e-mail aux administrateurs complalim pour revendiquer la gestion d'une entreprise existante, quand elle n'a aucun gestionnaire."""

    permission_classes = [IsAuthenticated]

    def get(self, request, siret):
        company = get_object_or_404(Company, siret=siret)
        if company.supervisors.exists():
            # ne devrait pas arriver, sécurité supplémentaire
            raise ProjectAPIException(
                global_error="Cette entreprise a déjà un gestionnaire. Votre demande n'a pas été envoyée."
            )
        user = request.user
        send_mail(
            subject="Nouvelle demande d'accès à une entreprise (sans gestionnaire)",
            message=f"{user.name} (id: {user.id}) a demandé à devenir gestionnaire de l'entreprise {company.social_name} dont le siret est {siret}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return Response({})


class RequestCompanyAccessView(APIView):
    """Envoi un e-mail aux gestionnaires d'une entreprise pour demander à devenir co-gestionnaire."""

    permission_classes = [IsAuthenticated]

    def get(self, request, siret):
        company = get_object_or_404(Company, siret=siret)
        if not company.supervisors.exists():
            # ne devrait pas arriver, sécurité supplémentaire
            raise ProjectAPIException(
                global_error="Cette entreprise n'a pas de gestionnaire. Votre demande n'a pas été envoyée."
            )
        user = request.user
        send_mail(
            subject=f"{user.name} souhaite devenir gestionnaire Compl'Alim de {company.social_name}",
            message=f"{user.name} a demandé à devenir co-gestionnaire de l'entreprise {company.social_name}. Veuillez vous rendre sur la plateforme pour accéder ou refuser cette demande.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=company.supervisors.values_list("user__email"),
        )
        return Response({})


class CompanyCreateView(CreateAPIView):
    """Création d'une entreprise"""

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
