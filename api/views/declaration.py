from rest_framework.generics import CreateAPIView
from api.serializers import DeclarationSerializer
from data.models import Declaration
from api.permissions import IsDeclarant


class DeclarationCreateApiView(CreateAPIView):
    model = Declaration
    serializer_class = DeclarationSerializer
    permission_classes = [IsDeclarant]
