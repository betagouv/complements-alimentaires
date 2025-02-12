from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView

from api.permissions import IsInstructor


class IngredientRetrieveUpdateView(RetrieveUpdateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.query_params.get("history", None):
            context["history"] = True
        return context

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        else:
            return [IsInstructor()]

    def get_serializer_class(self):
        if self.request.method != "GET":
            return self.modification_serializer_class
        return self.serializer_class
