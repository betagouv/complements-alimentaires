from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import NotFound, ParseError
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


class DeclarantRoleView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisorOfThisCompany]

    def patch(self, request, company_pk, collaborator_pk, action):
        """On gère l'ajout et le retrait dans la même méthode car le code est presque le même."""

        company = get_object_or_404(Company, pk=company_pk)
        collaborator = get_object_or_404(User, pk=collaborator_pk)

        self.check_object_permissions(request, company)

        if collaborator not in company.staff:
            raise NotFound()  # pas une permission car lié à 2 objets et non lié à l'utilisateur lui-même

        declarant, _ = Declarant.objects.get_or_create(user=collaborator)
        if action == "add":
            declarant.companies.add(company_pk)
        elif action == "remove":
            declarant.companies.remove(company_pk)
        else:
            raise ParseError()

        return Response(StaffUserSerializer(collaborator, context={"company_id": company_pk}).data)
