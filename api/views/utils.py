from rest_framework.generics import RetrieveAPIView


class IngredientRetrieveView(RetrieveAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.query_params.get("history", None):
            context["history"] = True
        return context
