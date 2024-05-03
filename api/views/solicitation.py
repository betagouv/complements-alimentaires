from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.company import Company
from data.models.solicitation import Solicitation

from ..serializers import UnprocessedSolicitationSerializer

# class SolicitationListView(ListAPIView):
#     """Liste les demandes non traitées dont l'utilisateur est le destinataire"""

#     model = Solicitation
#     serializer_class = UnprocessedSolicitationSerializer

#     def get_queryset(self):
#         return Solicitation.objects.filter(recipients=self.request.user, processor__isnull=True)


class SolicitationListView(APIView):
    """Liste les demandes non traitées dont l'utilisateur est le destinataire, pour cette entreprise"""

    # TODO: ListAPIView à la place / ou ne plus utiliser la company passée en
    def get(self, request, pk, *args, **kwargs):
        company = get_object_or_404(Company.objects.filter(supervisors=request.user), pk=pk)
        # TODO: serait mieux d'utiliser un champ comme is_processed, mais est actuellement une property, pas un generatedField
        solicitations = Solicitation.objects.filter(
            recipients=self.request.user, company=company, processor__isnull=True
        )
        serializer = UnprocessedSolicitationSerializer(solicitations, many=True)
        return Response(serializer.data)
