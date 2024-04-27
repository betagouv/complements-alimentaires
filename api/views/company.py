from enum import StrEnum, auto

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.choices import CountryChoices
from data.models import Company, Supervisor
from data.utils.external_utils import SiretData
from data.validators import validate_siret, validate_vat  # noqa

from ..exception_handling import ProjectAPIException
from ..permissions import IsSupervisorOfThisCompany
from ..serializers import CompanySerializer, StaffUserSerializer


class CountryListView(APIView):
    def get(self, request):
        countries = [{"value": country[0], "text": country[1]} for country in CountryChoices.choices]
        return Response(countries)


class CompanyStatusChoices(StrEnum):
    """4 cas sont possibles après vérification d'un numéro d'identification valide"""

    # Entreprise non enregistrée
    UNREGISTERED_COMPANY = auto()
    # Entreprise enregistrée et supervisée par l'utilisateur lui-même
    REGISTERED_AND_SUPERVISED_BY_ME = auto()
    # Entreprise enregistrée et supervisée par un autre gestionnaire que l'utilisateur
    REGISTERED_AND_SUPERVISED_BY_OTHER = auto()
    # Entreprise enregistrée mais non supervisée, sans gestionnaire (ex: suite à un import)
    REGISTERED_AND_UNSUPERVISED = auto()


def _get_identifier_type(request) -> str:
    """Helper pour récupérer le type de numéro d'identification (vat ou siret) depuis la requête."""

    identifier_type = request.query_params.get("identifierType", None)
    if identifier_type not in ["siret", "vat"]:
        raise ProjectAPIException(global_error="Le paramètre `identifierType` doit être `siret` ou `vat`")
    return identifier_type


class CheckCompanyIdentifierView(APIView):
    """Vérifie le numéro d'identification pour indiquer au front-end dans quel cas fonctionnel on se situe."""

    permission_classes = [IsAuthenticated]

    def get(self, request, identifier):
        identifier_type = _get_identifier_type(request)

        # Utilise les validateurs siret/vat pour réinjecter les potentielles erreurs
        # On n'utilise pas un model serializer car ça testerait d'autres contraintes (ex : unicité du champ)
        validation_fuction = globals()[f"validate_{identifier_type}"]
        try:
            validation_fuction(identifier)
        except DjangoValidationError as e:
            raise ProjectAPIException(field_errors={"identifier": e.messages})

        company, company_siret_data = None, None
        # Si le numéro d'identification est valide, alors on essaie de trouver l'entreprise liée
        try:
            company = Company.objects.get(**{identifier_type: identifier})
        except Company.DoesNotExist:
            company_status = CompanyStatusChoices.UNREGISTERED_COMPANY
            # Essaie de récupérer les données entreprise depuis l'API SIRET pour faciliser la saisie
            if identifier_type == "siret":
                company_siret_data = SiretData.fetch(identifier)  # None en cas d'échec du fetch
        else:
            if company.supervisors.exists():
                supervisor = request.user.role("supervisor")
                if supervisor and company in supervisor.companies.all():
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME
                else:
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER
            else:
                company_status = CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED

        return Response(
            {
                "company_status": company_status,  # pour déterminer les étapes suivantes côté front
                "company": (CompanySerializer(company).data if company else None),  # ex : pour set l'ID dans le state
                "company_siret_data": company_siret_data,
            }
        )


class ClaimCompanySupervisionView(APIView):
    """Envoi un e-mail aux administrateurs complalim pour revendiquer la gestion d'une entreprise existante, quand elle n'a aucun gestionnaire."""

    permission_classes = [IsAuthenticated]

    def get(self, request, identifier):
        company = get_object_or_404(Company, **{_get_identifier_type(request): identifier})
        if company.supervisors.exists():  # ne devrait pas arriver, sécurité supplémentaire
            raise ProjectAPIException(
                global_error="Cette entreprise a déjà un gestionnaire. Votre demande n'a pas été envoyée."
            )
        user = request.user
        send_mail(
            subject="Nouvelle demande d'accès à une entreprise (sans gestionnaire)",
            message=f"{user.name} (id: {user.id}) a demandé à devenir gestionnaire de l'entreprise {company.social_name} dont le N° de {_get_identifier_type(request)} est {identifier}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return Response({})


class ClaimCompanyCoSupervisionView(APIView):
    """Envoi un e-mail aux gestionnaires d'une entreprise pour demander à devenir co-gestionnaire."""

    permission_classes = [IsAuthenticated]

    def get(self, request, identifier):
        company = get_object_or_404(Company, **{_get_identifier_type(request): identifier})
        if not company.supervisors.exists():  # ne devrait pas arriver, sécurité supplémentaire
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
    """Création d'une entreprise, et attribution d'un rôle de gestionnaire à son créateur"""

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    @transaction.atomic
    def perform_create(self, serializer):
        new_company = serializer.save()
        supervisor, _ = Supervisor.objects.get_or_create(user=self.request.user)
        supervisor.companies.add(new_company)  # NOTE: on suppose que `new_company` n'est pas déjà dedans
        return new_company


class CompanyRetrieveView(RetrieveAPIView):
    """Récupération d'une entreprise dont l'utilisateur est gestionnaire"""

    queryset = Company.objects.all()
    permission_classes = [IsSupervisorOfThisCompany]
    serializer_class = CompanySerializer


class GetCompanyStaffView(APIView):
    """Récupération des utilisateurs ayant au moins un rôle dans cette entreprise"""

    def get(self, request, pk, *args, **kwargs):
        company = get_object_or_404(Company.objects.supervised_by(request.user), pk=pk)
        serializer = StaffUserSerializer(company.staff, many=True, context={"company_id": pk})
        return Response(serializer.data)
