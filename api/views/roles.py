from django.apps import apps
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.company import Company
from data.models.roles import Declarant

from ..permissions import IsSupervisorOfThisCompany
from ..serializers.user import StaffUserSerializer

User = get_user_model()


class DeclarantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declarant
        fields = ("companies",)


class CompanyRoleView(APIView):
    """Endpoint unique permettant d'ajouter ou retirer un rôle lié à une entreprise (déclarant ou gestionnaire)"""

    permission_classes = [IsAuthenticated, IsSupervisorOfThisCompany]

    def patch(self, request, company_pk: int, collaborator_pk: int, role_class_name: str, action: str):
        company = get_object_or_404(Company, pk=company_pk)
        collaborator = get_object_or_404(User, pk=collaborator_pk)

        self.check_object_permissions(request, company)

        if collaborator not in company.staff:
            raise NotFound()  # pas une permission car lié à 2 objets et non lié à l'utilisateur lui-même

        role_class = apps.get_model("data", role_class_name)

        role, _ = role_class.objects.get_or_create(user=collaborator)
        if action == "add":
            role.companies.add(company_pk)
        elif action == "remove":
            role.companies.remove(company_pk)
        else:
            raise APIException("Wrong provided action")

        return Response(StaffUserSerializer(collaborator, context={"company_id": company_pk}).data)
