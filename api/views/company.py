import logging
from enum import StrEnum, auto

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from django_filters import rest_framework as django_filters
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils.filters import CamelCaseOrderingFilter, DepartmentFilterBackend
from api.utils.search import UnaccentSearchFilter
from api.utils.urls import get_base_url
from config import email
from data.choices import CountryChoices
from data.models import Company, DeclarantRole, SupervisorRole
from data.models.solicitation import CompanyAccessClaim, SupervisionClaim
from data.utils.external_utils import SiretData
from data.validators import validate_siret, validate_vat  # noqa

from ..exception_handling import ProjectAPIException
from ..permissions import IsController, IsSupervisor, IsSupervisorOrAgent
from ..serializers import (
    CollaboratorSerializer,
    CompanyControllerSerializer,
    CompanySerializer,
    ControllerCompanySerializer,
    MinimalCompanySerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


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
    """Helper pour récupérer le type de numéro d'identification (tva ou siret) depuis la requête."""

    identifier_type = request.query_params.get("identifierType", None)
    if identifier_type not in ["siret", "vat"]:
        raise ProjectAPIException(global_error="Le paramètre `identifierType` doit être `siret` ou `tva`")
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
                if company.supervisors.filter(id=request.user.id).exists():
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME
                else:
                    company_status = CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER
            else:
                company_status = CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED

        return Response(
            {
                "company_status": company_status,  # pour déterminer les étapes suivantes côté front
                "company": (MinimalCompanySerializer(company).data if company else None),
                "company_siret_data": company_siret_data,
            }
        )


class ClaimCompanySupervisionView(APIView):
    """Envoi une solicitation au staff complalim pour revendiquer la gestion d'une entreprise existante, quand elle n'a aucun gestionnaire."""

    permission_classes = [IsAuthenticated]

    def post(self, request, identifier):
        company = get_object_or_404(Company, **{_get_identifier_type(request): identifier})
        if company.supervisors.exists():  # ne devrait pas arriver, sécurité supplémentaire
            raise ProjectAPIException(
                global_error="Cette entreprise a déjà un gestionnaire. Votre demande n'a pas été envoyée."
            )
        SupervisionClaim.objects.create(
            sender=request.user,
            company=company,
            personal_msg=request.data.get("message"),
        )
        return Response({})


class ClaimCompanyAccessView(APIView):
    """Envoi une solicitation aux gestionnaires d'une entreprise pour demander en avoir accès."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        if not company.supervisors.exists():
            raise ProjectAPIException(
                global_error="Cette entreprise n'a pas de gestionnaire. Votre demande n'a pas été envoyée."
            )
        CompanyAccessClaim.objects.create(
            sender=request.user,
            company=company,
            personal_msg=request.data.get("message"),
            declarant_role=request.data.get("declarant_role"),
            supervisor_role=request.data.get("supervisor_role"),
        )
        return Response({})


class CompanyCreateView(CreateAPIView):
    """Création d'une entreprise, et attribution d'un rôle de gestionnaire à son créateur"""

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    @transaction.atomic
    def perform_create(self, serializer):
        new_company = serializer.save()
        SupervisorRole.objects.create(company=new_company, user=self.request.user)
        DeclarantRole.objects.create(company=new_company, user=self.request.user)
        return new_company


class CompanyRetrieveUpdateView(RetrieveUpdateAPIView):
    """Récupération d'une entreprise dont l'utilisateur est gestionnaire ou instructeur, ou modification quand l'utilisateur est gestionnaire"""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticated(), IsSupervisorOrAgent()]
        else:
            return [IsAuthenticated(), IsSupervisor()]


class CompanyControlRetrieveView(RetrieveAPIView):
    model = Company
    permission_classes = [IsController]
    serializer_class = CompanyControllerSerializer
    queryset = Company.objects.all()


class CompanyCollaboratorsListView(ListAPIView):
    """Récupération des utilisateurs ayant au moins un rôle dans cette entreprise"""

    model = User
    serializer_class = CollaboratorSerializer

    def get_queryset(self):
        company = get_object_or_404(
            Company.objects.filter(supervisors=self.request.user), pk=self.kwargs[self.lookup_field]
        )
        return company.collaborators.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"company_id": self.kwargs[self.lookup_field]})
        return context


class AddCompanyRoleView(APIView):
    """Endpoint permettant d'ajouter un rôle lié à une entreprise (déclarant ou gestionnaire) à un utilisateur"""

    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        company = get_object_or_404(Company, pk=request.data["company_pk"])

        self.check_object_permissions(request, company)
        role_class = apps.get_model("data", request.data["role_name"])
        new_role, _ = role_class.objects.get_or_create(company=company, user=user)

        return Response(CollaboratorSerializer(user, context={"company_id": request.data["company_pk"]}).data)


class RemoveCompanyRoleView(APIView):
    """Endpoint permettant de retirer un rôle lié à une entreprise (déclarant ou gestionnaire) à un collaborateur"""

    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, user_pk):
        collaborator = get_object_or_404(User, pk=user_pk)
        company = get_object_or_404(Company, pk=request.data["company_pk"])

        if collaborator not in company.collaborators:
            raise NotFound()  # pas une permission car lié à 2 objets et non lié à l'utilisateur lui-même

        self.check_object_permissions(request, company)
        role_class = apps.get_model("data", request.data["role_name"])
        role_class.objects.filter(company=company, user=collaborator).delete()  # évite le try/except

        return Response(CollaboratorSerializer(collaborator, context={"company_id": request.data["company_pk"]}).data)


class AddMandatedCompanyView(GenericAPIView):
    """
    Cet endpoint permet de mandater une autre entreprise pour la création des déclarations
    """

    permission_classes = [IsAuthenticated, IsSupervisor]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def post(self, request, pk):
        company = self.get_object()

        siret = request.data.get("siret")
        vat = request.data.get("vat")

        if not siret and not vat:
            raise ProjectAPIException(global_error="Le SIRET ou le numéro de TVA doivent être spécifiés")

        try:
            mandated_company = Company.objects.get(siret=siret) if siret else Company.objects.get(vat=vat)
        except Company.DoesNotExist as _:
            raise NotFound()

        company.mandated_companies.add(mandated_company)
        company.save()

        brevo_template = 27
        for supervisor in mandated_company.supervisor_roles.all():
            try:
                email.send_sib_template(
                    brevo_template,
                    {
                        "COMPANY_NAME": company.social_name,
                        "MANDATED_COMPANY_NAME": mandated_company.social_name,
                        "DASHBOARD_LINK": f"{get_base_url()}tableau-de-bord?company={mandated_company.id}",
                    },
                    supervisor.user.email,
                    supervisor.user.get_full_name(),
                )
            except Exception as _:
                logger.exception(f"Email not sent on AddMandatedCompanyView for recipient {supervisor.user.id}")

        serializer = self.get_serializer(company)
        return Response(serializer.data)


class RemoveMandatedCompanyView(GenericAPIView):
    """
    Cet endpoint permet d'enlever une entreprise mandatée
    """

    permission_classes = [IsAuthenticated, IsSupervisor]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def post(self, request, pk):
        company = self.get_object()

        mandated_company_id = request.data.get("id")

        if not mandated_company_id:
            raise ProjectAPIException(global_error="L'ID de l'entreprise mandatée doit être spécifié")

        try:
            mandated_company = company.mandated_companies.get(pk=mandated_company_id)
            company.mandated_companies.remove(mandated_company)
            company.save()
        except Company.DoesNotExist as _:
            pass

        serializer = self.get_serializer(company)
        return Response(serializer.data)


class CompanyPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class ControlCompanyListView(ListAPIView):
    model = Company
    serializer_class = ControllerCompanySerializer
    permission_classes = [IsController]
    pagination_class = CompanyPagination
    filter_backends = [
        DepartmentFilterBackend,
        django_filters.DjangoFilterBackend,
        CamelCaseOrderingFilter,
        UnaccentSearchFilter,
    ]
    search_fields = ["social_name", "siret", "vat"]
    ordering_fields = ["creation_date", "modification_date", "social_name", "postal_code"]
    queryset = Company.objects.all()
