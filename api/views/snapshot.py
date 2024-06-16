from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView

from api.serializers import SnapshotSerializer
from data.models import Declaration, Snapshot


class DeclarationSnapshotListView(ListAPIView):
    model = Snapshot
    serializer_class = SnapshotSerializer
    permission_classes = []  # TODO (permission sur la declaration)

    def get_queryset(self):
        declaration = get_object_or_404(Declaration, pk=self.kwargs[self.lookup_field])
        return declaration.snapshots.order_by("-creation_date").all()
