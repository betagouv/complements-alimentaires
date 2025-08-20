from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination

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


common_excel_styles = {
    "fill": {
        "fill_type": "solid",
        "start_color": "FF000091",
    },
    "alignment": {
        "horizontal": "center",
        "vertical": "center",
        "wrapText": True,
        "shrink_to_fit": True,
    },
    "border_side": {
        "border_style": "thin",
        "color": "FF6A6AF4",
    },
    "font": {
        "name": "Arial",
        "size": 12,
        "bold": True,
        "color": "FFFFFFFF",
    },
}


class ControlExcelPagination(LimitOffsetPagination):
    default_limit = 2000
    max_limit = 2000
