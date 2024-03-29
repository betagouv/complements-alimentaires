from rest_framework.generics import CreateAPIView
from api.serializers import DeclarationSerializer
from data.models import Declaration
from rest_framework import permissions


class DeclarationCreateApiView(CreateAPIView):
    model = Declaration
    serializer_class = DeclarationSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO : Changer pour mettre le bon rôle
