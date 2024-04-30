from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from api.permissions import IsDeclarationAuthor
from api.serializers import DeclarationSerializer, DeclarationShortSerializer
from data.models import Declaration


class DeclarationListCreateApiView(ListCreateAPIView):
    model = Declaration
    # permission_classes = [IsDeclarant] # TODO: remplacer par IsDeclarantOfThisCompany

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
