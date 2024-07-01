from django.db.models import F, Func
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

from django_filters import rest_framework as django_filters
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from unidecode import unidecode

from api.permissions import (
    CanAccessIndividualDeclaration,
    CanAccessUserDeclatarions,
    IsDeclarant,
    IsDeclarationAuthor,
    IsInstructor,
    IsSupervisor,
    IsVisor,
)
from api.serializers import DeclarationSerializer, DeclarationShortSerializer, SimpleDeclarationSerializer
from api.utils.filters import BaseNumberInFilter, CamelCaseOrderingFilter
from api.views.declaration.declaration_flow import DeclarationFlow
from data.models import Company, Declaration, InstructionRole, VisaRole


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
        # Afin d'inclure les compagnies avec la lettre chosie on doit prendre la lettre de l'alphabet
        # s'après. Par exemple, un filtre avec company_name_end "U" doit contenir "Umbrella corporation".
        # "Cz" doit inclure "Czech industries"

        normalized_input = unidecode(args[0].lower())
        # Si le premier char est "z" on peut considérer qu'on n'a pas de end-filter
        if normalized_input[0] == "z":
            return self._annotate_queryset(queryset)

        # Si le dernier char est "z" on peut l'ignorer et faire monter l'avant-dernier
        if normalized_input[-1] == "z":
            normalized_input = normalized_input[slice(-1)]
        last_char = normalized_input[-1]
        letter_order = "abcdefghijklmnopqrstuvwxyz"
        if last_char in letter_order:
            normalized_input = normalized_input[slice(-1)] + letter_order[letter_order.index(last_char) + 1]
        return self._annotate_queryset(queryset).filter(name_unaccented_lower__lt=normalized_input)

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


class OngoingDeclarationsListView(GenericDeclarationsListView):
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

    def perform_snapshot_creation(self, request, declaration):
        """
        Possible de le surcharger si la création du snapshot nécessite un
        traitement spécial
        """
        declaration.create_snapshot(
            user=request.user,
            comment=request.data.get("comment", ""),
            expiration_days=request.data.get("expiration"),
        )
        declaration.private_notes = request.data.get("privateNotes", "")

    def post(self, request, *args, **kwargs):
        declaration = self.get_object()
        flow = DeclarationFlow(declaration)
        transition_method = getattr(flow, self.transition)
        flow_permission_method = getattr(transition_method, "has_permission", None)
        if flow_permission_method and not flow_permission_method(request.user):
            raise PermissionDenied()
        transition_method()
        self.on_transition_success(request, declaration)
        if self.create_snapshot:
            self.perform_snapshot_creation(request, declaration)
        declaration.save()
        serializer = self.get_serializer(declaration)
        return Response(serializer.data)


class DeclarationSubmitView(DeclarationFlowView):
    """
    DRAFT -> AWAITING_INSTRUCTION
    """

    permission_classes = [IsDeclarationAuthor, IsDeclarant]
    transition = "submit"
    create_snapshot = True


class DeclarationTakeForInstructionView(DeclarationFlowView):
    """
    AWAITING_INSTRUCTION -> ONGOING_INSTRUCTION
    """

    permission_classes = [IsInstructor]
    transition = "take_for_instruction"

    def on_transition_success(self, request, declaration):
        declaration.instructor = InstructionRole.objects.get(user=request.user)
        return super().on_transition_success(request, declaration)


class DeclarationTakeForVisaView(DeclarationFlowView):
    """
    AWAITING_VISA -> ONGOING_VISA
    """

    permission_classes = [IsVisor]
    transition = "take_for_visa"

    def on_transition_success(self, request, declaration):
        declaration.visor = VisaRole.objects.get(user=request.user)
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


class DeclarationRefuseVisaView(DeclarationFlowView):
    """
    ONGOING_VISA -> AWAITING_INSTRUCTION
    """

    permission_classes = [IsVisor]
    transition = "refuse_visa"
    create_snapshot = True

    def perform_snapshot_creation(self, request, declaration):
        declaration.create_snapshot(user=request.user)

    def on_transition_success(self, request, declaration):
        """
        Dans le cas d'un refus de visa, on remet à vide les champs post_validation.
        On met également les notes privées à destination de l'admnistration dans la déclaration.
        """
        declaration.post_validation_producer_message = ""
        declaration.post_validation_status = ""
        declaration.post_validation_expiration_days = None
        declaration.private_notes = request.data.get("private_notes", "")
        return super().on_transition_success(request, declaration)


# Nous utilisons une Non-deterministic state machine. Lors qu'un.e instructeur.ice demande une
# visa, nous assignnos la déclaration à `AWAITING_VISA` et ajoutons un propriété dans le modèle
# spécifiant quel sera le status à assigner après le flow de validation.
class VisaRequestFlowView(DeclarationFlowView):
    """
    ONGOING_INSTRUCTION -> AWAITING_VISA
    Cette view doit être sous-classée. Elle assigne le `post_validation_status`
    spécifié. Les sous-classes doivent donc déclarer cette propriété.
    """

    permission_classes = [IsInstructor]
    transition = "request_visa"
    post_validation_status = None
    create_snapshot = True

    def perform_snapshot_creation(self, request, declaration):
        """
        Dans le cas d'une requête de validation, on ne mettra pas le commentaire à
        destination du producteur dans le snapshot créé. On le met dans le modèle pour
        pouvoir l'envoyer au producteur si la décision est acceptée par la viseuse.
        On met également les notes privées à destination de l'admnistration dans la déclaration.
        """
        declaration.create_snapshot(user=request.user)

    def on_transition_success(self, request, declaration):
        declaration.post_validation_producer_message = request.data.get("comment", "")
        declaration.post_validation_expiration_days = request.data.get("expiration")
        declaration.private_notes = request.data.get("private_notes", "")

        if not self.post_validation_status:
            raise Exception("VisaRequestFlowView doit être sous-classée et doit spécifier le post_validation_status")
        declaration.post_validation_status = self.post_validation_status
        return super().on_transition_success(request, declaration)


class DeclarationObserveWithVisa(VisaRequestFlowView):
    post_validation_status = Declaration.DeclarationStatus.OBSERVATION


class DeclarationObjectWithVisa(VisaRequestFlowView):
    post_validation_status = Declaration.DeclarationStatus.OBJECTION


class DeclarationRejectWithVisa(VisaRequestFlowView):
    post_validation_status = Declaration.DeclarationStatus.REJECTED


class DeclarationAuthorizeWithVisa(VisaRequestFlowView):
    post_validation_status = Declaration.DeclarationStatus.AUTHORIZED
