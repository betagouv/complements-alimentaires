from rest_framework.generics import ListAPIView

from data.models.solicitation import Solicitation

from ..serializers import UnprocessedSolicitationSerializer


class SolicitationListView(ListAPIView):
    """Liste les demandes non traitées dont l'utilisateur est le destinataire"""

    model = Solicitation
    serializer_class = UnprocessedSolicitationSerializer

    def get_queryset(self):
        # TODO: serait mieux d'utiliser un champ comme is_processed, mais est actuellement une property, pas un generatedField
        return Solicitation.objects.filter(recipients=self.request.user, processor__isnull=True)
