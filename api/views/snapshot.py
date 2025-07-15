from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView

from api.permissions import CanAccessIndividualDeclaration, IsController, IsInstructor, IsVisor
from api.serializers import SnapshotSerializer
from data.models import Declaration, Snapshot


class DeclarationSnapshotListView(ListAPIView):
    model = Snapshot
    serializer_class = SnapshotSerializer
    permission_classes = (CanAccessIndividualDeclaration | IsInstructor | IsVisor | IsController,)

    def get_queryset(self):
        declaration = get_object_or_404(Declaration, pk=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, declaration)
        self.check_permissions(self.request)
        qs = declaration.snapshots.order_by("creation_date")
        if not IsInstructor().has_permission(self.request, self) and not IsVisor().has_permission(self.request, self):
            qs = qs.exclude(
                action__in=[
                    Snapshot.SnapshotActions.REQUEST_VISA,
                    Snapshot.SnapshotActions.TAKE_FOR_VISA,
                    Snapshot.SnapshotActions.REFUSE_VISA,
                ]
            )
        return qs.all()
