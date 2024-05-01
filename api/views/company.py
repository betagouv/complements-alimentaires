from enum import StrEnum, auto

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.choices import CountryChoices
from data.models import Company, SupervisorRole
from data.utils.external_utils import SiretData
from data.validators import validate_siret, validate_vat  # noqa

from ..exception_handling import ProjectAPIException
from ..permissions import IsSupervisor
from ..serializers import CollaboratorSerializer, CompanySerializer


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
                if company.supervisors.filter(id=request.user.id).exists():
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
        SupervisorRole.objects.create(company=new_company, user=self.request.user)
        return new_company


class CompanyRetrieveView(RetrieveAPIView):
    """Récupération d'une entreprise dont l'utilisateur est gestionnaire"""

    queryset = Company.objects.all()
    permission_classes = [IsSupervisor]
    serializer_class = CompanySerializer


class GetCompanyCollaboratorsView(APIView):
    """Récupération des utilisateurs ayant au moins un rôle dans cette entreprise"""

    def get(self, request, pk, *args, **kwargs):
        company = get_object_or_404(Company.objects.filter(supervisors=request.user), pk=pk)
        serializer = CollaboratorSerializer(company.collaborators, many=True, context={"company_id": pk})
        return Response(serializer.data)


User = get_user_model()


class CompanyRoleView(APIView):
    """Endpoint unique permettant d'ajouter ou retirer un rôle lié à une entreprise (déclarant ou gestionnaire)"""

    permission_classes = [IsAuthenticated, IsSupervisor]

    def patch(self, request, company_pk: int, collaborator_pk: int, role_class_name: str, action: str):
        company = get_object_or_404(Company, pk=company_pk)
        collaborator = get_object_or_404(User, pk=collaborator_pk)

        self.check_object_permissions(request, company)

        if collaborator not in company.collaborators:
            raise NotFound()  # pas une permission car lié à 2 objets et non lié à l'utilisateur lui-même

        role_class = apps.get_model("data", role_class_name)

        # Techniquement, l'utilisation de `action` est redondant car on pourrait le déduire, mais ça peut faire
        # un garde-fou si côté front, le state de l'UI n'est pas le bon (ex: page non rafraichie.)
        try:
            role = role_class.objects.get(company=company, user=collaborator)
        except role_class.DoesNotExist:
            if action == "add":
                role = role_class.objects.create(company=company, user=collaborator)
        else:
            if action == "remove":
                role.delete()

        return Response(CollaboratorSerializer(collaborator, context={"company_id": company_pk}).data)
