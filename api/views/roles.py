from django.apps import apps
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.company import Company

from ..permissions import IsSupervisorOfThisCompany
from ..serializers.user import CollaboratorSerializer

User = get_user_model()


class CompanyRoleView(APIView):
    """Endpoint unique permettant d'ajouter ou retirer un rôle lié à une entreprise (déclarant ou gestionnaire)"""

    permission_classes = [IsAuthenticated, IsSupervisorOfThisCompany]

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
