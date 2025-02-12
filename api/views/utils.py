from rest_framework.generics import RetrieveUpdateAPIView


class IngredientRetrieveUpdateView(RetrieveUpdateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.query_params.get("history", None):
            context["history"] = True
        return context

    # TODO: limit modifications to Instructors
    # def update(self, instance, validated_data):

    def get_serializer_class(self):
        if self.request.method != "GET":
            return self.modification_serializer_class
        return self.serializer_class
