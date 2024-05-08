from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.company import Company
from data.models.solicitation import CoSupervisionClaim

from ..permissions import IsSolicitationRecipient
from ..serializers import CoSupervisionClaimSerializer


class CoSupervisionClaimListView(ListAPIView):
    serializer_class = CoSupervisionClaimSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company.objects.filter(supervisors=user), pk=self.kwargs["pk"])
        return CoSupervisionClaim.objects.filter(recipients=user, company=company, processor__isnull=True)


class ProcessCoSupervisionClaim(APIView):
    """Effectue une action de traitement sur une demande de co-gestion"""

    permission_classes = [IsSolicitationRecipient]

    def post(self, request, pk: int, *args, **kwargs):
        solicitation = get_object_or_404(CoSupervisionClaim, pk=pk)
        self.check_object_permissions(request, solicitation)
        action = getattr(solicitation, request.data["action_name"])
        action(processor=request.user)
        return Response({})
