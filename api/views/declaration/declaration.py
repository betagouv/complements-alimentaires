from django.db.models import F, Func
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

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
    IsSupervisor,
)
from api.serializers import DeclarationSerializer, DeclarationShortSerializer, SimpleDeclarationSerializer
from api.utils.filters import BaseNumberInFilter, CamelCaseOrderingFilter
from api.views.declaration.declaration_flow import DeclarationFlow
from data.models import Company, Declaration, InstructionRole


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


class Unaccent(Func):
    function = "unaccent"


class DeclarationFilterSet(django_filters.FilterSet):
    author = BaseNumberInFilter(field_name="author__id")
    company = BaseNumberInFilter(field_name="company__id")
    company_name_start = django_filters.CharFilter(method="company_name_start__gte")
    company_name_end = django_filters.CharFilter(method="company_name_end__lte")

    class Meta:
        model = Declaration
        fields = [
            "company",
            "status",
            "author",
            "company_name_start",
            "company_name_end",
        ]

    def company_name_start__gte(self, queryset, value, *args, **kwargs):
        return self._annotate_queryset(queryset).filter(name_unaccented_lower__gte=args[0].lower())

    def company_name_end__lte(self, queryset, value, *args, **kwargs):
        return self._annotate_queryset(queryset).filter(name_unaccented_lower__lte=args[0].lower())

    def _annotate_queryset(self, queryset):
        return queryset.annotate(name_unaccented_lower=Lower(Unaccent(F("company__social_name"))))


class DeclarationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class GenericDeclarationsListView(ListAPIView):
    model = Declaration
    pagination_class = DeclarationPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        CamelCaseOrderingFilter,
    ]
    filterset_class = DeclarationFilterSet


class AllDeclarationsListView(GenericDeclarationsListView):
    serializer_class = SimpleDeclarationSerializer
    permission_classes = [IsInstructor]
    ordering_fields = ["creation_date", "modification_date", "name"]
    queryset = Declaration.objects.exclude(status=Declaration.DeclarationStatus.DRAFT)


class CompanyDeclarationsListView(GenericDeclarationsListView):
    # Une fois l'instruction commencée on pourra avoir un serializer différent pour cette vue
    serializer_class = SimpleDeclarationSerializer
    permission_classes = [IsSupervisor]

    def get_queryset(self):
        company = get_object_or_404(
            Company.objects.filter(supervisors=self.request.user, pk=self.kwargs[self.lookup_field])
        )
        return company.declarations.exclude(status=Declaration.DeclarationStatus.DRAFT)


class DeclarationFlowView(GenericAPIView):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    transition = None
    create_snapshot = False

    def on_transition_success(self, request, declaration):
        """
        Hook à surcharger dans le cas où il faut faire des choses particulières
        après le succès de la transition
        """
        pass

    def post(self, request, *args, **kwargs):
        declaration = self.get_object()
        flow = DeclarationFlow(declaration)
        transition_method = getattr(flow, self.transition)
        flow_permission_method = getattr(transition_method, "has_permission", None)
        if flow_permission_method and not flow_permission_method(request.user):
            raise PermissionDenied()
        transition_method()
        if self.create_snapshot:
            declaration.create_snapshot(
                user=request.user,
                comment=request.data.get("comment", ""),
                expiration_days=request.data.get("expiration"),
            )
        self.on_transition_success(request, declaration)
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)


class DeclarationSubmitView(DeclarationFlowView):
    """
    DRAFT -> AWAITING_INSTRUCTION
    """

    permission_classes = [IsDeclarationAuthor, IsDeclarant]
    transition = "submit"
    create_snapshot = True


class DeclarationTakeView(DeclarationFlowView):
    """
    AWAITING_INSTRUCTION -> ONGOING_INSTRUCTION
    """

    permission_classes = [IsInstructor]
    transition = "take_for_instruction"

    def on_transition_success(self, request, declaration):
        declaration.instructor = InstructionRole.objects.get(user=request.user)
        return super().on_transition_success(request, declaration)


class DeclarationObserveView(DeclarationFlowView):
    """
    ONGOING_INSTRUCTION -> OBSERVATION
    """

    permission_classes = [IsInstructor]
    transition = "observe_no_visa"
    create_snapshot = True

    def on_transition_success(self, request, declaration):
        # Envoyer un email au déclarant.e avec le notes de l'observation
        return super().on_transition_success(request, declaration)


class DeclarationAuthorizeView(DeclarationFlowView):
    """
    ONGOING_INSTRUCTION -> AUTHORIZED
    """

    permission_classes = [IsInstructor]
    transition = "authorize_no_visa"
    create_snapshot = True

    def on_transition_success(self, request, declaration):
        # Envoyer un email au déclarant.e l'informant de l'autorisation
        return super().on_transition_success(request, declaration)


class DeclarationResubmitView(DeclarationFlowView):
    """
    OBSERVATION -> ONGOING_INSTRUCTION
    """

    permission_classes = [IsDeclarationAuthor, IsDeclarant]
    transition = "resubmit"
    create_snapshot = True
