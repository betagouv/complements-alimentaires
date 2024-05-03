from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.company import Company
from data.models.solicitation import Solicitation

from ..permissions import IsSolicitationRecipient
from ..serializers import UnprocessedSolicitationSerializer


class SolicitationListView(ListAPIView):
    """Liste les solicitations non traitées dont l'utilisateur est le destinataire"""

    serializer_class = UnprocessedSolicitationSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company.objects.filter(supervisors=user), pk=self.kwargs["pk"])
        return Solicitation.objects.filter(recipients=user, company=company, processor__isnull=True)


class SolicitationProcessView(APIView):
    """Effectue une action de traitement sur une solicitation (RPC-style)"""

    permission_classes = [IsSolicitationRecipient]

    def post(self, request, pk: int, action: str, *args, **kwargs):
        solicitation = get_object_or_404(Solicitation, pk=pk)
        self.check_object_permissions(request, solicitation)
        solicitation.process(action=action, processor=request.user)
        return Response({})
