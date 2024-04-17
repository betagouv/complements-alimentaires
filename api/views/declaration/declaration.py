from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from api.serializers import DeclarationSerializer, DeclarationShortSerializer
from data.models import Declaration
from api.permissions import IsDeclarant, IsDeclarationAuthor
from api.views.declaration.declaration_flow import DeclarationFlow


class DeclarationListCreateApiView(ListCreateAPIView):
    model = Declaration
    permission_classes = [IsDeclarant]

    def get_queryset(self):
        return self.request.user.declarations

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeclarationSerializer
        return DeclarationShortSerializer


class DeclarationRetrieveUpdateView(RetrieveUpdateAPIView):
    model = Declaration
    serializer_class = DeclarationSerializer
    permission_classes = [IsDeclarationAuthor]
    queryset = Declaration.objects.all()


class DeclarationFlowView(GenericAPIView):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    transition = None

    def post(self, request, *args, **kwargs):
        declaration = self.get_object()
        flow = DeclarationFlow(declaration)
        transition_method = getattr(flow, self.transition)
        flow_permission_method = getattr(transition_method, "has_permission", None)
        if flow_permission_method and not flow_permission_method(request.user):
            raise PermissionDenied
        transition_method()
        declaration.save()
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)


class DeclarationSubmitView(DeclarationFlowView):
    permission_classes = [IsDeclarationAuthor]
    transition = "submit_for_instruction"


class DeclarationApproveView(DeclarationFlowView):
    # permission_classes = [] TODO : Ajouter la permission pour l'instruction
    transition = "approve"


class DeclarationRejectView(DeclarationFlowView):
    # permission_classes = [] TODO : Ajouter la permission pour l'instruction
    transition = "reject"
