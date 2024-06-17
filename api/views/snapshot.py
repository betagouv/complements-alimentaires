from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView

from api.permissions import IsDeclarationAuthor, IsInstructor
from api.serializers import SnapshotSerializer
from data.models import Declaration, Snapshot


class DeclarationSnapshotListView(ListAPIView):
    model = Snapshot
    serializer_class = SnapshotSerializer
    permission_classes = (IsDeclarationAuthor | IsInstructor,)

    def get_queryset(self):
        declaration = get_object_or_404(Declaration, pk=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, declaration)
        self.check_permissions(self.request)
        return declaration.snapshots.order_by("-creation_date").all()
