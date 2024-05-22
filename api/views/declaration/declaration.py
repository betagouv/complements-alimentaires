from django_filters import rest_framework as django_filters
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import (
    CanAccessIndividualDeclaration,
    CanAccessUserDeclatarions,
    IsDeclarant,
    IsDeclarationAuthor,
    IsInstructor,
)
from api.serializers import DeclarationSerializer, DeclarationShortSerializer, SimpleDeclarationSerializer
from api.utils.filters import BaseNumberInFilter, CamelCaseOrderingFilter
from api.views.declaration.declaration_flow import DeclarationFlow
from data.models import Company, Declaration


class UserDeclarationsListCreateApiView(ListCreateAPIView):
    model = Declaration
    permission_classes = [IsDeclarant, CanAccessUserDeclatarions]

    def get_queryset(self):
        return self.request.user.declarations

    def perform_create(self, serializer):
        # Lors de la création, des validations concernant l'objet créé doivent être faits ici
        # https://www.django-rest-framework.org/api-guide/permissions/#limitations-of-object-level-permissions
        company_id = self.request.data.get("company")
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist as _:
            raise NotFound("Company not found")
        if not company.declarants.filter(id=self.request.user.id).exists():
            raise PermissionDenied()
        return super().perform_create(serializer)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeclarationSerializer
        return DeclarationShortSerializer


class DeclarationRetrieveUpdateView(RetrieveUpdateAPIView):
    model = Declaration
    serializer_class = DeclarationSerializer
    permission_classes = [CanAccessIndividualDeclaration]
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
            raise PermissionDenied()
        transition_method()
        declaration.save()
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)


class DeclarationFilterSet(django_filters.FilterSet):
    author = BaseNumberInFilter(field_name="author__id")
    company = BaseNumberInFilter(field_name="company__id")
    company_name_start = django_filters.CharFilter(field_name="company__social_name", lookup_expr="gte")
    company_name_end = django_filters.CharFilter(field_name="company__social_name", lookup_expr="lte")

    class Meta:
        model = Declaration
        fields = [
            "company",
            "status",
            "author",
            "company_name_start",
            "company_name_end",
        ]


class DeclarationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class AllDeclarationsListView(ListAPIView):
    model = Declaration
    serializer_class = SimpleDeclarationSerializer
    permission_classes = [IsInstructor]
    ordering_fields = ["creation_date", "modification_date", "name"]
    pagination_class = DeclarationPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        CamelCaseOrderingFilter,
    ]
    filterset_class = DeclarationFilterSet
    queryset = Declaration.objects.all()


class DeclarationSubmitView(DeclarationFlowView):
    permission_classes = [IsDeclarationAuthor, IsDeclarant]
    transition = "submit_for_instruction"


class DeclarationApproveView(DeclarationFlowView):
    # permission_classes = [] TODO : Ajouter la permission pour l'instruction
    transition = "approve"


class DeclarationRejectView(DeclarationFlowView):
    # permission_classes = [] TODO : Ajouter la permission pour l'instruction
    transition = "reject"
